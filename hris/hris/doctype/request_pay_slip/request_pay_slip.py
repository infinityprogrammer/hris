# Copyright (c) 2024, RAFI and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate
from frappe.model.document import Document

class RequestPaySlip(Document):

	def before_validate(self):
		self.designation = frappe.db.get_value('Employee', self.employee, 'designation')
		self.pay_period = getdate(self.date).strftime("%B - %Y")
