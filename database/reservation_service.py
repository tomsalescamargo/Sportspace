from database.supabase_client import SupabaseClient
from model.Reservation import Reservation
from utils.exceptions import FormValidationException
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ReservationService(SupabaseClient):

    def __init__(self, client):
        super().__init__(client)

    def validate_reservation(self, reservation: Reservation):
        response = (
            self._client
            .table('courts')
            .select('*')
            .eq('id', reservation.court_id)
            .limit(1)
            .execute()
        )
        court = response.data[0]
        # check if reservation time is allowed
        start_time = datetime.strptime(court["start_hour"], "%H:%M:%S").time()
        end_time = datetime.strptime(court["end_hour"], "%H:%M:%S").time()
        reservation_time = reservation.date_time.time()

        if reservation_time < start_time or reservation_time > end_time:
            raise FormValidationException(f"Horário de reserva inválido. Para a quadra '{court['name']}', o horário deve estar entre {start_time} e {end_time}.")

        #check if there is already existing reservation
        existing_reservation = (
            self._client
            .table('reservations')
            .select('*')
            .eq('court_id', reservation.court_id)
            .eq('date_time', reservation.date_time)
            .limit(1)
            .execute()
        )

        if existing_reservation.data:
            raise FormValidationException(f"Ja existe uma reserva para a quadra '{court['id']}' no horário {reservation.date_time}")


    def create_reservation(self, reservation: Reservation):
        reservation_dict = {
            "client_id": reservation.client_id,
            "court_id": reservation.court_id,
            "date_time": str(reservation.date_time),
            "status": reservation.status.value
        }

        response = self._client.table('reservations').insert(reservation_dict).execute()
        return response

    def get_reservations(self):
        response = self._client.table('reservations').select('*, clients(name), courts(name)').execute()
        return response.data

    def get_reservations_by_client(self, client_id):
        response = (
            self._client
            .table('reservations')
            .select('*, clients(name), courts(name)')
            .eq('client_id', client_id)
            .order('date_time', desc=True)
            .execute()
        )
        return response.data

    def update_reservation(self, reservation_id, reservation):
        reservation_dict = {
            "client_id": reservation.client_id,
            "court_id": reservation.court_id,
            "date_time": str(reservation.date_time),
            "status": reservation.status
        }

        response = self._client.table('reservations').update(reservation_dict).eq('id', reservation_id).execute()
        return response

    def delete_reservation(self, reservation_id):
        response = self._client.table('reservations').delete().eq('id', reservation_id).execute()
        return response

    def get_reservations_by_court_and_date(self, court_id, date_str):
        """
        Busca reservas de uma quadra em um dia específico.
        date_str formato esperado: 'YYYY-MM-DD'
        """
        start_dt = f"{date_str}T00:00:00"
        end_dt = f"{date_str}T23:59:59"

        response = (
            self._client
            .table('reservations')
            .select('*, clients(name)')
            .eq('court_id', court_id)
            .gte('date_time', start_dt)
            .lte('date_time', end_dt)
            .execute()
        )
        return response.data
