from openerp import models, api
from xero import Xero
from xero.auth import PrivateCredentials

# ==========================================================================================================================

class franchisee_bill(models.Model):

	_inherit = "franchisee.bill"

	@api.model
	def create(self, vals):
		new_data = super(franchisee_bill, self).create(vals)
		print("MASUK METHOD CREATE KEPANGGIL XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
		self.generate_xero_invoice(new_data)
		return new_data

	def generate_xero_invoice(self, data):
		with open('C:\\OpenSSL\\bin\\publickey.cer') as keyfile:
			rsa_key = keyfile.read()

		credentials = PrivateCredentials('XHTKCYJGSUC1TM8AXQBRCKAGPKDZ5W', rsa_key)
		xero = Xero(credentials)
		invoice = {
			"Type": "ACCREC", 	
			"Contact": {
				"Name": "Test"
			},
			"LineItems": {
				"LineItem": {
					"Description": "coba",
					"Quantity": "test",
					"UnitAmount": 10
				}
			}
		}

		xero.invoices.save(invoice)