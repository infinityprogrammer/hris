# Copyright (c) 2024, RAFI and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import (
	add_days,
	add_months,
	cint,
	date_diff,
	flt,
	get_first_day,
	get_last_day,
	getdate,
	today,
	add_to_date
)


def execute(filters=None):
	columns, data = [], []

	data = get_data(filters)
	columns = get_columns(filters)

	return columns, data



def get_data(filters):
	data = []

	clusters = get_cluster_list(filters)

	customers = get_customer_list(filters)
	company_currency = frappe.db.get_value('Company', filters.get("company"), 'default_currency')
	for cluster in clusters:
		
		for customer in customers:
			customer_data = {}
			customer_data["company"] = filters.get("company")
			customer_data["currency"] = company_currency
			customer_data["cluster"] = cluster.cluster
			customer_data["customer"] = customer.customer
			customer_data["opening_till"] = get_customer_opening_due(filters, customer.customer, cluster.cluster)
			customer_data["current_month_from"] = get_customer_till_monthend(filters, customer.customer, cluster.cluster)

			if not customer_data["opening_till"] and not customer_data["current_month_from"]:
				pass
			else:
				data.append(customer_data)

	return data

def get_customer_opening_due(filters, customer, cluster):

	opening_due = frappe.db.sql(
		"""
		SELECT 
		--
		ifnull(sum(round((IF((SELECT account_currency from `tabAccount` acc where acc.name = inv.debit_to) = inv.currency, outstanding_amount, 
		(outstanding_amount/conversion_rate)))*conversion_rate, 2)), 0) as base_outstanding_amount
		--
		FROM `tabSales Invoice` inv
		where outstanding_amount != 0
		and company = %(company)s
		and customer = %(customer)s
		and due_date <= %(due_date)s
		and cluster = %(cluster)s
		and docstatus = 1
		""",{'customer': customer, 'company': filters.get("company"), 
	   		'due_date': filters.get("till_date"), 'cluster': cluster},as_dict=1)

	return opening_due[0].base_outstanding_amount

def get_customer_till_monthend(filters, customer, cluster):
	
	first = add_to_date(filters.get("till_date"), days=1)
	last_day = get_last_day(filters.get("till_date"))

	opening_due = frappe.db.sql(
		"""
		SELECT 
		--
		ifnull(sum(round((IF((SELECT account_currency from `tabAccount` acc where acc.name = inv.debit_to) = inv.currency, outstanding_amount, 
		(outstanding_amount/conversion_rate)))*conversion_rate, 2)), 0) as base_outstanding_amount
		--
		FROM `tabSales Invoice` inv
		where outstanding_amount != 0
		and company = %(company)s
		and customer = %(customer)s
		and due_date between %(first)s and %(last_day)s
		and docstatus = 1
		and cluster = %(cluster)s
		""",{'customer': customer, 'company': filters.get("company"), 
	   		'first': first, 'last_day': last_day, 'cluster': cluster},as_dict=1)

	return opening_due[0].base_outstanding_amount

def get_customer_list(filters):

	last_day = get_last_day(filters.get("till_date"))
	customer_list = frappe.db.sql(
		"""
		SELECT distinct customer FROM `tabSales Invoice` where docstatus = 1
		and company = %(company)s and due_date <= %(last_day)s 
		and outstanding_amount not between -1 and 100""",{'last_day': last_day, 'company': filters.get("company")},as_dict=1)

	return customer_list

def get_cluster_list(filters):
	
	last_day = get_last_day(filters.get("till_date"))

	customer_list = frappe.db.sql(
		"""
		SELECT distinct cluster FROM `tabSales Invoice` where docstatus = 1
		and company = %(company)s and due_date <= %(last_day)s 
		and outstanding_amount not between -1 and 100 """,{'last_day': last_day, 'company': filters.get("company")},as_dict=1)

	return customer_list


def get_columns(filters):

	tilldate = add_to_date(filters.get("till_date"), days=1)

	return [
		{
			"label": _("Company"),
			"fieldname": "company",
			"fieldtype": "Link",
			"options": "Company",
			"width": 180,
		},
		{
			"label": _("Cluster"),
			"fieldname": "cluster",
			"fieldtype": "Link",
			"options": "cluster",
			"width": 140,
		},
		{
			"label": _("Customer"),
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 140,
		},
		{
			"label": _(f"Opening Till {filters.get('till_date')}"),
			"fieldname": "opening_till",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 190,
		},
		{
			"label": _(f"Current Month From {tilldate}"),
			"fieldname": "current_month_from",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 230,
		},
	]