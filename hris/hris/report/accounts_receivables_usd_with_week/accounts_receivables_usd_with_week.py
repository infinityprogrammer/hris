# Copyright (c) 2025, RAFI and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate, now_datetime, nowdate, flt, cint


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters) 
	
	return columns, data

def get_data(filters):
	
	data = []
	customers = frappe.db.sql("""SELECT distinct customer 
								FROM `tabSales Invoice` where outstanding_amount != 0
						   		and docstatus = 1
								and year(posting_date) = 2024""", as_dict=1)

	grand_total = 0
	for row in customers:

		exchange_rate = 1
		customer = row.customer

		outstandings = frappe.db.sql("""SELECT customer, WEEK(posting_date)week_no, sum(outstanding_amount) as outstanding_amount
								FROM `tabSales Invoice` where customer = %(customer)s
								and year(posting_date) = 2024
							   	and docstatus = 1
								group by WEEK(posting_date) having sum(outstanding_amount) != 0""", 
								{'customer': customer}, as_dict=1)

		cust_total = 0
		for d in outstandings:

			if row.currency == "USD":
				d.outstanding_amount = flt(d.outstanding_amount)*exchange_rate
			
			if row.currency == "EUR":
				d.outstanding_amount = flt(d.outstanding_amount)* 1.05
			
			if row.currency == "RUB":
				d.outstanding_amount = flt(d.outstanding_amount)* 0.011
			
			if row.currency == "AED":
				d.outstanding_amount = flt(d.outstanding_amount)* 0.27

			d['customer_name'] = d.customer
			d['week_no'] = d.week_no
			d['outstanding_amount'] = d.outstanding_amount
			d['currency'] = "USD"

			grand_total += d.outstanding_amount
			cust_total += d.outstanding_amount
		
			data.append(d)
		
		
		toatl_str = f"{frappe.bold(customer)} {frappe.bold('Total')}"
		data.append({'customer_name': toatl_str, 'week_no': '', 'outstanding_amount': cust_total})
		data.append({})
	

	
	data.append({'customer_name': frappe.bold('Grand Total'), 'week_no': '', 'outstanding_amount': grand_total})

	return data

def get_columns():
	columns = [
		
		{
			"fieldname": "customer_name",
			"label": "Customer Name",
			"fieldtype": "Data",
			"width": 300
		},
		# {
		# 	"fieldname": "currency",
		# 	"label": "Currency",
		# 	"fieldtype": "Data",
		# 	"width": 100
		# },
		{
			"fieldname": "week_no",
			"label": "Week",
			"fieldtype": "Data",
			"width": 90
		},
		{
			"fieldname": "outstanding_amount",
			"label": "Outstanding Amount",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 180
		},
		

	]
	return columns