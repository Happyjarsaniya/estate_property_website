frappe.ui.form.on('Tower Sector Detail', { 
    // Auto-generate Floor Details
    total_no_of_floor: function(frm) {
        if (frm.doc.total_no_of_floor) {
            frm.clear_table("floor_details");

            for (let i = 0; i <= frm.doc.total_no_of_floor; i++) {
                let row = frm.add_child("floor_details");
                row.floor_no = i;
                if (i === 0) {
                    row.floor_label = "Ground Floor";  
                    row.total_resident_unit = 0;  
                    row.total_commercial_unit = 0;
                }
            }

            frm.refresh_field("floor_details");
        }
    },

    refresh: function(frm) {
        // Make Ground Floor Resident & Commercial Units Read-Only
        // all rows child table HTML wrapper--->grid.wrapper
        frm.fields_dict["floor_details"].grid.wrapper.on('change', 'input[data-fieldname="floor_no"]', function() {
            set_read_only_fields(frm);
        });

        set_read_only_fields(frm);
    },
    
    // add row btn hide 
    onload: function(frm) {
        frm.fields_dict["floor_details"].grid.cannot_add_rows = true;
    },

    // Restrict Input in Total Resident & Commercial Unit Fields
    property_type: function(frm) { update_fields(frm); },
    total_no_of_residential_units: function(frm) { update_total_units(frm); },
    total_no_of_commercial_units: function(frm) { update_total_units(frm); }
});

// Function to Restrict Editing of Ground Floor Units
function set_read_only_fields(frm) {
    frm.doc.floor_details.forEach(row => {
        let is_ground_floor = row.floor_no === 0;

        frm.fields_dict["floor_details"].grid.update_docfield_property("total_resident_unit", "read_only", is_ground_floor);
        frm.fields_dict["floor_details"].grid.update_docfield_property("total_commercial_unit", "read_only", is_ground_floor);
    });

    frm.refresh_field("floor_details");
}

// Hide/Show Fields Based on Property Type
function update_fields(frm) {
    let is_residential = frm.doc.property_type === "Residential";
    let is_commercial = frm.doc.property_type === "Commercial";

    // Main Form fields hide --> set_df_property
    frm.set_df_property('total_no_of_residential_units', 'hidden', is_commercial);
    frm.set_df_property('total_no_of_commercial_units', 'hidden', is_residential);

    if (is_residential) frm.set_value('total_no_of_commercial_units', 0);
    if (is_commercial) frm.set_value('total_no_of_residential_units', 0);

    // Child Table fields read-only --> update_docfield_property
    frm.fields_dict["floor_details"].grid.update_docfield_property("total_resident_unit", "read_only", is_commercial);
    frm.fields_dict["floor_details"].grid.update_docfield_property("total_commercial_unit", "read_only", is_residential);

    update_total_units(frm);
}

// Calculate Total Units
function update_total_units(frm) {
    let res = frm.doc.total_no_of_residential_units || 0;
    let com = frm.doc.total_no_of_commercial_units || 0;
    frm.set_value('total_units', frm.doc.property_type === "Mixed Use" ? res + com : res || com);
}
