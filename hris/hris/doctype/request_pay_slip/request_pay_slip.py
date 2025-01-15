# Copyright (c) 2024, RAFI and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate
from frappe.model.document import Document

class RequestPaySlip(Document):

	def before_validate(self):
		self.designation = frappe.db.get_value('Employee', self.employee, 'designation')
		self.pay_period = getdate(self.date).strftime("%B - %Y")

		if not any(row.component == "Basic Salary" for row in self.details):
			
			self.append("details",{
				"component": "Basic Salary",
				"amount": frappe.db.get_value('Employee', self.employee, 'ctc'),
				"currency": frappe.db.get_value('Employee', self.employee, 'salary_currency')
			})
		
		if not any(row.component == "Bonus" for row in self.details):
			if frappe.db.get_value('Employee', self.employee, 'custom_bonus_gross_currency'):
				self.append("details",{
					"component": "Bonus",
					"amount": frappe.db.get_value('Employee', self.employee, 'custom_bonus_gross'),
					"currency": frappe.db.get_value('Employee', self.employee, 'custom_bonus_gross_currency')
				})
		

		total_amount = sum(row.amount for row in self.details if row.amount)
		self.total_salary = total_amount