import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from delivery import calculate_delivery_cost


class TestDeliveryValidation(unittest.TestCase):
    """Проверка входных данных и границ."""

    def test_weight_below_minimum_returns_error(self):
        cost, date = calculate_delivery_cost(0.05, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_weight_above_maximum_returns_error(self):
        cost, date = calculate_delivery_cost(50.1, 100, "обычный")
        self.assertEqual(cost, -1)

    def test_weight_at_minimum_boundary_is_accepted(self):
        cost, date = calculate_delivery_cost(0.1, 100, "обычный")
        self.assertNotEqual(cost, -1)

    def test_weight_at_maximum_boundary_is_accepted(self):
        cost, date = calculate_delivery_cost(50.0, 100, "обычный")
        self.assertNotEqual(cost, -1)

    def test_distance_below_minimum_returns_error(self):
        cost, date = calculate_delivery_cost(1.0, 0, "обычный")
        self.assertEqual(cost, -1)

    def test_distance_above_maximum_returns_error(self):
        cost, date = calculate_delivery_cost(1.0, 5001, "обычный")
        self.assertEqual(cost, -1)

    def test_distance_at_maximum_boundary_is_accepted(self):
        cost, date = calculate_delivery_cost(1.0, 5000, "обычный")
        self.assertNotEqual(cost, -1)

    def test_invalid_package_type_returns_error(self):
        cost, date = calculate_delivery_cost(1.0, 100, "жидкий")
        self.assertEqual(cost, -1)

    def test_empty_package_type_returns_error(self):
        cost, date = calculate_delivery_cost(1.0, 100, "")
        self.assertEqual(cost, -1)


class TestDeliveryBaseCost(unittest.TestCase):
    """Базовая стоимость: 200 + distance * 5."""

    def test_base_cost_for_small_package(self):
        cost, _ = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertEqual(cost, 200 + 100 * 5)

    def test_base_cost_for_distance_one(self):
        cost, _ = calculate_delivery_cost(1.0, 1, "обычный")
        self.assertEqual(cost, 205)


class TestDeliveryWeightCoefficients(unittest.TestCase):
    """Весовые коэффициенты 1.2 (5–20) и 1.5 (>=20)."""

    def test_weight_below_5_has_no_coefficient(self):
        cost, _ = calculate_delivery_cost(4.9, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_weight_exactly_5_gets_coefficient(self):
        cost, _ = calculate_delivery_cost(5.0, 100, "обычный")
        self.assertEqual(int(700 * 1.2), cost)

    def test_weight_just_above_5_gets_coefficient(self):
        cost, _ = calculate_delivery_cost(5.1, 100, "обычный")
        self.assertEqual(int(700 * 1.2), cost)

    def test_weight_in_middle_range_gets_coefficient(self):
        cost, _ = calculate_delivery_cost(10.0, 100, "обычный")
        self.assertEqual(int(700 * 1.2), cost)

    def test_weight_just_below_20_gets_coefficient(self):
        cost, _ = calculate_delivery_cost(19.9, 100, "обычный")
        self.assertEqual(int(700 * 1.2), cost)

    def test_weight_exactly_20_gets_high_coefficient(self):
        cost, _ = calculate_delivery_cost(20.0, 100, "обычный")
        self.assertEqual(int(700 * 1.5), cost)

    def test_weight_above_20_gets_high_coefficient(self):
        cost, _ = calculate_delivery_cost(30.0, 100, "обычный")
        self.assertEqual(int(700 * 1.5), cost)


class TestDeliveryPackageTypeSurcharge(unittest.TestCase):
    """Надбавки: хрупкий +300, опасный +1000."""

    def test_fragile_adds_300(self):
        cost, _ = calculate_delivery_cost(1.0, 100, "хрупкий")
        self.assertEqual(cost, 700 + 300)

    def test_dangerous_adds_1000(self):
        cost, _ = calculate_delivery_cost(1.0, 100, "опасный")
        self.assertEqual(cost, 700 + 1000)

    def test_fragile_with_heavy_weight(self):
        cost, _ = calculate_delivery_cost(10.0, 100, "хрупкий")
        self.assertEqual(int(700 * 1.2) + 300, cost)


class TestDeliveryExpress(unittest.TestCase):
    """Экспресс дороже обычной доставки (коэффициент 1.5)."""

    def test_express_is_more_expensive_than_normal(self):
        normal, _ = calculate_delivery_cost(1.0, 100, "обычный", False)
        express, _ = calculate_delivery_cost(1.0, 100, "обычный", True)
        self.assertGreater(express, normal)

    def test_express_cost_coefficient(self):
        normal, _ = calculate_delivery_cost(1.0, 100, "обычный", False)
        express, _ = calculate_delivery_cost(1.0, 100, "обычный", True)
        self.assertEqual(express, int(normal * 1.5))

    def test_express_with_fragile(self):
        cost, _ = calculate_delivery_cost(1.0, 100, "хрупкий", True)
        self.assertEqual(int((700 + 300) * 1.5), cost)


class TestDeliveryDate(unittest.TestCase):
    """Дата отправки фиксирована: 2026-09-03."""

    def test_date_for_short_distance_is_next_day(self):
        _, date = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertEqual(date, "2026-09-04")

    def test_date_for_500km_is_next_day(self):
        _, date = calculate_delivery_cost(1.0, 500, "обычный")
        self.assertEqual(date, "2026-09-04")

    def test_date_for_501km_is_two_days(self):
        _, date = calculate_delivery_cost(1.0, 501, "обычный")
        self.assertEqual(date, "2026-09-05")

    def test_date_for_1000km_is_two_days(self):
        _, date = calculate_delivery_cost(1.0, 1000, "обычный")
        self.assertEqual(date, "2026-09-05")

    def test_date_for_999km_is_two_days(self):
        _, date = calculate_delivery_cost(1.0, 999, "обычный")
        self.assertEqual(date, "2026-09-05")

    def test_express_short_distance_minimum_one_day(self):
        _, date = calculate_delivery_cost(1.0, 100, "обычный", True)
        self.assertEqual(date, "2026-09-04")

    def test_express_long_distance(self):
        _, date = calculate_delivery_cost(1.0, 2000, "обычный", True)
        self.assertEqual(date, "2026-09-05")

    def test_date_for_max_distance(self):
        _, date = calculate_delivery_cost(1.0, 5000, "обычный")
        self.assertEqual(date, "2026-09-13")


class TestDeliveryIntegration(unittest.TestCase):
    """Комплексные сценарии."""

    def test_full_scenario_heavy_dangerous_express(self):
        cost, date = calculate_delivery_cost(25.0, 1500, "опасный", True)
        base = 200 + 1500 * 5
        base = int(base * 1.5) + 1000
        expected = int(base * 1.5)
        self.assertEqual(cost, expected)

    def test_error_returns_zero_date(self):
        cost, date = calculate_delivery_cost(-5, 100, "обычный")
        self.assertEqual((cost, date), (-1, "0000-00-00"))


if __name__ == "__main__":
    unittest.main()