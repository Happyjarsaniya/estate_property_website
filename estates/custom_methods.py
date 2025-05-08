# import frappe
# from frappe.utils import today, add_days

# def send_payment_reminders():
#     overdue_invoices = frappe.get_all("Sales Invoice", 
#         filters={"status": "Overdue", "due_date": ["<", today()]},
#         fields=["name", "customer", "due_date", "outstanding_amount"]
#     )

#     for invoice in overdue_invoices:
#         customer_email = frappe.get_value("Customer", invoice["customer"], "email_id")
        
#         if customer_email:
#             # Send Email Notification
#             frappe.sendmail(
#                 recipients=customer_email,
#                 subject=f"Payment Overdue Reminder - Invoice {invoice['name']}",
#                 message=f"""
#                 <p>Dear {invoice['customer']},</p>
#                 <p>Your payment for invoice <b>{invoice['name']}</b> is overdue.</p>
#                 <p><b>Due Date:</b> {invoice['due_date']}</p>
#                 <p><b>Outstanding Amount:</b> ₹{invoice['outstanding_amount']}</p>
#                 <p>Please make the payment as soon as possible.</p>
#                 <p>Thank you,</p>
#                 <p>Your Company</p>
#                 """
#             )

#         # System Notification for Admin
#         frappe.publish_realtime(
#             event="msgprint",
#             message=f"Overdue payment reminder sent for Invoice {invoice['name']}",
#             user="administrator"
#         )

#     return f"Sent {len(overdue_invoices)} payment reminders."

