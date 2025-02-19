// Copyright (c) 2025, RAFI and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Accounts Receivables USD With Week"] = {
	"filters": [
		{
			"fieldname": "fiscal_year",
			"label": __("Fiscal Year"),
			"fieldtype": "Link",
			"options": "Fiscal Year",
			"default": 2024,
		}
	]
};
