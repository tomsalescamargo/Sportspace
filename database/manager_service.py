from database.supabase_client import SupabaseClient
from model.FixedCost import FixedCost


class ManagerService(SupabaseClient):

    def __init__(self, client):
        super().__init__(client)

    def create_fixed_cost(self, fc: FixedCost):
        fixed_cost = {
            "name": fc.name,
            "description": fc.description,
            "value": fc.value,
        }
        response = self._client.table(
            'fixed_costs').insert(fixed_cost).execute()
        return response
