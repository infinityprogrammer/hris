# Copyright (c) 2024, RAFI and contributors
# For license information, please see license.txt

import frappe
from frappe import _, _dict
from frappe.utils import cstr, getdate, cint, flt


def execute(filters=None):
	columns, data = [], []
	data = get_data(filters)
	columns = get_columns(filters)
	return columns, data

def get_data(filters):
	data = []

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

	revenue_cluster = frappe.db.get_all("cluster", filters={'custom_cluster_type': 'Revenue'}, fields=["name"])

	support_cluster = frappe.db.get_all("cluster", filters={'custom_cluster_type': 'Support'}, fields=["name"])

	dev_cluster = frappe.db.get_all("cluster", filters={'custom_cluster_type': 'Development'}, fields=["name"])

	attrs = ["Revenue", "Emp Cost", "Others"]
	
	fiscal_year = filters.get("fiscal_year")

	for row in revenue_cluster:
		net = {}
		for attr in attrs:
			cluster_dict = {}
			for month in all_months:
				
				budget_amt = get_budget_amount(month, row.name, fiscal_year, attr)
				actual_amt = get_actual_amount(month, row.name, fiscal_year, attr)

				variance = flt(actual_amt - budget_amt)

				cluster_dict[f"{month.lower()}_budget"] = budget_amt
				cluster_dict[f"{month.lower()}_actual"] = actual_amt
				cluster_dict[f"{month.lower()}_variance"] = variance

				if attr == "Revenue":
					net[f"{month.lower()}_budget"] = budget_amt
					net[f"{month.lower()}_actual"] = actual_amt
					net[f"{month.lower()}_variance"] = variance
				
				if attr == "Emp Cost":
					net[f"{month.lower()}_budget"] -= budget_amt
					net[f"{month.lower()}_actual"] -= actual_amt
					net[f"{month.lower()}_variance"] -= variance
				
				if attr == "Others":
					net[f"{month.lower()}_budget"] -= budget_amt
					net[f"{month.lower()}_actual"] -= actual_amt
					net[f"{month.lower()}_variance"] -= variance
			
			cluster_dict['cluster'] = row.name
			cluster_dict['rc_type'] = attr
			data.append(cluster_dict)

		
		net['cluster'] = row.name
		net['rc_type'] = "Net"
		data.append(net)
		data.append({})
	
	net_cluster_dict = {}

	for month in all_months:
		net_cluster_dict[f"{month.lower()}_budget"] = 0
		net_cluster_dict[f"{month.lower()}_actual"] = 0
		net_cluster_dict[f"{month.lower()}_variance"] = 0

	for attr in attrs:
		
		cluster_dict = {}
		
		for month in all_months:
			margin_budget = get_margin_budget_amount(month, fiscal_year, attr)
			margin_actual = get_margin_actual_amount(month, fiscal_year, attr)
			margin_variance = margin_actual - margin_budget

			cluster_dict[f"{month.lower()}_budget"] = margin_budget
			cluster_dict[f"{month.lower()}_actual"] = margin_actual
			cluster_dict[f"{month.lower()}_variance"] = margin_variance
			
			if attr == "Revenue":
				
				net_cluster_dict[f"{month.lower()}_budget"] += margin_budget
				net_cluster_dict[f"{month.lower()}_actual"] += margin_actual
				net_cluster_dict[f"{month.lower()}_variance"] += margin_variance

			if attr == "Emp Cost":
				net_cluster_dict[f"{month.lower()}_budget"] -= margin_budget
				net_cluster_dict[f"{month.lower()}_actual"] -= margin_actual
				net_cluster_dict[f"{month.lower()}_variance"] -= margin_variance
			
			if attr == "Others":
				net_cluster_dict[f"{month.lower()}_budget"] -= margin_budget
				net_cluster_dict[f"{month.lower()}_actual"] -= margin_actual
				net_cluster_dict[f"{month.lower()}_variance"] -= margin_variance

		cluster_dict['cluster'] = "Subtotal"
		cluster_dict['rc_type'] = attr
		data.append(cluster_dict)

	data.append({})

	net_cluster_dict['cluster'] = "Net Revenue Margin"
	net_cluster_dict['rc_type'] = ""
	data.append(net_cluster_dict)

	data.append({})

	attrs_cost = ["Emp Cost", "Others"]

	support_cluster_dict = {}
	support_cluster_dict_oth = {}
	support_cluster_dict_sub_total = {}
	m_sub_total = {}
	fin_margin = {}
	
	for month in all_months:
		support_cluster_dict[f"{month.lower()}_budget"] = 0
		support_cluster_dict[f"{month.lower()}_actual"] = 0
		support_cluster_dict[f"{month.lower()}_variance"] = 0

		support_cluster_dict_oth[f"{month.lower()}_budget"] = 0
		support_cluster_dict_oth[f"{month.lower()}_actual"] = 0
		support_cluster_dict_oth[f"{month.lower()}_variance"] = 0

		support_cluster_dict_sub_total[f"{month.lower()}_budget"] = 0
		support_cluster_dict_sub_total[f"{month.lower()}_actual"] = 0
		support_cluster_dict_sub_total[f"{month.lower()}_variance"] = 0

		m_sub_total[f"{month.lower()}_budget"] = 0
		m_sub_total[f"{month.lower()}_actual"] = 0
		m_sub_total[f"{month.lower()}_variance"] = 0

		fin_margin[f"{month.lower()}_budget"] = 0
		fin_margin[f"{month.lower()}_actual"] = 0
		fin_margin[f"{month.lower()}_variance"] = 0

	for c_cluster in support_cluster:
		for attr in attrs_cost:
			cluster_dict = {}
			for month in all_months:
				
				budget_amt = get_budget_amount(month, c_cluster.name, fiscal_year, attr)
				actual_amt = get_actual_amount(month, c_cluster.name, fiscal_year, attr)
				variance = flt(actual_amt - budget_amt)

				cluster_dict[f"{month.lower()}_budget"] = budget_amt
				cluster_dict[f"{month.lower()}_actual"] = actual_amt
				cluster_dict[f"{month.lower()}_variance"] = variance

				if attr == "Emp Cost":
					support_cluster_dict[f"{month.lower()}_budget"] += budget_amt
					support_cluster_dict[f"{month.lower()}_actual"] += actual_amt
					support_cluster_dict[f"{month.lower()}_variance"] += variance
				
				if attr == "Others":
					support_cluster_dict_oth[f"{month.lower()}_budget"] += budget_amt
					support_cluster_dict_oth[f"{month.lower()}_actual"] += actual_amt
					support_cluster_dict_oth[f"{month.lower()}_variance"] += variance
				
				support_cluster_dict_sub_total[f"{month.lower()}_budget"] += budget_amt
				support_cluster_dict_sub_total[f"{month.lower()}_actual"] += actual_amt
				support_cluster_dict_sub_total[f"{month.lower()}_variance"] += variance

			cluster_dict['cluster'] = c_cluster.name
			cluster_dict['rc_type'] = attr
			data.append(cluster_dict)
	

	data.append({})

	attrs_subtotal = ["Emp Cost", "Others", "Sub Total"]

	for attr in attrs_subtotal:
		
		cluster_dict = {}
		
		if attr == "Emp Cost":
			support_cluster_dict['cluster'] = "Subtotal"
			support_cluster_dict['rc_type'] = attr
			data.append(support_cluster_dict)

		if attr == "Others":
			support_cluster_dict_oth['cluster'] = "Subtotal"
			support_cluster_dict_oth['rc_type'] = attr
			data.append(support_cluster_dict_oth)
		
		if attr == "Sub Total":
			support_cluster_dict_sub_total['cluster'] = "Subtotal"
			support_cluster_dict_sub_total['rc_type'] = attr
			data.append(support_cluster_dict_sub_total)
	
	data.append({})

	attrs_dev = ["Dev Cost", "Others"]

	for d_cluster in dev_cluster:
		for attr in attrs_dev:
			cluster_dict = {}
			for month in all_months:

				budget_amt = get_budget_amount(month, d_cluster.name, fiscal_year, attr)
				actual_amt = get_actual_amount(month, d_cluster.name, fiscal_year, attr)
				variance = flt(actual_amt - budget_amt)

				cluster_dict[f"{month.lower()}_budget"] = budget_amt
				cluster_dict[f"{month.lower()}_actual"] = actual_amt
				cluster_dict[f"{month.lower()}_variance"] = variance

				m_sub_total[f"{month.lower()}_budget"] += budget_amt
				m_sub_total[f"{month.lower()}_actual"] += actual_amt
				m_sub_total[f"{month.lower()}_variance"] += variance
	
			cluster_dict['cluster'] = d_cluster.name
			cluster_dict['rc_type'] = attr
			data.append(cluster_dict)


	data.append({})
	
	m_sub_total['cluster'] = ""
	m_sub_total['rc_type'] = "Subtotal"
	data.append(m_sub_total)

	for month in all_months:
		
		fin_margin[f"{month.lower()}_budget"] =  net_cluster_dict[f"{month.lower()}_budget"] - m_sub_total[f"{month.lower()}_budget"] - support_cluster_dict_sub_total[f"{month.lower()}_budget"]
		fin_margin[f"{month.lower()}_actual"] = net_cluster_dict[f"{month.lower()}_actual"] - m_sub_total[f"{month.lower()}_actual"] - support_cluster_dict_sub_total[f"{month.lower()}_variance"]
		fin_margin[f"{month.lower()}_variance"] = net_cluster_dict[f"{month.lower()}_variance"] - m_sub_total[f"{month.lower()}_variance"] - support_cluster_dict_sub_total[f"{month.lower()}_variance"]



	fin_margin['cluster'] = "Margin"
	fin_margin['rc_type'] = ""
	data.append(fin_margin)

	return data

def get_columns(filters):

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

	month_abbreviations = {
		"January": "Jan",
		"February": "Feb",
		"March": "Mar",
		"April": "Apr",
		"May": "May",
		"June": "Jun",
		"July": "Jul",
		"August": "Aug",
		"September": "Sep",
		"October": "Oct",
		"November": "Nov",
		"December": "Dec"
	}
	
	columns =  [
		{
			"label": _("Cluster"),
			"fieldname": "cluster",
			"fieldtype": "Link",
			"options": "cluster",
			"width": 150,
		},
		{
			"label": _("Type"),
			"fieldname": "rc_type",
			"fieldtype": "Data",
			"width": 100,
		}
	]
	
	for month in all_months_lowercase:
		capitalized_month = month.capitalize()

		columns += [
			{
				"label": _(f"{month_abbreviations.get(capitalized_month)} Budget {filters.get('fiscal_year')}"),
				"fieldname": f"{month}_budget",
				"fieldtype": "Float",
				"width": 140,
			},
			{
				"label": _(f"{month_abbreviations.get(capitalized_month)} Actual {filters.get('fiscal_year')}"),
				"fieldname": f"{month}_actual",
				"fieldtype": "Float",
				"width": 140,
			},
			{
				"label": _(f"{month_abbreviations.get(capitalized_month)} Variance {filters.get('fiscal_year')}"),
				"fieldname": f"{month}_variance",
				"fieldtype": "Float",
				"width": 140,
			}
		]
	
	return columns

def get_budget_amount(month, cluster, fiscal_year, type):

	budget_amount = frappe.db.sql("""SELECT ifnull(custom_amount_allocation, 0)amount
								FROM `tabCluster Budget` a, `tabMonthly Distribution Percentage` b
								where a.name = b.parent and b.parentfield = 'monthly_distribution'
								and b.month = %(month)s and a.type = %(type)s
							   	and a.cluster = %(cluster)s and a.fiscal_year = %(fiscal_year)s""",
								{'month': month, 'type': type, 'cluster': cluster, 'fiscal_year': fiscal_year}, as_dict=True)
	if budget_amount:
		return budget_amount[0].amount
	else:
		return 0

def get_actual_amount(month, cluster, fiscal_year, type):
	
	if type == "Revenue":
		gl_amount = frappe.db.sql("""SELECT ifnull(sum(credit-debit), 0)balance
									FROM `tabGL Entry` where account like '4%%'
									and is_cancelled = 0 and cluster = %(cluster)s 
									and year(posting_date) = %(fiscal_year)s and MONTHNAME(posting_date) = %(month)s""",
									{'month': month, 'type': type, 'cluster': cluster, 'fiscal_year': fiscal_year}, as_dict=True)
		
		if gl_amount:
			return gl_amount[0].balance
		else:
			return 0
	
	if type == "Emp Cost":
		gl_amount = frappe.db.sql("""SELECT ifnull(sum(debit-credit), 0)balance
									FROM `tabGL Entry` where account like '5001%%'
									and is_cancelled = 0 and cluster = %(cluster)s 
									and year(posting_date) = %(fiscal_year)s and MONTHNAME(posting_date) = %(month)s""",
									{'month': month, 'type': type, 'cluster': cluster, 'fiscal_year': fiscal_year}, as_dict=True)
		if gl_amount:
			return gl_amount[0].balance
		else:
			return 0

	if type == "Others":

		gl_amount = frappe.db.sql("""SELECT ifnull(sum(debit-credit), 0)balance
									FROM `tabGL Entry`gl, `tabAccount` acc where 
									gl.account = acc.name and gl.account like '5%%'
									and is_cancelled = 0 and cluster = %(cluster)s
									and year(posting_date) = %(fiscal_year)s AND MONTHNAME(posting_date) = %(month)s
									and acc.account_number not in (5001)""",
									{'month': month, 'type': type, 'cluster': cluster, 'fiscal_year': fiscal_year}, as_dict=True)
		if gl_amount:
			return gl_amount[0].balance
		else:
			return 0
	
	if type == "Dev Cost":

		gl_amount = frappe.db.sql("""SELECT ifnull(sum(debit-credit), 0)balance
									FROM `tabGL Entry`gl, `tabAccount` acc where 
									gl.account = acc.name and gl.account like '1311%%'
									and is_cancelled = 0 and cluster = %(cluster)s
									and year(posting_date) = %(fiscal_year)s AND MONTHNAME(posting_date) = %(month)s""",
									{'month': month, 'type': type, 'cluster': cluster, 'fiscal_year': fiscal_year}, as_dict=True)
		if gl_amount:
			return gl_amount[0].balance
		else:
			return 0

def get_margin_budget_amount(month, fiscal_year, type):

	budget_amount = frappe.db.sql("""SELECT ifnull(sum(custom_amount_allocation), 0)amount
								FROM `tabCluster Budget` a, `tabMonthly Distribution Percentage` b
								where a.name = b.parent and b.parentfield = 'monthly_distribution'
								and b.month = %(month)s and a.type = %(type)s
							   	and a.cluster in (SELECT name FROM `tabcluster` where custom_cluster_type = 'Revenue') 
							   	and a.fiscal_year = %(fiscal_year)s""",
								{'month': month, 'type': type, 'fiscal_year': fiscal_year}, as_dict=True)
	if budget_amount:
		return budget_amount[0].amount
	else:
		return 0

def get_margin_actual_amount(month, fiscal_year, type):

	if type == "Revenue":

		gl_amount = frappe.db.sql("""SELECT ifnull(sum(credit-debit), 0)balance
									FROM `tabGL Entry` where account like '4%%'
									and is_cancelled = 0 and cluster in (SELECT name FROM `tabcluster` where custom_cluster_type = 'Revenue') 
									and year(posting_date) = %(fiscal_year)s and MONTHNAME(posting_date) = %(month)s""",
									{'month': month, 'type': type, 'fiscal_year': fiscal_year}, as_dict=True)
		
		if gl_amount:
			return gl_amount[0].balance
		else:
			return 0
	
	if type == "Emp Cost":
		gl_amount = frappe.db.sql("""SELECT ifnull(sum(debit-credit), 0)balance
									FROM `tabGL Entry` where account like '5001%%'
									and is_cancelled = 0 and cluster in (SELECT name FROM `tabcluster` where custom_cluster_type = 'Revenue') 
									and year(posting_date) = %(fiscal_year)s and MONTHNAME(posting_date) = %(month)s""",
									{'month': month, 'type': type, 'fiscal_year': fiscal_year}, as_dict=True)
		if gl_amount:
			return gl_amount[0].balance
		else:
			return 0

	if type == "Others":

		gl_amount = frappe.db.sql("""SELECT ifnull(sum(debit-credit), 0)balance
									FROM `tabGL Entry`gl, `tabAccount` acc where 
									gl.account = acc.name and gl.account like '5%%'
									and is_cancelled = 0 and cluster in (SELECT name FROM `tabcluster` where custom_cluster_type = 'Revenue') 
									and year(posting_date) = %(fiscal_year)s AND MONTHNAME(posting_date) = %(month)s
									and acc.account_number not in (5001)""",
									{'month': month, 'type': type, 'fiscal_year': fiscal_year}, as_dict=True)
		if gl_amount:
			return gl_amount[0].balance
		else:
			return 0
	
	if type == "Dev Cost":

		gl_amount = frappe.db.sql("""SELECT ifnull(sum(debit-credit), 0)balance
									FROM `tabGL Entry`gl, `tabAccount` acc where 
									gl.account = acc.name and gl.account like '1311%%'
									and is_cancelled = 0 and cluster in (SELECT name FROM `tabcluster` where custom_cluster_type = 'Development') 
									and year(posting_date) = %(fiscal_year)s AND MONTHNAME(posting_date) = %(month)s
									and acc.account_number not in (5001)""",
									{'month': month, 'type': type, 'fiscal_year': fiscal_year}, as_dict=True)
		if gl_amount:
			return gl_amount[0].balance
		else:
			return 0