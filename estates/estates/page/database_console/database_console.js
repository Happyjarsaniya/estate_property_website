frappe.pages['database-console'].on_page_load = function(wrapper) {
    new MyPage(wrapper);
}

MyPage = Class.extend({
    init: function(wrapper) {
        this.page = frappe.ui.make_app_page({
            parent: wrapper,
            title: 'Database Console',
            single_column: true
        });

        // Render Page Content
        this.make();
    },

    make: function() {
        let me = this;  // Correct reference

        // Append HTML directly
        $(this.page.main).html(frappe.estates_page.body);  // Directly setting HTML
		//execute method
		// form query
		function makeTable(data){

		}

		// workwith form data
		function makeQuery(formQuery){
			document.querySelector("#queryResult").innerHTML = formQuery;
		}	

        // Submit event for the form
        $("#queryForm").submit(function(e) {
            e.preventDefault();
			let formquery=$("#query")[0].value;
			console.log(formquery);
			makeQuery(formquery);
        });
    },
});

// HTML Form Template
frappe.estates_page = {
    body: `
	<div id=""></div>
        <form id="queryForm">
          <div class="form-group">
            <label for="exampleInputEmail1">Email address</label>
           	<textarea class="form-control" id="query exampleFormControlTextarea1" rows="3"></textarea>
			<small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>
          </div>
          <button type="submit" class="btn btn-primary">Submit</button>
        </form>
	</div>
	<div id="quertResult"></div>	
    `
};
