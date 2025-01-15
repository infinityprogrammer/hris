# Copyright (c) 2024, RAFI and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt, cint
from frappe.model.document import Document

class EmployeeInvoice(Document):
	
	def before_validate(self):
		self.total_invoice_amount = flt(self.salary_amount)+flt(self.travel_expense)+flt(self.bonus)+flt(self.commission)