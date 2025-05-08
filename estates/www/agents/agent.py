import frappe
from estates.utils import paginate

def get_context(context):
    # Fetch all required fields in a single query
    context.agents = frappe.get_all("Agent", fields=["agent_name", "image", "email", "phone"])
    return context
