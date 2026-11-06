import random


class UpgradeStrategy:
    """Strategy: формула расчёта шанса апгрейда.
    Классическая для сайтов-апгрейдеров:
    шанс = (цена входной / цена целевой) * 100 * house_edge
    """
    HOUSE_EDGE = 0.95  # комиссия сайта 5%

    @staticmethod
    def calculate_chance(input_price, output_price):
        if output_price <= 0:
            return 0
        chance = (input_price / output_price) * 100 * UpgradeStrategy.HOUSE_EDGE
        return min(max(round(chance, 2), 1), 99)  # от 1% до 99%

    @staticmethod
    def roll(chance):
        return random.random() * 100 < chance
