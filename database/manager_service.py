from database.supabase_client import SupabaseClient
from model.FixedCost import FixedCost


class ManagerService(SupabaseClient):

    def __init__(self, client):
        super().__init__(client)

    # TODO: remover data daqui e do banco de dados. (tem q ficar por enquanto até o professor corrigir a entrega pq senao ele vai tentar registrar custo fixo e n vai bater com o banco)
    def create_fixed_cost(self, fc: FixedCost):
        fixed_cost = {
            "name": fc.name,
            "description": fc.description,
            "value": fc.value,
            "date": "2025-12-8"
        }
        response = self._client.table(
            'fixedCosts').insert(fixed_cost).execute()
        return response