import frappe
jenvs = {
    "methods": [
        "exp:estates.jinja.exp"
    ],
}

def exp(num):
    return float(num)**2