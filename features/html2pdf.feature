
Feature: Generate a PDF micro-service


  Scenario: Generate PDF when a HTML page is send
    Given A micro-service up and running
    When I send the content of the page "resources/example.html"
    Then I receive a valid PDF file
