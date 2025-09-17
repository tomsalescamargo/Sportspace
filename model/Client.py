from typing import List
from .Reservation import Reservation

class Client:
    def __init__(self, id: int, name: str, phone: str, cpf: str):
        if not isinstance(id, int):
            raise TypeError("O ID deve ser um número inteiro.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("O Nome deve ser uma string e não pode ser vazio.")
        if not isinstance(phone, str) or not phone.strip():
            raise ValueError("O Telefone deve ser uma string e não pode ser vazio.")
        if not isinstance(cpf, str):
            raise TypeError("O CPF deve ser uma string.")

        self.__id = id
        self.__name = name.strip()
        self.__phone = phone.strip()
        self.__cpf = cpf.strip()
        self.__reservations: List[Reservation] = []


    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def phone(self) -> str:
        return self.__phone

    @property
    def cpf(self) -> str:
        return self.__cpf

    @property
    def reservations(self) -> List[Reservation]:
        return self.__reservations

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

    @phone.setter
    def phone(self, phone: str):
        if not isinstance(phone, str) or not phone.strip():
            raise ValueError("O Telefone deve ser uma string e não pode ser vazio.")
        self.__phone = phone.strip()

    @cpf.setter
    def cpf(self, cpf: str):
        if not isinstance(cpf, str):
            raise TypeError("A CPF deve ser uma string.")
        self.__cpf = cpf

    @reservations.setter
    def reservations(self, reservations: List[Reservation]):
        self.__reservations = reservations


    def add_reservation(self, reservation: Reservation):
        if not isinstance(reservation, Reservation):
            raise TypeError("Apenas objetos da classe Reserva podem ser adicionados.")
        self.__reservations.append(reservation)

    def __str__(self) -> str:
        return f"Cliente(ID={self.id}, Nome='{self.nome}', Telefone='{self.telefone}', CPF='{self.cpf}')"