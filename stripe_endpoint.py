import stripe
from flask import Flask, request, jsonify
import os
import boto3
from botocore.exceptions import ClientError
import json

def get_secret():
    secret_name = "Uniyo_Stripe_secret_keys"
    region_name = "eu-north-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']

    return json.loads(secret)

secrets = get_secret()
STRIPE_SECRET_KEY = secrets["STRIPE_SECRET_KEY_TEST"]

stripe.api_key = STRIPE_SECRET_KEY

app = Flask(__name__)

@app.route("/create-payment-intent", methods=["POST"])
def create_payment_intent():
    # Extract payment data from the request
    amount = request.json["amount"]
    # Create a PaymentIntent
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency='usd',
    )
    return jsonify({
      'clientSecret': intent['client_secret']
    })

if __name__ == "__main__":
    app.run(port=4242)