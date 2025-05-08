import frappe

from estates.utils import sendmail


# email agent for property page
@frappe.whitelist
def contact_agent(**args):
    print(args)
    print("\n\n\n",args.get('property_code'),args['property_code'])
    doc=frappe.get_doc("Property", args.get('property_code'))
    msg=f"From: {args.get('name')}<br> {args.get('email')}<br> {args.get('message')}"
    attachments =  [frappe.attach_print(doc,doc.doctype,file_name=doc.name)]
    sendmail(doc,[args.get('agent_email')],msg=msg,title="Property Enquiry", attachments=attachments)
    return "Message Sent to agent, you'll be responded to as soon as possible.<br>Thank You!!! "


# import frappe

# @frappe.whitelist(allow_guest=True)
# def create_lead(full_name, email, mobile_no, subject, message):
#     try:
#         lead = frappe.get_doc({
#             "doctype": "Lead",
#             "lead_name": full_name,
#             "email_id": email,
#             "mobile_no": mobile_no,
#             "subject": subject,
#             "message": message,
#             "status": "Open"
#         })
#         lead.insert(ignore_permissions=True)
#         frappe.db.commit()

#         return {
#             "success": True,
#             "lead_id": lead.name
#         }
#     except Exception as e:
#         return {
#             "success": False,
#             "error": str(e)
#         }
