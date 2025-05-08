import frappe
def sendmail(doc,recipients,msg,title,attachments=None):
    email_args={
        'recipients': recipients,
        'message':msg,
        'subject':title,
        'reference_doctype':doc.doctype,
        'reference_name':doc.name,
    }
    if attachments:email_args['attachments']=attachments
    # send mail
    frappe.enqueue(method=frappe.sendmail,queue='short',timeout=300, **email_args)


def paginate(doctype, page=1, conditions="", fields=None):
    prev, next = 0, 0
    limit = 3  # Records per page

    # Default Fields
    if fields is None:
        fields = ["name"]

    # Convert fields list to SQL string
    fields_str = ", ".join(fields)

    # SQL Query
    query = f"SELECT {fields_str} FROM `tab{doctype}` {conditions} ORDER BY creation DESC"

    # Fetch paginated records
    properties = frappe.db.sql(f"{query} LIMIT {(page-1)*limit}, {limit}", as_dict=True)
    next_set = frappe.db.sql(f"{query} LIMIT {page*limit}, {limit}", as_dict=True)

    # Set pagination
    prev, next = (page-1, page+1) if next_set else (page-1, 0)

    return {"properties": properties, "prev": prev, "next": next}

 
 
import math

def exp(value):
    return math.exp(value)
