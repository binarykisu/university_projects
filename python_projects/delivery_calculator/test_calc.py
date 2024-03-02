import unittest
from datetime import datetime
from calculator import calculate_delivery_fee, check_values

# Performing unit testing to prevent future bugs and ensure functions work correctly
class TestCalculator(unittest.TestCase):
  
  def test_calculate_delivery_fee(self):
    """This function tests the calculate_delivery_fee function."""
    result = calculate_delivery_fee(790, 2235, 4, datetime(2024, 1, 15, 13, 0))
    self.assertEqual(result, {"delivery_fee": 710})

  def test_check_values(self):
    """This function tests the check_values function."""
    result = check_values(790, 2235, 4, '2024-01-15T13:00:00Z')
    self.assertEqual(result, (790, 2235, 4, datetime(2024, 1, 15, 13, 0)))
