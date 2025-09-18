from typing import List
from .Reservation import Reservation
from model.exceptions import FormValidationException

class Client:
    def __init__(self, id: int, name: str, phone: str, cpf: str):
        self.__id = id
        self.name = name
        self.phone = phone
        self.cpf = cpf
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
            raise FormValidationException("O ID deve ser um número inteiro.")
        self.__id = id

    @name.setter
    def name(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise FormValidationException("O Nome não pode ser vazio.")
        if any(char.isdigit() for char in name):
            raise FormValidationException("O Nome não pode conter números.")
        self.__name = name.strip()

    @phone.setter
    def phone(self, phone: str):
        if not isinstance(phone, str) or not phone.strip():
            raise FormValidationException("O Telefone não pode ser vazio.")
        if not phone.isdigit():
            raise FormValidationException("O Telefone deve conter apenas números.")
        self.__phone = phone.strip()

    @cpf.setter
    def cpf(self, cpf: str):
        if not isinstance(cpf, str) or not cpf.strip():
            raise FormValidationException("O CPF não pode ser vazio.")
        if not cpf.isdigit() or len(cpf) != 11:
            raise FormValidationException("O CPF deve conter exatamente 11 dígitos numéricos.")
        self.__cpf = cpf.strip()

    @reservations.setter
    def reservations(self, reservations: List[Reservation]):
        self.__reservations = reservations


    def add_reservation(self, reservation: Reservation):
        if not isinstance(reservation, Reservation):
            raise TypeError("Apenas objetos da classe Reserva podem ser adicionados.")
        self.__reservations.append(reservation)

    def __str__(self) -> str:
        return f"Cliente(ID={self.id}, Nome='{self.name}', Telefone='{self.phone}', CPF='{self.cpf}')"