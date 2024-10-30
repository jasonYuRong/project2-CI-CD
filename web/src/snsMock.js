import { SNSClient, PublishCommand } from "@aws-sdk/client-sns";

// Check if running locally (localhost) to mock AWS service calls
const isLocal = window.location.hostname === 'localhost';

// Initialize SNS client for production environment
const snsClient = !isLocal ? new SNSClient({ region: 'your-region' }) : null;

// Mock function to simulate SNS publish in local environment
const mockSNSPublish = (params) => {
    console.log("SNS Publish: ", params);
};

// Function to publish a product search request to SNS
export async function searchProduct(productID, productName) {
    const params = {
        Message: JSON.stringify({
            action: 'search',
            productID: productID,
            productName: productName
        }),
        TopicArn: 'arn:aws:sns:your-region:your-account-id:ProductActionsTopic'
    };

    if (isLocal) {
        mockSNSPublish(params); // Use mock function in local environment
    } else {
        try {
            const data = await snsClient.send(new PublishCommand(params));
            console.log("Message sent", data);
        } catch (err) {
            console.error("Error publishing message", err);
        }
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
        TopicArn: 'arn:aws:sns:your-region:your-account-id:ProductActionsTopic'
    };

    if (isLocal) {
        mockSNSPublish(params); // Use mock function in local environment
    } else {
        try {
            const data = await snsClient.send(new PublishCommand(params));
            console.log("Message sent", data);
        } catch (err) {
            console.error("Error publishing message", err);
        }
    }
}