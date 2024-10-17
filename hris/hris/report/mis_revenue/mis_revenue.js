// Copyright (c) 2024, RAFI and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["MIS Revenue"] = {
	"filters": [
		{
			"fieldname":"fiscal_year",
			"label": __("Fiscal Year"),
			"fieldtype": "Link",
			"options": "Fiscal Year",
			"reqd": 1,
			"width": "60px",
			"default": "2024"
		},
		{
			"fieldname": "aed_exchange_rate",
			"label": __("AED Exchange Rate"),
			"fieldtype": "Float",
			"reqd": 1,
			"default": 0.27
		},
		{
			"fieldname": "rub_exchange_rate",
			"label": __("RUB Exchange Rate"),
			"fieldtype": "Float",
			"reqd": 1,
			"default": 0.012
		},
		{
			"fieldname": "eur_exchange_rate",
			"label": __("EUR Exchange Rate"),
			"fieldtype": "Float",
			"reqd": 1,
			"default": 1.07
		},
	]
};
