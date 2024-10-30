// src/snsService.js
import { SNSClient, PublishCommand } from "@aws-sdk/client-sns";

const snsClient = new SNSClient({ region: 'your-region' });

// Function to publish a product search request to SNS
export async function searchProduct(productID, productName) {
    const params = {
        Message: JSON.stringify({
            action: 'search',
            productID: productID,
            productName: productName
        }),
        TopicArn: 'arn:aws:sns:us-east-2:626635440285:ProductActionsTopic'
    };

    try {
        const data = await snsClient.send(new PublishCommand(params));
        console.log("Message sent", data);
    } catch (err) {
        console.error("Error publishing message", err);
    }
}

// Function to publish an order request to SNS
export async function placeOrder(productID, quantity) {
    const params = {
        Message: JSON.stringify({
            action: 'order',
            productID: productID,
            quantity: quantity
        }),
        TopicArn: 'arn:aws:sns:us-east-2:626635440285:ProductActionsTopic'
    };

    try {
        const data = await snsClient.send(new PublishCommand(params));
        console.log("Message sent", data);
    } catch (err) {
        console.error("Error publishing message", err);
    }
}