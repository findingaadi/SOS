import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('xxxxxxxxxxx')

def lambda_handler(event, context):
    print("received event", json.dumps(event))
    
    
    if 'body' in event:
        try:
            data = json.loads(event['body'])
            name = data.get("name")
            email = data.get("email")
            number = data.get("number")
            radius = data.get("radius")
            location = data.get("location")

            subscriber_id = str(uuid.uuid4())
            
            table.put_item(
                Item = {
                    'id': subscriber_id,
                    'name': name,
                    'email': email,
                    'number': number,
                    'radius': radius,
                    'location': location
                }
            )

            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({'message': 'Data stored successfully!'})
            }

        except Exception as e:
            print("error:", str(e))
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'failed to store data'})
            }
    return {
        'statusCode': 400,
        'body': json.dumps({'error': 'invalid input'})
    }
