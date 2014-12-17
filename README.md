Python_code_examples
====================

Description for 'google_geocode_unit_tests.py':

This program is designed to test Google’s Geocode API. It is implemented in Python and assumes that you are using Python 3.3 or a compatible version. Additionally, the Python module requests is utilized throughout and its installation is required (install requests).

Run with: $ python google_geocode_unit_tests.py

The test cases begin with basic behavioral tests revolving around variations on the same
address/location query, testing by latitude and longitude, full address, partial address variations,
with and without commas, the city alone, and an incorrect version of the address. Following
these basic tests I tested a Canadian address to ensure that addresses outside of the USA
yielded a proper location response, and then a series of edge cases for international
monuments, extreme and non­existent coordinates, bad data, searching for two addresses at
once, and parameter misuse
