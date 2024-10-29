import boto3
import json
from botocore.exceptions import ClientError

# Initialize SQS and DynamoDB clients
region_name = 'us-east-2'
sqs = boto3.client('sqs', region_name=region_name)
dynamodb = boto3.resource('dynamodb', region_name=region_name)

# Reference your DynamoDB Products table
products_table = dynamodb.Table('Products')

# Define the SQS queue URL
queue_url = 'https://sqs.us-east-2.amazonaws.com/626635440285/OrderProcessingQueue'

def poll_sqs_for_orders():
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
                order_details = json.loads(message['Body'])
                
                if order_details.get('action') == 'order':
                    product_id = order_details['productID']
                    quantity_purchased = order_details['quantity']

                    # Update product info in DynamoDB (e.g., reduce stock)
                    update_product_in_dynamodb(product_id, quantity_purchased)

                    # Delete message from SQS after processing
                    sqs.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=message['ReceiptHandle']
                    )
        else:  
            print("No messages in the queue. Polling again...")      

def update_product_in_dynamodb(product_id, quantity_purchased):
    # Reduce the stock in DynamoDB by the quantity purchased
    try:
        response = products_table.update_item(
            Key={'productID': product_id},
            UpdateExpression="SET stock = stock - :val",
            ConditionExpression="stock >= :val",
            ExpressionAttributeValues={
                ':val': quantity_purchased
            },
            ReturnValues="UPDATED_NEW"
        )
        print(f"Updated product {product_id}: New stock = {response['Attributes']['stock']}")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print(f"Failed to update product {product_id}: Not enough stock available.")
        else:
            print(f"Failed to update product {product_id}: {e}")

if __name__ == "__main__":
    poll_sqs_for_orders()