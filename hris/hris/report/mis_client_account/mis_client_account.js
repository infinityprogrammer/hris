// Copyright (c) 2024, RAFI and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["MIS Client Account"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": "2024-01-01",
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
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
