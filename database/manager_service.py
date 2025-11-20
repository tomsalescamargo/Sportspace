import calendar
from datetime import datetime

from database.supabase_client import SupabaseClient
from model.ExtraService import ExtraService
from model.FixedCost import FixedCost
from utils.enums import ReservationStatus


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

    def get_fixed_costs(self) -> list[dict]:
        response = (
            self._client
            .table('fixed_costs')
            .select('id,name,description,value')
            .order('name', desc=False)
            .execute()
        )
        return response.data or []

    def delete_fixed_cost(self, fixed_cost_id: int):
        return (
            self._client
            .table('fixed_costs')
            .delete()
            .eq('id', fixed_cost_id)
            .execute()
        )

    def get_court_occupancy_report(self):
        courts = self.get_courts()
        if not courts:
            return []

        usage_by_court = {court.id: 0 for court in courts}
        court_names = {court.id: court.name for court in courts}

        reservations_response = (
            self._client
            .table('reservations')
            .select('court_id,status,courts(name)')
            .execute()
        )

        reservations = reservations_response.data or []
        for reservation in reservations:
            if reservation.get('status') == ReservationStatus.CANCELADA.value:
                continue
            court_id = reservation.get('court_id')
            if court_id is None:
                continue

            # Cada reserva representa um bloco de uma hora, pois o sistema não armazena duração.
            usage_by_court[court_id] = usage_by_court.get(court_id, 0) + 1
            court = reservation.get('courts') or {}
            court_names[court_id] = court.get('name', court_names.get(court_id, f'Quadra {court_id}'))

        report_rows = []
        for court_id, court_name in court_names.items():
            report_rows.append({
                'court_id': court_id,
                'court_name': court_name,
                'hours_used': usage_by_court.get(court_id, 0)
            })

        report_rows.sort(key=lambda row: row['court_name'])
        return report_rows

    def get_monthly_revenue_report(self, year: int, month: int) -> dict:
        """Calcula o faturamento bruto e o total de custos fixos de um mês específico."""
        first_day = datetime(year, month, 1, 0, 0, 0)
        last_day = calendar.monthrange(year, month)[1]
        last_moment = datetime(year, month, last_day, 23, 59, 59)

        start_iso = first_day.isoformat()
        end_iso = last_moment.isoformat()

        reservations_response = (
            self._client
            .table('reservations')
            .select('date_time,status,courts(price_per_hour)')
            .gte('date_time', start_iso)
            .lte('date_time', end_iso)
            .execute()
        )

        paid_statuses = {
            ReservationStatus.CONFIRMADA.value,
            ReservationStatus.CONCLUIDA.value,
        }

        total_revenue = 0.0
        for reservation in reservations_response.data or []:
            if reservation.get('status') not in paid_statuses:
                continue
            court = reservation.get('courts') or {}
            price_per_hour = court.get('price_per_hour', 0)
            try:
                total_revenue += float(price_per_hour)
            except (TypeError, ValueError):
                continue

        # Custos fixos são tratados como recorrentes mensais; somamos todos os registros cadastrados.
        fixed_costs_records = self.get_fixed_costs()

        total_fixed_costs = 0.0
        fixed_costs_items = []
        for fixed_cost in fixed_costs_records:
            name = fixed_cost.get('name', 'N/D')
            description = fixed_cost.get('description', '')
            try:
                value = float(fixed_cost.get('value', 0))
            except (TypeError, ValueError):
                continue

            total_fixed_costs += value
            fixed_costs_items.append({
                'name': name,
                'description': description,
                'value': value,
            })

        net_result = total_revenue - total_fixed_costs

        return {
            'year': year,
            'month': month,
            'total_revenue': total_revenue,
            'total_fixed_costs': total_fixed_costs,
            'net_result': net_result,
            'fixed_costs': fixed_costs_items,
        }

    def create_extra_service(self, service: ExtraService):
        data = {
            "service": service.service,
            "value": service.value
        }
        return self._client.table('extra_services').insert(data).execute()

    def get_extra_services(self) -> list[ExtraService]:
        response = (
            self._client
            .table('extra_services')
            .select('*')
            .order('service')
            .execute()
        )
        services = []
        for item in response.data or []:
            services.append(ExtraService(
                id=item['id'],
                service=item['service'],
                value=item['value']
            ))
        return services

    def update_extra_service(self, service: ExtraService):
        data = {
            "service": service.service,
            "value": service.value
        }
        return (
            self._client
            .table('extra_services')
            .update(data)
            .eq('id', service.id)
            .execute()
        )

    def delete_extra_service(self, service_id: int):
        return (
            self._client
            .table('extra_services')
            .delete()
            .eq('id', service_id)
            .execute()
        )