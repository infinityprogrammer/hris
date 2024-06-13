// Copyright (c) 2024, RAFI and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Cluster Budget Analysis"] = {
	"filters": [
		{
			"fieldname": "fiscal_year",
			"label": __("Fiscal Year"),
			"fieldtype": "Link",
			"options": "Fiscal Year",
			"reqd": 1,
			"default": 2024
		},
		{
			"fieldname": "aed_exchange_rate",
			"label": __("AED Exchange Rate"),
			"fieldtype": "Float",
			"reqd": 1,
			"default": 1
		},
		{
			"fieldname": "rub_exchange_rate",
			"label": __("RUB Exchange Rate"),
			"fieldtype": "Float",
			"reqd": 1,
			"default": 1
		},
		{
			"fieldname": "eur_exchange_rate",
			"label": __("EUR Exchange Rate"),
			"fieldtype": "Float",
			"reqd": 1,
			"default": 1
		},
	]
};
