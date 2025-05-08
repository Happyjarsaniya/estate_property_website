import frappe
from frappe import _

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw(_("You must be logged in to add a property."), frappe.PermissionError)

    context.user = frappe.session.user

    page = int(frappe.form_dict.get("page", 1))
    status = frappe.form_dict.get("status")  # Rent  Sale  Lease
    city = frappe.form_dict.get("city")
    property_type = frappe.form_dict.get("type")
    page_size = 3
    offset = (page - 1) * page_size

    # all Property names that have Units with matching allocation_type
    unit_filters = {}
    if status and status != "All":
        unit_filters["allocation_type"] = status

    allocated_properties = frappe.get_all(
        "Unit Allocation",
        filters=unit_filters,
        fields=["property"],
        group_by="property"
    )
    allocated_property_names = [d.property for d in allocated_properties]

    # property filters
    property_filters = {}
    if city:
        property_filters["city"] = city
    if property_type:
        property_filters["property_type"] = property_type
    if status and status != "All":
        property_filters["name"] = ["in", allocated_property_names]

    #  Fetch paginated properties
    properties = frappe.get_list(
    "Property",
    filters=property_filters,
    fields=[
        "name", "property_name", "property_type", "property_price",
        "address", "average_carpet_area", "image", "property_ownership"
    ],
    # limit=page_size,
    # start=offset  # Use `start` instead of `offset` for pagination in older versions
)

    total_count = frappe.db.count("Property", filters=property_filters)

    #  data for filters
    cities = frappe.get_all("City", fields=["name"])
    property_types = frappe.get_all("Property Type", fields=["name"])
    agents = frappe.get_all("Agent", fields=["name", "agent_name", "image", "phone", "email"])

    # Set context for Jinja template
    context.properties = properties
    context.cities = cities
    context.property_types = property_types
    context.agents = agents
    context.selected_status = status or "All"
    context.prev = page - 1 if page > 1 else None
    context.next = page + 1 if offset + page_size < total_count else None

    return context
