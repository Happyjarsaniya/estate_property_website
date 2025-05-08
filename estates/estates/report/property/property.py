# # Copyright (c) 2025, hepi and contributors
# # For license information, please see license.txt

from __future__ import unicode_literals
from frappe import _
import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    # columns = get_columns()
    data = get_data(filters)

    return data  #,colums

# def get_columns():
#     return [
#         {"label": _("ID"), "fieldname": "name", "fieldtype": "Link", "options": "Property", "width": 70},
#         {"label": _("Property Name"), "fieldname": "property_name", "fieldtype": "Data", "width": 150},
#         {"label": _("Address"), "fieldname": "address", "fieldtype": "Data", "width": 150},
#         {"label": _("Type"), "fieldname": "property_type", "fieldtype": "Data", "width": 50},
#         {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 80},
#         {"label": _("Price"), "fieldname": "property_price", "fieldtype": "Currency", "width": 100},
#         {"label": _("Discount"), "fieldname": "discount", "fieldtype": "Percent", "width": 20},
#         {"label": _("Grand Total"), "fieldname": "grand_total", "fieldtype": "Currency", "width": 150},
#         {"label": _("Agent"), "fieldname": "agent", "fieldtype": "Data", "width": 100},
#         {"label": _("Agent Name"), "fieldname": "agent_name", "fieldtype": "Data", "width": 150},
#     ]

def get_data(filters):
    conditions = ""

    if filters.get("status"):
        conditions += f" AND status = '{filters.get('status')}'"

    if filters.get("agent"):
        conditions += f" AND agent = '{filters.get('agent')}'"

    query = f"""
        SELECT name, property_name, address, property_type, status, property_price, discount, grand_total, agent, agent_name
        FROM `tabProperty`
        WHERE (creation BETWEEN '{filters.get('from')}' AND '{filters.get('to')}') {conditions};
    """
    
    return frappe.db.sql(query, as_dict=True)
