app_name = "hris"
app_title = "Hris"
app_publisher = "RAFI"
app_description = "HRIS"
app_email = "rafisoft23@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/hris/css/hris.css"
# app_include_js = "/assets/hris/js/hris.js"

# include js, css files in header of web template
# web_include_css = "/assets/hris/css/hris.css"
# web_include_js = "/assets/hris/js/hris.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "hris/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "hris.utils.jinja_methods",
# 	"filters": "hris.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "hris.install.before_install"
# after_install = "hris.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "hris.uninstall.before_uninstall"
# after_uninstall = "hris.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "hris.utils.before_app_install"
# after_app_install = "hris.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "hris.utils.before_app_uninstall"
# after_app_uninstall = "hris.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "hris.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Employee":{
        "before_save": [
            "hris.hris.events.set_employee_number",
        ],
    },
    "Contract":{
        "autoname": [
            "hris.hris.events.set_contract_name",
        ],
    },
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	# "all": [
	# 	"hris.tasks.all"
	# ],
	# "daily": [
	# 	"hris.tasks.daily"
	# ],
	# "hourly": [
	# 	"hris.tasks.hourly"
	# ],
	# "weekly": [
	# 	"hris.tasks.weekly"
	# ],
	# "monthly": [
	# 	"hris.tasks.monthly"
	# ],
    "cron": {
		"30 0 * * *": [
			"hris.hris.tasks.set_employee_age",
		],
	},
}

# Testing
# -------

# before_tests = "hris.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "hris.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "hris.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["hris.utils.before_request"]
# after_request = ["hris.utils.after_request"]

# Job Events
# ----------
# before_job = ["hris.utils.before_job"]
# after_job = ["hris.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"hris.auth.validate"
# ]

fixtures = [
    {"dt": "Custom Field", "filters": [
        [
            "name", "in", 
            [
                "Employee-custom_other_components",
				"Employee-custom_salary_tax_and_other_component",
				"Employee-custom_salary_history_data",
				"Employee-custom_salary_history_details",
				"Employee-custom_total_payment",
				"Employee-custom_additional_payment",
				"Employee-custom_payroll_company",
				"Employee-custom_hourly_salary_rate",
				"Employee-custom_bonus_gross",
				"Employee-custom_swift_code_of_intermediary_bank",
				"Employee-custom_swift_code_of_beneficiary_bank",
				"Employee-custom_intermediary_bank_name",
				"Employee-custom_receiver_name",
				"Employee-custom_date_of_termination",
				"Employee-custom_length_of_service",
				"Employee-custom_contract_date_to",
				"Employee-custom_contract_date_from",
				"Employee-custom_column_break_0alwu",
				"Employee-custom_contract_number",
				"Employee-custom_contract_name",
				"Employee-custom_column_break_khc3p",
				"Employee-custom_contract_type",
				"Employee-custom_contract_details",
				"Employee-custom_technical_level",
				"Employee External Work History-custom_comment",
				"Employee External Work History-custom_grade",
				"Employee External Work History-custom_date_of_title_assignment",
				"Employee-custom_current_cluster",
				"Employee-custom_grade_start_date",
				"Employee-custom_language_level",
				"Employee-custom_language",
				"Employee-custom_relationship",
				"Employee-custom_column_break_knbxb",
				"Employee-custom_dependent_date_of_birth",
				"Employee-custom_dependents_name",
				"Employee-custom_dependents",
				"Employee-custom_technical_media_link_",
				"Employee-custom_other_social_media",
				"Employee-custom_personal_phone_number",
				"Employee-custom_national_id_card",
				"Employee-custom_social_or_pension_number",
				"Employee-custom_tax_number",
				"Employee-custom_employee_age",
				"Employee-custom_employee_number",
                "Employee-custom_emergency_contact_surname",
                "Employee-custom_nationality_country",
                "Employee-custom_additional_payment_currency",
				"Employee-custom_bonus_gross_currency",
				"Employee-custom_emergency_contact_names",
				"Employee-custom_contact_details",
				"Employee-custom_emergency_contact_surname",
				"Employee-custom_hourly_salary_currency",
				"Employee-custom_national_id_card_date_of_issue",
				"Employee-custom_national_id_card_date_of_expiry",
				"Employee-custom_passport_copy_2",
				"Employee-custom_column_break_phksl",
				"Employee-custom_column_break_vuspi",
				"Employee-custom_passport_number_2",
				"Employee-custom_passport_1_date_of_issue",
				"Employee-custom_passport_2_date_of_expiry",
				"Employee-custom_passport_2_place_of_issue",
				"Employee-custom_personal_phone_number_2",
				"Employee-custom_time_zone",
				"Employee-custom_column_break_czeci",
				"Employee-custom_language_2",
				"Employee-custom_language_2_level",
                "cluster-custom_cluster_type",
                "Monthly Distribution Percentage-custom_amount_allocation",
                "Contract-custom_agreement_no",
                "Employee-custom_cluster_assignment_type"
            ]
        ]
    ]},
    {
        "dt": "Property Setter",
        "filters": [
            [
                "doc_type", 
                "in", 
                [
                    "Employee",
                ],
            ],
        ],
    },
]
