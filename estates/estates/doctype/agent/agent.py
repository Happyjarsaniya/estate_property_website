import frappe
from frappe.model.document import Document
from frappe.utils.file_manager import save_file

class Agent(Document):
    pass

@frappe.whitelist(allow_guest=True)
def create_agent():
    try:
        agent_name = frappe.form_dict.get("agent_name")
        email = frappe.form_dict.get("email")
        phone = frappe.form_dict.get("phone")
        image = frappe.request.files.get("image")  # File Upload Handling

        if not agent_name or not email:
            return {"message": "Agent Name and Email are required"}

        if frappe.db.exists("Agent", {"email": email}):
            return {"message": "Agent with this email already exists"}

        # Create new Agent document
        agent = frappe.get_doc({
            "doctype": "Agent",
            "agent_name": agent_name,
            "email": email,
            "phone": phone
        })

        # Save image file if uploaded
        if image:
            file_doc = save_file(image.filename, image.read(), "Agent", agent.name, is_private=0)
            agent.image = file_doc.file_url  # Save file URL to Agent Doctype

        agent.insert(ignore_permissions=True)
        frappe.db.commit()

        return {"message": "success", "agent_name": agent.name}

    except Exception as e:
        frappe.log_error(f"Agent Creation Error: {str(e)}", "Agent Creation")
        return {"message": str(e)}
