"""Модульные тесты для функции validate_password."""

import unittest

from src.password_validator import validate_password


class TestPasswordValidator(unittest.TestCase):

    # --- Позитивное тестирование ---
    def test_valid_latin(self):
        self.assertTrue(validate_password("SecurePass1!"))

    def test_valid_cyrillic(self):
        self.assertTrue(validate_password("ПарольТест9#"))

    # --- Анализ граничных значений длины (BVA) ---
    def test_length_7(self):
        self.assertFalse(validate_password("Aa1!aaa"))  # 7 символов

    def test_length_8(self):
        self.assertTrue(validate_password("Aa1!aaaa"))  # 8 символов

    def test_length_20(self):
        self.assertTrue(validate_password("Aa1!" + "a" * 16))  # 20 символов

    def test_length_21(self):
        self.assertFalse(validate_password("Aa1!" + "a" * 17))  # 21 символ

    # --- Классы эквивалентности (неполный состав) ---
    def test_missing_upper(self):
        self.assertFalse(validate_password("securepass1!"))

    def test_missing_lower(self):
        self.assertFalse(validate_password("SECUREPASS1!"))

    def test_missing_digit(self):
        self.assertFalse(validate_password("SecurePassword!"))

    def test_missing_special(self):
        self.assertFalse(validate_password("SecurePassword1"))

    def test_invalid_special_char(self):
        self.assertFalse(validate_password("SecurePass1_"))  # _ не входит в перечень

    # --- Тестирование исключительных ситуаций (ValueError - пробелы) ---
    def test_space_inside_raises_value_error(self):
        with self.assertRaises(ValueError):
            validate_password("Pass 1234!")

    def test_space_start_raises_value_error(self):
        with self.assertRaises(ValueError):
            validate_password(" Pass1234!")

    def test_space_end_raises_value_error(self):
        with self.assertRaises(ValueError):
            validate_password("Pass1234! ")

    # --- Тестирование исключительных ситуаций (TypeError - неверный тип) ---
    def test_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            validate_password(None)

    def test_int_raises_type_error(self):
        with self.assertRaises(TypeError):
            validate_password(12345678)

    def test_list_raises_type_error(self):
        with self.assertRaises(TypeError):
            validate_password(["P", "a", "s", "s", "1", "!"])