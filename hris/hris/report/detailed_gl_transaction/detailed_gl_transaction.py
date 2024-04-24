# Copyright (c) 2024, RAFI and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, now_datetime, nowdate, flt, cint, get_datetime_str, nowdate, get_link_to_form, today



def execute(filters=None):
	columns, data = [], []

	columns = get_columns(filters)
	data = get_data(filters)

	return columns, data

def get_data(filters):
	data = []
	accounts = frappe.db.sql(
		"""
		SELECT name FROM `tabAccount` where company = %(company)s and is_group = 0
		""",filters,as_dict=1)
	
	for account in accounts:
		opening = get_account_opening(account.name, filters)
		data.append(opening)

		transactions = get_account_transactions(account.name, filters)
		for row in transactions:
			data.append(row)

		totals = get_account_totals(account.name, filters)
		data.append(totals)

		closing = get_account_closing(account.name, filters)
		data.append(closing)
		data.append({})
		
	return data

def get_account_opening(account, filters):
	opening_dict = {}
	opening = frappe.db.sql(
		"""
		(SELECT ifnull(sum((debit_in_account_currency - credit_in_account_currency)), 0)balance FROM `tabGL Entry`
		where account = %(account)s and posting_date < %(from_date)s and is_cancelled = 0)
		""",{'account': account, 'from_date': filters.get("from_date")},as_dict=1)

	# opening_dict['posting_date'] = filters.get("from_date")
	opening_dict['account_currency'] = frappe.db.get_value('Account', account, 'account_currency')
	opening_dict['company'] = frappe.db.get_value('Account', account, 'company')
	opening_dict['account'] = f"Opening : {account}"
	opening_dict['debit_in_account_currency'] = abs(opening[0].balance) if flt(opening[0].balance) > 0 else 0
	opening_dict['credit_in_account_currency'] = abs(opening[0].balance) if flt(opening[0].balance) < 0 else 0

	return opening_dict


def get_account_transactions(account, filters):
	transactions = frappe.db.sql(
		"""
		SELECT * FROM (SELECT company, posting_date, account, account_currency, 
		debit_in_account_currency, credit_in_account_currency, party_type, party,voucher_no, voucher_type,
		remarks, against_voucher FROM `tabGL Entry` where is_cancelled = 0
		and account = %(account)s and posting_date between %(from_date)s and %(to_date)s
		order by account, posting_date)a1
		""",{'account': account, 'from_date': filters.get("from_date"), 'to_date': filters.get("to_date")},as_dict=1)

	return transactions


def get_account_closing(account, filters):
	closing_dict = {}
	closing = frappe.db.sql(
		"""
		(SELECT ifnull(sum((debit_in_account_currency - credit_in_account_currency)), 0)balance FROM `tabGL Entry`
		where account = %(account)s and posting_date <= %(to_date)s and is_cancelled = 0)
		""",{'account': account, 'to_date': filters.get("to_date")},as_dict=1)

	# opening_dict['posting_date'] = filters.get("to_date")
	closing_dict['account_currency'] = frappe.db.get_value('Account', account, 'account_currency')
	closing_dict['company'] = frappe.db.get_value('Account', account, 'company')
	closing_dict['account'] = f"Closing (Opening + Total)"
	closing_dict['debit_in_account_currency'] = abs(closing[0].balance) if flt(closing[0].balance) > 0 else 0
	closing_dict['credit_in_account_currency'] = abs(closing[0].balance) if flt(closing[0].balance) < 0 else 0

	return closing_dict

def get_account_totals(account, filters):
	closing_dict = {}
	closing = frappe.db.sql(
		"""
		(SELECT ifnull(sum((debit_in_account_currency - credit_in_account_currency)), 0)balance FROM `tabGL Entry`
		where account = %(account)s and posting_date between %(from_date)s and %(to_date)s and is_cancelled = 0)
		""",{'account': account, 'from_date': filters.get("from_date"),'to_date': filters.get("to_date")},as_dict=1)

	# opening_dict['posting_date'] = filters.get("to_date")
	closing_dict['account_currency'] = frappe.db.get_value('Account', account, 'account_currency')
	closing_dict['company'] = frappe.db.get_value('Account', account, 'company')
	closing_dict['account'] = f"Total"
	closing_dict['debit_in_account_currency'] = abs(closing[0].balance) if flt(closing[0].balance) > 0 else 0
	closing_dict['credit_in_account_currency'] = abs(closing[0].balance) if flt(closing[0].balance) < 0 else 0

	return closing_dict


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
