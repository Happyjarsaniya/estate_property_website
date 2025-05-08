import frappe

def get_context(context):
    unit_number = frappe.form_dict.unit_number

    if not unit_number:
        context.error = True
        context.message = "No unit_number found in URL."
        return context

    try:
        doc = frappe.get_doc("Unit Allocation", unit_number)
    except frappe.DoesNotExistError:
        context.error = True
        context.message = f"Unit Allocation '{unit_number}' not found."
        return context

    context.unit_number = doc.unit_number 
    context.property = doc.property
    context.owner = doc.owner
    context.tower = doc.tower
    context.sold_price = doc.sold_price
    context.allocation_type = doc.allocation_type
    context.party = doc.party
    context.reference_date = doc.reference_date
    context.payment_status = doc.payment_status
    context.total_amount = doc.total_amount
    context.payment_schedule_details = [
        {
            "no": i + 1,
            "stage": row.stage_details,
            "percentage": row.payment,
            "amount": row.amount,
            "gst": row.gst,
            "gst_amount": row.gst_amount,
            "total_amount": row.total_amount,
            "status": row.status
        }
        for i, row in enumerate(doc.payment_schedule_details)
    ]
    
    return context
