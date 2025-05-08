# Copyright (c) 2025, happy and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TowerSectorDetail(Document):
    def validate(self):
        total_floors = int(self.total_no_of_floor)

        if total_floors <= 0:
            frappe.throw("Total No. of Floor must be greater than 0.")

        # Check Duplicate Tower Name under the Same Property
        existing_tower = frappe.db.count('Tower Sector Detail', {
            'property_name': self.property_name,
            'tower_name': self.tower_name,
            'docstatus': 1
        })
        if existing_tower > 0:
            frappe.throw(f'Tower Name "{self.tower_name}" already exists in Property "{self.property_name}"!')

        # all tower count from Property
        allowed_tower = frappe.db.get_value('Property', self.property_name, 'total_num_of_towersector')
        current_tower_count = frappe.db.count('Tower Sector Detail', {
            'property_name': self.property_name,
            'docstatus': 1
        })
        if current_tower_count >= allowed_tower:
            frappe.throw(f'"{self.property_name}" can have only {allowed_tower} Tower/Sector, not more than that!')

        # Validate Floor Details
        if not self.floor_details:
            frappe.throw("Floor Details are required.")

        total_resident = 0
        total_commercial = 0

        for row in self.floor_details:
            resident_units = int(row.total_resident_unit or 0)
            commercial_units = int(row.total_commercial_unit or 0)
            floor_no = int(row.floor_no or 0)  

            # Restriction for Ground Floor (Floor 0)
            if floor_no == 0:
                if resident_units > 0 or commercial_units > 0:
                    frappe.throw("Ground Floor (Floor 0) cannot have Residential or Commercial Units.")

            # Mixing of Residential and Commercial Units
            if self.property_type == "Commercial" and resident_units > 0:
                frappe.throw(f'Floor {floor_no}: Residential Units cannot be added in a Commercial Tower!')
            if self.property_type == "Residential" and commercial_units > 0:
                frappe.throw(f'Floor {floor_no}: Commercial Units cannot be added in a Residential Tower!')

            # Each Floor Has One Unit compulsory
            if resident_units == 0 and commercial_units == 0:
                frappe.throw(f'Floor {floor_no} must have at least one unit (Residential or Commercial).')

            total_resident += resident_units
            total_commercial += commercial_units

        # Validate Unit Limits
        max_resident = int(self.total_no_of_residential_units or 0)
        max_commercial = int(self.total_no_of_commercial_units or 0)

        if total_resident != max_resident:
            frappe.throw(f'Total Resident Units ({total_resident}) cannot exceed the allowed Residential Units ({max_resident}).')

        if total_commercial != max_commercial:
            frappe.throw(f'Total Commercial Units ({total_commercial}) cannot exceed the allowed Commercial Units ({max_commercial}).')
            
 # when project status Construction
        project_status = frappe.db.get_value("Property", self.property_name, "project_status")

        if project_status == "Under Construction" and self.total_units > 0:
            frappe.throw("Cannot assign units to a tower while the project is 'Under Construction'.")
