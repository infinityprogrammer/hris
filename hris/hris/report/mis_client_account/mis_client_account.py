# Copyright (c) 2024, RAFI and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, now_datetime, nowdate, flt, cint, get_datetime_str, nowdate, get_link_to_form, today



def execute(filters=None):
	columns, data = [], []
	data = get_data(filters)

	for row in data:
		cluster = get_customer_cluster(row.get("customer"))
		row["cluster"] = cluster

	columns = get_columns(filters)

	return columns, data

def get_customer_cluster(customer):

	cluster = frappe.db.sql(
		"""
		SELECT cluster
		FROM `tabSales Invoice`
		where docstatus = 1 and customer = %(customer)s
		limit 1""",{'customer': customer}, as_dict=1)
	
	if cluster:
		return cluster[0].cluster
	else:
		return

def get_data(filters):
	si_data = []
	
	consolidated_data = get_client_total_value(filters)

	consolidated_total = 0.0
	for row in consolidated_data:
		data_context = {}
		
		data_context["customer"] = row.customer
		data_context["account_currency"] = row.account_currency
		data_context["ytd_balance"] = row.ytd_balance
		data_context["usd_currency"] = "USD"
		if row.account_currency == "USD":
			data_context["ytd_balance_usd"] = row.ytd_balance
		else:
			balance_usd = get_balalnce_in_usd(row.ytd_balance, row.account_currency, filters)
			data_context["ytd_balance_usd"] = balance_usd

		consolidated_total += data_context["ytd_balance_usd"]

		si_data.append(data_context)
	
	consolidated_total_context = {}
	consolidated_total_context["customer"] = "Total"
	consolidated_total_context["ytd_balance_usd"] = consolidated_total
	si_data.append(consolidated_total_context)
	si_data.append({})


	for customer in consolidated_data:
		customer_data = get_customer_data(customer.customer, filters)
		si_data = si_data + customer_data

	return si_data

def get_customer_data(customer, filters):

	customer_data = []
	customer_balance = frappe.db.sql(
		"""
		SELECT customer, posting_date, si.name, grand_total,
		outstanding_amount, 
		currency as inv_currency,acc.account_currency
		FROM `tabSales Invoice` si, `tabAccount` acc
		where si.debit_to = acc.name
		and si.docstatus = 1
		and round(outstanding_amount) != 0
		and customer = %(customer)s
		and posting_date between %(from_date)s and %(to_date)s
		""",{'customer': customer, 'from_date': filters.get('from_date'), 'to_date': filters.get('to_date')}, as_dict=1)
	
	c_grand_total = 0.0 
	c_outstanding = 0.0 
	c_usd_outstanding = 0.0 
	c_currency = ""
	c_acc_currency = ""

	for row in customer_balance:
		c_currency = row.inv_currency
		c_acc_currency = row.account_currency

		data_context = {}
		c_grand_total += row.grand_total
		c_outstanding += row.outstanding_amount


		data_context["customer"] = row.customer
		data_context["posting_date"] = row.posting_date
		data_context["inv_no"] = row.name
		data_context["grand_total"] = row.grand_total
		data_context["ytd_balance"] = row.outstanding_amount
		data_context["inv_currency"] = row.inv_currency
		data_context["account_currency"] = row.account_currency

		if row.account_currency == "USD":
			data_context["ytd_balance_usd"] = row.outstanding_amount
		else:
			data_context["ytd_balance_usd"] = get_balalnce_in_usd(row.outstanding_amount, row.account_currency, filters)

		c_usd_outstanding += flt(data_context["ytd_balance_usd"])

		customer_data.append(data_context)

	c_total = {}
	c_total["customer"] = "Total"
	c_total["grand_total"] = c_grand_total
	c_total["ytd_balance"] = c_outstanding
	c_total["ytd_balance_usd"] = c_usd_outstanding
	c_total["ytd_balance_usd"] = c_usd_outstanding
	c_total["inv_currency"] = c_currency
	c_total["usd_currency"] = "USD"
	c_total["account_currency"] = c_acc_currency

	customer_data.append(c_total)

	return customer_data

def get_balalnce_in_usd(ytd_balance, account_currency, filters):
	if account_currency == "AED":
		return ytd_balance * flt(filters.get("aed_exchange_rate"))
	
	if account_currency == "RUB":
		return ytd_balance * flt(filters.get("rub_exchange_rate"))
	
	if account_currency == "EUR":
		return ytd_balance * flt(filters.get("eur_exchange_rate"))

	return ytd_balance

def get_client_total_value(filters):

	total_balance = frappe.db.sql(
		"""
		SELECT customer,
		acc.account_currency,
		sum(outstanding_amount)ytd_balance
		FROM `tabSales Invoice` si, `tabAccount` acc
		where si.debit_to = acc.name
		and si.docstatus = 1
		and round(outstanding_amount) != 0
		and YEAR(si.posting_date) = YEAR(CURDATE()) 
		AND si.posting_date <= CURDATE()
		group by customer, acc.account_currency order by 1
		""",{}, as_dict=1)
	
	return total_balance

def get_columns(filters):
	return [
		{
			"label": _("Customer"),
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 250,
		},
		{
			"label": _("Cluster"),
			"fieldname": "cluster",
			"fieldtype": "Link",
			"options": "cluster",
			"width": 120,
		},
		{
			"label": _("Posting Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 140,
		},
		{
			"label": _("Invoice No"),
			"fieldname": "inv_no",
			"fieldtype": "Link",
			"options": "Sales Invoice",
			"width": 120,
		},
		{
			"label": _("Type"),
			"fieldname": "type",
			"fieldtype": "Data",
			"width": 140,
		},
		{
			"label": _("Value"),
			"fieldname": "grand_total",
			"fieldtype": "Currency",
			"options": "inv_currency",
			"width": 150,
		},
		{
			"label": _("YTD Balance"),
			"fieldname": "ytd_balance",
			"fieldtype": "Currency",
			"options": "account_currency",
			"width": 150,
		},
		{
			"label": _("YTD Balance $"),
			"fieldname": "ytd_balance_usd",
			"fieldtype": "Currency",
			"options": "usd_currency",
			"width": 150,
		},
	]