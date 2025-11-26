# Copyright (c) 2024, RAFI and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe import _, _dict
from frappe.utils import cstr, getdate, cint, add_to_date, get_last_day, add_days, flt
from datetime import datetime
from dateutil.relativedelta import relativedelta
from hris.hris.report.cashflow_regular.cashflow_regular import get_cashflow_category



def execute(filters=None):
	columns, data = [], []

	data = get_data(filters)
	columns = get_columns(filters)

	for row in data:
		row['category'] = get_cashflow_category(row.get('title') or "")
	
	return columns, data



def get_data(filters):

	data = []

	context_opening = get_opening(filters)
	data.append(context_opening)

	cash_in_title = {}
	cash_in_title['title'] = f"<b>Cash inflow (Money-in)</b>"
	data.append(cash_in_title)

	customer_list = get_dist_customer(filters)

	for customer in customer_list:
		opening_customer = {}
		opening_customer["title"] = customer.customer

		customer_opening_outstanding = get_customer_opening_outstanding(customer.customer, filters)
		opening_customer["opening_till"] = customer_opening_outstanding

		opening_customer["current_month_from"] = get_current_month_balance(customer.customer, filters)
		opening_customer["next_1"] = get_outstanding_from_to(customer.customer, filters, 1)
		opening_customer["next_2"] = get_outstanding_from_to(customer.customer, filters, 2)
		opening_customer["next_3"] = get_outstanding_from_to(customer.customer, filters, 3)

		data.append(opening_customer)

	sum_of_money_in = {}
	sum_of_money_in['title'] = f"<b>Customer - Sum of Money In</b>"

	sum_of_money_in['opening_till'] = get_all_customer_opening_outstanding(filters)
	sum_of_money_in["current_month_from"] = get_current_month_balance_all_customer(filters)

	sum_of_money_in["next_1"] = get_outstanding_from_to_all_customer(filters, 1)
	sum_of_money_in["next_2"] = get_outstanding_from_to_all_customer(filters, 2)
	sum_of_money_in["next_3"] = get_outstanding_from_to_all_customer(filters, 3)

	data.append(sum_of_money_in)

	cash_out_title = {}
	cash_out_title['title'] = f"<b>Cash Out flow (Money - Out)</b>"
	data.append(cash_out_title)

	supplier_list = get_dist_supplier(filters)

	for supplier in supplier_list:
		opening_supplier = {}
		opening_supplier["title"] = supplier.supplier
		
		supplier_opening_outstanding = get_supplier_opening_outstanding(supplier.supplier, filters)
		opening_supplier["opening_till"] = supplier_opening_outstanding

		opening_supplier["current_month_from"] = get_current_month_balance_supplier(supplier.supplier, filters)
		opening_supplier["next_1"] = get_outstanding_from_to_supplier(supplier.supplier, filters, 1)
		opening_supplier["next_2"] = get_outstanding_from_to_supplier(supplier.supplier, filters, 2)
		opening_supplier["next_3"] = get_outstanding_from_to_supplier(supplier.supplier, filters, 3)

		data.append(opening_supplier)
	
	sum_of_money_out = {}
	sum_of_money_out['title'] = f"<b>Supplier - Sum of Money Out</b>"
	sum_of_money_out['opening_till'] = get_all_supplier_opening_outstanding(filters) *-1

	sum_of_money_out["current_month_from"] = get_current_month_balance_all_supplier(filters) *-1

	sum_of_money_out["next_1"] = get_outstanding_from_to_all_supplier(filters, 1) *-1
	sum_of_money_out["next_2"] = get_outstanding_from_to_all_supplier(filters, 2) *-1
	sum_of_money_out["next_3"] = get_outstanding_from_to_all_supplier(filters, 3) *-1
	data.append(sum_of_money_out)


	account_title = {}
	account_title['title'] = f"<b>Account Entry (Money - Out)</b>"
	data.append(account_title)

	accounts = get_dist_accounts(filters)

	for account in accounts:
		account_val = {}
		account_val["title"] = account.account
		
		account_val["opening_till"] = 0

		account_val["current_month_from"] = get_account_budget_value(account.account, filters, 0)

		account_val["next_1"] = get_account_budget_value(account.account, filters, 1)
		account_val["next_2"] = get_account_budget_value(account.account, filters, 2)
		account_val["next_3"] = get_account_budget_value(account.account, filters, 3)

		data.append(account_val)
	
	account_sum_title = {}
	account_sum_title['title'] = f"<b>Account - Sum of Money Out</b>"
	account_sum_title["opening_till"] = 0

	account_sum_title["current_month_from"] = get_all_account_budget_value(filters, 0) * -1

	account_sum_title["next_1"] = get_all_account_budget_value(filters, 1) * -1
	account_sum_title["next_2"] = get_all_account_budget_value(filters, 2) * -1
	account_sum_title["next_3"] = get_all_account_budget_value(filters, 3) * -1

	data.append(account_sum_title)


	net_cash_flow = {}
	net_cash_flow['title'] = f"<b>Net Cashflow</b>"
	
	cash_in = get_all_customer_opening_outstanding(filters)
	supplier_out = get_all_supplier_opening_outstanding(filters) *-1
	account_out = 0
	

	net_cash_flow["opening_till"] = flt(cash_in)+flt(supplier_out)+flt(account_out)


	current_month_in = get_current_month_balance_all_customer(filters)
	current_month_supplier_out = get_current_month_balance_all_supplier(filters) *-1
	current_month_account_out = get_all_account_budget_value(filters, 0) * -1

	net_cash_flow["current_month_from"] = flt(current_month_in)+flt(current_month_supplier_out)+flt(current_month_account_out)

	first_in_customer = get_outstanding_from_to_all_customer(filters, 1)
	first_out_supplier = get_outstanding_from_to_all_supplier(filters, 1) *-1
	first_out_account = get_all_account_budget_value(filters, 1) * -1

	net_cash_flow["next_1"] = flt(first_in_customer)+flt(first_out_supplier)+flt(first_out_account)

	second_in_customer = get_outstanding_from_to_all_customer(filters, 2)
	second_out_supplier = get_outstanding_from_to_all_supplier(filters, 2) *-1
	second_out_account = get_all_account_budget_value(filters, 2) * -1

	net_cash_flow["next_2"] = flt(second_in_customer)+flt(second_out_supplier)+flt(second_out_account)

	third_in_customer = get_outstanding_from_to_all_customer(filters, 3)
	third_out_supplier = get_outstanding_from_to_all_supplier(filters, 3) *-1
	third_out_account = get_all_account_budget_value(filters, 3) * -1

	net_cash_flow["next_3"] = flt(third_in_customer)+flt(third_out_supplier)+flt(third_out_account)

	data.append(net_cash_flow)

	ending_balance = {}
	ending_balance['title'] = f"<b>Ending Balance</b>"
	ending_balance["opening_till"] = net_cash_flow["opening_till"] + flt(context_opening["opening_till"])

	ending_balance["current_month_from"] = net_cash_flow["current_month_from"]

	ending_balance["next_1"] = net_cash_flow["next_1"]
	ending_balance["next_2"] = net_cash_flow["next_2"]
	ending_balance["next_3"] = net_cash_flow["next_3"]

	data.append(ending_balance)

	data[0]["current_month_from"] = ending_balance["opening_till"]
	data[-1]["current_month_from"] = data[-1]["current_month_from"]+ending_balance["opening_till"]

	data[0]["next_1"] = data[-1]["current_month_from"]
	data[-1]["next_1"] += data[0]["next_1"]

	data[0]["next_2"] = data[-1]["next_1"]
	data[-1]["next_2"] += data[0]["next_2"]

	data[0]["next_3"] = data[-1]["next_2"]
	data[-1]["next_3"] += data[0]["next_3"]
		
	return data

def get_opening(filters):
	opening = {}
	opening['title'] = f"<b>Opening Balance</b>"

	opening['opening_till'] = get_initial_opening(filters)

	opening['current_month_from'] = 1
	opening['next_1'] = 1
	opening['next_2'] = 1
	opening['next_3'] = 1
	
	return opening

def get_initial_opening(filters):

	initial_opening = frappe.db.sql(
        """
		SELECT ifnull((sum(debit) - sum(credit)), 0)balance 
		FROM `tabGL Entry` gl where gl.is_cancelled = 0
		and account in (SELECT name FROM `tabAccount` acc 
		where acc.name like '11%%' and acc.is_group = 0 and acc.company = %(company)s)
		and gl.company = %(company)s
		and gl.posting_date <= %(tilldate)s
		""",{'company': filters.get("company"), 'tilldate': filters.get("till_date")}, as_dict=1,
    )
	
	return initial_opening[0].balance


def get_dist_customer(filters):
	
	last_date = get_future_month_last_day(filters.get("till_date"), 3)
	
	dist_customer = frappe.db.sql(
        """
		SELECT distinct customer
		FROM `tabSales Invoice` where company = %(company)s
		and docstatus = 1 and outstanding_amount not between -1 and 200 
		and posting_date <= %(last_date)s
		""",{'company': filters.get("company"), 'last_date': last_date}, as_dict=1,
    )

	return dist_customer

def get_customer_outstanding(filters, customer_code, month):

	customer_outstanding = frappe.db.sql(
        """
		SELECT ifnull(round(sum(outstanding_amount)), 0)outstanding_amount 
		FROM `tabSales Invoice` where docstatus = 1
		and customer = %(customer_code)s
		and company = %(company)s and month(posting_date) = %(month)s
		and year(posting_date) = %(year)s
		""",{'year': filters.get("fiscal_year"), 'month': month, 'company': filters.get("company"), 'customer_code': customer_code}, as_dict=1,
    )

	return customer_outstanding[0].outstanding_amount

def get_columns(filters):

	tilldate = add_to_date(filters.get("till_date"), days=1)
	
	month_1 = get_future_month(filters.get("till_date"), 1)
	month_2 = get_future_month(filters.get("till_date"), 2)
	month_3 = get_future_month(filters.get("till_date"), 3)
	
	return [
		{
			"label": _(f"<b>{filters.get('company')}</b>"),
			"fieldname": "title",
			"fieldtype": "Data",
			"width": 300,
		},
		{
			"label": _(f"Category"),
			"fieldname": "category",
			"fieldtype": "Data",
			"width": 160,
		},
		{
			"label": _(f"Opening Till {filters.get('till_date')}"),
			"fieldname": "opening_till",
			"fieldtype": "Float",
			"width": 180,
		},
		{
			"label": _(f"Current Month From {tilldate}"),
			"fieldname": "current_month_from",
			"fieldtype": "Float",
			"width": 230,
		},
		{
			"label": _(f"{month_1}"),
			"fieldname": "next_1",
			"fieldtype": "Float",
			"width": 130,
		},
		{
			"label": _(f"{month_2}"),
			"fieldname": "next_2",
			"fieldtype": "Float",
			"width": 130,
		},
		{
			"label": _(f"{month_3}"),
			"fieldname": "next_3",
			"fieldtype": "Float",
			"width": 130,
		},
	]

def get_future_month(date_str, months_ahead):
    
	given_date = datetime.strptime(date_str, "%Y-%m-%d")

	future_date = given_date + relativedelta(months=months_ahead)

	month_name = future_date.strftime("%B")
	year = future_date.year

	date_str = f"{month_name} {year}"

	return date_str

def get_future_month_last_day(date_str, months_ahead):
    # Parse the given date string
    given_date = datetime.strptime(date_str, "%Y-%m-%d")
    
    # Calculate the future date
    future_date = given_date + relativedelta(months=months_ahead)
    
    # Calculate the first day of the next month and subtract one day to get the last day of the current month
    next_month = future_date + relativedelta(months=1)
    last_day_date = next_month.replace(day=1) - relativedelta(days=1)
    
    # Extract the month name and year
    month_name = future_date.strftime("%B")
    year = future_date.year
    
    # Format the last day in the desired format
    last_day_formatted = last_day_date.strftime("%Y-%m-%d")
    
    return last_day_formatted

def get_month_first_last_days(date_str, months_ahead):
    
    given_date = datetime.strptime(date_str, "%Y-%m-%d")
    
    future_date = given_date + relativedelta(months=months_ahead)
    
    first_day_date = future_date.replace(day=1)
    
    next_month = future_date + relativedelta(months=1)
    last_day_date = next_month.replace(day=1) - relativedelta(days=1)
    
    first_day_formatted = first_day_date.strftime("%Y-%m-%d")
    last_day_formatted = last_day_date.strftime("%Y-%m-%d")
    
    return first_day_formatted, last_day_formatted

def get_customer_opening_outstanding(customer, filters):
	
	outstand = frappe.db.sql(
        """
		SELECT ifnull(sum(outstanding_amount * conversion_rate), 0)outstanding_amount
		FROM `tabSales Invoice` where company = %(company)s
		and docstatus = 1 and customer = %(customer)s
		and due_date <= %(due_date)s and outstanding_amount not between -1 and 200
		""",{'company': filters.get("company"), 'customer': customer, 'due_date': filters.get("till_date")}, as_dict=1,
    )

	return outstand[0].outstanding_amount

def get_all_customer_opening_outstanding(filters):
	
	outstand = frappe.db.sql(
        """
		SELECT ifnull(sum(outstanding_amount * conversion_rate), 0)outstanding_amount
		FROM `tabSales Invoice` where company = %(company)s
		and docstatus = 1 
		and due_date <= %(due_date)s;
		""",{'company': filters.get("company"), 'due_date': filters.get("till_date")}, as_dict=1,
    )

	return outstand[0].outstanding_amount


def get_current_month_balance(customer, filters):
	
	month_last_day = get_last_day(filters.get("till_date"))
	month_first_day = add_days(filters.get("till_date"), 1)

	outstand = frappe.db.sql(
        """
		SELECT ifnull(sum(outstanding_amount * conversion_rate), 0)outstanding_amount
		FROM `tabSales Invoice` where company = %(company)s
		and docstatus = 1 and customer = %(customer)s
		and due_date between %(month_first_day)s and %(month_last_day)s;
		""",{'company': filters.get("company"), 'customer': customer, 'month_first_day': month_first_day, 'month_last_day': month_last_day}, as_dict=1,
    )

	return outstand[0].outstanding_amount

def get_current_month_balance_all_customer(filters):
	
	month_last_day = get_last_day(filters.get("till_date"))
	month_first_day = add_days(filters.get("till_date"), 1)

	outstand = frappe.db.sql(
        """
		SELECT ifnull(sum(outstanding_amount * conversion_rate), 0)outstanding_amount
		FROM `tabSales Invoice` where company = %(company)s
		and docstatus = 1
		and due_date between %(month_first_day)s and %(month_last_day)s;
		""",{'company': filters.get("company"), 'month_first_day': month_first_day, 'month_last_day': month_last_day}, as_dict=1,
    )

	return outstand[0].outstanding_amount

def get_outstanding_from_to(customer, filters, index):
	
	first_day, last_day = get_month_first_last_days(filters.get("till_date"), index)

	outstand = frappe.db.sql(
        """
		SELECT ifnull(sum(outstanding_amount * conversion_rate), 0)outstanding_amount
		FROM `tabSales Invoice` where company = %(company)s
		and docstatus = 1 and customer = %(customer)s
		and due_date between %(first_day)s and %(last_day)s and outstanding_amount not between -1 and 200
		""",{'company': filters.get("company"), 'customer': customer, 'first_day': first_day, 'last_day': last_day}, as_dict=1,
    )

	return outstand[0].outstanding_amount

def get_dist_supplier(filters):

	last_date = get_future_month_last_day(filters.get("till_date"), 3)
	
	dist_supplier = frappe.db.sql(
        """
		SELECT distinct supplier
		FROM `tabPurchase Invoice` where company = %(company)s
		and docstatus = 1 and outstanding_amount != 0 
		and posting_date <= %(last_date)s
		""",{'company': filters.get("company"), 'last_date': last_date}, as_dict=1,
    )

	return dist_supplier

def get_supplier_opening_outstanding(supplier, filters):
	
	outstand = frappe.db.sql(
        """
		SELECT ifnull(sum(outstanding_amount * conversion_rate), 0)outstanding_amount
		FROM `tabPurchase Invoice` where company = %(company)s
		and docstatus = 1 and supplier = %(supplier)s
		and due_date <= %(due_date)s;
		""",{'company': filters.get("company"), 'supplier': supplier, 'due_date': filters.get("till_date")}, as_dict=1,
    )

	return outstand[0].outstanding_amount

def get_current_month_balance_supplier(supplier, filters):
	
	month_last_day = get_last_day(filters.get("till_date"))
	month_first_day = add_days(filters.get("till_date"), 1)

	outstand = frappe.db.sql(
        """
		SELECT ifnull(sum(outstanding_amount * conversion_rate), 0)outstanding_amount
		FROM `tabPurchase Invoice` where company = %(company)s
		and docstatus = 1 and supplier = %(supplier)s
		and due_date between %(month_first_day)s and %(month_last_day)s;
		""",{'company': filters.get("company"), 'supplier': supplier, 'month_first_day': month_first_day, 'month_last_day': month_last_day}, as_dict=1,
    )

	return outstand[0].outstanding_amount

def get_outstanding_from_to_supplier(supplier, filters, index):
	
	first_day, last_day = get_month_first_last_days(filters.get("till_date"), index)

	outstand = frappe.db.sql(
        """
		SELECT ifnull(sum(outstanding_amount * conversion_rate), 0)outstanding_amount
		FROM `tabPurchase Invoice` where company = %(company)s
		and docstatus = 1 and supplier = %(supplier)s
		and due_date between %(first_day)s and %(last_day)s;
		""",{'company': filters.get("company"), 'supplier': supplier, 'first_day': first_day, 'last_day': last_day}, as_dict=1,
    )

	return outstand[0].outstanding_amount

def get_all_supplier_opening_outstanding(filters):
	
	outstand = frappe.db.sql(
        """
		SELECT ifnull(sum(outstanding_amount * conversion_rate), 0)outstanding_amount
		FROM `tabPurchase Invoice` where company = %(company)s
		and docstatus = 1 
		and due_date <= %(due_date)s;
		""",{'company': filters.get("company"), 'due_date': filters.get("till_date")}, as_dict=1,
    )

	return outstand[0].outstanding_amount

def get_current_month_balance_all_supplier(filters):
	
	month_last_day = get_last_day(filters.get("till_date"))
	month_first_day = add_days(filters.get("till_date"), 1)

	outstand = frappe.db.sql(
        """
		SELECT ifnull(sum(outstanding_amount * conversion_rate), 0)outstanding_amount
		FROM `tabPurchase Invoice` where company = %(company)s
		and docstatus = 1
		and due_date between %(month_first_day)s and %(month_last_day)s;
		""",{'company': filters.get("company"), 'month_first_day': month_first_day, 'month_last_day': month_last_day}, as_dict=1,
    )

	return outstand[0].outstanding_amount

def get_outstanding_from_to_all_customer(filters, index):
	
	first_day, last_day = get_month_first_last_days(filters.get("till_date"), index)

	outstand = frappe.db.sql(
        """
		SELECT ifnull(sum(outstanding_amount * conversion_rate), 0)outstanding_amount
		FROM `tabSales Invoice` where company = %(company)s
		and docstatus = 1
		and due_date between %(first_day)s and %(last_day)s;
		""",{'company': filters.get("company"), 'first_day': first_day, 'last_day': last_day}, as_dict=1,
    )

	return outstand[0].outstanding_amount

def get_outstanding_from_to_all_supplier(filters, index):
	
	first_day, last_day = get_month_first_last_days(filters.get("till_date"), index)

	outstand = frappe.db.sql(
        """
		SELECT ifnull(sum(outstanding_amount * conversion_rate), 0)outstanding_amount
		FROM `tabPurchase Invoice` where company = %(company)s
		and docstatus = 1
		and due_date between %(first_day)s and %(last_day)s;
		""",{'company': filters.get("company"), 'first_day': first_day, 'last_day': last_day}, as_dict=1,
    )

	return outstand[0].outstanding_amount

def get_dist_accounts(filters):
	company = filters.get("company")
	year_date = getdate(filters.get("till_date")).year

	dist_accounts = frappe.db.sql(
        """
		SELECT account FROM `tabAccount Budget` 
		where company = %(company)s
		and fiscal_year = %(fiscal_year)s
		""",{'company': filters.get("company"), 'fiscal_year': year_date}, as_dict=1,
    )

	return dist_accounts

def get_account_opening_balance(filters, account):
	opening_date = filters.get("till_date")

	account_balance = frappe.db.sql(
        """
		SELECT ifnull((sum(debit) - sum(credit)), 0)balance FROM `tabGL Entry` 
		where account = %(account)s
		and is_cancelled = 0 and posting_date <= %(posting_date)s
		""",{'account': account, 'posting_date': opening_date}, as_dict=1,
    )

	return account_balance[0].balance

def get_current_month_from_balance_account(account, filters):

	opening_date = filters.get("till_date")
	
	first_day = add_days(filters.get("till_date"), 1)

	last_day = get_last_day(opening_date)

	account_balance = frappe.db.sql(
        """
		SELECT ifnull((sum(debit) - sum(credit)), 0)balance FROM `tabGL Entry` 
		where account = %(account)s
		and is_cancelled = 0 and posting_date between %(first_day)s and %(last_day)s
		""",{'account': account, 'first_day': first_day, 'last_day': last_day }, as_dict=1,
    )

	return account_balance[0].balance

def get_account_budget_value(account, filters, index):
	first_day, last_day = get_month_first_last_days(filters.get("till_date"), index)

	month_name = getdate(first_day).strftime('%B')
	year = getdate(first_day).year

	allocate_amount = frappe.db.sql(
        """
		SELECT ifnull(custom_amount_allocation, 0)custom_amount_allocation
		FROM `tabAccount Budget` a, `tabMonthly Distribution Percentage` b
		where a.name = b.parent and parenttype = 'Account Budget'
		and fiscal_year = %(year)s and month = %(month_name)s and account = %(account)s
		""",{'account': account, 'month_name': month_name, 'year': year }, as_dict=1,
    )

	return allocate_amount[0].custom_amount_allocation

def get_all_account_budget_value(filters, index):
	first_day, last_day = get_month_first_last_days(filters.get("till_date"), index)

	month_name = getdate(first_day).strftime('%B')
	year = getdate(first_day).year

	allocate_amount = frappe.db.sql(
        """
		SELECT ifnull(sum(custom_amount_allocation), 0)custom_amount_allocation
		FROM `tabAccount Budget` a, `tabMonthly Distribution Percentage` b
		where a.name = b.parent and parenttype = 'Account Budget'
		and fiscal_year = %(year)s and month = %(month_name)s
		""",{'month_name': month_name, 'year': year }, as_dict=1,
    )

	return allocate_amount[0].custom_amount_allocation