// Copyright (c) 2024, RAFI and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Budget Cashflow Simple"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			// "default": frappe.defaults.get_user_default("Company"),
			"default": "Techno Limited",
			"reqd": 1,
			on_change: function() {
				var company = frappe.query_report.get_filter_value('company');
				frappe.db.get_value("Company", company, "default_currency", function(value) {
					frappe.query_report.set_filter_value('company_currency', value["default_currency"]);
				});
			}
		},
		{
			"fieldname":"till_date",
			"label": __("Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.get_today(),
		},
		// {
		// 	"fieldname":"company_currency",
		// 	"label": __("Company Currency"),
		// 	"fieldtype": "Data",
		// },
		// {
		// 	"fieldname":"exchange_rate",
		// 	"label": __("Exchange Rate"),
		// 	"fieldtype": "Float",
		// },
	]
};
