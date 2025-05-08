// Copyright (c) 2025, hepi and contributors
// For license information, please see license.txt

frappe.query_reports["Property"] = {
	"filters": [
		{
			"fieldname": "property",
			"label": __("Property Name"),
			"fieldtype": "Data",
			"width": 100,
			"reqd": 0,
		},
		{
			"fieldname": "from",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": 80,
			"reqd": 1,
			"default": frappe.datetime.year_start()
		},
		{
			"fieldname": "to",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": 80,
			"reqd": 1,
			"default": frappe.datetime.year_end()
		}, 
		{
			"fieldname": "agent",
			"label": __("Agent Name"),
			"fieldtype": "Link",
			"options":"Agent",
			"width": 100,
			"reqd": 0,
		},
		{
			"fieldname": "status",
			"label": __("Status"),
			"fieldtype": "Select",
			"default":"",
			"options":['','Sale','Rent','Lease'],
			"width": 100,
			"reqd": 0,
		}


	]
};
// console.log("Report data in add_card_to_dashboard:", this.report);
