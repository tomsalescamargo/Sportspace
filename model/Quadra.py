class Quadra:
    def __init__(self, id: int, nome: str, tipo: str, descricao: str, preco_hora: float):
        if not isinstance(id, int):
            raise TypeError("O ID deve ser um número inteiro.")
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("O Nome deve ser uma string e não pode ser vazio.")
        if not isinstance(tipo, str) or not tipo.strip():
            raise ValueError("O Tipo deve ser uma string e não pode ser vazio.")
        if not isinstance(descricao, str):
            raise TypeError("A Descrição deve ser uma string.")
        if not isinstance(preco_hora, (int, float)):
            raise TypeError("O Preço por Hora deve ser um número.")
        if preco_hora < 0:
            raise ValueError("O Preço por Hora não pode ser negativo.")

        self.__id = id
        self.__nome = nome.strip()
        self.__tipo = tipo.strip()
        self.__descricao = descricao
        self.__preco_hora = float(preco_hora)

    @property
    def id(self) -> int:
        return self.__id

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def tipo(self) -> str:
        return self.__tipo

    @property
    def descricao(self) -> str:
        return self.__descricao

    @property
    def preco_hora(self) -> float:
        return self.__preco_hora

    @id.setter
    def id(self, id: int):
        if not isinstance(id, int):
            raise TypeError("O ID deve ser um número inteiro.")
        self.__id = id

    @nome.setter
    def nome(self, nome: str):
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("O Nome deve ser uma string e não pode ser vazio.")
        self.__nome = nome.strip()

    @tipo.setter
    def tipo(self, tipo: str):
        if not isinstance(tipo, str) or not tipo.strip():
            raise ValueError("O Tipo deve ser uma string e não pode ser vazio.")
        self.__tipo = tipo.strip()

    @descricao.setter
    def descricao(self, descricao: str):
        if not isinstance(descricao, str):
            raise TypeError("A Descrição deve ser uma string.")
        self.__descricao = descricao

    @preco_hora.setter
    def preco_hora(self, preco: float):
        if not isinstance(preco, (int, float)):
            raise TypeError("O Preço por Hora deve ser um número.")
        if preco < 0:
            raise ValueError("O Preço por Hora não pode ser negativo.")
        self.__preco_hora = float(preco)

    def __str__(self) -> str:
        return f"Quadra id={self.id} -> nome='{self.nome}', tipo='{self.tipo}', preco_hora={self.preco_hora})"