import requests

class LpClient():
    def __init__(self, app_id, app_secret):
        self.app_id = app_id,
        self.app_secret = app_secret
        self.auth = (app_id, app_secret)

    def __make_request__(self, path, data):
        print self.auth
        response = requests.post('https://www.lightningplayground.co/{0}'.format(path), json=data, auth=self.auth)
        print response.text
        return response.json()

    def create_invoice(self, amount, purpose):
        return self.__make_request__("api/payment/request", {
            "amount": amount,
            "purpose": purpose
        })

    def send_payment(self, amount, recipient, purpose):
        return self.__make_request__("api/payment/send", {
            "amount": amount,
            "invoice_id": recipient,
            "purpose": purpose
        })