// Copyright (c) 2024, RAFI and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Cluster Wise Overdue Invoices"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			// "default": frappe.defaults.get_user_default("Company"),
			"default": "Techno Limited",
			"reqd": 1,
		},
		{
			"fieldname":"till_date",
			"label": __("Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.get_today(),
		},
	]
};
