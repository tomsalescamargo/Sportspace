"""
Este módulo define a janela de gerenciamento de reservas.
"""
import FreeSimpleGUI as sg
import ui.styles as styles
from model.Reservation import Reservation
from utils.enums import ReservationStatus
from datetime import datetime

from utils.exceptions import FormValidationException


def run_manage_reservations(reservation_service):
    """
    Cria e exibe a janela de gerenciamento de reservas.
    """
    layout = [
        [sg.Text('Gerenciar Reservas', font=styles.HEADING_FONT,
                 pad=styles.HEADING_PAD)],
        [sg.Column([
            [sg.Button('Criar Reserva', key='create_reservation',
                       **styles.main_button_style)],
            [sg.Button('Listar Reservas', key='list_reservations',
                       **styles.main_button_style)],
            [sg.Button('Voltar', key='back_to_main',
                       **styles.main_button_style)]
        ], element_justification='center', expand_x=True)]
    ]

    window = sg.Window('Gerenciar Reservas', layout,
                       **styles.main_window_style)

    next_window = 'back_to_main'
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'back_to_main'):
            break
        elif event == 'create_reservation':
            _run_register_reservation_form(reservation_service)
        elif event == 'list_reservations':
            _run_list_reservations_table(reservation_service)

    window.close()
    return next_window


def _run_register_reservation_form(reservation_service):
    """
    Cria e exibe o formulário de cadastro de nova reserva.
    """

    # Fazer a busca e setup dos dados no inicio para fazer tudo somente uma vez
    courts = reservation_service.get_courts()

    if not courts:
        sg.popup(
            'Nenhuma quadra cadastrada. Cadastre uma quadra antes de criar uma reserva.')
        return

    clients = reservation_service.get_clients()

    if not clients:
        sg.popup('Nenhum cliente cadastrado.')
        return

    court_hash = {court.name: court.id for court in courts}
    court_names = list(court_hash.keys())
    hours = [f'{h:02d}:00' for h in range(24)]

    selected_client = None

    layout = [
        [sg.Text('Cadastrar Nova Reserva', font=styles.HEADING_FONT)],
        [sg.Text('Quadra:', size=styles.INPUT_LABEL_SIZE),
         sg.Combo(court_names, key='court_name', default_value=court_names[0],
                  readonly=True, size=(30, 1))],
        [sg.Text('Cliente:', size=styles.INPUT_LABEL_SIZE),
         sg.Text('Nenhum selecionado', key='-CLIENT_NAME-'),
         sg.Button('Buscar', **styles.form_button_style)],

        [sg.Text('Data:', size=styles.INPUT_LABEL_SIZE),
         sg.Input(key='date', size=(16, 1), readonly=True,
                  disabled_readonly_background_color='white'),
         sg.CalendarButton('Selecionar', target='date', format='%Y-%m-%d', **styles.form_button_style)],
        [sg.Text('Hora:', size=styles.INPUT_LABEL_SIZE),
         sg.Combo(hours, key='time', default_value=hours[0], readonly=True, size=(10, 1))],
        [sg.Push(), sg.Button('Salvar', **styles.form_button_style),
         sg.Cancel('Cancelar', **styles.form_button_style)]
    ]

    window = sg.Window('Cadastrar Reserva', layout, modal=True)

    try:
        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Cancelar'):
                break

            # buscar cliente
            if event == 'Buscar':
                client = _run_client_search_window(clients)
                if client:
                    selected_client = client
                    window['-CLIENT_NAME-'].update(client.name)

            if event == 'Salvar':
                if not selected_client:
                    sg.popup('Erro', 'Nenhum cliente selecionado.')
                    continue

                if not values['date']:
                    sg.popup('Erro de Validação', 'A data não pode ser vazia.')
                    continue

                try:
                    date_time_str = f"{values['date']} {values['time']}"
                    date_time = datetime.strptime(
                        date_time_str, '%Y-%m-%d %H:%M')

                    new_reservation = Reservation(
                        client_id=selected_client.id,
                        court_id=court_hash[values['court_name']],
                        date_time=date_time,
                        status=ReservationStatus.AGUARDANDO_PAGAMENTO
                    )

                    # reservation client da throw em FormValidationException caso algo esteja errado
                    reservation_service.validate_reservation(new_reservation)
                    reservation_service.create_reservation(new_reservation)

                    sg.popup('Sucesso', 'Reserva cadastrada com sucesso!')
                    break
                except FormValidationException as e:
                    sg.popup('Erro ao validar reserva', e)
                except Exception as e:
                    sg.popup('Erro ao salvar', e)
                finally:
                    window.refresh()
    finally:
        window.close()


def _run_list_reservations_table(reservation_service):
    reservations = reservation_service.get_reservations()

    headings = ['ID', 'Cliente', 'Quadra', 'Data e Hora', 'Status']
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

    layout = [
        [sg.Text('Lista de Reservas', font=styles.HEADING_FONT)],
        [sg.Table(
            values=table_data,
            headings=headings,
            auto_size_columns=False,
            col_widths=[3, 20, 20, 15, 18],
            justification='left',
            num_rows=15,
            alternating_row_color='lightblue',
            key='-TABLE-',
            row_height=25,
            enable_events=True
        )],
        [sg.Button('Voltar', **styles.form_button_style),
         sg.Button('Editar', **styles.form_button_style),
         sg.Button('Pagamento', **styles.form_button_style),
         sg.Button('Serv. Extra', **styles.form_button_style)]
    ]

    window = sg.Window('Lista de Reservas', layout, modal=True)

    selected_reservation = None
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Voltar'):
            break
        
        if event == '-TABLE-':
            if values['-TABLE-']:
                selected_index = values['-TABLE-'][0]
                selected_reservation = reservations[selected_index]

        if event == 'Editar':
            if selected_reservation:
                _run_edit_reservation_form(reservation_service, selected_reservation)
                # Refresh the table after editing
                reservations = reservation_service.get_reservations()
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
                window['-TABLE-'].update(values=table_data)
            else:
                sg.popup('Por favor, selecione uma reserva para editar.')

    window.close()

def _run_edit_reservation_form(reservation_service, reservation):
    courts = reservation_service.get_courts()
    clients = reservation_service.get_clients()

    court_hash = {court.name: court.id for court in courts}
    court_names = list(court_hash.keys())

    client_hash = {client.name: client.id for client in clients}
    client_names = list(client_hash.keys())

    reservation_datetime = datetime.strptime(reservation['date_time'], '%Y-%m-%dT%H:%M:%S')

    hours = [f'{h:02d}:00' for h in range(24)]

    layout = [
        [sg.Text('Editar Reserva', font=styles.HEADING_FONT)],
        [sg.Text('Quadra:', size=styles.INPUT_LABEL_SIZE),
         sg.Combo(court_names, key='court_name', default_value=reservation['courts']['name'], readonly=True, size=(30, 1))],
        [sg.Text('Cliente:', size=styles.INPUT_LABEL_SIZE),
            sg.Combo(client_names, key='client_name', default_value=reservation['clients']['name'], readonly=True, size=(30, 1))],
        [sg.Text('Data:', size=styles.INPUT_LABEL_SIZE),
         sg.Input(key='date', size=(16, 1), readonly=True, default_text=reservation_datetime.strftime('%Y-%m-%d'),
                  disabled_readonly_background_color='white'),
         sg.CalendarButton('Selecionar', target='date', format='%Y-%m-%d', **styles.form_button_style)],
        [sg.Text('Hora:', size=styles.INPUT_LABEL_SIZE),
         sg.Combo(hours, key='time', default_value=reservation_datetime.strftime('%H:%M'), readonly=True, size=(10, 1))],
        [sg.Push(), sg.Button('Salvar', **styles.form_button_style),
         sg.Button('Excluir', **styles.form_button_style), sg.Cancel('Cancelar', **styles.form_button_style)]
    ]

    window = sg.Window('Editar Reserva', layout, modal=True)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Cancelar'):
            break

        if event == 'Salvar':
            try:
                date_time_str = f"{values['date']} {values['time']}"
                date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')

                updated_reservation = Reservation(
                    client_id = client_hash[values['client_name']],
                    court_id = court_hash[values['court_name']],
                    date_time = date_time,
                    status = reservation['status']
                )

                reservation_service.validate_reservation(updated_reservation)
                reservation_service.update_reservation(reservation['id'], updated_reservation)
                sg.popup('Sucesso', 'Reserva atualizada com sucesso!')
                break
            except FormValidationException as e:
                sg.popup('Erro de validação', e)
            except Exception as e:
                sg.popup('Erro ao salvar', e)

        if event == 'Excluir':
            if sg.popup_yes_no('Tem certeza que deseja excluir esta reserva?') == 'Yes':
                try:
                    reservation_service.delete_reservation(reservation['id'])
                    sg.popup('Sucesso', 'Reserva excluída com sucesso!')
                    break
                except Exception as e:
                    sg.popup('Erro ao excluir', e)

    window.close()

def _run_client_search_window(clients):
    """
    Cria e exibe uma janela de busca de clientes usando tabela.
    Retorna o cliente selecionado ou None.
    """

    headings = ['ID', 'Nome', 'CPF']
    table_data = [[client.id, client.name, client.cpf] for client in clients]

    # manter dados para busca
    original_clients = clients.copy()
    current_table_data = table_data.copy()

    layout = [
        [sg.Text('Buscar Cliente', font=styles.HEADING_FONT)],
        [sg.Text('Digite o nome do cliente:', size=(20, 1))],
        [sg.Input(key='-SEARCH-', enable_events=True, size=(40, 1))],
        [sg.Text('')],
        [sg.Table(
            values=current_table_data,
            headings=headings,
            key='-TABLE-',
            enable_events=True,
            auto_size_columns=False,
            col_widths=[8, 25, 18],
            justification='left',
            num_rows=12,
            alternating_row_color='lightblue',
            selected_row_colors=('white', 'blue'),
        )],
    ]

    window = sg.Window('Buscar Cliente', layout, modal=True, size=(500, 400))

    try:
        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Cancelar'):
                return None

            # busca em tempo real
            if event == '-SEARCH-':
                search_term = values['-SEARCH-'].lower().strip()

                if search_term:
                    # filtrar clientes por nome
                    filtered_clients = [
                        client for client in clients
                        if search_term in client.name.lower()
                    ]
                    current_table_data = [
                        [client.id, client.name, client.cpf] for client in filtered_clients]
                    original_clients = filtered_clients
                else:
                    # mostrar todos os clientes
                    current_table_data = table_data.copy()
                    original_clients = clients.copy()

                window['-TABLE-'].update(values=current_table_data)

            # retornamos o objecto Client
            if event == '-TABLE-':
                selected_rows = values['-TABLE-']
                if selected_rows:
                    selected_index = selected_rows[0]
                    return original_clients[selected_index]

    finally:
        window.close()
