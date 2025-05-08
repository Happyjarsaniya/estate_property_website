document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("agent-form").addEventListener("submit", function (event) {
        event.preventDefault(); // Stop page refresh

        let agent_name = document.getElementById("agent_name").value;
        let email = document.getElementById("email").value;
        let phone = document.getElementById("phone").value;
        let image = document.getElementById("image").files[0];

        if (!email.includes("@")) {
            frappe.msgprint("Invalid Email");
            return;
        }

        if (image) {
            let formData = new FormData();
            formData.append("file", image);
            formData.append("is_private", 0);
            formData.append("doctype", "Agent");

            frappe.call({
                method: "frappe.client.upload_file",
                args: {
                    file_name: image.name,
                    file_url: "",
                    doctype: "Agent",
                    docname: "new-agent"
                },
                callback: function (response) {
                    if (response.message.file_url) {
                        saveAgent(agent_name, email, phone, response.message.file_url);
                    } else {
                        frappe.msgprint("Error uploading image");
                    }
                }
            });
        } else {
            saveAgent(agent_name, email, phone, "");
        }
    });
});

function saveAgent(agent_name, email, phone, image_url) {
    frappe.call({
        method: "estates.estates.doctype.agent.agent.create_agent",
        args: {
            agent_name: agent_name,
            email: email,
            phone: phone,
            image: image_url
        },
        callback: function (response) {
            if (response.message === "success") {
                frappe.msgprint("Agent Created Successfully!");
                document.getElementById("agent-form").reset();
            } else {
                frappe.msgprint("Error: " + response.message);
            }
        }
    });
}
