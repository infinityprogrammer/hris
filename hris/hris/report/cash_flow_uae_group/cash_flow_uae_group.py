# Copyright (c) 2024, RAFI and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []

	data = get_data(filters)

	return columns, data


def get_data(filters):
	
	companies = frappe.db.get_list('Company', {'default_currency': 'AED'}, pluck='name')

	clusters_and_customers = frappe.db.sql(
        """
		SELECT distinct customer, cluster 
		FROM `tabSales Invoice` where docstatus = 1
		and company in %(companies)s
		order by 2, 1""",{'companies': companies}, as_dict=1,
    )

	for row in clusters_and_customers:
		pass

def get_columns(filters):
	pass