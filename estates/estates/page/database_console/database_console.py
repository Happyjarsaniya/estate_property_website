import frappe

@frappe.whitelist()
def query_databasse(query):
    data={'reply':0}
    if frappe.session.user != "Administrator":
        data['content']='Unauthorised User'
        return data
    try:
        content = frappe.db.sql(f"""{query}""",as_dict=True)
        data['reply']=1
        data['content']=content
    except Exception as e:
        data['reply']=2
        data['content']=e
        
    return data    
        
   