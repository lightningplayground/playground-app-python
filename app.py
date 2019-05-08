from flask import Flask, render_template, jsonify
from flask import request, redirect, session

from integrations import LpClient
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = "Your_secret_string"

lp_client = LpClient(
    app_id=os.getenv("PLAYGROUND_APP_ID"),
    app_secret=os.getenv("PLAYGROUND_APP_SECRET")
)

'''
-----------------------------
Invoice Generation
-----------------------------

This endpoint allows you to create an invoice for a certain amount
On the basis of your app_id and app_secret

'''
@app.route('/invoice', methods=["POST"])
def invoice():
    amount = 1000
    invoice = lp_client.create_invoice(
        amount=amount,
        purpose="One round of Survivor42"
    )
    ## TODO: Store invoice information into a database
    
    ## The invoice_id generated should be used as a token for future operations
    ## such as sending winnings / payments / refund to the customer

    return jsonify({
        "invoice_id": invoice["id"],
        "invoice_url": invoice["frame_url"]
    })

'''
-----------------------------
Webhook Events Handler
-----------------------------

This endpoint allows you to receive events from Lightning Playground
Which can be used to update the status of invoice information / round
information locally.

'''
@app.route('/webhook', methods=["POST"])
def webhook():
    request_body_params = request.get_json(silent=True, force=True)

    event = request_body_params.get("event")
    invoice_id = request_body_params.get("invoice_id")
    transaction_id = request_body_params.get("transaction_id")
    
    if event == "PAYMENT_SUCCESS":
        #TODO:  Update the invoice information to mark it paid in the local database
        pass

    return "", 200 # Ensure a 200 is always passed back to the webhook

'''
-----------------------------
Application Home Page
-----------------------------

Homepage for your application

'''
@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


'''
-----------------------------
Round Handler
-----------------------------

Page to be redirected to after invoice has been successfully paid for 
so the user can continue to the actual feature / round in the app / game

'''
@app.route('/round/<invoice_id>', methods=["GET"])
def round(invoice_id):
    # TODO: Retrieve token / invoice information from database
    #       Check if invoice is satisfied
    #       Check if invoice is already used to complete the game
    #       If all the conditions are good allow access to the game
    return render_template('round.html', invoice_id=invoice_id)
