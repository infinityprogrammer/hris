// Copyright (c) 2024, RAFI and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Client Account Details"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname": "customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
		},
	]
};
