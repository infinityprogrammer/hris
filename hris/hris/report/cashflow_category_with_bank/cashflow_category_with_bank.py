# Copyright (c) 2024, RAFI and contributors
# For license information, please see license.txt

import frappe
from frappe import _



def execute(filters=None):
	columns, data = [], []

	data = get_data(filters)
	columns = get_columns(filters)

	return columns, data


def get_data(filters):
	
	data = frappe.db.sql(
		"""
		SELECT gl.company, posting_date,cashflow_category, 
		account, gl.account_currency, debit_in_account_currency, credit_in_account_currency,
		voucher_no, voucher_type, party_type, party, against_voucher, remarks
		FROM `tabGL Entry` gl, `tabAccount` acc 
		where gl.account = acc.name and acc.account_type in ('Bank', 'Cash')
		and gl.is_cancelled = 0 and posting_date between %(from_date)s and %(to_date)s
		""",filters,as_dict=1)

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
			"label": _("Cashflow Category"),
			"fieldname": "cashflow_category",
			"fieldtype": "Link",
			"options": "Cashflow Category",
			"width": 180,
		},
		{
			"label": _("Posting Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 140,
		},
		{
			"label": _("Account"),
			"fieldname": "account",
			"fieldtype": "Link",
			"options": "Account",
			"width": 290,
		},
		{
			"label": _("Account Currency"),
			"fieldname": "account_currency",
			"fieldtype": "Link",
			"options": "Currency",
			"width": 140,
		},
		{
			"label": _("Debit"),
			"fieldname": "debit_in_account_currency",
			"fieldtype": "Currency",
			"options": "account_currency",
			"width": 150,
		},
		{
			"label": _("Credit"),
			"fieldname": "credit_in_account_currency",
			"fieldtype": "Currency",
			"options": "account_currency",
			"width": 150,
		},
		{
			"label": _("Voucher No"),
			"fieldname": "voucher_no",
			"fieldtype": "Dynamic Link",
			"options": "voucher_type",
			"width": 160,
		},
		{
			"label": _("Voucher Type"),
			"fieldname": "voucher_type",
			"fieldtype": "Link",
			"options": "DocType",
			"width": 160,
		},
		{
			"label": _("Party Type"),
			"fieldname": "party_type",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("Party"),
			"fieldname": "party",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("Against Voucher"),
			"fieldname": "against_voucher",
			"fieldtype": "Data",
			"width": 130,
		},
		{
			"label": _("Remarks"),
			"fieldname": "remarks",
			"fieldtype": "Data",
			"width": 130,
		}
	]