# Copyright (c) 2024, RAFI and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []

	columns = get_columns(filters)
	data = get_data(filters)

	return columns, data

def get_data(filters):
	condition = ""
	
	if filters.get("customer"):
		condition += " and inv.customer = %(customer)s"
	
	data = frappe.db.sql(
		"""
		SELECT inv.name, posting_date, company, customer, grand_total, 
		outstanding_amount, concat(item_code, ' - ', item_name)item_code, description, inv.currency,
		(IF((SELECT account_currency from `tabAccount` acc where acc.name = inv.debit_to) = inv.currency, outstanding_amount, 
        (outstanding_amount/conversion_rate)))inv_outstanding_amount
		FROM `tabSales Invoice` inv, `tabSales Invoice Item` item 
		where inv.name = item.parent and inv.docstatus = 1
		and inv.company = %(company)s {0}
		""".format(condition),{'company': filters.get("company"), 'customer': filters.get("customer")},as_dict=1)

	return data

def get_columns(filters):
	return [
		{
			"label": _("Company"),
			"fieldname": "company",
			"fieldtype": "Link",
			"options": "Company",
			"width": 180,
		},
		{
			"label": _("Posting Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 140,
		},
		{
			"label": _("Invocie Currency"),
			"fieldname": "currency",
			"fieldtype": "Link",
			"options": "Currency",
			"width": 140,
		},
		{
			"label": _("Item"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 190,
		},
		{
			"label": _("Invoice No"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Sales Invoice",
			"width": 140,
		},
		{
			"label": _("Description"),
			"fieldname": "description",
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"label": _("Grand Total"),
			"fieldname": "grand_total",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150,
		},
		{
			"label": _("Outstanding"),
			"fieldname": "inv_outstanding_amount",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150,
		},
	]
