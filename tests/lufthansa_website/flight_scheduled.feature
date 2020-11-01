Feature: Comparing flight scheduled updated data from api with lufthansa website

  Scenario: Compare updated data from API with lufthansa website
    Given I connect to broker and get updated data about flights
    When I request flight status from API
    And go to lufthansa website
    And confirm privacy settings
    And I click to flight status
    And enter data from API
    Then data should be the same