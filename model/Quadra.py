class Court:
    def __init__(self, id: int, name: str, court_type: str, description: str, capacity: int, price_per_hour: float, start_hour: str, end_hour: str):
        if not isinstance(id, int):
            raise TypeError("O ID deve ser um número inteiro.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("O Nome deve ser uma string e não pode ser vazio.")
        if not isinstance(court_type, str) or not court_type.strip():
            raise ValueError("O Tipo deve ser uma string e não pode ser vazio.")
        if not isinstance(description, str):
            raise TypeError("A Descrição deve ser uma string.")
        if not isinstance(price_per_hour, (int, float)):
            raise TypeError("O Preço por Hora deve ser um número.")
        if price_per_hour < 0:
            raise ValueError("O Preço por Hora não pode ser negativo.")

        self.__id = id
        self.__name = name.strip()
        self.__court_type = court_type.strip()
        self.__description = description
        self.__capacity = capacity
        self.__price_per_hour = float(price_per_hour)
        self.__start_hour = start_hour
        self.__end_hour = end_hour

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
            raise TypeError("O ID deve ser um número inteiro.")
        self.__id = id

    @name.setter
    def name(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("O Nome deve ser uma string e não pode ser vazio.")
        self.__name = name.strip()

    @court_type.setter
    def court_type(self, court_type: str):
        if not isinstance(court_type, str) or not court_type.strip():
            raise ValueError("O Tipo deve ser uma string e não pode ser vazio.")
        self.__court_type = court_type.strip()

    @description.setter
    def description(self, description: str):
        if not isinstance(description, str):
            raise TypeError("A Descrição deve ser uma string.")
        self.__description = description

    @price_per_hour.setter
    def price_per_hour(self, price: float):
        if not isinstance(price, (int, float)):
            raise TypeError("O Preço por Hora deve ser um número.")
        if price < 0:
            raise ValueError("O Preço por Hora não pode ser negativo.")
        self.__price_per_hour = float(price)

    @capacity.setter
    def capacity(self, capacity: int):
        if not isinstance(capacity, int):
            raise TypeError("A Capacidade deve ser um número inteiro.")
        self.__capacity = capacity

    @start_hour.setter
    def start_hour(self, start_hour: str):
        self.__start_hour = start_hour

    @end_hour.setter
    def end_hour(self, end_hour: str):
        self.__end_hour = end_hour

    def __str__(self) -> str:
        return f"Quadra id={self.id} -> nome='{self.name}', tipo='{self.court_type}', preco_hora={self.price_per_hour})"
