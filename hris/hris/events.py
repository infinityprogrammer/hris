import frappe
from frappe.model.document import Document
from frappe.utils import getdate, now_datetime, nowdate, flt, cint, get_datetime_str, nowdate, get_link_to_form, today
from frappe import _


def set_employee_number(self, args):
    self.custom_employee_number = self.name

    if self.date_of_birth:
        self.custom_employee_age = getdate(today()).year - getdate(self.date_of_birth).year
    
    if self.date_of_joining:
        self.custom_length_of_service = getdate(today()).year - getdate(self.date_of_joining).year