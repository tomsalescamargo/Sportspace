from datetime import datetime, timedelta
from utils.enums import ReservationStatus


def build_court_daily_schedule(court, reservations):
    """
    Gera a grade de horários de uma quadra para um dia,
    marcando reservas existentes.
    """
    start_hour = _parse_hour(court.start_hour)
    end_hour = _parse_hour(court.end_hour)

    # mapa hora -> reserva (considera qualquer status, mas usamos status para exibir)
    reservations_by_hour = {}
    for res in reservations:
        try:
            dt = datetime.fromisoformat(res['date_time'])
            reservations_by_hour[dt.hour] = res
        except Exception:
            continue

    schedule = []
    current = start_hour
    while current < end_hour:
        hour_label = current.strftime('%H:%M')
        res = reservations_by_hour.get(current.hour)
        if res:
            client_name = res['clients']['name'] if res.get('clients') else 'N/A'
            status = res.get('status', '')
            display_status = status
            try:
                display_status = ReservationStatus(status).value
            except Exception:
                pass
            schedule.append({
                'hour': hour_label,
                'status': 'Ocupado',
                'client_name': client_name,
                'reservation_status': display_status
            })
        else:
            schedule.append({
                'hour': hour_label,
                'status': 'Disponível',
                'client_name': '-',
                'reservation_status': '-'
            })
        current += timedelta(hours=1)

    return schedule


def _parse_hour(hour_str):
    # Aceita formatos "HH:MM" ou "HH:MM:SS"
    try:
        return datetime.strptime(hour_str, '%H:%M:%S')
    except ValueError:
        return datetime.strptime(hour_str, '%H:%M')
