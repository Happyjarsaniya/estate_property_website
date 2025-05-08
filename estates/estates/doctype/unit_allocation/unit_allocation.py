# Copyright (c) 2025, happy and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date 
from frappe.utils import nowdate, getdate, formatdate
from dateutil.relativedelta import relativedelta
from datetime import timedelta
today = frappe.utils.today()  
 

class UnitAllocation(Document):   
    def validate(self):
        # Fetch Payment Schedule Details
        if self.property:
            self.fetch_payment_schedule_details()
        self.calculate_payment_schedule_totals()
        self.validate_unit_status()
        self.calculate_total_amount()
        
        
        if self.allocation_type == "Lease" and self.lease_start_date and self.lease_end_date:
            self.generate_lease_schedule()

        
        if self.agreement_start_date and self.agreement_enddate:
          if self.agreement_start_date >= self.agreement_enddate:
              frappe.throw("End Date must be after Start")
        
        
        
        # lease table related 
        # for row in self.payment_schedule_details:
        #     # Ensure required fields are available
        #     if getattr(row, "due_date", None) and row.status == "UnPaid":
        #         if row.due_date < today() and getattr(row, "is_overdue", 0):
        #             frappe.msgprint(
        #                 f"Payment stage '{row.stage_details}' is overdue and unpaid."
        #             )
        # for row in self.payment_schedule_details:
        #     if getattr(row, "due_date", None) and row.status == "UnPaid":
        #         if row.due_date < today():
        #             row.is_overdue = 1
        #         else:
        #             row.is_overdue = 0
    
    
    # auto calculate total amount filed for allocation type lease  
    def calculate_total_amount(self):
        monthly_rent_price = self.monthly_rent_price or 0
        lease_duration = self.lease_duration or 0

        total_months = lease_duration * 12
        self.total_amount = monthly_rent_price * total_months


    # lease child table show months  
    def generate_lease_schedule(self):
        self.set("lease_schedule", []) 
        start_date = getdate(self.lease_start_date)
        end_date = getdate(self.lease_end_date)
        index = 1

        while start_date < end_date:
            self.append("lease_schedule", {
                "no": index,
                "month": start_date.strftime('%B'),
                "year": start_date.year,
                "payment_date":start_date,
                "due_date": start_date + timedelta(days=7),
                "status": "Unpaid",
                "is_overdue": 0,
            })
            index += 1
            start_date += relativedelta(months=1)             
        
    def calculate_payment_schedule_totals(self):
        sold_price = self.get("lease_price") or 0 
        for row in self.payment_schedule_details:
            if row.payment is not None:
                row.amount = (sold_price * float(row.payment)) / 100
                row.gst_amount = (row.amount * float(row.gst or 0)) / 100
                row.total_amount = row.amount + row.gst_amount


    # Check unit available before allocation
    def validate_unit_status(self):
        unit_status = frappe.db.get_value("Unit Details", self.unit_number, "status")
        if unit_status != "Available":
            frappe.throw(f"Unit {self.unit_number} is currently '{unit_status}' and cannot be allocated.")
   
    #Unit as Booked when allocation is submitted
    def on_submit(self):
        frappe.db.set_value("Unit Details", {"name":self.unit_number}, "status", "Booked")
        frappe.msgprint(f"Unit {self.unit_number} status updated to 'Booked'.")
    
    #  Unit status to Available when allocation canceled
    def on_cancel(self):
        frappe.db.set_value("Unit Details", self.unit_number, {"status": "Available"})
        frappe.msgprint(f"Unit {self.unit_number} status updated back to 'Available'.")

    # fetch payment schedule details from property doc
    def fetch_payment_schedule_details(self):
        self.payment_schedule_details = []  
        schedule_data = get_payment_schedule(self.property)

        for row in schedule_data:
            self.append("payment_schedule_details", row)

# Fetch Payment Schedule Data
@frappe.whitelist()
def get_payment_schedule(property_name):
    if not property_name:
        return []
    try:
        property_doc = frappe.get_doc("Property", property_name)
    except frappe.DoesNotExistError:
        frappe.throw(f"Property '{property_name}' does not exist.")

    return [{   
        "stage_details": row.stage_details,
        "payment": row.payment,
        "amount": row.amount,
        "gst": row.gst,
        "gst_amount": row.gst_amount,
        "total_amount": row.total_amount,
        "status":row.status
    } for row in property_doc.payment_schedule_details]
    
    
    
@frappe.whitelist()
def create_stage_payment_entry(unit_allocation_name, stage):
    unit_allocation = frappe.get_doc("Unit Allocation", unit_allocation_name)
    
    # matching stage row find
    matching_stage = None
    for row in unit_allocation.payment_schedule_details:
        if row.stage_details == stage:
            matching_stage = row
            break

    if not matching_stage:
        frappe.throw(f"Stage '{stage}' not found in Payment Schedule Details")

    payment_entry = frappe.new_doc("Payment Entry")
    payment_entry.insert()
    frappe.msgprint("Payment Entry Created")
    return payment_entry.name




def send_overdue_rent_notifications():
    today = getdate(nowdate())

    unit_allocations = frappe.get_all("Unit Allocation", fields=["name", "party", "unit_number"])
    for allocation in unit_allocations:
        doc = frappe.get_doc("Unit Allocation", allocation.name)
        for rent in doc.rent_schedule:
            payment_date = getdate(rent.payment_date)
            if payment_date < today and rent.status != "Paid":
                party_email = frappe.db.get_value("Customer", doc.party, "email_id")
                if not party_email:
                    continue  #no email found skip 

                subject = f"Overdue Rent Reminder for Unit {doc.unit_number}"
                message = f"""
                        Dear {doc.party},
                        This is a reminder that your rent payment for the month of {rent.month} {rent.year} was due on {formatdate(rent.payment_date)}.
                        As of today ({formatdate(today)}), this payment is overdue. Kindly make the payment within the next 2 days to avoid additional late fees.
                        If the payment is not received within 2 days, late charges will be applicable as per the agreement terms.
                        Thank you for your attention.
                        Regards,  
                        Estate Management Team"""

                frappe.sendmail(
                    recipients=[party_email],
                    subject=subject,
                    message=message
                )
                break  #only 1mail per allocation


