Feature: The customer service back-end
    As a customer administrator
    I need a RESTful catalog service
    So that I can keep track of all my customers

Background:
    Given the server is started
    # Given the following Customers
    #     | first_name | last_name | userid     | password  | address  |
    #     | Yuteng     | Zhang     | test1      | 123       |  |
    #     | Bohan      | Zhang     | test2      | 456       |  |
    #     | Allen      | Zhang     | test3      | 789       |  |

Scenario: The server is running
    When I visit the "home page"
    Then I should see "Customer REST API Service"
    And I should not see "404 Not Found"

Scenario: Create a Customer
    When I visit the "Home Page"
    And I set the "First Name" to "Yuteng"
    And I set the "Last Name" to "Zhang"
    And I set the "UserID" to "test4"
    And I set the "Password" to "123456"
    And I press the "Create" button
    Then I should see the message "Success"

    # When I copy the "Customer Id" field
    # And I press the "Clear" button
    # Then the "Customer Id" field should be empty
    # And the "First Name" field should be empty
    # And the "Last Name" field should be empty
    # And the "Password" field should be empty
    # And the "Active" field should be empty
    # When I paste the "Customer Id" field
    # And I press the "Retrieve" button
    # Then I should see "Yuteng" in the "First Name" field
    # And I should see "Zhang" in the "Last Name" field
    # And I should see "1" in the "User ID" field
    # And I should see "true" in the "Active" field

    # And I should see "1" in the "Address ID" field
    # And I should see "Main Street" in the "Street" field
    # And I should see "California" in the "State" field
    # And I should see "LA" in the "City" field
    # And I should see "12345" in the "Postal Code" field


Scenario: List all Customers
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "Yuteng" in the results
    And I should see "Bohan" in the results
    And I should see "Allen" in the results

Scenario: Read a Customer
    When I visit the "Home Page"
    And I set the "First Name" to "Bohan"
    And I press the "Search" button
    Then I should see "Bohan" in the "First Name" field
    And I should see "Zhang" in the "Last Name" field
    And I should see "true" in the "Active" field

Scenario: Update a Customer
    When I visit the "Home Page"
    And I set the "First Name" to "Allen"
    And I press the "Search" button
    Then I should see "Allen" in the "First Name" field
    And I should see "Zhang" in the "Last Name" field
    When I change "First Name" to "test"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Customer Id" field
    And I press the "Clear" button
    And I paste the "Customer Id" field
    And I press the "Retrieve" button
    Then I should see "test" in the "First Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "test" in the results
    Then I should not see "Allen" in the results


Scenario: Delete a Customer
    When I visit the "Home Page"
    And I set the "First Name" to "a"
    And I press the "Search" button
    Then I should see "a" in the "First Name" field
    And I should see "b" in the "Last Name" field
    When I press the "Delete" button
    And I set the "First Name" to "a"
    And I press the "Search" button
    Then I should see "a" in the results
    And I should not see "b" in the results

Scenario: Query Customers
    When I visit the "Home Page"
    And I set the "Last Name" to "Zhang"
    And I press the "Search" button
    Then I should see "Yuteng" in the results
    And I should see "Bohan" in the results
    And I should see "Allen" in the results

# Scenario: Action