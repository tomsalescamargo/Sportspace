from database.supabase_client import SupabaseClient, db_client

class ReservationClient(SupabaseClient):
    def __init__(self):
        self.client = db_client.client

    def validate_reservation(self, reservation):
        return False, "placeholder"

    def add_to_reservations(self, reservation):
        pass
reservation_client = ReservationClient()
