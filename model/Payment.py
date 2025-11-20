from utils.exceptions import FormValidationException
from datetime import datetime

class Payment:
    def __init__(self, reservation_id: int, method: str, value: float, date: str = None):
        self.reservation_id = reservation_id
        self.method = method
        self.value = value
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")

    @property
    def value(self) -> float:
        return self.__value

    @value.setter
    def value(self, value: float):
        try:
            val = float(value)
            if val <= 0:
                raise ValueError
            self.__value = val
        except ValueError:
            raise FormValidationException("O valor do pagamento deve ser positivo.")