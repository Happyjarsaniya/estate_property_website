// Copyright (c) 2025, happy and contributors
// For license information, please see license.txt
frappe.ui.form.on("Property", {
	
    // property_price: function(frm) {
    //     frm.compute_total(frm);
    // },
    // discount: function(frm) {
    //     console.log("Discount updated: ", frm.doc.discount);
    //     frm.copy_discount(frm);
    //     frm.compute_total(frm);
    // },


	// refresh: function(frm){
	// 	frm.copy_discount = function(frm){
	// 		frm.doc.amenities.forEach(d => {
	// 			d.discount = frm.doc.discount;
    //             console.log(d)
	// 		});
	// 		frm.refresh_field('amenities');
			
	// 	};
	// },
	
	
	
	// 	refresh: function(frm) {
	// 		frm.fields_dict["payment_schedule_details"].grid.update_docfield_property("property_price", "read_only", 1);
	// 		frm.refresh_field("payment_schedule_details");
	// 	}
	// ,
	
	
	
	validate: function (frm) {
		// let amenity_list = [];
		// let duplicate_found = false;

		// frm.doc.amenities.forEach(row => {
		// 	if (amenity_list.includes(row.amenity)) {
		// 		duplicate_found = true;
		// 	} else {
		// 		amenity_list.push(row.amenity);
		// 	}
		// });

		// if (duplicate_found) {
		// 	frappe.msgprint(__("Duplicate amenities are not allowed!")); // Warning
		// 	frappe.validated = false; // Prevent form save
		// }

		// Function to check for duplicate amenities
		// frm.check_amenities_duplicate = function (row, amenity) {
		// 	let duplicate = frm.doc.amenities.find(a => a.amenity === row.amenity && a.name !== row.name);
		// 	if (duplicate) {
		// 		frappe.msgprint(__("This amenity is already added!")); // Warning
		// 		frappe.model.delete_doc(cdt, cdn); // Remove row
		// 		return;
		// 	}
		// };
		// console.log("frm.check_amenities_duplicate: ", frm.check_amenities_duplicate);
		// console.log("frm.compute_total: ", frm.compute_total);
		
		// Updated compute_total function (Grand Total Calculation)
		frm.compute_total = function(frm) {
			let total = 0;
			// Loop  child table
			if (frm.doc.amenities) {
				frm.doc.amenities.forEach(d => {
					total += d.amenity_price || 0;
				});
			}
			// New total calculation
			let new_total = (frm.doc.property_price || 0) + total;
			if (frm.doc.discount) {
				new_total = new_total - (new_total * (frm.doc.discount / 100));
			}
			console.log(new_total);
			frm.set_value('grand_total', new_total);
		};  
    
		// Copy discount to amenities
		// frm.copy_discount = function(frm){
		// 	frm.doc.amenities.forEach(d => {
		// 		d.discount = frm.doc.discount;
        //         console.log(d)
		// 	});
		// 	frm.refresh_field('amenities');
			
		// };
		

	
        
	}
});


//------------Amenity Child Table Events
frappe.ui.form.on('Property Amenity Detail', {

	// amenity: function (frm, cdt, cdn) {
	// 	let row = locals[cdt][cdn];

	// 	// Duplicate check logic
	// 	let duplicate = frm.doc.amenities.find(a => a.amenity === row.amenity && a.name !== row.name);
	// 	if (duplicate) {
	// 		console.log(item.amenity)
	// 		frappe.msgprint(__("This amenity is already added!"));
	// 		frappe.model.delete_doc(cdt, cdn); // Remove row
	// 		return;
	// 	}

	// 	// Call custom functions
	// 	frm.check_amenities_duplicate(row, row.amenity);
	// 	frm.compute_total(frm);

	// 	console.log(row);
	// },

	// amenities_remove: function (frm, cdt, cdn) {
	// 	console.log("Amenity Removed");
	// 	frm.compute_total(frm);
	// }
});
