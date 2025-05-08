// document.querySelector("#contact-agent").addEventListener('click',
//     (e)=>{
//         let agent_email = document.querySelector("#email").value;
//         console.log(agent_email);
//         let property_code=document.querySelector("#property-name").textContent;
//         let d = new frappe.ui.Dialog({
//             title: 'Enter details',
//             fields: [
//                 {
//                     label: 'Your Name',
//                     fieldname: 'name',
//                     fieldtype: 'Data'
//                 },
//                 {
//                     label: 'Your Email',
//                     fieldname: 'email',
//                     fieldtype: 'Data'
//                 },
//                 {
//                     label: 'Message',
//                     fieldname: 'message',
//                     fieldtype: 'Small Text'
//                 }
//             ],
//             size: 'small', // small, large, extra-large 
//             primary_action_label: 'Submit',
//             primary_action(values) {
//                 values.agent_email=agent_email;
//                 values.property_code=property_code;
//                 console.log(values);
//                 //ApI call 
//                 frappe.call({
//                     method: "estates.api.contact_agent", //dotted path to server method
//                     args:values,
//                     callback: function(r) {
//                     // code snippet
//                         console.log(r)
//                         frappe.msgprint({
//                             title:__('Notification'),
//                             indicator:'green',
//                             message:__(r.message)
//                         });
//                     }
//                 });
//                 d.hide();
//             }
//         });
        
//         d.show();
//         console.log('Dialog Start')
//     })


// 



document.querySelector('#contact-agent').addEventListener('click', (e)=>{
    let agent_email = document.querySelector('#email').value;
    console.log(agent_email);
    let d = new frappe.ui.Dialog({
        title: 'Enter details',
        fields: [
            {
                label: 'First Name',
                fieldname: 'first_name',
                fieldtype: 'Data'
            },
            {
                label: 'Last Name',
                fieldname: 'last_name',
                fieldtype: 'Data'
            },
            {
                label: 'Age',
                fieldname: 'age',
                fieldtype: 'Int'
            }
        ],
        size: 'small', // small, large, extra-large 
        primary_action_label: 'Submit',
        primary_action(values) {
            console.log(values);
            d.hide();
        }
    });
    

    console.log('DIALOG START');
    d.show();
    console.log('DIALOG END');
    
    
    
})