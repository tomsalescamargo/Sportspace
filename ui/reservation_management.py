"""
Este módulo define a janela de gerenciamento de reservas.
"""
import FreeSimpleGUI as sg
import ui.styles as styles
from database.reservation_handler import reservation_client
from model.Reservation import Reservation
from utils.enums import ReservationStatus
from datetime import datetime

from utils.exceptions import FormValidationException

def run_manage_reservations():
    """
    Cria e exibe a janela de gerenciamento de reservas.
    """
    layout = [
        [sg.Text('Gerenciar Reservas', font=styles.HEADING_FONT, pad=styles.HEADING_PAD)],
        [sg.Column([
            [sg.Button('Criar Reserva', key='create_reservation', **styles.main_button_style)],
            [sg.Button('Listar Reservas', key='list_reservations', **styles.main_button_style)],
            [sg.Button('Listar Reservas de um Cliente', key='list_reservations_by_client', **styles.main_button_style)],
            [sg.Button('Voltar', key='back_to_main', **styles.main_button_style)]
        ], element_justification='center', expand_x=True)]
    ]

    window = sg.Window('Gerenciar Reservas', layout, **styles.main_window_style)

    next_window = 'back_to_main'
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'back_to_main'):
            break
        elif event == 'create_reservation':
            _run_register_reservation_form()
        elif event == 'list_reservations':
            # _run_list_reservations_table()
            sg.popup('Funcionalidade ainda não implementada.')
        elif event == 'list_reservations_by_client':
            # _run_list_reservations_by_client_table()
            sg.popup('Funcionalidade ainda não implementada.')

    window.close()
    return next_window

def _run_register_reservation_form():
    """
    Cria e exibe o formulário de cadastro de nova reserva.
    """

    # Fazer a busca e setup dos dados no inicio para fazer tudo somente uma vez
    courts = reservation_client.get_courts()

    if not courts:
        sg.popup('Nenhuma quadra cadastrada. Cadastre uma quadra antes de criar uma reserva.')
        return

    clients = reservation_client.get_clients()

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
         sg.Input(key='date', size=(16, 1), readonly=True, disabled_readonly_background_color='white'), 
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
                    date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')

                    new_reservation = Reservation(
                        client_id=selected_client.id,
                        court_id=court_hash[values['court_name']],
                        date_time=date_time,
                        status=ReservationStatus.AGUARDANDO_PAGAMENTO
                    )

                    # reservation client da throw em FormValidationException caso algo esteja errado
                    reservation_client.validate_reservation(new_reservation)
                    reservation_client.add_to_reservations(new_reservation)

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
                    current_table_data = [[client.id, client.name, client.cpf] for client in filtered_clients]
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
