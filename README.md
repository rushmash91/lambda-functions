# AWS Lambda Functions for React App Deployment

This repository is a collection of AWS Lambda functions that are designed to help automate various tasks within AWS, particularly for React App Deployment to static website hosting in S3. Each function in this repository is standalone, meaning that it can be used independently of the others. As the repository grows, more functions will be added, each providing unique functionality.

## List of Functions

1. [React App Deployment: CodeCommit to S3](#react-app-deployment-codecommit-to-s3) (s3-publish-codecommit-trigger.py)
2. [OpenAI API Integration Function](#openai-api-integration-function) (get-openai-poem.py)

---

### React App Deployment: CodeCommit to S3

This function is specifically designed for React web projects. It helps you automatically transfer your built React application (the `build` folder) from your AWS CodeCommit repository to an AWS S3 bucket. The S3 bucket is then set up as a static website host, serving your React application.

The function gets a list of all files (blobs) in a specified branch of your repository, checks if the file is in the `build` directory, and then uploads the file to a specified S3 bucket.

#### How to use this function

Before using this function, make sure to set the following environment variables in your Lambda function settings:

- `S3_BUCKET_NAME`: The name of the S3 bucket where the files will be uploaded and your React app will be hosted.
- `AWS_REGION`: The AWS region where your CodeCommit repository is located.
- `CODECOMMIT_REPO_NAME`: The name of your CodeCommit repository.
- `CODECOMMIT_BRANCH_NAME`: The branch in your repository to pull the files from.

You can then deploy the function in your AWS Lambda service. Once the function is triggered, it will automatically delete all objects in the specified S3 bucket and then upload the new files from the `build` folder of the specified CodeCommit repository.

Please note that this function only uploads files from the `build` directory of your repository and not the directory itself. The `build` prefix is also removed when the files are uploaded to the S3 bucket. This is perfect for a static website setup where all the build files need to reside at the root level of the hosting bucket.

---

### OpenAI API Integration Function

This function integrates the OpenAI API to generate creative content based on prompts. It retrieves the OpenAI API key from environment variables, constructs the parameters and headers for the OpenAI API call, makes the request, and processes the response.

#### How to use this function

Before using this function, make sure to set the following environment variable in your Lambda function settings:

- `OPENAI_API_KEY`: The key to authenticate with the OpenAI API.(Use parameter store with KMS)

This function can be deployed in your AWS Lambda service. Once the function is triggered, it uses the OpenAI API to generate text based on a given prompt.

---

Please stay tuned as more functions, specifically targeted towards React application deployment and management in AWS, will be added to this repository in the future.
