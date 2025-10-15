

def populate_reservations_table(reservations):
    table_data = []
    for res in reservations:
        client_name = res['clients']['name'] if res.get('clients') else 'N/A'
        court_name = res['courts']['name'] if res.get('courts') else 'N/A'
        table_data.append([
            res['id'],
            client_name,
            court_name,
            res['date_time'],
            res['status']
        ])
    return table_data
