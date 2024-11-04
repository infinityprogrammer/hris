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
	data = []
	customers = get_all_customer(filters)
	all_months = [
		"January",
		"February",
		"March",
		"April",
		"May",
		"June",
		"July",
		"August",
		"September",
		"October",
		"November",
		"December"
	]
	for row in customers:
		context = {}
		context["customer"] = row.customer
		ytd_sum = 0.0
		for month in all_months:
			customer_value = frappe.db.sql(
				"""
				SELECT customer,
				acc.account_currency,
				sum(grand_total)outstanding_amount
				FROM `tabSales Invoice` si, `tabAccount` acc
				where si.debit_to = acc.name
				and si.docstatus = 1
				and round(grand_total) != 0
				and YEAR(si.posting_date) = %(year)s 
				AND MONTHNAME(si.posting_date) = %(monthname)s
				and si.customer = %(customer)s
				group by customer, acc.account_currency
				""",{'year': filters.get('fiscal_year'), 'monthname': month, 'customer': row.customer}, as_dict=1)
			

			c_outstanding_amount = 0.0
			for row in customer_value:
				if row.account_currency == "USD":
					c_outstanding_amount += row.outstanding_amount
					ytd_sum += row.outstanding_amount
				else:
					c_outstanding_amount += get_balalnce_in_usd(row.outstanding_amount, row.account_currency, filters)
					ytd_sum += get_balalnce_in_usd(row.outstanding_amount, row.account_currency, filters)

			context[month.lower()] = c_outstanding_amount
		
		context["ytd"] = ytd_sum
	
		data.append(context)

	return data
			

def get_balalnce_in_usd(ytd_balance, account_currency, filters):
	if account_currency == "AED":
		return ytd_balance * flt(filters.get("aed_exchange_rate"))
	
	if account_currency == "RUB":
		return ytd_balance * flt(filters.get("rub_exchange_rate"))
	
	if account_currency == "EUR":
		return ytd_balance * flt(filters.get("eur_exchange_rate"))

	return ytd_balance


def get_all_customer(filters):

	all_customer = frappe.db.sql(
		"""
		SELECT distinct customer FROM 
		`tabSales Invoice` si 
		where si.docstatus = 1
		-- and customer = 'HUMANS OOO'
		and year(posting_date) = %(fiscal_year)s""",{'fiscal_year': filters.get('fiscal_year')}, as_dict=1)
	
	
	return all_customer

def get_columns(filters):
	return [
		{
			"label": _(f"Customer"),
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 180,
		},
		{
			"label": _("Cluster"),
			"fieldname": "cluster",
			"fieldtype": "Link",
			"options": "cluster",
			"width": 120,
		},
		{
			"label": _(f"January {filters.get('fiscal_year')}"),
			"fieldname": "january",
			"fieldtype": "Currency",
			"options": "usd_currency",
			"width": 130,
		},
		{
			"label": _(f"February {filters.get('fiscal_year')}"),
			"fieldname": "february",
			"fieldtype": "Currency",
			"options": "usd_currency",
			"width": 130,
		},
		{
			"label": _(f"March {filters.get('fiscal_year')}"),
			"fieldname": "march",
			"fieldtype": "Currency",
			"options": "usd_currency",
			"width": 130,
		},
		{
			"label": _(f"April {filters.get('fiscal_year')}"),
			"fieldname": "april",
			"fieldtype": "Currency",
			"options": "usd_currency",
			"width": 130,
		},
		{
			"label": _(f"May {filters.get('fiscal_year')}"),
			"fieldname": "may",
			"fieldtype": "Currency",
			"options": "usd_currency",
			"width": 130,
		},
		{
			"label": _(f"June {filters.get('fiscal_year')}"),
			"fieldname": "june",
			"fieldtype": "Currency",
			"options": "usd_currency",
			"width": 130,
		},
		{
			"label": _(f"July {filters.get('fiscal_year')}"),
			"fieldname": "july",
			"fieldtype": "Currency",
			"options": "usd_currency",
			"width": 130,
		},
		{
			"label": _(f"August {filters.get('fiscal_year')}"),
			"fieldname": "august",
			"fieldtype": "Currency",
			"options": "usd_currency",
			"width": 130,
		},
		{
			"label": _(f"September {filters.get('fiscal_year')}"),
			"fieldname": "september",
			"fieldtype": "Currency",
			"options": "usd_currency",
			"width": 130,
		},
		{
			"label": _(f"October {filters.get('fiscal_year')}"),
			"fieldname": "october",
			"fieldtype": "Currency",
			"options": "usd_currency",
			"width": 130,
		},
		{
			"label": _(f"November {filters.get('fiscal_year')}"),
			"fieldname": "november",
			"fieldtype": "Currency",
			"options": "usd_currency",
			"width": 130,
		},
		{
			"label": _(f"December {filters.get('fiscal_year')}"),
			"fieldname": "december",
			"fieldtype": "Currency",
			"options": "usd_currency",
			"width": 130,
		},
		{
			"label": _(f"YTD {filters.get('fiscal_year')}"),
			"fieldname": "ytd",
			"fieldtype": "Currency",
			"options": "usd_currency",
			"width": 130,
		}
	]