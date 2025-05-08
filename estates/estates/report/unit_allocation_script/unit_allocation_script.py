# Copyright (c) 2025, happy and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Property", "fieldname": "property", "fieldtype": "Link", "options": "Property", "width": 150},
        {"label": "Owner", "fieldname": "owner1", "fieldtype": "Link", "options": "Customer", "width": 150},
        {"label": "Tower", "fieldname": "tower", "fieldtype": "Link", "options": "Tower Sector Detail", "width": 150},
        {"label": "Unit Number", "fieldname": "unit_number", "fieldtype": "Link", "options": "Unit Details", "width": 120},
        {"label": "Allocation Type", "fieldname": "allocation_type", "fieldtype": "Select", "width": 120},
        {"label": "Party", "fieldname": "party", "fieldtype": "Link", "options": "Customer", "width": 150},
        {"label": "Reference Date", "fieldname": "reference_date", "fieldtype": "Date", "width": 110},
        {"label": "Payment Status", "fieldname": "payment_status", "fieldtype": "Select", "width": 100},
        {"label": "Total Amount", "fieldname": "total_amount", "fieldtype": "Currency", "width": 120},
    ]

def get_data(filters):
    conditions = ""
    if filters and filters.get("property"):
        conditions += " AND property = %(property)s"
    if filters and filters.get("allocation_type"):
        conditions += " AND allocation_type = %(allocation_type)s"

    return frappe.db.sql(f"""
        SELECT
            property,
            owner1,
            tower,
            unit_number,
            allocation_type,
            party,
            reference_date,
            payment_status,
            total_amount
        FROM `tabUnit Allocation`
        WHERE docstatus < 2 {conditions}
    """, filters, as_dict=True)
