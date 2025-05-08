import frappe

def get_context(context):
    try:
        docname = frappe.form_dict.get("docname")
        
        context.property = frappe.get_doc("Property", docname)
        context.agent = None
        if getattr(context.property, "agent", None):
            context.agent = frappe.get_doc("Agent", context.property.agent)

        context.property_price = (context.property, "property_price", 0)
        context.average_carpet_area = (context.property, "average_carpet_area", "N/A")
        context.property_ownership = (context.property, "property_ownership", "N/A")
        # getattr
        # Fetch related properties
        related_properties = frappe.get_all(
        "Property",
        filters={
        "property_type": context.property.property_type,
        "name": ["!=", context.property.name]
        },
        fields=[
        "name", "property_name", "status", "address",
        "property_price", "property_ownership",
        "average_carpet_area", "image","property_type"
        ],
        order_by="creation desc",
        limit=3
        )

        context.related_properties = related_properties

        # context.units = frappe.get_all(
        #     "Unit Details",
        #     # filters={"property_type": "Residential"},
            
        #     filters={"property": context.property.name, "property_type": "Residential"},
        #     fields=["unit_number", "no_of_bedrooms", "no_of_bathrooms", "no_of_balconies","unit_size"],
        #     distinct=True
        # )
        # return context
    
        context.units = frappe.get_all(
        "Unit Details",
        filters={"property": context.property.name},
        fields=[
            "unit_number",
            "unit_type",
            "property_type",
            "no_of_bedrooms",
            "no_of_bathrooms",
            "no_of_balconies",
            "unit_size",
            "seating_capacity",
            "cabin_count",
            "meeting_rooms"
        ],
        order_by="creation asc",
        limit=1
    )


    except Exception as e:
        frappe.local.flags.redirect_location = "/404"
        raise frappe.Redirect

    return context

