import boto3
import json

# Initialize SQS and DynamoDB clients
region_name = 'us-east-2'
sqs = boto3.client('sqs', region_name=region_name)
dynamodb = boto3.resource('dynamodb', region_name=region_name)

# Reference your DynamoDB Products table
products_table = dynamodb.Table('Products')

# Define the SQS queue URL
queue_url = 'https://sqs.us-east-2.amazonaws.com/626635440285/ProductLookupQueue'

def poll_sqs_for_product_lookup():
    while True:
        # Poll SQS for messages
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10
        )

        if 'Messages' in response:
            for message in response['Messages']:
                # Extract the message body
                search_details = json.loads(message['Body'])
                
                if search_details.get('action') == 'search':
                    product_id = search_details.get('productID', None)
                    product_name = search_details.get('productName', None)
                    
                    if not product_id and not product_name:
                        print("No valid product ID or product name provided in the message.")
                        continue

                    print(f"Searching for product with ID {product_id} or name {product_name}...")

                    # Retrieve product info from DynamoDB
                    product_info = get_product_from_dynamodb(product_id, product_name)
                    
                    if product_info:
                        print(f"Product found: {product_info}")
                    else:
                        print(f"Product with ID {product_id} or name {product_name} not found.")

                    # Delete message from SQS after processing
                    sqs.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=message['ReceiptHandle']
                    )
        else:  
            print("No messages in the queue. Polling again...")

def get_product_from_dynamodb(product_id, product_name):
    if product_id:
        response = products_table.get_item(Key={'productID': product_id})
    else:
        # If searching by name, scan the table
        print("Scanning the table for the product name...")
        response = products_table.scan(
            FilterExpression=boto3.dynamodb.conditions.Attr('name').eq(product_name)
        )
    
    return response.get('Item', None)

if __name__ == "__main__":
    poll_sqs_for_product_lookup()