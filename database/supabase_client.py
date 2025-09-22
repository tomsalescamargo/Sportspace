"""
Este módulo gerencia a comunicação com o banco de dados Supabase.
"""
from model.Client import Client
from model.Court import Court


class SupabaseClient:
    """
    Cliente principal da aplicação. Contém métodos comuns a todas as subclasses.
    """

    def __init__(self, client):
        self._client = client

    @property
    def client(self):
        return self._client

    def get_courts(self) -> list[Court]:
        response = self._client.table('courts').select('*').execute()
        courts = []
        for item in response.data:
            courts.append(Court(
                id=item['id'],
                name=item['name'],
                court_type=item['court_type'],
                description=item['description'],
                capacity=item['capacity'],
                price_per_hour=item['price_per_hour'],
                start_hour=item['start_hour'],
                end_hour=item['end_hour'],
            ))
        return courts

    def get_clients(self) -> list[Client]:
        response = self._client.table('clients').select(
            '*').order("name", desc=False).execute()
        clients = []
        for item in response.data:
            clients.append(Client(
                id=item['id'],
                name=item['name'],
                phone=item['phone'],
                cpf=item['cpf']
            ))
        return clients
