import datetime


def calculate_delivery_cost(weight, distance, package_type, is_express=False):
    # проверка границ
    if weight < 0.1 or weight > 50.0 or distance < 1 or distance > 5000:
        return -1, "0000-00-00"

    if package_type not in ["обычный", "хрупкий", "опасный"]:
        return -1, "0000-00-00"

    # базовая цена
    total = 200 + distance * 5

    # коэффициент веса
    if 5.0 <= weight < 20.0:
        total = total * 1.2
    elif weight >= 20.0:
        total = total * 1.5

    # надбавка за тип
    if package_type == "хрупкий":
        total = total + 300
    elif package_type == "опасный":
        total = total + 1000

    # экспресс дороже
    if is_express:
        total = total * 1.5

    # дней на доставку
    days = distance // 500
    if days < 1:
        days = 1

    if distance % 500 != 0:
        days = days + 1

    if is_express:
        days = days // 2
        if days < 1:
            days = 1

    # дата отправки фиксирована
    start = datetime.date(2026, 9, 3)
    date = start + datetime.timedelta(days=days)

    return int(total), date.strftime("%Y-%m-%d")