import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from Laba2_Rufat import check_login, check_password, check_confirm, register, mask_password


class TestLogin(unittest.TestCase):

    def test_empty(self):
        ok, err = check_login("")
        self.assertFalse(ok)
        self.assertEqual(err, "Логин пустой")

    def test_ok(self):
        ok, err = check_login("ivan_01")
        self.assertTrue(ok)

    def test_short(self):
        ok, err = check_login("ab1")
        self.assertFalse(ok)
        self.assertIn("не короче 5", err)

    def test_cyrillic(self):
        ok, err = check_login("Иван01")
        self.assertFalse(ok)
        self.assertIn("латиницу", err)

    def test_bad_chars(self):
        ok, err = check_login("ivan!")
        self.assertFalse(ok)
        self.assertIn("латиницу", err)

    def test_blacklist_admin(self):
        ok, err = check_login("admin")
        self.assertFalse(ok)
        self.assertIn("чёрного списка", err)

    def test_blacklist_admin_upper(self):
        ok, err = check_login("ADMIN")
        self.assertFalse(ok)
        self.assertIn("чёрного списка", err)

    def test_blacklist_qwerty(self):
        ok, err = check_login("qwerty")
        self.assertFalse(ok)

    def test_phone_ok(self):
        ok, err = check_login("+7-123-456-7890")
        self.assertTrue(ok)

    def test_phone_bad(self):
        ok, err = check_login("+7-12-456-7890")
        self.assertFalse(ok)

    def test_email_ok(self):
        ok, err = check_login("user123@mail.ru")
        self.assertTrue(ok)

    def test_email_admin(self):
        ok, err = check_login("admin@mail.ru")
        self.assertFalse(ok)
        self.assertIn("чёрного списка", err)

    def test_email_bad(self):
        ok, err = check_login("user@")
        self.assertFalse(ok)

    def test_exactly_5(self):
        ok, err = check_login("abcde")
        self.assertTrue(ok)


class TestPassword(unittest.TestCase):

    def test_empty(self):
        ok, err = check_password("")
        self.assertFalse(ok)
        self.assertEqual(err, "Пароль пустой")

    def test_short(self):
        ok, err = check_password("Па1!")
        self.assertFalse(ok)
        self.assertIn("не короче 7", err)

    def test_no_upper(self):
        ok, err = check_password("пароль1!")
        self.assertFalse(ok)
        self.assertIn("заглавная", err)

    def test_no_lower(self):
        ok, err = check_password("ПАРОЛЬ1!")
        self.assertFalse(ok)
        self.assertIn("строчная", err)

    def test_no_digit(self):
        ok, err = check_password("Пароль!!")
        self.assertFalse(ok)
        self.assertIn("цифра", err)

    def test_no_special(self):
        ok, err = check_password("Пароль12")
        self.assertFalse(ok)
        self.assertIn("спецсимвол", err)

    def test_ok(self):
        ok, err = check_password("Пароль1!")
        self.assertTrue(ok)

    def test_latin(self):
        ok, err = check_password("Password1!")
        self.assertFalse(ok)

    def test_space(self):
        ok, err = check_password("Пароль 1!")
        self.assertFalse(ok)


class TestConfirm(unittest.TestCase):

    def test_empty(self):
        ok, err = check_confirm("Пароль1!", "")
        self.assertFalse(ok)
        self.assertIn("пустое", err)

    def test_mismatch(self):
        ok, err = check_confirm("Пароль1!", "Пароль2!")
        self.assertFalse(ok)
        self.assertIn("не совпадают", err)

    def test_ok(self):
        ok, err = check_confirm("Пароль1!", "Пароль1!")
        self.assertTrue(ok)


class TestRegister(unittest.TestCase):

    def test_ok(self):
        ok, err = register("ivan_01", "Пароль1!", "Пароль1!")
        self.assertTrue(ok)

    def test_bad_login(self):
        ok, err = register("ab", "Пароль1!", "Пароль1!")
        self.assertFalse(ok)

    def test_bad_password(self):
        ok, err = register("ivan_01", "short", "short")
        self.assertFalse(ok)

    def test_mismatch(self):
        ok, err = register("ivan_01", "Пароль1!", "Пароль2!")
        self.assertFalse(ok)


class TestMask(unittest.TestCase):

    def test_prefix(self):
        masked = mask_password("Пароль1!")
        self.assertTrue(masked.startswith("hash:"))

    def test_same_input(self):
        self.assertEqual(mask_password("abc"), mask_password("abc"))

    def test_diff_input(self):
        self.assertNotEqual(mask_password("abc"), mask_password("abd"))


if __name__ == "__main__":
    unittest.main()