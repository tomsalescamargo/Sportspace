"""
Este módulo gerencia a comunicação com o banco de dados Supabase.
"""
import os
from dotenv import load_dotenv
import supabase
from model.Client import Client
from model.Court import Court
from model.FixedCost import FixedCost

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

#TODO: sepa isso aqui vai ficar grande tbm, separar
class SupabaseClient:
    def __init__(self):
        self.client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

    def get_courts(self) -> list[Court]:
        response = self.client.table('courts').select('*').execute()
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

    def create_court(self, court: Court):
        """
        Cria uma quadra nova na tabela 'courts' do banco de dados.

        Args:
            court: Um objeto Court com os dados da quadra a ser criada.
        """
        court_dict = {
            "name": court.name,
            "court_type": court.court_type,
            "description": court.description,
            "capacity": court.capacity,
            "price_per_hour": court.price_per_hour,
            "start_hour": court.start_hour,
            "end_hour": court.end_hour,
        }
        response = self.client.table('courts').insert(court_dict).execute()
        return response

    #TODO: remover data daqui e do banco de dados. (tem q ficar por enquanto até o professor corrigir a entrega pq senao ele vai tentar registrar custo fixo e n vai bater com o banco)
    def create_fixed_cost(self, fc: FixedCost):
        fixed_cost = {
            "name": fc.name,
            "description": fc.description,
            "value" : fc.value,
            "date" : "2025-12-8"
        }
        response = self.client.table('fixedCosts').insert(fixed_cost).execute()
        return response

    def create_client(self, client: Client):
        client_dict = {
            "name": client.name,
            "phone": client.phone,
            "cpf": client.cpf
        }
        response = self.client.table('clients').insert(client_dict).execute()
        return response

    def get_clients(self) -> list[Client]:
        response = self.client.table('clients').select('*').execute()
        clients = []
        for item in response.data:
            clients.append(Client(
                id=item['id'],
                name=item['name'],
                phone=item['phone'],
                cpf=item['cpf']
            ))
        return clients

    def update_client(self, client_id: int, data_to_update: dict):
        response = self.client.table('clients').update(data_to_update).eq('id', client_id).execute()
        return response

    def delete_client(self, client_id: int):
        response = self.client.table('clients').delete().eq('id', client_id).execute()
        return response

db_client = SupabaseClient()
