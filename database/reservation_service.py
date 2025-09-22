from database.supabase_client import SupabaseClient
from model.Reservation import Reservation


class ReservationService(SupabaseClient):

    def __init__(self, client):
        super().__init__(client)

    def validate_reservation(self, reservation: Reservation):
        return False, "placeholder"

    def add_to_reservations(self, reservation: Reservation):
        pass