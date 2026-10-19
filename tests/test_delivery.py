import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from delivery import calculate_delivery_cost


class TestDelivery(unittest.TestCase):

    def test_weight_min(self):
        cost, date = calculate_delivery_cost(0.05, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_weight_max(self):
        cost, date = calculate_delivery_cost(50.1, 100, "обычный")
        self.assertEqual(cost, -1)

    def test_weight_01(self):
        cost, date = calculate_delivery_cost(0.1, 100, "обычный")
        self.assertNotEqual(cost, -1)

    def test_weight_50(self):
        cost, date = calculate_delivery_cost(50.0, 100, "обычный")
        self.assertNotEqual(cost, -1)

    def test_distance_0(self):
        cost, date = calculate_delivery_cost(1.0, 0, "обычный")
        self.assertEqual(cost, -1)

    def test_distance_5001(self):
        cost, date = calculate_delivery_cost(1.0, 5001, "обычный")
        self.assertEqual(cost, -1)

    def test_distance_5000(self):
        cost, date = calculate_delivery_cost(1.0, 5000, "обычный")
        self.assertNotEqual(cost, -1)

    def test_bad_type(self):
        cost, date = calculate_delivery_cost(1.0, 100, "жидкий")
        self.assertEqual(cost, -1)

    def test_empty_type(self):
        cost, date = calculate_delivery_cost(1.0, 100, "")
        self.assertEqual(cost, -1)

    def test_base_cost(self):
        cost, _ = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_cost_1km(self):
        cost, _ = calculate_delivery_cost(1.0, 1, "обычный")
        self.assertEqual(cost, 205)

    def test_weight_4_9(self):
        cost, _ = calculate_delivery_cost(4.9, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_weight_5(self):
        cost, _ = calculate_delivery_cost(5.0, 100, "обычный")
        self.assertEqual(cost, 840)

    def test_weight_5_1(self):
        cost, _ = calculate_delivery_cost(5.1, 100, "обычный")
        self.assertEqual(cost, 840)

    def test_weight_10(self):
        cost, _ = calculate_delivery_cost(10.0, 100, "обычный")
        self.assertEqual(cost, 840)

    def test_weight_19_9(self):
        cost, _ = calculate_delivery_cost(19.9, 100, "обычный")
        self.assertEqual(cost, 840)

    def test_weight_20(self):
        cost, _ = calculate_delivery_cost(20.0, 100, "обычный")
        self.assertEqual(cost, 1050)

    def test_weight_30(self):
        cost, _ = calculate_delivery_cost(30.0, 100, "обычный")
        self.assertEqual(cost, 1050)

    def test_fragile(self):
        cost, _ = calculate_delivery_cost(1.0, 100, "хрупкий")
        self.assertEqual(cost, 1000)

    def test_dangerous(self):
        cost, _ = calculate_delivery_cost(1.0, 100, "опасный")
        self.assertEqual(cost, 1700)

    def test_fragile_heavy(self):
        cost, _ = calculate_delivery_cost(10.0, 100, "хрупкий")
        self.assertEqual(cost, 1140)

    def test_express_expensive(self):
        normal, _ = calculate_delivery_cost(1.0, 100, "обычный", False)
        express, _ = calculate_delivery_cost(1.0, 100, "обычный", True)
        self.assertTrue(express > normal)

    def test_express_cost(self):
        normal, _ = calculate_delivery_cost(1.0, 100, "обычный", False)
        express, _ = calculate_delivery_cost(1.0, 100, "обычный", True)
        self.assertEqual(express, int(normal * 1.5))

    def test_express_fragile(self):
        cost, _ = calculate_delivery_cost(1.0, 100, "хрупкий", True)
        self.assertEqual(cost, 1500)

    def test_date_short(self):
        _, date = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertEqual(date, "2026-09-04")

    def test_date_500(self):
        _, date = calculate_delivery_cost(1.0, 500, "обычный")
        self.assertEqual(date, "2026-09-04")

    def test_date_501(self):
        _, date = calculate_delivery_cost(1.0, 501, "обычный")
        self.assertEqual(date, "2026-09-05")

    def test_date_999(self):
        _, date = calculate_delivery_cost(1.0, 999, "обычный")
        self.assertEqual(date, "2026-09-05")

    def test_date_1000(self):
        _, date = calculate_delivery_cost(1.0, 1000, "обычный")
        self.assertEqual(date, "2026-09-05")

    def test_express_date_short(self):
        _, date = calculate_delivery_cost(1.0, 100, "обычный", True)
        self.assertEqual(date, "2026-09-04")

    def test_express_date_2000(self):
        _, date = calculate_delivery_cost(1.0, 2000, "обычный", True)
        self.assertEqual(date, "2026-09-05")

    def test_date_max(self):
        _, date = calculate_delivery_cost(1.0, 5000, "обычный")
        self.assertEqual(date, "2026-09-13")

    def test_error_returns_zeros(self):
        cost, date = calculate_delivery_cost(-5, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")


class TestBigScenario(unittest.TestCase):

    def test_heavy_dangerous_express(self):
        cost, date = calculate_delivery_cost(25.0, 1500, "опасный", True)
        base = 200 + 1500 * 5
        base = int(base * 1.5) + 1000
        expected = int(base * 1.5)
        self.assertEqual(cost, expected)

    def test_ok_with_all_options(self):
        cost, date = calculate_delivery_cost(10.0, 1000, "хрупкий", True)
        base = 200 + 1000 * 5
        base = int(base * 1.2) + 300
        expected = int(base * 1.5)
        self.assertEqual(cost, expected)
        self.assertEqual(date, "2026-09-04")


if __name__ == "__main__":
    unittest.main()