# Copyright (c) 2024, RAFI and contributors
# For license information, please see license.txt

import frappe

from frappe.model.document import Document

class ClusterBudget(Document):
	@frappe.whitelist()
	def get_months(self):
		month_list = [
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
			"December",
		]
		idx = 1
		for m in month_list:
			mnth = self.append("monthly_distribution")
			mnth.month = m
			mnth.percentage_allocation = 100.0 / 12
			mnth.idx = idx
			idx += 1
