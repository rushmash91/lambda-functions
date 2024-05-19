import json
import boto3
import urllib3
import os

def lambda_handler(event, context):
    # Get the API key from the environment variables
    api_key = os.getenv('OPENAI_API_KEY')

    # Parameters for the OpenAI API call
    model = "text-davinci-003"
    prompt = """Instructions: Follow all the points below 
      1. Write a rhyming poem about Arush Sharma. 
      2. Write in 3 paragraphs of 4 lines each with the rhyming scheme of aabb."""
    max_tokens = 400
    temperature = 0.4

    # Headers for the OpenAI API call
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    # Body for the OpenAI API call
    body = {
        'model': model,
        'prompt': prompt,
        'max_tokens': max_tokens,
        'temperature': temperature
    }

    # Initialize a PoolManager instance
    http = urllib3.PoolManager()

    # Call the OpenAI API
    response = http.request(
        'POST',
        'https://api.openai.com/v1/completions',
        body=json.dumps(body).encode('utf-8'),
        headers=headers
    )

    # Parse the response
    response_json = json.loads(response.data.decode('utf-8'))

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        'body': json.dumps({'text': response_json['choices'][0]['text'].strip()})
    }
