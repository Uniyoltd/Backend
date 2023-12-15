import stripe
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

app = Flask(__name__)

@app.route("/create-payment-intent", methods=["POST"])
def create_payment_intent():
    # Extract payment data from the request
    amount = request.json["amount"]
    currency = request.json["currency"]

    # Create a payment intent
    stripe.api_key = STRIPE_SECRET_KEY
    payment_intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=currency,
    )

    # Return the payment intent ID to the Flutter app
    return jsonify({"clientSecret": payment_intent["client_secret"]})

@app.route("/confirm-payment-intent", methods=["POST"])
def confirm_payment_intent():
    # Extract payment intent ID from the request
    payment_intent_id = request.json["paymentIntentId"]

    # Confirm the payment intent
    stripe.api_key = STRIPE_SECRET_KEY
    payment_intent = stripe.PaymentIntent.confirm(payment_intent_id)

    # Return the payment status to the Flutter app
    return jsonify({"status": payment_intent["status"]})

if __name__ == "__main__":
    app.run(debug=True)


app = Flask(__name__)