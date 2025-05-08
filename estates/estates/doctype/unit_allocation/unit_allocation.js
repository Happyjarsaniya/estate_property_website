// Copyright (c) 2025, happy and contributors
// For license information, please see license.txt

frappe.ui.form.on('Unit Allocation', {

    duration_months(frm) {
        const duration = frm.doc.duration_months;  
        const start_date = frappe.datetime.nowdate();  

        let current_date = frappe.datetime.str_to_obj(start_date);  // convert start date to date object
        let month_names = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ];

        for (let i = 0; i < duration; i++) {
            let row = frm.add_child('rent_schedule'); 
            let month = current_date.getMonth();
            let year = current_date.getFullYear();

            row.month = month_names[month];
            row.year = year;
            row.status = 'Unpaid';
            row.payment_date = frappe.datetime.obj_to_str(current_date);

            current_date.setMonth(current_date.getMonth() + 1);
        }

        frm.refresh_field('rent_schedule'); 
    },

    allocation_type(frm) {
        // Hide or Show child table based on allocation type
        if (frm.doc.allocation_type === 'Sale') {
            frm.set_df_property('payment_schedule_details', 'hidden', 0);
        } else {
            frm.set_df_property('payment_schedule_details', 'hidden', 1);
        }
    },

    onload_post_render(frm) {
        // not show the table on load
        if (frm.doc.allocation_type === 'Sale') {
            frm.set_df_property('payment_schedule_details', 'hidden', 0);
        } else {
            frm.set_df_property('payment_schedule_details', 'hidden', 1);
        }
    },
    agreement_start_date(frm) {
        if (frm.doc.agreement_start_date) {
            let start_date = frappe.datetime.str_to_obj(frm.doc.agreement_start_date);
            let end_date = frappe.datetime.add_months(start_date, 11);
            frm.set_value('agreement_enddate', frappe.datetime.obj_to_str(end_date));
        }
    },

    //lease end date autocalculate based on duration 
    lease_start_date: function(frm) {
        frm.trigger("set_lease_end_date");
    },
    lease_duration: function(frm) {
        frm.trigger("set_lease_end_date");
    },
    set_lease_end_date: function(frm) {
        if (frm.doc.lease_start_date && frm.doc.lease_duration) {
            let start_date = frappe.datetime.str_to_obj(frm.doc.lease_start_date);
            let duration_years = parseFloat(frm.doc.lease_duration);
    
            if (!isNaN(duration_years)) {
                start_date.setFullYear(start_date.getFullYear() + duration_years);  
                frm.set_value('lease_end_date', frappe.datetime.obj_to_str(start_date));  
            }
        }
    },

    refresh: function(frm) {
        // Show "Make Payment" button when the document is submitted
        if (frm.doc.docstatus == 1) {  
            frm.page.add_action_item(__('Make Payment'), function() {
                frappe.new_doc('Payment Entry', {
                    unit_allocation: frm.doc.name,
                    party: frm.doc.customer_name,
                    paid_amount: frm.doc.total_amount || 0,
                    posting_date: frappe.datetime.nowdate(),
                    reference_date: frm.doc.reference_date,
                });
            });
        }
    },


    //  Filter Unit Number based on selected Tower
    tower: function(frm) {
        if (frm.doc.tower) {
            frm.set_query('unit_number', function() {
                return {
                    filters: [
                        ['Unit Details', 'property', '=', frm.doc.property],
                        ['Unit Details', 'tower', '=', frm.doc.tower],
                        ['Unit Details', 'status', '!=', 'Booked']
                    ]
                };
            });

            frm.set_value('unit_number', ''); // Reset unit number when tower changes
        }
    },

    //  Filter Tower based on selected Property
    property: function(frm) {
        if (frm.doc.property) {
            frappe.call({
                method: "estates.estates.doctype.unit_allocation.unit_allocation.get_payment_schedule",
                args: {
                    property_name: frm.doc.property
                },
                callback: function(r) {
                    if (r.message) {
                        frm.clear_table("payment_schedule_details");
                        r.message.forEach((row, index) => {
                            let child = frm.add_child("payment_schedule_details");
                            child.property_price = row.property_price;
                            child.stage_details = row.stage_details;
                            child.payment = row.payment;
                            child.amount = row.amount;
                            child.gst = row.gst;
                            child.gst_amount = row.gst_amount;
                            child.total_amount = row.total_amount;
                            child.status = row.status
                        });
                        frm.refresh_field("payment_schedule_details");
                    }
                }
            });

            //Tower Filtering
            frm.set_query("tower", function() {
                return {
                    filters: {
                        "property_name": frm.doc.property
                    }
                };
            });
            frm.set_value('tower', ''); 
            frm.set_value('unit_number', ''); 
        }
    },

    validate: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('Make Stage Payment'), () => {
                frappe.prompt([
                    {
                        fieldname: 'stage',
                        label: 'Select Stage',
                        fieldtype: 'Select',
                        options: frm.doc.payment_schedule_details.map(d => d.stage_details),
                        reqd: 1
                    }
                ], function(values) {
                    frappe.call({
                        method: 'estates.estates.doctype.unit_allocation.unit_allocation.create_stage_payment_entry',
                        args: {
                            unit_allocation_name: frm.doc.name,
                            stage: values.stage
                        },
                        callback: function(r) {
                            if (r.message) {
                                frappe.set_route('Form', 'Payment Entry', r.message);
                            }
                        }
                    });
                }, 'Select Payment Stage', 'Create');
            });
        }
    }
});



    


// function calculate_total_amount(frm) {
//     let total = 0;

    // Ensure payment_details exists and is an array
//     if (frm.doc.payment_details && Array.isArray(frm.doc.payment_details)) {
//         frm.doc.payment_details.forEach(function(row) {
//             total += row.total_amount || 0;
//         });
//     }

    // Set and refresh the total_amount field
//     frm.set_value('total_amount', total);
//     frm.refresh_field('total_amount');
// }
