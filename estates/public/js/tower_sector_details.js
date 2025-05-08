frappe.ui.form.on('Tower/Sector Details', {
    total_no_of_floor: function(frm) {
        if (frm.doc.total_no_of_floor) {
            frm.clear_table("floor_details");  // Clear existing records
            
            for (let i = 0; i <= frm.doc.total_no_of_floor; i++) {
                let row = frm.add_child("floor_details");

                // Assign Floor Number dynamically
                row.floor_no = i === 0 ? "Ground Floor" : `Floor No-${i}`;
                row.total_resident_unit = 0;  // Default value
                row.total_commercial_unit = 5;  // Default value
            }
            frm.refresh_field("floor_details");
        }
    }
});
