# Copyright (c) 2025, happy and contributors
# For license information, please see license.txt
from  __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import date  


class Property(Document):
    def after_insert(self):
      frappe.msgprint((f"Document {self.name} inserted Successfully "))
      frappe.sendmail(
        recipients= "happyjarsaniya0@gmail.com",
        message="Create New Property Successfully",
        subject="mail",
      ),
      
    # like average carpet area = 1200 sq.ft and property area = 10000 and proejct lend area = 50000 
    def validate(self):   
      
      # Average Carpet Area
      if self.average_carpet_area is None or self.average_carpet_area <= 0:
          frappe.throw("Average Carpet Area must be greater than 0.")
      if self.property_area and float(self.average_carpet_area) > float(self.property_area):
          frappe.throw("Average Carpet Area cannot be greater than Property Area.")

      # Property Area
      if not self.property_area or float(self.property_area) <= 0:
          frappe.throw("Property Area must be greater than 0.")

      if self.project_land_area and float(self.property_area) > float(self.project_land_area):
          frappe.throw("Property Area cannot be greater than Project Land Area.")

      if self.property_area and float(self.project_land_area) < float(self.property_area):
          frappe.throw("Project Land Area cannot be smaller than Property Area.")
          
# Validate project start date and project end date 
      if self.project_start_date and self.expected_project_end_date:
          if self.project_start_date >= self.expected_project_end_date:
              frappe.throw("End Date must be after Start")
              
      today = frappe.utils.today()  
             

    # def before_save(self):
    #     total_percent = 0  

    #     for row in self.payment_schedule_details:
    #         if not row.property_price:
    #             row.property_price = self.property_price 

           
    #         row.amount = (row.property_price * row.payment) / 100

    #         row.gst_amount = (row.amount * row.gst) / 100
    #         row.total_amount = row.amount + row.gst_amount  

    #         total_percent += row.payment

    #     if total_percent > 100:
    #         frappe.throw("Total Payment Percentage cannot exceed 100%")
    
    
    