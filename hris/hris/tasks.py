import frappe
from frappe.model.document import Document
from frappe.utils import getdate, now_datetime, nowdate, flt, cint, get_datetime_str, nowdate, get_link_to_form, today
from frappe import _


def set_employee_age():
    empl_age = frappe.db.sql("""UPDATE `tabEmployee` SET custom_employee_age = TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE())""", 
                         as_dict=True)
    
    empl_age = frappe.db.sql("""UPDATE `tabEmployee` SET custom_length_of_service = TIMESTAMPDIFF(YEAR, date_of_joining, CURDATE())""", 
                         as_dict=True)

def employee_periodic_notification():
    emps = frappe.db.sql("""SELECT name, employee_name, date_of_joining,user_id, datediff(curdate(), date_of_joining)diff
                                FROM `tabEmployee` where status = 'Active' and datediff(curdate(), date_of_joining) in (30, 75, 165);""", 
                                as_dict=True)
    
    recipients = get_users_with_role("HR User")

    for emp in emps:
        recipients.append(emp.user_id)
        email_args = {
            "recipients": recipients,
            "message": f"{emp.employee_name} successfully completed {emp.diff} days",
            "subject": f"{emp.employee_name} successfully completed {emp.diff} days",
            "reference_doctype": 'Employee',
            "reference_name": emp.name
        }
        
        frappe.sendmail(**email_args)

def get_users_with_role(role):
    
    user_list = frappe.get_all("User", fields=["`tabUser`.name"],          
    filters = [
        ["Has Role", "role", "=", role],
        ["User", "name", "not in", ["Guest", "Administrator"]],
        ["User", "enabled", "=", 1]
    ],as_list=1)
    
    return [user for users in user_list for user in users]