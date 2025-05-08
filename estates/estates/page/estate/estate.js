// frappe.pages['estate'].on_page_load = function(wrapper) {
//     new MyPage(wrapper);
// }

// MyPage = Class.extend({
//     init: function(wrapper) {
//         this.page = frappe.ui.make_app_page({
//             parent: wrapper,
//             title: 'Estate Page',
//             single_column: true
//         });

//         // Render Page Content
//         this.make();
//     },

//     make: function() {
//         let me = this;

//         // Append HTML directly
//         $(this.page.main).append(frappe.estates_page.body);

//         // Fetch Total Price
//         me.get_total_price();

//         // Call Chart Function
//         me.page_chart();
//     },

//     get_total_price: function() {
//         frappe.call({
//             method: "estates.estates.page.estate.estate.get_total_price",
//             callback: function(r) {
//                 console.log(r)
//                 if (r.message && typeof r.message === "object") {
//                     $("#total-price").text(`₹ ${r.message.total || 0}`);
//                 } else {
//                     $("#total-price").text(`₹ ${r.message}`);
//                 }
//             }
//         });
//     },

	

// 	//chart
// 	get_property_price_by_status: function() {
//         frappe.call({
//             method: "estates.estates.page.estate.estate.get_property_price_by_status",
//             callback: function(r) {
//                 console.log(r)
// 				// let price_tuple=[]
// 				let statuses = []
// 				let prices = []
// 				let message=r.message
// 				message.forEach((item,i)=>{
// 					statuses.push(item[0])
// 					prices.push(item[1])
// 					// price_tuple.push(item[1])
// 				});
// 				console.log(statuses,prices)
                
//             }
//         });
//     },

//     page_chart: function() {
//         let chart = new frappe.Chart("#frost-chart", {
//             data: {
//                 labels: statuses,

//                 datasets: [
//                     {
//                         name: statuses[0],
//                         chartType: "bar",
//                         values:prices
//                     },

//                 ]
//             },

//             yMarkers: [{ label: "Marker", value: 70, options: { labelPos: "left" } }],
//             yRegions: [{ label: "Region", start: Math.min(prices[0], prices[1], prices[2]), end: Math.min(prices[0], prices[1], prices[2]), options: { labelPos: "right" } }],

//             title: "Estate Price Chart",
//             type: "axis-mixed",//or 'line' 'bar' 'percentage' 'pie'
//             height: 300,
//             colors: ['purple', '#ffaa6f', 'light-blue'],

//             tooltipOptions: {
//                 formatTooltipX: d => (d + "").toUpperCase(),
//                 formatTooltipY: d => d + " pts"
//             }
//         });
// 		// chart.export();
//     }
// });

// // HTML Dashboard Template
// frappe.estates_page = {
//     body: `
//         <div class="widget-group">
//             <div class="widget-group-head">
//                 <div class="widget-group-control"></div>
//             </div>
//             <div class="widget-group-body grid-col-3">
                
//                 <!-- Total Outgoing Bills -->
//                 <div class="widget number-widget-box">
//                     <div class="widget-head">
//                         <div class="widget-label">
//                             <div class="widget-title">Total Outgoing Bills</div>
//                         </div>
//                     </div>
//                     <div class="widget-body">
//                         <div class="widget-content">
//                             <div class="number" id="total-price">₹ 0.00</div>
//                         </div>
//                     </div>
//                 </div>

//                 <!-- Total Incoming Bills -->
//                 <div class="widget number-widget-box">
//                     <div class="widget-head">
//                         <div class="widget-label">
//                             <div class="widget-title">Total Incoming Bills</div>
//                         </div>
//                     </div>
//                     <div class="widget-body">
//                         <div class="widget-content">
//                             <div class="number">₹ 0.00</div>
//                         </div>
//                     </div>
//                 </div>

//                 <!-- Total Incoming Payment -->
//                 <div class="widget number-widget-box">
//                     <div class="widget-head">
//                         <div class="widget-label">
//                             <div class="widget-title">Total Incoming Payment</div>
//                         </div>
//                     </div>
//                     <div class="widget-body">
//                         <div class="widget-content">
//                             <div class="number">₹ 0.00</div>
//                         </div>
//                     </div>
//                 </div>

//                 <!-- Total Outgoing Payment -->
//                 <div class="widget number-widget-box">
//                     <div class="widget-head">
//                         <div class="widget-label">
//                             <div class="widget-title">Total Outgoing Payment</div>
//                         </div>
//                     </div>
//                     <div class="widget-body">
//                         <div class="widget-content">
//                             <div class="number">₹ 0.00</div>
//                         </div>
//                     </div>
//                 </div>

//             </div>
//         </div>
//         <div id="frost-chart"></div>
//     `
// };


frappe.pages['estate'].on_page_load = function(wrapper) {
    new MyPage(wrapper);
}

MyPage = Class.extend({
    init: function(wrapper) {
        this.page = frappe.ui.make_app_page({
            parent: wrapper,
            title: 'Estate Page',
            single_column: true
        });

        // Render Page Content
        this.make();
    },

    make: function() {
        let me = this;

        // Append HTML directly
        $(this.page.main).append(frappe.estates_page.body);

        // Fetch Total Price
        me.get_total_price();

        // Fetch Property Prices Before Rendering Chart
        me.get_property_price_by_status();
    },

    get_total_price: function() {
        frappe.call({
            method: "estates.estates.page.estate.estate.get_total_price",
            callback: function(r) {
                console.log("Total Price Response:", r);

                if (r.message && typeof r.message === "object") {
                    $("#total-price").text(`₹ ${r.message.total || 0}`);
                } else {
                    $("#total-price").text(`₹ ${r.message}`);
                }
            }
        });
    },

    get_property_price_by_status: function() {
        let me = this; // Reference to MyPage instance

        frappe.call({
            method: "estates.estates.page.estate.estate.get_property_price_by_status",
            callback: function(r) {
                console.log("Chart Data Response:", r);

                let statuses = [];
                let prices = [];

                let message = r.message;
                message.forEach((item) => {
                    statuses.push(item[0]); // Property status
                    prices.push(item[1]);   // Property price
                });

                console.log("Chart Data:", statuses, prices);

                // Now Call the Chart Rendering Function
                me.page_chart(statuses, prices);
            }
        });
    },

    page_chart: function(statuses, prices) {
        let chart = new frappe.Chart("#frost-chart", {
            data: {
                labels: statuses, // Use fetched data

                datasets: [
                    {
                        name: "Property Prices",
                        chartType: "bar",
                        values: prices // Use fetched data
                    }
                ]
            },

            yMarkers: [{ label: "Marker", value: 70000, options: { labelPos: "left" } }],
            yRegions: [{
                label: "Region",
                start: 0,
                end:10000000000,
                options: { labelPos: "right" }
            }],

            title: "Estate Price Chart",
            type: "bar", // or 'line', 'pie', 'percentage'
            height: 400,
            colors: ['purple', '#ffaa6f', 'light-blue'],

            tooltipOptions: {
                formatTooltipX: d => (d + "").toUpperCase(),
                formatTooltipY: d => d + " ₹"
            }
        });

        console.log("Chart Rendered");
    }
});

// HTML Dashboard Template
frappe.estates_page = {
    body: `
        <div class="widget-group">
            <div class="widget-group-head">
                <div class="widget-group-control"></div>
            </div>
            <div class="widget-group-body grid-col-3">
                
                <!-- Total Outgoing Bills -->
                <div class="widget number-widget-box">
                    <div class="widget-head">
                        <div class="widget-label">
                            <div class="widget-title">Total Outgoing Bills</div>
                        </div>
                    </div>
                    <div class="widget-body">
                        <div class="widget-content">
                            <div class="number" id="total-price">₹ 0.00</div>
                        </div>
                    </div>
                </div>

                <!-- Total Incoming Bills -->
                <div class="widget number-widget-box">
                    <div class="widget-head">
                        <div class="widget-label">
                            <div class="widget-title">Total Incoming Bills</div>
                        </div>
                    </div>
                    <div class="widget-body">
                        <div class="widget-content">
                            <div class="number">₹ 0.00</div>
                        </div>
                    </div>
                </div>

                <!-- Total Incoming Payment -->
                <div class="widget number-widget-box">
                    <div class="widget-head">
                        <div class="widget-label">
                            <div class="widget-title">Total Incoming Payment</div>
                        </div>
                    </div>
                    <div class="widget-body">
                        <div class="widget-content">
                            <div class="number">₹ 0.00</div>
                        </div>
                    </div>
                </div>

                <!-- Total Outgoing Payment -->
                <div class="widget number-widget-box">
                    <div class="widget-head">
                        <div class="widget-label">
                            <div class="widget-title">Total Outgoing Payment</div>
                        </div>
                    </div>
                    <div class="widget-body">
                        <div class="widget-content">
                            <div class="number">₹ 0.00</div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
        <div id="frost-chart"></div>
    `
};
