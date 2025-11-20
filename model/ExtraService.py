from utils.exceptions import FormValidationException

class ExtraService:
    def __init__(self, id: int, service: str, value: float):
        self.__id = id
        self.service = service
        self.value = value

    @property
    def id(self) -> int:
        return self.__id

    @property
    def service(self) -> str:
        return self.__service

    @property
    def value(self) -> float:
        return self.__value

    @service.setter
    def service(self, service: str):
        if not isinstance(service, str) or not service.strip():
            raise FormValidationException("O nome do serviço não pode ser vazio.")
        self.__service = service.strip()

    @value.setter
    def value(self, value: float):
        try:
            val = float(value)
            if val < 0:
                raise ValueError
            self.__value = val
        except ValueError:
            raise FormValidationException("O valor deve ser um número positivo.")

    def __str__(self):
        return f"{self.service} (R$ {self.value:.2f})"