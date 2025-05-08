import frappe
from frappe.model.document import Document
from datetime import datetime
from dateutil.relativedelta import relativedelta

def on_submit(doc, method=None):
    # Rent Schedule as status chage when payment entry entry this date status chage unpaid to Paid
    if doc.custom_unit_allocation and doc.custom_month:
        unit_doc = frappe.get_doc("Unit Allocation", doc.custom_unit_allocation)
        for row in unit_doc.rent_schedule:
            if row.month == doc.custom_month and row.status != "Paid":
                frappe.db.set_value("Rent Schedule", row.name, "status", "Paid")
        frappe.msgprint(f"Rent Schedule: '{doc.custom_month}' marked as Paid.")


    # Payment Schedule Details as status chage when payment entry entry this date status chage unpaid to Paid
    if doc.custom_unit_allocation and doc.custom_paid_stage:
        unit_doc = frappe.get_doc("Unit Allocation", doc.custom_unit_allocation)
        for row in unit_doc.payment_schedule_details:
            if row.stage_details == doc.custom_paid_stage and row.status != "Paid":
                frappe.db.set_value("Payment Schedule Details", row.name, "status", "Paid")
        frappe.msgprint(f"Stage '{doc.custom_paid_stage}' marked as Paid in Unit Allocation.")
         
    # Lease Schedule as status chage when payment entry entry this date status chage unpaid to Paid
    if doc.custom_unit_allocation and doc.custom_lease_month:
        lease_date = datetime.strptime(doc.custom_lease_month, "%d-%m-%Y").date()
        unit_doc = frappe.get_doc("Unit Allocation", doc.custom_unit_allocation)
        updated = False

        for row in unit_doc.lease_schedule:
            # Match with Payment Date in child table
            if row.payment_date and row.payment_date == lease_date and row.status != "Paid":
                frappe.db.set_value("Lease Schedule", row.name, "status", "Paid")
                updated = True

        if updated:
            frappe.msgprint(f"Lease month {doc.custom_lease_month} marked as Paid.")
        else:
            frappe.msgprint("No matching unpaid lease found.")

        
        
        
    unit_allocation = frappe.get_doc("Unit Allocation", doc.custom_unit_allocation)
    # Fetch child table records
    payment_schedules = frappe.get_all(
        "Payment Schedule Details",
        filters={"parent": unit_allocation.name},
        fields=[
            "stage_details",
            "payment",
            "amount",
            "gst",
            "gst_amount",
            "total_amount",
            "status"
        ]
    )
    total_paid_data = frappe.db.get_all(
    "Payment Entry",
    filters={
        "custom_unit_allocation": doc.custom_unit_allocation,
        "docstatus": 1
    },
    fields=["sum(paid_amount) as total_paid"]
)

# Extract total_paid correctly
    total_paid = total_paid_data[0]["total_paid"]   
    total_amount = unit_allocation.total_amount

    if total_paid >= total_amount:
        new_status = "Paid"
    elif total_paid > 0:
        new_status = "Partially Paid"
    else:
        new_status = "Unpaid"
    frappe.db.set_value("Unit Allocation", doc.custom_unit_allocation, "payment_status", new_status)
    frappe.msgprint(f"Payment Status Updated: {new_status}")

    return payment_schedules


# dropdown only show unpaid status in when allocation type is sale show stages
@frappe.whitelist()
def get_stage_options(unit_allocation_name):
    if not unit_allocation_name:
        return []

    unpaid_stages = frappe.get_all(
        "Payment Schedule Details",
        filters={
            "parent": unit_allocation_name,
            "parenttype": "Unit Allocation",
            "status": "Unpaid"
        },
        fields=["stage_details", "total_amount"]
    )

    return unpaid_stages


# dropdown only show unpaid status in when allocation type is rent  show month
@frappe.whitelist()
def get_rent_months(unit_allocation):
    if not unit_allocation:
        return []

    unpaid_months = frappe.get_all(
        "Rent Schedule",
        filters={
            "parent": unit_allocation,
            "parenttype": "Unit Allocation",
            "status": "Unpaid"
        },
        fields=["month"]
    )

    return [row.month for row in unpaid_months]


# dropdown only show unpaid status in when allocation type is lease show payment date 
@frappe.whitelist()
def get_lease_months(unit_allocation):
    if not unit_allocation:
        return []

    doc = frappe.get_doc("Unit Allocation", unit_allocation)
    unpaid_months = []

    for row in doc.lease_schedule:
        if row.status != "Paid" and row.payment_date:
            unpaid_months.append({
                "value": row.payment_date.strftime("%d-%m-%Y"),
                "label": row.payment_date.strftime("%d-%m-%Y")
            })

    return unpaid_months