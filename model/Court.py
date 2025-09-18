from model.exceptions import FormValidationException
from datetime import time

class Court:
    def __init__(self, id: int, name: str, court_type: str, description: str, capacity: int, price_per_hour: float, start_hour: str, end_hour: str):
        self.__id = id
        self.name = name
        self.court_type = court_type
        self.description = description
        self.capacity = capacity
        self.price_per_hour = price_per_hour
        self.start_hour = start_hour
        self.end_hour = end_hour

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def court_type(self) -> str:
        return self.__court_type

    @property
    def description(self) -> str:
        return self.__description

    @property
    def capacity(self) -> int:
        return self.__capacity

    @property
    def price_per_hour(self) -> float:
        return self.__price_per_hour

    @property
    def start_hour(self) -> str:
        return self.__start_hour

    @property
    def end_hour(self) -> str:
        return self.__end_hour

    @id.setter
    def id(self, id: int):
        if not isinstance(id, int):
            raise FormValidationException("O ID deve ser um número inteiro.")
        self.__id = id

    @name.setter
    def name(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise FormValidationException("O Nome não pode ser vazio.")
        self.__name = name.strip()

    @court_type.setter
    def court_type(self, court_type: str):
        if not isinstance(court_type, str) or not court_type.strip():
            raise FormValidationException("O Tipo deve ser uma string e não pode ser vazio.")
        self.__court_type = court_type.strip()

    @description.setter
    def description(self, description: str):
        if not isinstance(description, str):
            raise FormValidationException("A Descrição deve ser uma string.")
        self.__description = description

    @price_per_hour.setter
    def price_per_hour(self, price: float):
        try:
            price = float(price)
        except ValueError:
            raise FormValidationException("O Preço por Hora deve ser um número válido.")
        if price < 0:
            raise FormValidationException("O Preço por Hora não pode ser negativo.")
        self.__price_per_hour = price

    @capacity.setter
    def capacity(self, capacity: int):
        try:
            capacity = int(capacity)
        except ValueError:
            raise FormValidationException("A Capacidade deve ser um número inteiro válido.")
        if capacity <= 0:
            raise FormValidationException("A Capacidade deve ser um número positivo.")
        self.__capacity = capacity

    @start_hour.setter
    def start_hour(self, start_hour: str):
        self.__start_hour = start_hour


    @end_hour.setter
    def end_hour(self, end_hour: str):
        start_time = time(int(self.__start_hour[:2]))
        end_time = time(int(end_hour[:2]))
        if start_time >= end_time:
            raise FormValidationException("A Hora de Abertura deve ser anterior à Hora de Fechamento.")
        self.__end_hour = str(end_time)

    def __str__(self) -> str:
        return f"Quadra id={self.id} -> nome='{self.name}', tipo='{self.court_type}', preco_hora={self.price_per_hour})"
