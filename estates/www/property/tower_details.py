import frappe
def get_context(context):
    property_name = frappe.form_dict.get("property_name") 

    if not property_name:
        frappe.throw("Property not specified.")
    
    # Fetch towers for property
    context.towers = frappe.get_all(
        "Tower Sector Detail", 
        filters={"property_name": property_name, "docstatus": 1},
        fields=["property_name","name", "type", "property_type", "tower_name", "total_no_of_floor", 
                "total_no_of_residential_units","total_no_of_commercial_units", "total_units"]
    )
    
    # child table tower (floor details)
    for tower in context.towers:
        tower["floor_details"] = frappe.get_all(
            "Floor Details", 
            filters={"parent": tower.name}, 
            fields=["floor_no", "total_resident_unit", "total_commercial_unit"]
        )

    return context
