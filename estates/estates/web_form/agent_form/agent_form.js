// frappe.ready(function() {
// 	// bind events here
// })

// frappe.ready(function() {
// // 	// bind events here

// // 	document.querySelector('.page-header').innerHTML=
// // 	`<h2 class='text-success'>Agent New Form</h2>`;


	
// 	frappe.web_form.after_load=()=>{
// 		frappe.web_form.on('email',(field,value)=>{
// 			frappe.msgprint('loaded')
// 			console.log('event',e)
// 			if(!value.includes('@')){
// 				frappe.throw(_("Invalid Email"))
// 			}
// 		});


// 		frappe.web_form.validate = ()=>{
// 			let data = frappe.web_form.get_values();
// 			if(!data.email.includes('@')){
// 				frappe.msgprint("Please enter a valid email");  
// 				return false;
// 			}
// 			return true;
// 		};
// 	}


// })

// frappe.ready(function () {
//     console.log("Agent Form Script Loaded");

//     frappe.web_form.after_load = () => {
//         console.log("Web Form Loaded");

//         // Listen for changes in the "email" field
//         frappe.web_form.on("email", (field, value) => {
//             console.log("email Field Changed:", value);  // Debugging output

//             if (!value.includes('@')) {
//                 frappe.throw(__('Invalid email: Please enter a valid email address.'));
//             }
//         });

//         // Final validation before form submission
//         frappe.web_form.validate = () => {
//             let email = frappe.web_form.get_value("email"); // Get email field value
//             console.log("Validating Form, email Entered:", email); // Debugging output

//             if (!email || !email.includes('@')) {
//                 frappe.msgprint(__('Invalid email: Please enter a valid email address.'));
//                 return false;  // Prevent form submission
//             }
//             return true;  // Allow form submission
//         };
//     };
// });



frappe.ready(function() {
    frappe.web_form.after_load = () => {

        // Validate email on field change
        frappe.web_form.on('email', (field, value) => {
            if (!validate_email(value)) {
                frappe.msgprint({
                    title: __('Invalid Email'),
                    message: __('Please enter a valid email address.'),
                    indicator: 'red'
                });
            }
        });

        // Prevent form submission if email is invalid
        frappe.web_form.validate = () => {
            let data = frappe.web_form.get_values();
            if (!validate_email(data.email)) {
                frappe.msgprint({
                    title: __('Validation Error'),
                    message: __('Please enter a valid email before submitting.'),
                    indicator: 'red'
                });
                return false; // Stop form submission
            }
            return true;
        };
    };
});

// Function to validate email format
function validate_email(email) {
    let email_regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return email_regex.test(email);
}
