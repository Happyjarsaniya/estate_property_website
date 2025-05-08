# import frappe

# def get_context(context):
#     context.name ='hepi'
#     return context


import math
import frappe

def get_context(context):
    context.name="happy"
    context["exp"] = math.exp  # Pass exp() function to Jinja
    print(f"\n\n\n{frappe.form_dict}\n\n\n")
    return context


