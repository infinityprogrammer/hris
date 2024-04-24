import frappe
from frappe.model.document import Document
from frappe.utils import getdate, now_datetime, nowdate, flt, cint, get_datetime_str, nowdate, get_link_to_form, today
from frappe import _


def set_employee_age():
    empl_age = frappe.db.sql("""UPDATE `tabEmployee` SET custom_employee_age = TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE())""", 
                         as_dict=True)
    
    empl_age = frappe.db.sql("""UPDATE `tabEmployee` SET custom_length_of_service = TIMESTAMPDIFF(YEAR, date_of_joining, CURDATE())""", 
                         as_dict=True)