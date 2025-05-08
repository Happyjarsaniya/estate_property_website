// Copyright (c) 2025, happy and contributors
// For license information, please see license.txt

frappe.ui.form.on('Unit Details', {
    // filtre based on property name only show this property related  tower 
    property: function(frm) {
        if (frm.doc.property) {
            frm.set_query('tower', function() {
                return {
                    filters: {
                        'property_name': frm.doc.property
                    }
                };
            });
        }
    },
      
    property_name: function(frm) {
        frm.set_query("tower_name", function() {
            return {
                filters: {
                    property_name: frm.doc.property_name
                }
            };
        });
    },
    
    
    // based on unit_number auto generate floor number like 201 floor_number = 2 ,1101 floorl_num = 11
    unit_number: function(frm) {
        if (frm.doc.unit_number && frm.doc.unit_number != "0") {
            let unit_no = frm.doc.unit_number.toString().trim(); 
            let floor_no = (unit_no.length >= 3) ? unit_no.substring(0, unit_no.length - 2) : unit_no.substring(0, 1);

            frm.set_value('floor_number', parseInt(floor_no) || 0); 
        }
    },
    
    // Auto-Calculate Carpet Area Based on Unit Size like
//     Unit Size	Min Carpet Area (80%)	Max Carpet Area (90%)	Avg Carpet Area
//     1000 sq.ft	800 sq.ft	            900 sq.ft	            850 sq.ft
    unit_size: function(frm) {
        if (frm.doc.unit_size > 0) {
            let min_area = frm.doc.unit_size * 0.8;
            let max_area = frm.doc.unit_size * 0.9;
            frm.set_value('average_carpet_area', (min_area + max_area) / 2);
        }
    },

    // based on unit type Automatically set bed balcony and bathroom
    unit_type: function(frm) {
            let unit_mapping = {
                "1BHK": { no_of_bedrooms: 1, no_of_bathrooms: 1, no_of_balconies: 1 },
                "2BHK": { no_of_bedrooms: 2, no_of_bathrooms: 2, no_of_balconies: 1 },
                "3BHK": { no_of_bedrooms: 3, no_of_bathrooms: 2, no_of_balconies: 2 },
                "4BHK": { no_of_bedrooms: 4, no_of_bathrooms: 3, no_of_balconies: 2 },
                "5BHK": { no_of_bedrooms: 5, no_of_bathrooms: 4, no_of_balconies: 3 }
            };
    
            if (unit_mapping[frm.doc.unit_type]) {
                // Automatically set 
                frm.set_value('no_of_bedrooms', unit_mapping[frm.doc.unit_type].no_of_bedrooms);
                frm.set_value('no_of_bathrooms', unit_mapping[frm.doc.unit_type].no_of_bathrooms);
                frm.set_value('no_of_balconies', unit_mapping[frm.doc.unit_type].no_of_balconies);
            }
        },    
});
