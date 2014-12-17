Python_code_examples
====================

Description for 'google_geocode_unit_tests.py':

The test cases begin with basic behavioral tests revolving around variations on the same
address/location query, testing by latitude and longitude, full address, partial address variations,
with and without commas, the city alone, and an incorrect version of the address. Following
these basic tests I tested a Canadian address to ensure that addresses outside of the USA
yielded a proper location response, and then a series of edge cases for international
monuments, extreme and non­existent coordinates, bad data, searching for two addresses at
once, and parameter misuse
