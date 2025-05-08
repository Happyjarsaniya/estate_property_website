// Copyright (c) 2025, happy and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Agent", {
// 	refresh(frm) {

// 	},
// });
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("agent-form").addEventListener("submit", function (event) {
        event.preventDefault(); // Stop form from refreshing page

        let agent_name = document.getElementById("agent_name").value;
        let email = document.getElementById("email").value;
        let phone = document.getElementById("phone").value;

        // Validation
        if (!email.includes("@")) {
            alert("Invalid Email");
            return;
        }

        frappe.call({
            method: "estates.estates.www.agents.agent.create_agent",
            args: {
                agent_name: agent_name,
                email: email,
                phone: phone
            },
            callback: function (response) {
                if (response.message === "success") {
                    alert("Agent Created Successfully!");
                    document.getElementById("agent-form").reset();
                } else {
                    alert("Error: " + response.message);
                }
            }
        });
    });
});
