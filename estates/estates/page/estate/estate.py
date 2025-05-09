import frappe

@frappe.whitelist()
def get_total_price():
    total = frappe.db.sql("""SELECT SUM(grand_total) as total FROM `tabProperty`""", as_dict=True)
    return total[0]["total"] if total and total[0]["total"] else 0

@frappe.whitelist()
def get_property_price_by_status():
    price=frappe.db.sql(""" SELECT status, SUM(grand_total) FROM  `tabProperty` GROUP BY status ORDER BY status ASC;""")
    
    return price