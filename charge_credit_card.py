from authorizenet import apicontractsv1
from authorizenet.apicontrollers import*
from decimal import*

import os

api_login_id = os.environ['AUTHORIZENET_API_LOGIN_ID']
transaction_key = os.environ['AUTHORIZENET_TRANSACTION_KEY']
 
merchantAuth = apicontractsv1.merchantAuthenticationType()
merchantAuth.name = api_login_id
merchantAuth.transactionKey = transaction_key

def charge(card_number, expiration_date, amount, merchant_id):
    """Executes transaction for specified amount on card number passed in"""
    
    creditCard = apicontractsv1.creditCardType()
    creditCard.cardNumber = card_number
    creditCard.expirationDate = expiration_date

    payment = apicontractsv1.paymentType()
    payment.creditCard = creditCard

    transactionrequest = apicontractsv1.transactionRequestType()
    transactionrequest.transactionType ="authCaptureTransaction"
    transactionrequest.amount = amount
    transactionrequest.payment = payment


    createtransactionrequest = apicontractsv1.createTransactionRequest()
    createtransactionrequest.merchantAuthentication = merchantAuth
    createtransactionrequest.refId = merchant_id

    createtransactionrequest.transactionRequest = transactionrequest
    createtransactioncontroller = createTransactionController(createtransactionrequest)
    createtransactioncontroller.execute()

    response = createtransactioncontroller.getresponse()

    if (response.messages.resultCode=="Ok"):
        print("Transaction ID : %s"% response.transactionResponse.transId)
    else:
        print("response code: %s"% response.messages.resultCode)