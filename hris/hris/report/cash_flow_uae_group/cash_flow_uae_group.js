// Copyright (c) 2024, RAFI and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Cash Flow UAE Group"] = {
	"filters": [
		{
			"fieldname":"fiscal_year",
			"label": __("Fiscal Year"),
			"fieldtype": "Link",
			"options": "Fiscal Year",
			"default": frappe.sys_defaults.fiscal_year,
		},
	]
};
