$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response for customer
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
        // if (res.addresses.length > 0){
        //     $("#customer_addressid").val(res.addresses[res.addresses.length-1].id);
        //     $("#customer_street").val(res.addresses[res.addresses.length-1].street);
        //     $("#customer_city").val(res.addresses[res.addresses.length-1].city);
        //     $("#customer_state").val(res.addresses[res.addresses.length-1].state);
        //     $("#customer_postalcode").val(res.addresses[res.addresses.length-1].postal_code);
    }

    // Updates the form with data from the response for address
    // function update_form_data_address(res) {
    //     if (res.length > 0){
    //         $("#address_id").val(res[res.length-1].id);
    //         $("#customer_address_id").val(res[res.length-1].customer_id);
    //         $("#customer_street").val(res[res.length-1].street);
    //         $("#customer_city").val(res[res.length-1].city);
    //         $("#customer_state").val(res[res.length-1].state);
    //         $("#customer_postalcode").val(res[res.length-1].postal_code);
    //     }
    // }

    /// Clears all form fields for customer
    function clear_form_data() {
        $("#customer_first_name").val("");
        $("#customer_last_name").val("");
        $("#customer_userid").val("");
        $("#customer_password").val("");
        $("#customer_active").val("");
    }

    /// Clears all form fields for address
    // function clear_form_data_address() {
    //     $("#customer_address_id").val("");
    //     $("#customer_street").val("");
    //     $("#customer_city").val("");
    //     $("#customer_state").val("");
    //     $("#customer_postalcode").val("");
    // }

    // Updates the flash message area for customers
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // Updates the flash message area for addresses
    // function flash_message_address(message) {
    //     $("#flash_message_addr").empty();
    //     $("#flash_message_addr").append(message);
    // }

    // ****************************************
    // Create a Customer
    // ****************************************

    $("#create-btn").click(function () {
        let first_name = $("#customer_first_name").val();
        let last_name = $("#customer_last_name").val();
        let userid = $("#customer_userid").val();
        let password = $("#customer_password").val();
        let active = true;
        if ($("#customer_active").val() == "false"){
            active = false;
        }

        let data = {
            "first_name": first_name,
            "last_name": last_name,
            "userid": userid,
            "password": password,
            "active": active,
            "addresses": []
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
        let customer_id = $("#customer_id").val();
        let first_name = $("#customer_first_name").val();
        let last_name = $("#customer_last_name").val();
        let userid = $("#customer_userid").val();
        let password = $("#customer_password").val();
        let active = true;
        if ($("#customer_active").val("") == "false"){
            active = false;
        }


        let data = {
            "first_name": first_name,
            "last_name": last_name,
            "userid": userid,
            "password": password,
            "active": active,
            "addresses": []
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
    // Retrieve a Customer
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
    // Delete a Customer
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
    // Activate a Customer
    // ****************************************

    $("#activate-btn").click(function () {
        let customer_id = $("#customer_id").val();
        let first_name = $("#customer_first_name").val();
        let last_name = $("#customer_last_name").val();
        let userid = $("#customer_userid").val();
        let password = $("#customer_password").val();
        let active = true;

        let data = {
            "first_name": first_name,
            "last_name": last_name,
            "userid": userid,
            "password": password,
            "active": active,
            "addresses": []
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
    // Deactivate a Customer
    // ****************************************

    $("#deactivate-btn").click(function () {
        let customer_id = $("#customer_id").val();
        let first_name = $("#customer_first_name").val();
        let last_name = $("#customer_last_name").val();
        let userid = $("#customer_userid").val();
        let password = $("#customer_password").val();
        let active = false;

        let data = {
            "first_name": first_name,
            "last_name": last_name,
            "userid": userid,
            "password": password,
            "active": active,
            "addresses": []
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
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#customer_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // $("#clear-address-btn").click(function () {
    //     $("#address_id").val("");
    //     $("#flash_message_addr").empty();
    //     clear_form_data_address()
    // });

    // ****************************************
    // Search for a Customer
    // ****************************************

    $("#search-btn").click(function () {

        let first_name = $("#customer_first_name").val();
        let last_name = $("#customer_last_name").val();
        let userid = $("#customer_userid").val();

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
        if (userid) {
            if (queryString.length > 0) {
                queryString += '&userid=' + userid
            } else {
                queryString += 'userid=' + userid
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/customers?${queryString}`,
            //contentType: "application/json",
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

    // // ****************************************
    // // Create an Address
    // // ****************************************

    // $("#create-address-btn").click(function () {
    //     let customer_id = $("#customer_address_id").val();
    //     let street = $("#customer_street").val();
    //     let city = $("#customer_city").val();
    //     let state = $("#customer_state").val();
    //     let postal_code = $("#customer_postalcode").val();

    //     let data = {
    //         "customer_id": customer_id,
    //         "street": street,
    //         "city": city,
    //         "state": state,
    //         "postal_code": postal_code
    //     };

    //     $("#flash_message_addr").empty();
        
    //     let ajax = $.ajax({
    //         type: "POST",
    //         url: `/customers/${customer_id}/addresses`,
    //         contentType: "application/json",
    //         data: JSON.stringify(data),
    //     });

    //     ajax.done(function(res){
    //         update_form_data_address(res)
    //         flash_message_address("Success")
    //     });

    //     ajax.fail(function(res){
    //         flash_message_address(res.responseJSON.message)
    //     });
    // });


    // // ****************************************
    // // Update an Address
    // // ****************************************

    // $("#update-address-btn").click(function () {
    //     let address_id = $("#address_id").val();
    //     let customer_id = $("#customer_address_id").val();
    //     let street = $("#customer_street").val();
    //     let city = $("#customer_city").val();
    //     let state = $("#customer_state").val();
    //     let postal_code = $("#customer_postalcode").val();

    //     let data = {
    //         "customer_id": customer_id,
    //         "street": street,
    //         "city": city,
    //         "state": state,
    //         "postal_code": postal_code
    //     };

    //     $("#flash_message_addr").empty();

    //     let ajax = $.ajax({
    //             type: "PUT",
    //             url: `/customers/${customer_id}/addresses/${address_id}`,
    //             contentType: "application/json",
    //             data: JSON.stringify(data)
    //         })

    //     ajax.done(function(res){
    //         update_form_data_address(res)
    //         flash_message_address("Success")
    //     });
    
    //     ajax.fail(function(res){
    //         flash_message_address(res.responseJSON.message)
    //     });

    // });

    // // ****************************************
    // // Retrieve an Address
    // // ****************************************

    // $("#retrieve-address-btn").click(function () {

    //     let address_id = $("#address_id").val();
    //     let customer_id = $("#customer_address_id").val();

    //     $("#flash_message_addr").empty();

    //     let ajax = $.ajax({
    //         type: "GET",
    //         url: `/customers/${customer_id}/addresses/${address_id}`,
    //         contentType: "application/json",
    //         data: ''
    //     })

    //     ajax.done(function(res){
    //         update_form_data_address(res)
    //         flash_message_address("Success")
    //     });
    
    //     ajax.fail(function(res){
    //         clear_form_data_address()
    //         flash_message_address(res.responseJSON.message)
    //     });

    // });

    // // ****************************************
    // // Delete an Address
    // // ****************************************

    // $("#delete-address-btn").click(function () {

    //     let address_id = $("#address_id").val();
    //     let customer_id = $("#customer_address_id").val();

    //     $("#flash_message_addr").empty();

    //     let ajax = $.ajax({
    //         type: "DELETE",
    //         url: `/customers/${customer_id}/addresses/${address_id}`,
    //         contentType: "application/json",
    //         data: '',
    //     })

    //     ajax.done(function(res){
    //         update_form_data_address(res)
    //         flash_message_address("Customer has been Deleted!")
    //     });

    //     ajax.fail(function(res){
    //         flash_message_address("Server error!")
    //     });
    // });

    // // ****************************************
    // // Search for all Address per Customer
    // // ****************************************

    // $("#search-btn").click(function () {

    //     let customer_id = $("#customer_address_id").val();

    //     $("#flash_message_addr").empty();

    //     let ajax = $.ajax({
    //         type: "GET",
    //         url: `/customers/${customer_id}/addresses`,
    //         //contentType: "application/json",
    //         data: ''
    //     })

    //     ajax.done(function(res){
    //         //alert(res.toSource())
    //         $("#search_results_addr").empty();
    //         let table = '<table class="table table-striped" cellpadding="10">'
    //         table += '<thead><tr>'
    //         table += '<th class="col-md-2">ID</th>'
    //         table += '<th class="col-md-2">Street</th>'
    //         table += '<th class="col-md-2">State</th>'
    //         table += '<th class="col-md-2">City</th>'
    //         table += '<th class="col-md-2">Postal Code</th>'
    //         table += '</tr></thead><tbody>'
    //         let firstAddress = "";
    //         for(let i = 0; i < res.length; i++) {
    //             let address = res[i];
    //             table +=  `<tr id="row_${i}"><td>${address.id}</td><td>${address.street}</td><td>${address.state}</td><td>${address.city}</td><td>${address.postal_code}</td></tr>`;
    //             if (i == 0) {
    //                 firstAddress = address;
    //             }
    //         }
    //         table += '</tbody></table>';
    //         $("#search_results_addr").append(table);

    //         // copy the first result to the form
    //         if (firstAddress != "") {
    //             update_form_data_address(firstAddress)
    //         }

    //         flash_message_address("Success")
    //     });

    //     ajax.fail(function(res){
    //         flash_message_address(res.responseJSON.message)
    //     });

    // });

})
