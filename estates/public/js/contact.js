// document.addEventListener("DOMContentLoaded",  function () {
//     document.getElementById("contact-form").addEventListener("submit", async function(event) {
//         event.preventDefault();

//         let formData = {
//             first_name: document.getElementById("first_name").value,
//             email_id: document.getElementById("email_id").value,
//             mobile_no: document.getElementById("mobile_no").value,
//             custom_price_range:document.getElementById("custom_price_range").value,
//             message: document.getElementById("message").value
//         };

//         console.log("Submitting Form Data:", formData);

//         try {
//             let response = await fetch("/api/method/estates.api.contact.create_lead", {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json",
//                     "Accept": "application/json",
//                     "X-Frappe-CSRF-Token": document.querySelector('meta[name="csrf_token"]').getAttribute('content')
//                 },
//                 body: JSON.stringify(formData)
//             });
//             // await = properly retrieve the parsed data.
//             let result = await response.json();
//             console.log("API Response:", result);

           
//             if (result.status && result.status === "success") {
//                 alert("Lead Created Successfully!");
//                 document.getElementById("contact-form").reset();
//                 return; 
//             }

//             let errorMessage = "Unknown error occurred!";
                
//             if (result._server_messages) {
//                 try {
//                     let serverMessages = JSON.parse(result._server_messages);
//                     errorMessage = serverMessages.length ? JSON.parse(serverMessages[0]).message : errorMessage;
//                 } catch (e) {
//                     console.error("Error parsing _server_messages:", e);
//                 }
//             } else if (result.message) {
//                 errorMessage = typeof result.message === "string" ? result.message : (result.message.message || errorMessage);
//             }

//             alert("" + errorMessage);
//             document.getElementById("contact-form").reset();

//         } catch (error) {
//             console.error("Unknown Error:", error);
//             alert("Unknown Error Occurred: " + error.message);
//         }
//     });
// });
