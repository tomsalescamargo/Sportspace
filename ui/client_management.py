"""
Este módulo define a janela de gerenciamento de clientes.
"""
import FreeSimpleGUI as sg
from model.Client import Client
import ui.styles as styles
from database.supabase_client import db_client

def run_manage_clients():
    layout = [
        [sg.Text('Gerenciar Clientes', font=styles.HEADING_FONT, pad=styles.HEADING_PAD)],
        [sg.Column([
            [sg.Button('Cadastrar Novo Cliente', key='register_client', size=styles.BUTTON_SIZE,
                       pad=styles.BUTTON_PAD)],
            [sg.Button('Listar Clientes', key='list_clients', size=styles.BUTTON_SIZE, pad=styles.BUTTON_PAD)],
            [sg.Button('Voltar', key='back_to_main', size=styles.BUTTON_SIZE, pad=styles.BUTTON_PAD)]
        ], element_justification='center', expand_x=True)]
    ]

    window = sg.Window('Gerenciar Clientes', layout, element_justification='center', size=styles.DEFAULT_WINDOW_SIZE)

    next_window = 'back_to_main'
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'back_to_main'):
            break
        elif event == 'register_client':
            _run_register_client_form()
        elif event == 'list_clients':
            _run_list_clients_table()

    window.close()
    return next_window


def _run_register_client_form():
    layout = [
        [sg.Text('Cadastrar Novo Cliente', font=styles.HEADING_FONT)],
        [sg.Text('Nome Completo:', size=(15, 1)), sg.Input(key='name')],
        [sg.Text('Telefone:', size=(15, 1)), sg.Input(key='phone')],
        [sg.Text('CPF:', size=(15, 1)), sg.Input(key='cpf')],
        [sg.Button('Salvar'), sg.Cancel('Cancelar')]
    ]

    window = sg.Window('Cadastrar Cliente', layout, modal=True)
    event, values = window.read()
    window.close()

    if event == 'Salvar':
        try:
            new_client = Client(
                id=0,
                name=values['name'],
                phone=values['phone'],
                cpf=values['cpf']
            )

            db_client.create_client(new_client)
            sg.popup('Sucesso', 'Cliente cadastrado com sucesso!')
        except (ValueError, TypeError) as e:
            sg.popup('Erro de Validação', f'Ocorreu um erro ao validar os dados: {e}')
        except Exception as e:
            sg.popup('Erro no Banco de Dados', f'Ocorreu um erro ao salvar o cliente: {e}')


def _run_list_clients_table():
    clients = db_client.get_clients()

    if not clients:
        sg.popup('Nenhum cliente encontrado.')
        return

    table_data = []
    for client in clients:
        row = [client.id, client.name, client.phone, client.cpf]
        table_data.append(row)

    headings = ['ID', 'Nome', 'Telefone', 'CPF']

    layout = [
        [sg.Text('Lista de Clientes Cadastrados', font=styles.HEADING_FONT)],
        [sg.Table(values=table_data, headings=headings, auto_size_columns=False,
                  col_widths=[5, 30, 15, 15],
                  justification='left', num_rows=min(len(table_data), 20))],
        [sg.Button('OK')]
    ]

    window = sg.Window('Lista de Clientes', layout, modal=True)
    window.read()
    window.close()
