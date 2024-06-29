# Copyright (c) 2024, RAFI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime
import calendar
from datetime import date
from frappe.utils import (
	add_days,
	add_months,
	cint,
	date_diff,
	flt,
	get_first_day,
	get_last_day,
	get_link_to_form,
	getdate,
	rounded,
	today,
)

class ClusterDistribution(Document):
	
	def before_validate(self):

		if self.salary_amount:
			for row in self.cluster_values:
				row.distributed_amount = flt(self.salary_amount) * flt(row.percentage)/100
	
	def on_submit(self):
		je = frappe.new_doc("Journal Entry")
		je.voucher_type = 'Journal Entry'
		je.company = self.company
		je.posting_date = get_last_day_of_month(self.month, cint(self.year))
		je.user_remark = f"Salary cluster allocation - {self.employee_name}"
		je.custom_cluster_distribution = self.name

		for row in self.cluster_values:
			je.append("accounts",{
				"account" : self.debit_account,
				"party_type" : "Employee",
				"party" : self.employee,
				"debit_in_account_currency" : row.distributed_amount,
				"credit_in_account_currency" : 0,
				"cost_center" : frappe.db.get_value('Company', self.company, 'cost_center'),
				"user_remark" : f"Salary cluster allocation - {self.employee_name} - {row.percentage}%",
				"cluster": row.cluster
			})
		
		je.append("accounts",{
			"account" : self.credit_account,
			"debit_in_account_currency" : 0,
			"credit_in_account_currency" : self.salary_amount,
			"cost_center" : frappe.db.get_value('Company', self.company, 'cost_center'),
			"user_remark" : f"Salary cluster allocation - {self.employee_name}",
			"cluster": row.cluster
		})

		je.save(ignore_permissions=True)
		je.submit()


def get_last_day_of_month(month_name, year):

    month_names = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }

    month = month_names.get(month_name)
    
    if month is None:
        return "Invalid month name"
    
    last_day = calendar.monthrange(year, month)[1]
    print(last_day)
    
    return date(year, month, last_day)