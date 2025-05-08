# import frappe
# import json

# @frappe.whitelist(allow_guest=True)
# def create_agent():
#     try:
       
#         data = frappe.request.data
#         input = json.loads(data)
#         print(input)  

#         # Validation: Agent Name & Email Required
#         if not input.get("agent_name") or not input.get("email"):
#             return {"status": "error", "message": "Agent name and email are required."}

#         # Check if Agent Already Exists
#         if frappe.db.exists("Agent", {"email": input["email"]}):
#             return {"status": "error", "message": f"Agent with email '{input['email']}' already exists."}

#         # Create New Agent Document
#         agent = frappe.get_doc({
#             "doctype": "Agent",
#             "agent_name": input["agent_name"],
#             "email": input["email"],
#             "phone": input.get("phone"),
#             "image": input.get("image") 
#         })

#         # Insert Agent in DB
#         agent.insert(ignore_permissions=True)
#         frappe.db.commit()

#         return {"status": "success", "message": "Agent created successfully", "agent_id": agent.name}

#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "Agent API Error")
#         return {"status": "error", "message": str(e)}
