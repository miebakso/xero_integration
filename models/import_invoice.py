import base64, csv, StringIO
from openerp.osv import osv, fields
from openerp.exceptions import ValidationError

# ==========================================================================================================================

class AccountInvoice(osv.osv):
	_inherit = "account.invoice"

# ==========================================================================================================================

class ImportInvoice(osv.osv_memory):
	_name = 'xero.integration.import.invoice'
	_description = 'Update all invoices from .csv file imported from XERO.'
	_columns = {
		'invoices': fields.binary('XERO Invoices', None, required=True),
		'invoices_filename': fields.char('XERO Invoices Filename', 100)
	}

	def _check_file_type(self, cr, uid, ids, context=None):
		obj = self.browse(cr, uid, ids[0], context=context)
		filename = obj.invoices_filename.split('.')
		filetype = filename[len(filename)-1]

		if filetype != 'csv': return False
		return True

	_constraints = [
		(_check_file_type, 'Uploaded file must be .csv file.', ['invoices_filename']),
	]

	def import_invoice(self, cr, uid, ids, context=None):
		obj = self.browse(cr, uid, ids[0], context=context)
		contents = base64.b64decode(obj.invoices)
		reader = csv.DictReader(StringIO.StringIO(contents))

		for row in reader:
			#JUNED: bukan kebiasaan baik untuk langsung mengakses key dict dengan []
			#khususnya karena ini hasil baca dari file yang kita ngga tau gimana cara generatenya.
			#alih2, gunakan row.get('InvoiceNumber', False) artinya coba ambil key InvoiceNumber
			#dari dict row, kalau ngga ada key itu maka hasilnya False (well kamu bisa taruh 
			#nilai apapun yang bermakna False sebagai ganti False)
			if not row or not row['InvoiceNumber']: continue

			if not row['Status'].lower() == "paid": continue
			#JUNEd: tampung dulu self.pool.get('account.invoice') ke variabel, seperti contoh ini
			#invoice_obj = self.pool.get('account.invoice')
			#baru dipake di bawah2nya
			invoice_ids = self.pool.get('account.invoice').search(cr, uid, [
				('number', '=', row['InvoiceNumber'])
			])

			if not invoice_ids: continue
			obj = self.pool.get('account.invoice').browse(cr, uid, invoice_ids[0], context=context)
			obj.state = 'paid'