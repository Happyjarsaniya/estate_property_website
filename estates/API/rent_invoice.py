# import frappe
# from frappe.utils import nowdate, add_days

# def send_rent_reminders():
#     due_invoices = frappe.get_all("Sales Invoice", 
#                                   filters={"due_date": ["<=", add_days(nowdate(), 2)], "outstanding_amount": [">", 0]},
#                                   fields=["name", "customer", "grand_total", "due_date"])

#     for invoice in due_invoices:
#         tenant_email = frappe.get_value("Tenant Details", invoice.customer, "email_id")
#         if tenant_email:
#             subject = f"Rent Payment Due for Invoice {invoice.name}"
#             message = f"Dear {invoice.customer},\n\nYour rent of {invoice.grand_total} is due on {invoice.due_date}. Please make the payment to avoid penalties.\n\nThank you."

#             frappe.sendmail(recipients=tenant_email, subject=subject, message=message)
#             frappe.msgprint(f"Reminder Sent to {tenant_email}")
