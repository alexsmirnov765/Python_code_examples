# Alexey Smirnov (alexsmirnov765@gmail.com)
#
# Requires installation Python v3.3 or higher + 'pip' module
#
# Requires installation of the Python 'requests' module (for example - 'pip install requests' or 'sudo pip install requests')
#
# Run with: python google_geocode_unit_tests.py

import unittest
import requests
import urllib
import time

class TestFunctions(unittest.TestCase):

	"""Google Geocode API Unit-tests"""

	######################
	# SetUp and Helper Functions

	maxDiff = None # set to unrestrict assertEqual() argument lengths

	def setUp(self):
		self.base = "http://maps.googleapis.com/maps/api/geocode/json?" # base url

	def tearDown(self):
		time.sleep(1)  # sleep to prevent exceeding query limit (where result['status'] == 'OVER_QUERY_LIMIT')

	def geocode(self, address, sensor="false"):
		params = urllib.urlencode({'address': address, 'sensor': sensor})
		url = str(self.base+params)
		response = requests.get(url, timeout=1) # timeout after 1 second
		return response.json()

	def reverse_geocode(self, lat, lng, sensor="false"):
		params = urllib.urlencode({'latlng': lat+','+lng, 'sensor': sensor})
		url = str(self.base+params)
		response = requests.get(url, timeout=1) # timeout after 1 second
		return response.json()

	def assertIsLatLng(self, result):
		self.assertEqual(result['status'], "OK")
		self.assertTrue("lat" in result["results"][0]['geometry']['location'])
		self.assertTrue("lng" in result["results"][0]['geometry']['location'])
		self.assertTrue(isinstance(result["results"][0]['geometry']['location']['lat'], float))
		self.assertTrue(isinstance(result["results"][0]['geometry']['location']['lng'], float))

	def assertZeroResults(self, result):
		self.assertEqual(len(result['results']), 0)
		self.assertEqual(result['status'], "ZERO_RESULTS") 

	######################
	# Basic Behavior Cases

	def test_existing_address(self):
		result = self.geocode("1600 Amphitheatre Parkway Mountain View CA 94043 USA")
		self.assertIsLatLng(result)
		self.assertEqual(result, self.reverse_geocode("37.4214111", "-122.0840372"))

	def test_reverse_address(self):
		result = self.reverse_geocode("37.4214111", "-122.0840372")
		self.assertIsLatLng(result)
		self.assertEqual(result, self.geocode("1600 Amphitheatre Parkway Mountain View CA 94043 USA"))

	def test_with_commas(self):
		result = self.geocode("1600 Amphitheatre Parkway, Mountain View, CA, 94043, USA")
		self.assertIsLatLng(result)
		self.assertEqual(result, self.reverse_geocode("37.4214111", "-122.0840372"))

	def test_without_country(self):
		result = self.geocode("1600 Amphitheatre Parkway Mountain View CA 94043")
		self.assertIsLatLng(result)
		self.assertEqual(result, self.reverse_geocode("37.4214111", "-122.0840372"))

	def test_without_zip_country(self):
		result = self.geocode("1600 Amphitheatre Parkway Mountain View CA")
		self.assertIsLatLng(result)
		self.assertEqual(result, self.reverse_geocode("37.4214111", "-122.0840372"))

	def test_without_state_zip_country(self):
		result = self.geocode("1600 Amphitheatre Parkway Mountain View")
		self.assertIsLatLng(result)
		self.assertEqual(result, self.reverse_geocode("37.4214111", "-122.0840372"))

	def test_without_city_state_zip_country(self):
		result = self.geocode("1600 Amphitheatre Parkway")
		self.assertIsLatLng(result)
		self.assertEqual(result, self.reverse_geocode("37.4214111", "-122.0840372"))

	def test_without_street_number(self):
		result = self.geocode("Mountain View CA 94043 USA")
		self.assertIsLatLng(result)

	def test_city(self):
		result = self.geocode("Mountain View")
		self.assertIsLatLng(result)

	def test_wrong_address(self):
		result = self.geocode("1600 Amphitheatre Parkway Mountain View WA 92043 USA")
		self.assertIsLatLng(result)
		self.assertTrue(result != self.reverse_geocode("37.4214111", "-122.0840372"))

	######################

	def test_canadian_address(self):
		result = self.geocode("100 Queen St W, Toronto, ON M5H 2N2, Canada")
		self.assertIsLatLng(result)

	######################
	# Edge Cases

	def test_eiffel_tower(self):
		result = self.geocode("Eiffel Tower")
		self.assertIsLatLng(result)
		self.assertEqual(result, self.geocode("Eiffel Tower, Avenue Anatole France, Paris, France"))

	def test_big_ben(self):
		result = self.geocode("Big Ben")
		self.assertIsLatLng(result)

	def test_north_pole(self):
		# longitude irrelevant
		result = self.reverse_geocode("90", "0")
		self.assertZeroResults(result)
		result = self.reverse_geocode("90", "90")
		self.assertZeroResults(result)
		result = self.reverse_geocode("90", "-0")
		self.assertZeroResults(result)
		result = self.reverse_geocode("90", "")
		self.assertZeroResults(result)

	def test_non_existent_lat(self):
		result = self.reverse_geocode("2700", "0")
		self.assertZeroResults(result)

	def test_non_existent_lng(self):
		result = self.reverse_geocode("0", "-4500.67")
		self.assertZeroResults(result)

	def test_bad_data_latlng(self):
		result = self.reverse_geocode("Xi#d@!", "/3*()")
		self.assertZeroResults(result)

	def test_bad_data_address(self):
		result = self.geocode("$ City ## /3*()")
		self.assertZeroResults(result)

	def test_two_addressess(self):
		result = self.geocode("838 Meander Court Walnut Creek CA 94598 1600 Amphitheatre Parkway Mountain View CA 94043 USA")
		self.assertIsLatLng(result)

	def param_misusage(self):
		result = self.reverse_geocode("838 Meander Court Walnut Creek CA 94598", "1600 Amphitheatre Parkway Mountain View CA 94043 USA")
		print(str(result))
		self.assertZeroResults(result)

if __name__ == '__main__':
	unittest.main()