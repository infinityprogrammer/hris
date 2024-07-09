# Copyright (c) 2023, Ahmed Emam and contributors
# For license information, please see license.txt

import frappe
from frappe import _, _dict
from frappe.utils import cstr, getdate


def execute(filters=None):
	columns, data = [], []
	if not filters.get("company"):
		return

	if not filters.get("till_date"):
		return

	data = get_data(filters)
	columns = get_columns(filters)

	return columns, data

def get_all_customer(company, till_date):

	customers = frappe.db.sql(
        """SELECT distinct customer_code FROM `tabSales Invoice` 
		where outstanding_amount NOT BETWEEN -100 AND 100 
		and docstatus = 1 and company = '{0}' and posting_date <= '{1}'""".format(company, till_date),
        as_dict=1,
    )

	return customers

def get_data(filters):
	data_inv = []
	customer_list = get_all_customer(filters.get("company"), filters.get("till_date"))

	company_currency = frappe.db.get_value('Company', filters.get("company"), 'default_currency')
	
	all_customer_outstanding_sum = 0
	for customer in customer_list:

		invoices = frappe.db.sql(
			"""SELECT
				name,
				(SELECT default_currency FROM `tabCompany` where name = inv.company)base_currency,
				customer,
				posting_date,
				currency,
				grand_total,
				due_date,
				DATEDIFF(curdate(), due_date) AS due_days,
				outstanding_amount,
				(outstanding_amount * conversion_rate)base_outstanding_amount,
				(DATEDIFF(curdate(), due_date) * outstanding_amount) AS val_out
			FROM `tabSales Invoice` inv
			WHERE
				outstanding_amount NOT BETWEEN -100 AND 100
				and posting_date <= %(posting_date)s
				AND docstatus = 1
				AND customer_code = %(customer_code)s
				AND company = %(company)s """,
			{
				'customer_code': customer.customer_code,
				'company': filters.get("company"),
				'posting_date': filters.get("till_date"),
			},
			as_dict=1
		)

		due_days_sum = 0
		outstanding_sum = 0
		last_customer = None
		value_outstanding_sum = 0
		per_customer_outstanding_sum = 0

		for inv in invoices:
			context = {}
			context['invoice_no'] = inv.name
			context['customer_code'] = inv.customer
			context['customer_name'] = inv.customer
			context['posting_date'] = inv.posting_date
			context['grand_total'] = inv.grand_total
			context['currency'] = inv.currency
			context['due_date'] = inv.due_date
			context['due_days'] = inv.due_days
			context['outstanding_amount'] = inv.outstanding_amount
			
			context['base_currency'] = inv.base_currency
			context['base_outstanding_amount'] = inv.base_outstanding_amount

			due_days_sum += inv.due_days
			outstanding_sum += inv.outstanding_amount
			
			last_customer = inv.customer
			per_customer_outstanding_sum += inv.base_outstanding_amount
			all_customer_outstanding_sum += inv.base_outstanding_amount
			context['customer_balance'] = per_customer_outstanding_sum
			context['total_balance'] = all_customer_outstanding_sum
			context['value_outstanding'] = inv.due_days * per_customer_outstanding_sum
			value_outstanding_sum += inv.due_days * per_customer_outstanding_sum
			data_inv.append(context)
		
		cons_context = {}
		cons_context['customer_code'] = f"<b>{last_customer}</b>"
		cons_context['customer_name'] = last_customer
		cons_context['due_days'] = due_days_sum
		cons_context['customer_balance'] = per_customer_outstanding_sum
		cons_context['value_outstanding'] = value_outstanding_sum
		cons_context['avg_value_outstanding'] = value_outstanding_sum / due_days_sum if due_days_sum else 1
		cons_context['base_currency'] = company_currency
		
		data_inv.append(cons_context)

	return data_inv


def get_columns(filters):
	return [
		{
			"label": _("Invoice No"),
			"fieldname": "invoice_no",
			"fieldtype": "Link",
			"options": "Sales Invoice",
			"width": 170,
		},
		{
			"label": _("Customer Code"),
			"fieldname": "customer_code",
			"fieldtype": "Data",
			"width": 140,
		},
		{
			"label": _("Customer Name"),
			"fieldname": "customer_name",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 150,
		},
		{
			"label": _("Invoice Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 130,
		},
		{
			"label": _("Grand Total"),
			"fieldname": "grand_total",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150,
		},
		{
			"label": _("Invoice Outstanding"),
			"fieldname": "outstanding_amount",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150,
		},
		{
			"label": _("Currency"),
			"fieldname": "currency",
			"fieldtype": "Link",
			"options": "Currency",
			"width": 100,
		},
		{
			"label": _("Outstanding Base Currency"),
			"fieldname": "base_outstanding_amount",
			"fieldtype": "Currency",
			"options": "base_currency",
			"width": 150,
		},
		{
			"label": _("Due Date"),
			"fieldname": "due_date",
			"fieldtype": "Date",
			"width": 100,
		},
		{
			"label": _("Due Days"),
			"fieldname": "due_days",
			"fieldtype": "Int",
			"width": 100,
		},
		{
			"label": _("Customer Balance"),
			"fieldname": "customer_balance",
			"fieldtype": "Currency",
			"options": "base_currency",
			"width": 140,
		},
		{
			"label": _("Total Balance"),
			"fieldname": "total_balance",
			"fieldtype": "Currency",
			"options": "base_currency",
			"width": 140,
		},
		{
			"label": _("Value Outstanding"),
			"fieldname": "value_outstanding",
			"fieldtype": "Currency",
			"options": "base_currency",
			"width": 140,
		},
		{
			"label": _("Average Value Outstanding"),
			"fieldname": "avg_value_outstanding",
			"fieldtype": "Currency",
			"options": "base_currency",
			"width": 200,
		}
	]