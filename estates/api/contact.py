import frappe
import json

@frappe.whitelist()
def create_lead():
    try:
        input_data = frappe.request.data
        item = json.loads(input_data)

        # Check if email already exists
        existing_lead = frappe.get_all("Lead", filters={"email_id": item.get("email_id")})
        if existing_lead:
            return {
                "status": "error",
                "message": "Email already exists. Please use a different email.",
                "field_to_clear": "email_id" ,
            }
        # Create lead
        lead = frappe.get_doc({
            "doctype": "Lead",
            "first_name": item.get("first_name"),
            "email_id": item.get("email_id"),
            "mobile_no": item.get("mobile_no"),
            "custom_price_range": item.get("custom_price_range"),
            "message": item.get("message")
        })
        lead.insert()
        frappe.db.commit()

        # Send email 
        send_email(lead)

        return {"status": "success", "message": "Lead Created Successfully!"}

    except Exception as e:
        frappe.log_error(message=frappe.get_traceback(), title="Lead Creation Error")
        return {"status": "error", "message": str(e)}


def send_email(lead):
    
    recipients = ["happyjarsaniya0@gmail.com"]

    subject = f"New Lead Created: {lead.first_name}"
    message = f"""
    <h3>New Lead Details</h3>
    <p><strong>Name:</strong> {lead.first_name}</p>
    <p><strong>Email:</strong> {lead.email_id}</p>
    <p><strong>Mobile:</strong> {lead.mobile_no}</p>
    <p><strong>Price Range:</strong> {lead.custom_price_range}</p>
    <p><strong>Message:</strong> {lead.message}</p>
    """

    frappe.sendmail(
        recipients=recipients,
        subject=subject,
        message=message,
        reference_doctype="Lead",
        reference_name=lead.name
    )
