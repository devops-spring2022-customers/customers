$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#customer_id").val(res.id);
        $("#customer_first_name").val(res.first_name);
        $("#customer_last_name").val(res.last_name);
        $("#customer_userid").val(res.userid);
        $("#customer_password").val(res.password);
        if (res.active == true) {
            $("#customer_active").val("true");
        } else {
            $("#customer_active").val("false");
        }
        if (res.addresses.length > 0){
            $("#customer_addressid").val(res.addresses[0].id);
            $("#customer_street").val(res.addresses[0].street);
            $("#customer_city").val(res.addresses[0].city);
            $("#customer_state").val(res.addresses[0].state);
            $("#customer_postal_code").val(res.addresses[0].postal_code);
        }
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#customer_first_name").val("");
        $("#customer_last_name").val("");
        $("#customer_userid").val("");
        $("#customer_password").val("");
        $("#customer_active").val("");

        $("#customer_street").val("");
        $("#customer_city").val("");
        $("#customer_state").val("");
        $("#customer_postal_code").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Customer
    // ****************************************

    $("#create-btn").click(function () {


        let first_name = $("#customer_first_name").val();
        let last_name = $("#customer_last_name").val();
        let user_id = $("#customer_userid").val();
        let password = $("#customer_password").val();
        let active = true;
        if ($("#customer_active").val("") == "false"){
            active = false;
        }
        let addresses = [];

        let data = {
            "first_name": first_name,
            "last_name": last_name,
            "userid": user_id,
            "password": password,
            "active": active,
            "addresses": addresses
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/customers",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Customer
    // ****************************************

    $("#update-btn").click(function () {

        let first_name = $("#customer_first_name").val();
        let last_name = $("#customer_last_name").val();
        let user_id = $("#customer_userid").val();
        let password = $("#customer_password").val();
        let active = true;
        if ($("#customer_active").val("") == "false"){
            active = false;
        }

        let data = {
            "first_name": first_name,
            "last_name": last_name,
            "userid": user_id,
            "password": password,
            "active": active
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/customers/${customer_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Pet
    // ****************************************

    $("#retrieve-btn").click(function () {

        let customer_id = $("#customer_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/customers/${customer_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Pet
    // ****************************************

    $("#delete-btn").click(function () {

        let customer_id = $("#customer_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/customers/${customer_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Customer has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#customer_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a Customer
    // ****************************************

    $("#search-btn").click(function () {

        let first_name = $("#customer_first_name").val();
        let last_name = $("#customer_last_name").val();
        let user_id = $("#customer_userid").val();

        let queryString = ""

        if (first_name) {
            queryString += 'first_name=' + first_name
        }
        if (last_name) {
            if (queryString.length > 0) {
                queryString += '&last_name=' + last_name
            } else {
                queryString += 'last_name=' + last_name
            }
        }
        if (user_id) {
            if (queryString.length > 0) {
                queryString += '&user_id=' + user_id
            } else {
                queryString += 'user_id=' + user_id
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/customers?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">First Name</th>'
            table += '<th class="col-md-2">Last Name</th>'
            table += '<th class="col-md-2">User ID</th>'
            table += '<th class="col-md-2">Password</th>'
            table += '<th class="col-md-2">Active</th>'
            table += '</tr></thead><tbody>'
            let firstCustomer = "";
            for(let i = 0; i < res.length; i++) {
                let customer = res[i];
                table +=  `<tr id="row_${i}"><td>${customer.id}</td><td>${customer.first_name}</td><td>${customer.last_name}</td><td>${customer.userid}</td><td>${customer.password}</td><td>${customer.active}</td></tr>`;
                if (i == 0) {
                    firstCustomer = customer;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstCustomer != "") {
                update_form_data(firstCustomer)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
