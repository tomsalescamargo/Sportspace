from database.supabase_client import SupabaseClient
from model.Client import Client


class ClientService(SupabaseClient):

    def __init__(self, client):
        super().__init__(client)

    def create_client(self, client: Client):
        client_dict = {
            "name": client.name,
            "phone": client.phone,
            "cpf": client.cpf
        }
        response = self._client.table('clients').insert(client_dict).execute()
        return response

    def update_client(self, client_id: int, data_to_update: dict):
        response = self._client.table('clients').update(
            data_to_update).eq('id', client_id).execute()
        return response

    def delete_client(self, client_id: int):
        response = self._client.table(
            'clients').delete().eq('id', client_id).execute()
        return response