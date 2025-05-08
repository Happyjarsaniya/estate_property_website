console.log("Custom Payment Entry JS Loaded");

frappe.ui.form.on("Payment Entry", {
    custom_paid_stage: function(frm) {
        if (frm.doc.custom_paid_stage && frm.stage_amount_map) {
            let amount = frm.stage_amount_map[frm.doc.custom_paid_stage];
            if (amount) {
                frm.set_value('custom_paid_amount_', amount);  
            }
        }
    },

    custom_unit_allocation: function(frm) {
        console.log("function call");
    
        if (!frm.doc.custom_unit_allocation) return;
        // ---> 1 Call get stage 
        frappe.call({
            method: "estates.overrides.payment_entry.get_stage_options",
            args: {
                unit_allocation_name: frm.doc.custom_unit_allocation
            },
            callback: function(res) {
                console.log(res.message, 'res.message');
    
                let stages_data = res.message;
    
                let stage_names = stages_data.map(row => row.stage_details);
                let unique_stages = [...new Set(stage_names)].sort();
    
                frm.set_df_property("custom_paid_stage", "options", unique_stages);
                frm.refresh_field("custom_paid_stage");
    
                let stage_amount_map = {};
                stages_data.forEach(row => {
                    stage_amount_map[row.stage_details] = row.total_amount;
                });
    
                console.log(stage_amount_map, 'Stage to Total Amount Map');
                frm.stage_amount_map = stage_amount_map;
            }
        });    
        // ---> 2 Call get rent months
        frappe.call({
            method: "estates.overrides.payment_entry.get_rent_months",
            args: {
                unit_allocation: frm.doc.custom_unit_allocation
            },
            callback: function(r) {
                console.log(r.message, "r.message");
                if (r.message) {
                    const month_order_map = {
                        "January": 1, "February": 2, "March": 3, "April": 4,
                        "May": 5, "June": 6, "July": 7, "August": 8,
                        "September": 9, "October": 10, "November": 11, "December": 12
                    };
                    const valid_months = r.message.filter(m => month_order_map[m]);

                    valid_months.sort((a, b) => month_order_map[a] - month_order_map[b]);

                    frm.set_df_property("custom_month", "options", valid_months);
                    frm.refresh_field("custom_month");

                }
            },
        });
        frappe.call({
            method: "estates.overrides.payment_entry.get_lease_months",
            args: {
                unit_allocation: frm.doc.custom_unit_allocation
            },
            callback: function(r) {
                if (r.message) {
                    frm.set_df_property("custom_lease_month", "options", r.message);
                    frm.refresh_field("custom_lease_month");
                }
            }
        });
    }
});
