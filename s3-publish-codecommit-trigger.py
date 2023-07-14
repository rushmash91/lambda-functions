import boto3
import os
import mimetypes

# Function to get list of all blobs in the provided branch of a CodeCommit repository.
def get_blob_list(codecommit, repository, branch):
    # Get initial differences
    response = codecommit.get_differences(
        repositoryName=repository,
        afterCommitSpecifier=branch,
    )
    # Store the blob details for each file in the differences
    blob_list = [difference['afterBlob'] for difference in response['differences']]
    
    # If there are more blobs, keep getting them until we have all
    while 'nextToken' in response:
        response = codecommit.get_differences(
            repositoryName=repository,
            afterCommitSpecifier=branch,
            nextToken=response['nextToken']
        )
        blob_list += [difference['afterBlob'] for difference in response['differences']]
    
    return blob_list

# Function to delete all objects from a given S3 bucket.
def delete_all_objects(bucket):
    print("Deleting all existing objects in the bucket.")
    for obj in bucket.objects.all():
        obj.delete()
    print("All objects have been deleted.")

# Main Lambda handler
def lambda_handler(event, context):
    print("Lambda function started.")

    # Connect to S3 bucket
    bucket = boto3.resource('s3').Bucket(os.getenv('S3_BUCKET_NAME'))
    print(f"Connected to bucket: {bucket.name}")

    # Delete all existing objects in the bucket
    delete_all_objects(bucket)

    # Connect to CodeCommit
    codecommit = boto3.client('codecommit', region_name=os.getenv('AWS_REGION'))
    print("Connected to CodeCommit.")

    # Get repository name from environment variables
    repository_name = os.getenv('CODECOMMIT_REPO_NAME')
    print(f"Using repository: {repository_name}")

    # Get list of all blobs in the repository
    for blob in get_blob_list(codecommit, repository_name, os.getenv('CODECOMMIT_BRANCH_NAME')):
        path = blob['path']
        print(f"Checking file: {path}")

        # Only proceed if the file is in the 'build' directory
        if not path.startswith('build/'):
            continue

        print(f"Processing file: {path}")
        content = (codecommit.get_blob(repositoryName=repository_name, blobId=blob['blobId']))['content']
        content_type = mimetypes.guess_type(path)[0]

        # Strip 'build/' from the path for S3 upload
        s3_path = path.replace('build/', '', 1)

        # Upload file to S3 with appropriate content type
        if content_type is not None:
            bucket.put_object(Body=(content), Key=s3_path, ContentType=content_type)
        else:
            bucket.put_object(Body=(content), Key=s3_path)

        print(f"Uploaded file: {path} to: {s3_path}")

    print("Lambda function finished.")

    return {
        'statusCode': 200,
        'body': 'Files from build directory uploaded to S3'
    }
