# Функция округления dx, dy при перемещении.
# Её необходимость возникла при обработке коллизий со стенами для обеспечения скольжения и
# предупреждения застреваний игрока в стене.
def m_round(value: float) -> float:
    from decimal import Decimal, ROUND_DOWN

    result = Decimal(value)
    if value > 0:
        return float(result.quantize(Decimal('1.'), rounding=ROUND_DOWN))
    else:
        return float(result.quantize(Decimal('1.'), rounding=ROUND_DOWN))
