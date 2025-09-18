from model.exceptions import FormValidationException

class FixedCost:
    def __init__(self, name: str, description: str, value: float):
        self.name = name
        self.description = description
        self.value = value

    @property
    def name(self) -> str:
        return self.__name

    @property
    def description(self) -> str:
        return self.__description

    @property
    def value(self) -> float:
        return self.__value

    @name.setter
    def name(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise FormValidationException("O Nome não pode ser vazio.")
        self.__name = name.strip()

    @description.setter
    def description(self, description: str):
        if not isinstance(description, str) or not description.strip():
            raise FormValidationException("A Descrição não pode ser vazia.")
        self.__description = description.strip()

    @value.setter
    def value(self, value: float):
        try:
            value = float(value)
        except ValueError:
            raise FormValidationException("O Valor deve ser um número válido.")
        if value <= 0:
            raise FormValidationException("O Valor deve ser um número positivo.")
        self.__value = value

    def __str__(self) -> str:
        return f"Custo Fixo: {self.name}, Descrição: {self.description}, Valor: {self.value}"