// Copyright (c) 2025, happy and contributors
// For license information, please see license.txt

frappe.query_reports["Unit Allocation Script"] = {
	"filters": [
		{
            "fieldname": "property",
            "label": "Property",
            "fieldtype": "Link",
            "options": "Property"
        },
        {
            "fieldname": "allocation_type",
            "label": "Allocation Type",
            "fieldtype": "Select",
            "options": ["", "Sale", "Rent", "Lease"]
        }
	]
};


