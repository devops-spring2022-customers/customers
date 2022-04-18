Feature: The customer service back-end
    As a customer administrator
    I need a RESTful catalog service
    So that I can keep track of all my customers

Background:
    Given the server is started

Scenario: The server is running
    When I visit the "home page"
    Then I should see "Customer REST API Service"
    And I should not see "404 Not Found"