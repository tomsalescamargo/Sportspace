from database.supabase_client import SupabaseClient
from model.ExtraService import ExtraService
from model.Payment import Payment
from model.Reservation import Reservation
from utils.exceptions import FormValidationException
from utils.enums import ReservationStatus, PaymentMethod
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

    def add_payment(self, payment: Payment):
        data = {
            "reservation_id": payment.reservation_id,
            "method": payment.method,
            "value": payment.value,
            "date": payment.date
        }
        return self._client.table('payments').insert(data).execute()

    def get_available_extra_services(self) -> list[ExtraService]:
        """Busca o catálogo de serviços extras (tabela 'extra_services')"""
        response = self._client.table('extra_services').select('*').execute()
        services = []
        for item in response.data:
            services.append(ExtraService(
                id=item['id'],
                service=item['service'],
                value=item['value']
            ))
        return services

    def add_service_to_reservation(self, reservation_id: int, service_id: int, quantity: int):

        existing_item_response = (
            self._client.table('services_reservations')
            .select('*')
            .eq('reservation_id', reservation_id)
            .eq('service_id', service_id)
            .execute()
        )

        response = None

        if existing_item_response.data:
            item = existing_item_response.data[0]
            old_quantity = int(item['quantity'])
            new_total_quantity = old_quantity + quantity

            response = (
                self._client.table('services_reservations')
                .update({'quantity': new_total_quantity})
                .eq('reservation_id', reservation_id)
                .eq('service_id', service_id)
                .execute()
            )
        else:
            data = {
                "reservation_id": reservation_id,
                "service_id": service_id,
                "quantity": quantity
            }
            response = self._client.table('services_reservations').insert(data).execute()

        res_info = (
            self._client.table('reservations')
            .select('status')
            .eq('id', reservation_id)
            .single()
            .execute()
        )

        if res_info.data:
            current_status = res_info.data['status']
            if current_status == ReservationStatus.CONFIRMADA.value:
                self.update_status(reservation_id, ReservationStatus.AGUARDANDO_PAGAMENTO.value)

        return response

    def update_status(self, reservation_id: int, new_status: str):
        return (
            self._client.table('reservations')
            .update({'status': new_status})
            .eq('id', reservation_id)
            .execute()
        )

    def calculate_reservation_balance(self, reservation_id: int):
        res_response = (
            self._client.table('reservations')
            .select('court_id, courts(price_per_hour)')
            .eq('id', reservation_id)
            .single()
            .execute()
        )
        reservation_data = res_response.data

        court_price = float(reservation_data['courts']['price_per_hour'])

        services_response = (
            self._client.table('services_reservations')
            .select('quantity, extra_services(value)')
            .eq('reservation_id', reservation_id)
            .execute()
        )

        services_total = 0.0
        for item in services_response.data:
            qty = int(item['quantity'])
            price = float(item['extra_services']['value'])
            services_total += qty * price

        payments_response = (
            self._client.table('payments')
            .select('value')
            .eq('reservation_id', reservation_id)
            .execute()
        )

        total_paid = sum(float(p['value']) for p in payments_response.data)

        total_cost = court_price + services_total
        remaining_balance = total_cost - total_paid

        return {
            "court_price": court_price,
            "services_total": services_total,
            "total_cost": total_cost,
            "total_paid": total_paid,
            "remaining_balance": max(0.0, remaining_balance)
        }

    def get_reservation_services(self, reservation_id: int):
        response = (
            self._client.table('services_reservations')
            .select('service_id, quantity, extra_services(service, value)')
            .eq('reservation_id', reservation_id)
            .execute()
        )
        return response.data or []

    def remove_service_from_reservation(self, reservation_id: int, service_id: int):
        return (
            self._client.table('services_reservations')
            .delete()
            .eq('reservation_id', reservation_id)
            .eq('service_id', service_id)
            .execute()
        )