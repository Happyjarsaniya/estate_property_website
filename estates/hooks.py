
from __future__ import unicode_literals
from . import __version__ as app_version
from estates.route import routes
from .jinja import jenvs

app_name = "estates"
app_title = "estates"
app_publisher = "happy"
app_description = "estates management details"
app_email = "happy@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
add_to_apps_screen = [
	{
		"name": "estates",
		"logo": "/assets/estate_App/homeland/images/logo.jpg",
		"title": "estates",
		"route": "property/index",
		# "has_permission": "estates.api.permission.has_app_permission"
	}
]

# Includes in <head>
# ------------------



# include js, css files in header of desk.html
# app_include_css = "/assets/estates/css/estates.css"
app_include_js = [
    "/assets/frappe/js/frappe.min.js",
    # "/assets/estates/js/contact_form.js"
]

# include js, css files in header of web template
# web_include_css = "/assets/estates/css/estates.css"
# web_include_js = "/assets/estates/js/estates.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "estates/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Payment Entry" : "public/js/payment_entry.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "estates/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }
website_route_rules = routes
    # {'from_route':'/property/detail/<docname>','to_route':'/property/detail/'}




jinja = {
    "methods": ["estates.utils.exp"]
}




# API function allow karna


# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "estates.utils.jinja_methods",
# 	"filters": "estates.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "estates.install.before_install"
# after_install = "estates.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "estates.uninstall.before_uninstall"
# after_uninstall = "estates.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "estates.utils.before_app_install"
# after_app_install = "estates.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "estates.utils.before_app_uninstall"
# after_app_uninstall = "estates.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "estates.notifications.get_notification_config"

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

override_doctype_class = {
	# "ToDo": "custom_app.overrides.CustomToDo"
    # "Payment Entry": "estates.overrides.payment_entry.CustomPaymentEntry"


}




# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	},
# estates/hooks.py
    "Payment Entry": {
      "on_submit": "estates.overrides.payment_entry.on_submit",
    #   "validate":"estates.overrides.payment_entry.validate_paid_stage"
    
    }
}


api_routes = [
   
	{"method":"POST","path": "/api/method/estates.API.agent_api.create_agent" },
]

# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"all": [
# 		"estates.tasks.all"
# 	],

    "daily": [
    #     "estates.custom_methods.send_payment_reminders",
    #     "estates.doctype.payment_entry_doctype.payment_entry_doctype.send_payment_reminder",
	#     "estates.API.rent_invoice.send_rent_reminders",
          "estates.estates.doctype.unit_allocation.unit_allocation.send_overdue_rent_notifications"
    ]
     


# 	"hourly": [
# 		"estates.tasks.hourly"
# 	],
# 	"weekly": [
# 		"estates.tasks.weekly"
# 	],
# 	"monthly": [
# 		"estates.tasks.monthly"
# 	],
}

# Testing
# -------

# before_tests = "estates.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "estates.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "estates.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["estates.utils.before_request"]
# after_request = ["estates.utils.after_request"]

# Job Events
# ----------
# before_job = ["estates.utils.before_job"]
# after_job = ["estates.utils.after_job"]

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
# 	"estates.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# website_redirects = [
#     {"source":"/property/login","target":"/login"},
#     {"source":"/property/register","target":"/registration-"}
# ]


