from database.supabase_client import SupabaseClient
from model.Court import Court


class CourtService(SupabaseClient):
    def __init__(self, client):
        super().__init__(client)

    def create_court(self, court: Court):
        court_dict = {
            "name": court.name,
            "court_type": court.court_type,
            "description": court.description,
            "capacity": court.capacity,
            "price_per_hour": court.price_per_hour,
            "start_hour": court.start_hour,
            "end_hour": court.end_hour,
        }
        response = self._client.table('courts').insert(court_dict).execute()
        return response

    def update_court(self, court: Court):
        court_dict = {
            "name": court.name,
            "court_type": court.court_type,
            "description": court.description,
            "capacity": court.capacity,
            "price_per_hour": court.price_per_hour,
            "start_hour": court.start_hour,
            "end_hour": court.end_hour,
        }
        response = (
            self._client.table('courts')
            .update(court_dict)
            .eq('id', court.id)
            .execute()
        )
        return response

    def delete_court(self, court_id: int):
        response = (
            self._client.table('courts')
            .delete()
            .eq('id', court_id)
            .execute()
        )
        return response
