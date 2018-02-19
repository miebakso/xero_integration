{
	'name': 'XERO Integration',
	'description': """
		Odoo 8 module for XERO integration.
	""",
	'category': 'Development',
	'version': '1.0.0',
	'author': 'Edrick',
	'maintainer': 'Edrick',
	'sequence': 150,
	'depends': [
		'base','account',
	],
	'data': [
		'views/xero_integration.xml',
		'views/import_invoice_view.xml',
	],
	'qweb': [
	],
	'demo': [
	],
	'test': [
	],
	'auto_install': False,
	'installable': True,
}