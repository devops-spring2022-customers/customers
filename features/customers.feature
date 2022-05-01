Feature: The customer service back-end
    As a customer administrator
    I need a RESTful catalog service
    So that I can keep track of all my customers

Background:
    Given the following Customers
        | first_name | last_name | userid | password   | address  |
        | Yuteng     | Zhang     | 1      | 123        |  |
        | Bohan      | Zhang     | 2      | 456        |  |
        | Allen      | Zhang     | 3      | 789        |  |
        | John       | Rofrano   | 4      | devops2022 |  |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customer RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Customer
    When I visit the "Home Page"
    And I set the "First Name" to "Yuteng"
    And I set the "Last Name" to "Zhang"
    And I set the "UserID" to "5"
    And I set the "Password" to "123456"
    And I press the "Create" button
    Then I should see the message "Success"

    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "Yuteng" in the "First Name" field
    And I should see "Zhang" in the "Last Name" field
    And I should see "5" in the "UserID" field
    And I should see "true" in the "Active" field

    When I press the "Clear" button
    Then the "Id" field should be empty
    And the "First Name" field should be empty
    And the "Last Name" field should be empty
    And the "Password" field should be empty
    And the "Active" field should be empty

Scenario: List all Customers
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "Yuteng" in the results
    And I should see "Bohan" in the results
    And I should see "Allen" in the results
    And I should not see "Harsh" in the results
    And I should not see "Jash" in the results

Scenario: Search for Customers
    When I visit the "Home Page"
    And I set the "Last Name" to "Zhang"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Allen" in the results
    And I should see "Yuteng" in the results
    And I should see "Bohan" in the results
    And I should not see "John" in the results

Scenario: Update a Customer
    When I visit the "Home Page"
    And I set the "First Name" to "Allen"
    And I press the "Search" button
    Then I should see "Allen" in the "First Name" field
    And I should see "Zhang" in the "Last Name" field
    When I change "First Name" to "test"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "test" in the "First Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "test" in the results
    Then I should not see "Allen" in the results

Scenario: Delete a Customer
    When I visit the "Home Page"
    And I set the "UserID" to "4"
    And I press the "Search" button
    Then I should see "John" in the "First Name" field
    And I should see "Rofrano" in the "Last Name" field

    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Delete" button
    And I press the "Clear" button
    And I press the "Search" button
    Then I should see "Yuteng" in the results
    And I should see "Bohan" in the results
    And I should see "Allen" in the results
    And I should not see "John" in the results

Scenario: Query Customers
    When I visit the "Home Page"
    And I set the "Last Name" to "Zhang"
    And I press the "Search" button
    Then I should see "Yuteng" in the results
    And I should see "Bohan" in the results
    And I should see "Allen" in the results

Scenario: Perform Actions on Customers
    When I visit the "Home Page"
    And I set the "UserID" to "2"
    And I press the "Search" button
    Then I should see "Bohan" in the "First Name" field
    And I should see "Zhang" in the "Last Name" field

    When I copy the "Id" field
    And I press the "Deactivate" button
    Then I should see the message "Success"
    
    When I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "false" in the "active" field

    When I set the "UserID" to "2"
    And I press the "Search" button
    Then I should see "Bohan" in the "First Name" field
    And I should see "Zhang" in the "Last Name" field

    When I copy the "Id" field
    And I press the "Activate" button
    Then I should see the message "Success"
    
    When I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "true" in the "active" field

Scenario: Create an Address
    When I visit the "Home Page"
    And I set the "First Name" to "Yuteng"
    And I set the "Last Name" to "Zhang"
    And I set the "UserID" to "5"
    And I set the "Password" to "123456"
    And I press the "Create" button
    Then I should see the message "Success"

    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field to "Customer Address ID"
    And I set the "Street" to "251 Mercer St # 801"
    And I set the "City" to "New York City"
    And I set the "State" to "New York"
    And I set the "PostalCode" to "10012"
    And I press the "Create" button from the "Address" form
    Then I should see the message "Success"
    And I should see "251 Mercer St # 801" in the "Street" field
    And I should see "New York City" in the "City" field
    And I should see "New York" in the "State" field
    And I should see "10012" in the "PostalCode" field

    When I press the "Clear" button from the "Address" form
    Then the "Id" field should be empty from the "Address" form
    And the "Street" field should be empty
    And the "City" field should be empty
    And the "State" field should be empty
    And the "PostalCode" field should be empty

Scenario: List all Addresses of a Customer
    When I visit the "Home Page"
    And I set the "First Name" to "Yuteng"
    And I set the "Last Name" to "Zhang"
    And I set the "UserID" to "5"
    And I set the "Password" to "123456"
    And I press the "Create" button
    Then I should see the message "Success"

    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field to "Customer Address ID"
    And I set the "Street" to "251 Mercer St # 801"
    And I set the "City" to "New York City"
    And I set the "State" to "New York"
    And I set the "PostalCode" to "10012"
    And I press the "Create" button from the "Address" form
    Then I should see the message "Success"
    And I should see "251 Mercer St # 801" in the "Street" field
    And I should see "New York City" in the "City" field
    And I should see "New York" in the "State" field
    And I should see "10012" in the "PostalCode" field

    # When I copy the "Id" field from the "Address" form
    # And I press the "Clear" button from the "Address" form
    # And I paste the "Id" field to "Customer Address ID"
    # And I set the "Street" to "500 W 120th St #510"
    # And I set the "City" to "New York City"
    # And I set the "State" to "New York"
    # And I set the "PostalCode" to "10027"
    # And I press the "Create" button from the "Address" form
    # Then I should see the message "Success"
    # And I should see "500 W 120th St #510" in the "Street" field
    # And I should see "New York City" in the "City" field
    # And I should see "New York" in the "State" field
    # And I should see "10027" in the "PostalCode" field

    # When I copy the "Id" field from the "Address" form
    # And I press the "Clear" button from the "Address" form
    # And I paste the "Id" field to "Customer Address ID"
    # And I press the "Search" button from the "Address" form
    When I press the "Search" button from the "Address" form
    Then I should see the message "Success"
    And I should see "251 Mercer St # 801" in the results for "Address"
    # And I should see "500 W 120th St #510" in the results for "Address"
    And I should see "10012" in the results for "Address"
    # And I should see "10027" in the results for "Address"
    And I should not see "2 W Loop Rd" in the results for "Address"
    And I should not see "10044" in the results for "Address"

Scenario: Update an Address
    When I visit the "Home Page"
    And I set the "First Name" to "Yuteng"
    And I set the "Last Name" to "Zhang"
    And I set the "UserID" to "5"
    And I set the "Password" to "123456"
    And I press the "Create" button
    Then I should see the message "Success"

    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field to "Customer Address ID"
    And I set the "Street" to "251 Mercer St # 801"
    And I set the "City" to "New York City"
    And I set the "State" to "New York"
    And I set the "PostalCode" to "10012"
    And I press the "Create" button from the "Address" form
    Then I should see the message "Success"
    And I should see "251 Mercer St # 801" in the "Street" field
    And I should see "New York City" in the "City" field
    And I should see "New York" in the "State" field
    And I should see "10012" in the "PostalCode" field

    When I set the "Street" to "Modified Street Name"
    And I press the "Update" button from the "Address" form
    Then I should see the message "Success"
    And I should see "Modified Street Name" in the "Street" field
    And I should see "New York City" in the "City" field
    And I should see "New York" in the "State" field
    And I should see "10012" in the "PostalCode" field

Scenario: Delete an Address
    When I visit the "Home Page"
    And I set the "First Name" to "Yuteng"
    And I set the "Last Name" to "Zhang"
    And I set the "UserID" to "5"
    And I set the "Password" to "123456"
    And I press the "Create" button
    Then I should see the message "Success"

    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field to "Customer Address ID"
    And I set the "Street" to "251 Mercer St # 801"
    And I set the "City" to "New York City"
    And I set the "State" to "New York"
    And I set the "PostalCode" to "10012"
    And I press the "Create" button from the "Address" form
    Then I should see the message "Success"
    And I should see "251 Mercer St # 801" in the "Street" field
    And I should see "New York City" in the "City" field
    And I should see "New York" in the "State" field
    And I should see "10012" in the "PostalCode" field

    When I press the "Delete" button from the "Address" form
    And I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should not see "251 Mercer St # 801" in the results
    And I should not see "New York City" in the results
    And I should not see "New York" in the results
    And I should not see "10012" in the results