# Copyright (c) 2023, Ahmed Emam and contributors
# For license information, please see license.txt

import frappe
from frappe import _, _dict
from frappe.utils import cstr, getdate, cint


def execute(filters=None):
	columns, data = [], []
	data = get_data(filters)
	columns = get_columns(filters)
	return columns, data

def get_data(filters):
	data = []
	context_opening = {}
	context_opening = get_opening(filters)
	# context_opening['title'] = f"<b>Opening Balances<b>"
	
	data.append(context_opening)

	cash_in_title = {}
	cash_in_title['title'] = f"<b>Cash inflow (Money-in)</b>"
	
	data.append(cash_in_title)

	customer_list = get_dist_customer(filters)
	
	all_months_lowercase = [
		"january",
		"february",
		"march",
		"april",
		"may",
		"june",
		"july",
		"august",
		"september",
		"october",
		"november",
		"december"
	]

	for row in customer_list:
		customer_w = {}
		customer_w['title'] = row.customer
		for index, month in enumerate(all_months_lowercase):
			customer_code = frappe.db.get_value('Customer', row.customer, 'customer_code')
			val = get_customer_cash_in(filters, customer_code, index+1)
			customer_w[month] = val[0].balance
		
		data.append(customer_w)

	month_sums = {
		'january': 0,
		'february': 0,
		'march': 0,
		'april': 0,
		'may': 0,
		'june': 0,
		'july': 0,
		'august': 0,
		'september': 0,
		'october': 0,
		'november': 0,
		'december': 0
	}

	for item in data[1:]:
		for month, value in item.items():
			if month != 'title':
				month_sums[month] += value

	month_sums['title'] = f"<b>Sum of Money (IN)</b>"
	data.append(month_sums)

	empty = {}
	empty['title'] = ""
	data.append(empty)

	cash_out_title = {}
	cash_out_title['title'] = f"<b>Cash Out flow (Money-Out)</b>"
	data.append(cash_out_title)

	out_context = {}
	out_items = get_cash_out_against(filters)

	supp_map = {
		'SUP-0012': 'HABARIPAY',
		'SUP-0020' : 'TSYS Card Tech LTD',
		'SUP-0024': 'ICC Solutions Limited',
		'SUP-0026': 'KEDINASAL',
	}
	
	out_list = []
	for out_row in out_items:
		out_it = {}
		out_it['title'] = out_row.against

		supp_name = supp_map.get(out_row.against)
		if supp_name:
			out_it['title'] = supp_name
		else:
			out_it['title'] = out_row.against

		for index, month in enumerate(all_months_lowercase):
			cashout = get_customer_cash_out(filters, index+1, out_row.against)
			if cashout:
				out_it[month] = cashout[0].balance
		
		out_list.append(out_it)

		data.append(out_it)
	
	month_sums_out = {
		'january': 0,
		'february': 0,
		'march': 0,
		'april': 0,
		'may': 0,
		'june': 0,
		'july': 0,
		'august': 0,
		'september': 0,
		'october': 0,
		'november': 0,
		'december': 0
	}

	# Iterate through the list and accumulate the values for each month
	for item in out_list:
		for month, value in item.items():
			if month != 'title':
				month_sums_out[month] += value

	month_sums_out['title'] = "<b>Sum of Money (OUT)</b>"
	
	data.append(month_sums_out)

	empty = {}
	empty['title'] = ""
	data.append(empty)

	# net_empty = {}
	# net_empty['title'] = "<b>Net Cashflow</b>"
	# data.append(net_empty)

	difference = {}
	for month in month_sums.keys():
		if month != 'title':
			difference[month] = month_sums[month] + month_sums_out[month]

	difference['title'] = "<b>Net Cashflow</b>"
	data.append(difference)


	end_balalnce = {}
	for month in month_sums.keys():
		if month != 'title':
			end_balalnce[month] = context_opening[month] + difference[month]
	
	end_balalnce['title'] = "<b>Ending balance</b>"
	data.append(end_balalnce)
	return data


def get_customer_cash_out(filters, month, against):
	
	out_val = frappe.db.sql(
        """
		SELECT against, ifnull(round((sum(credit)), 2), 0)* -1 as balance
		FROM `tabGL Entry` gl, `tabAccount` acc 
		where gl.account = acc.name
		and gl.company = %(company)s
		and credit > 0
		and gl.is_cancelled = 0
		and acc.account_type = 'Bank'
		and month(posting_date) = %(month)s and year(posting_date) = %(year)s
		and against = %(against)s
		group by against
		""",{'month': month,'year': filters.get("fiscal_year"), 'company': filters.get("company"), 'against': against}, as_dict=1,
    )

	return out_val

def get_cash_out_against(filters):
	
	out_items = frappe.db.sql(
        """
		SELECT against, ifnull(round((sum(credit)), 2), 0)* -1 as balance
		FROM `tabGL Entry` gl, `tabAccount` acc 
		where gl.account = acc.name
		and gl.company = %(company)s
		and credit > 0
		and gl.is_cancelled = 0
		and acc.account_type = 'Bank'
		and year(posting_date) = %(year)s
		group by against
		""",{'year': filters.get("fiscal_year"), 'company': filters.get("company")}, as_dict=1,
    )

	return out_items

def get_customer_cash_in(filters, customer_code, month):
	
	cust_str = ""
	if customer_code:
		cust_str = "against in (select name from `tabCustomer` where customer_code = %(customer_code)s)"
	else:
		cust_str = "against not in (select name from `tabCustomer`)"

	customer_val = frappe.db.sql(
        """
		SELECT ifnull(round((sum(debit)), 2), 0)balance
		FROM `tabGL Entry` gl, `tabAccount` acc 
		where gl.account = acc.name
		and gl.company = %(company)s
		and debit > 0
		and gl.is_cancelled = 0
		and acc.account_type = 'Bank'
		and month(posting_date) = %(month)s and year(posting_date) = %(year)s
		and {cust_str}
		""".format(cust_str=cust_str),{'month': month,'year': filters.get("fiscal_year"), 'company': filters.get("company"),'customer_code':customer_code}, as_dict=1,
    )

	return customer_val


def get_opening(filters):
	
	opening = {}

	jan_open_balance = get_jan_opening(filters)
	opening['january'] = jan_open_balance

	months_lowercase = [
		"february",
		"march",
		"april",
		"may",
		"june",
		"july",
		"august",
		"september",
		"october",
		"november",
		"december"
	]
	for index, month in enumerate(months_lowercase):
		
		all_opening = get_all_opening(filters, index+1)
		opening[month] = all_opening

	opening['title'] = f"<b>Opening Balance</b>"
	
	return opening


def get_dist_customer(filters):
	
	dist_customer = frappe.db.sql(
        """
		SELECT against as customer
		FROM `tabGL Entry` gl, `tabAccount` acc 
		where gl.account = acc.name
		and gl.company = %(company)s
		and gl.is_cancelled = 0
		and acc.account_type = 'Bank'
		and year(posting_date) = %(year)s
		and against in (SELECT name FROM `tabCustomer`)
		group by against
		union ALL
		SELECT 'Others'
		""",{'year': filters.get("fiscal_year"), 'company': filters.get("company")}, as_dict=1,
    )

	return dist_customer



def get_all_opening(filters, month):
	import datetime
	year = cint(filters.get("fiscal_year"))

	last_day = datetime.date(year, month, 1) + datetime.timedelta(days=32)
	last_day = last_day.replace(day=1) - datetime.timedelta(days=1)

	all_opening_balalnce = frappe.db.sql(
        """
		SELECT ifnull(round((sum(debit) - sum(credit)), 2), 0)balance
		FROM `tabGL Entry` gl, `tabAccount` acc 
		where gl.account = acc.name
		and gl.company = %(company)s
		and gl.is_cancelled = 0
		and acc.account_type = 'Bank'
		and gl.posting_date <= %(last_day)s
		""",{'month': month, 'year': year, 'company': filters.get("company"), 'last_day':last_day}, as_dict=1,
    )

	return all_opening_balalnce[0].balance


def get_jan_opening(filters):
	
	year = cint(filters.get("fiscal_year"))

	jan_opening_balalnce = frappe.db.sql(
        """
		SELECT ifnull(round((sum(debit) - sum(credit)), 2), 0)balance
		FROM `tabGL Entry` gl, `tabAccount` acc 
		where gl.account = acc.name
		and gl.company = %(company)s
		and gl.is_cancelled = 0
		and acc.account_type = 'Bank'
		and year(gl.posting_date) <= %(year)s
		""",{'year': year - 1, 'company': filters.get("company")}, as_dict=1,
    )

	return jan_opening_balalnce[0].balance

def get_columns(filters):
	
	return [
		{
			"label": _(f"<b>{filters.get('company')}</b>"),
			"fieldname": "title",
			"fieldtype": "Data",
			"width": 300,
		},
		{
			"label": _(f"January {filters.get('fiscal_year')}"),
			"fieldname": "january",
			"fieldtype": "Float",
			"width": 130,
		},
		{
			"label": _(f"February {filters.get('fiscal_year')}"),
			"fieldname": "february",
			"fieldtype": "Float",
			"width": 130,
		},
		{
			"label": _(f"March {filters.get('fiscal_year')}"),
			"fieldname": "march",
			"fieldtype": "Float",
			"width": 130,
		},
		{
			"label": _(f"April {filters.get('fiscal_year')}"),
			"fieldname": "april",
			"fieldtype": "Float",
			"width": 130,
		},
		{
			"label": _(f"May {filters.get('fiscal_year')}"),
			"fieldname": "may",
			"fieldtype": "Float",
			"width": 130,
		},
		{
			"label": _(f"June {filters.get('fiscal_year')}"),
			"fieldname": "june",
			"fieldtype": "Float",
			"width": 130,
		},
		{
			"label": _(f"July {filters.get('fiscal_year')}"),
			"fieldname": "july",
			"fieldtype": "Float",
			"width": 130,
		},
		{
			"label": _(f"August {filters.get('fiscal_year')}"),
			"fieldname": "august",
			"fieldtype": "Float",
			"width": 130,
		},
		{
			"label": _(f"September {filters.get('fiscal_year')}"),
			"fieldname": "september",
			"fieldtype": "Float",
			"width": 130,
		},
		{
			"label": _(f"October {filters.get('fiscal_year')}"),
			"fieldname": "october",
			"fieldtype": "Float",
			"width": 130,
		},
		{
			"label": _(f"November {filters.get('fiscal_year')}"),
			"fieldname": "november",
			"fieldtype": "Float",
			"width": 130,
		},
		{
			"label": _(f"December {filters.get('fiscal_year')}"),
			"fieldname": "december",
			"fieldtype": "Float",
			"width": 130,
		}
	]