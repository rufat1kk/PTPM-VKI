import re
import hashlib
import logging
import traceback
from datetime import datetime


logger = logging.getLogger("reg")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

file_handler = logging.FileHandler("../registration.log", encoding="utf-8")
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


black_list = ["admin", "root", "user", "test", "guest",
              "moderator", "support", "system", "qwerty", "password"]

salt = "my_secret_salt"


def mask_password(p):
    h = hashlib.sha256((salt + p).encode("utf-8")).hexdigest()
    return "hash:" + h[:10] + "..." + h[-4:]


def check_login(login):
    if login == "":
        return False, "Логин пустой"

    if re.match(r"^\+\d{1,3}-\d{3}-\d{3}-\d{4}$", login):
        if login.lower() in black_list:
            return False, "Логин из чёрного списка"
        return True, ""

    if re.match(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$", login):
        name = login.split("@")[0].lower()
        if name in black_list:
            return False, "Логин из чёрного списка"
        return True, ""

    if not re.match(r"^[A-Za-z0-9_]+$", login):
        return False, "Логин может содержать только латиницу, цифры и _"

    if len(login) < 5:
        return False, "Логин должен быть не короче 5 символов"

    if login.lower() in black_list:
        return False, "Логин из чёрного списка"

    return True, ""


def check_password(p):
    if p == "":
        return False, "Пароль пустой"

    if len(p) < 7:
        return False, "Пароль должен быть не короче 7 символов"

    if not re.match(r"^[А-Яа-яЁё0-9!@#$%^&*()_\-+=\[\]{};:'\",.<>/?\\|`~№]+$", p):
        return False, "Пароль может содержать только кириллицу, цифры и спецсимволы"

    if not re.search(r"[А-ЯЁ]", p):
        return False, "В пароле нужна хотя бы одна заглавная буква"

    if not re.search(r"[а-яё]", p):
        return False, "В пароле нужна хотя бы одна строчная буква"

    if not re.search(r"\d", p):
        return False, "В пароле нужна хотя бы одна цифра"

    if not re.search(r"[!@#$%^&*()_\-+=\[\]{};:'\",.<>/?\\|`~№]", p):
        return False, "В пароле нужен хотя бы один спецсимвол"

    return True, ""


def check_confirm(p, c):
    if c == "":
        return False, "Подтверждение пароля пустое"
    if p != c:
        return False, "Пароль и подтверждение не совпадают"
    return True, ""


def register(login, password, confirm):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_line = "time=" + now + " login=" + login \
               + " pwd=" + mask_password(password) \
               + " conf=" + mask_password(confirm)

    logger.debug("[ЗАПРОС] " + log_line)

    try:
        ok, err = check_login(login)
        if not ok:
            raise Exception(err)

        ok, err = check_password(password)
        if not ok:
            raise Exception(err)

        ok, err = check_confirm(password, confirm)
        if not ok:
            raise Exception(err)

        logger.info("[УСПЕХ] " + log_line + " -> регистрация выполнена")
        return True, ""

    except Exception as e:
        logger.warning("[ОШИБКА] " + log_line + " -> " + str(e))
        logger.debug("traceback:\n" + traceback.format_exc())
        return False, str(e)


if __name__ == "__main__":
    login = input("Логин: ").strip()
    pwd = input("Пароль: ")
    pwd2 = input("Повторите пароль: ")

    result, msg = register(login, pwd, pwd2)

    print()
    print("Результат:", result)
    print("Сообщение:", msg)