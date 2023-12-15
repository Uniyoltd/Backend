import stripe
from flask import Flask, request, jsonify

export STRIPE_SECRET_KEY="pk_test_51HpeESHLc8y1CsAnLsLMxbKbWUXWknhXna9UKn2bp7t4pERy8tdGhf7OsYc2HWQqcXraNXvKDSnTkwhcVQitYEbO00SfuhVZj0"
# "pk_live_51HpeESHLc8y1CsAnFfFkXR4DcT0aYH7qFwuWO0J4Z0aHhSs4A7t4jbhdG7k4yRdsbfSWuJW8AdiJcJF5JToFTnBd00ELeJ23Fc"

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
