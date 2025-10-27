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

    def update_client(self, client: Client):
        client_dict = {
            "name": client.name,
            "phone": client.phone,
            "cpf": client.cpf
        }
        response = self._client.table('clients').update(
            client_dict).eq('id', client.id).execute()
        return response

    def delete_client(self, client_id: int):
        try:
            self._client.table('reservations').delete().eq('client_id', client_id).execute()
        except Exception as e:
            print(f"Erro ao limpar reservas do cliente {client_id}: {e}")
            raise e

        response = self._client.table(
            'clients').delete().eq('id', client_id).execute()

        return response