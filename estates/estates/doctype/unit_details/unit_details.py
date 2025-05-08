# Copyright (c) 2025, happy and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class UnitDetails(Document):
    def validate(self):
        # Check for duplicate unit number in the same property and tower
        count = frappe.db.count('Unit Details', {
            'unit_number': self.unit_number,
            'property': self.property,
            'tower': self.tower,
            'name': ['!=', self.name]
        })

        if count > 0:
            frappe.throw(f'Unit Number "{self.unit_number}" already exists in Property "{self.property}" and Tower "{self.tower}".')
            