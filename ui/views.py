"""
Este módulo define as janelas (telas) da aplicação, utilizando a biblioteca FreeSimpleGUI.
Cada função `run_*` é responsável por uma janela específica e seu loop de eventos.
"""
import FreeSimpleGUI as sg
import os
from dotenv import load_dotenv
from supabase_client import SupabaseClient
from model.Court import Court
from model.FixedCost import FixedCost
from datetime import datetime
import ui.styles as styles

load_dotenv()

MANAGER_PASSWORD = os.getenv("MANAGER_PASSWORD")

#TODO: acho uma boa ideia separar essas views em diferentes arquivos, um pra cada 'modulo' pra que esse arquivo nao fique muito grande (ja ta meio grande)

def run_main_menu():
    """
    Cria e exibe a janela do menu principal.
    Retorna o nome da próxima janela a ser exibida.
    """
    layout = [
        [sg.Text('Sistema de Reserva de Quadras', font=styles.HEADING_FONT, pad=styles.HEADING_PAD)],
        [sg.Column([
            [sg.Button('Gerenciar Quadras', key='manage_courts', size=styles.BUTTON_SIZE, pad=styles.BUTTON_PAD)],
            [sg.Button('Gerenciar Clientes', key='manage_clients', size=styles.BUTTON_SIZE, pad=styles.BUTTON_PAD)],
            [sg.Button('Área do Gerente', key='manager_area', size=styles.BUTTON_SIZE, pad=styles.BUTTON_PAD)],
            [sg.Button('Sair', key='exit', size=styles.BUTTON_SIZE, pad=styles.BUTTON_PAD)]
        ], element_justification='center', expand_x=True)]
    ]

    window = sg.Window('Menu Principal', layout, element_justification='center', size=styles.DEFAULT_WINDOW_SIZE)
    
    next_window = 'exit'
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'exit'):
            break
        if event == 'manage_courts':
            next_window = 'manage_courts'
            break
        elif event == 'manage_clients':
            sg.popup('Funcionalidade ainda não implementada.')

            # next_window = 'manage_clients'
            # break
        elif event == 'manager_area':
            password = _run_password_prompt()
            if password == MANAGER_PASSWORD:
                next_window = 'manager_area'
                break
            elif password is not None:
                sg.popup("Senha incorreta.")
            

    window.close()
    return next_window

def run_manage_courts(db_client: SupabaseClient):
    """
    Cria e exibe a janela de gerenciamento de quadras.
    """
    layout = [
        [sg.Text('Gerenciar Quadras', font=styles.HEADING_FONT, pad=styles.HEADING_PAD)],
        [sg.Column([
            [sg.Button('Cadastrar Nova Quadra', key='register_court', size=styles.BUTTON_SIZE, pad=styles.BUTTON_PAD)],
            [sg.Button('Listar Quadras', key='list_courts', size=styles.BUTTON_SIZE, pad=styles.BUTTON_PAD)],
            [sg.Button('Voltar', key='back_to_main', size=styles.BUTTON_SIZE, pad=styles.BUTTON_PAD)]
        ], element_justification='center', expand_x=True)]
    ]

    window = sg.Window('Gerenciar Quadras', layout, element_justification='center', size=styles.DEFAULT_WINDOW_SIZE)

    next_window = 'back_to_main'
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'back_to_main'):
            break
        elif event == 'register_court':
            _run_register_court_form(db_client)
        elif event == 'list_courts':
            _run_list_courts_table(db_client)
            window.close()
    return next_window

def run_manager_area(db_client: SupabaseClient):
    """
    Cria e exibe a janela da área do gerente.
    """
    layout = [
        [sg.Text('Área do Gerente', font=styles.HEADING_FONT, pad=styles.HEADING_PAD)],
        [sg.Column([
            [sg.Button('Gerar Relatorios', key='generate_reports', size=styles.BUTTON_SIZE, pad=styles.BUTTON_PAD)],
            [sg.Button('Registrar Custo Fixo', key='register_fixed_cost', size=styles.BUTTON_SIZE, pad=styles.BUTTON_PAD)],
            [sg.Button('Voltar', key='back_to_main', size=styles.BUTTON_SIZE, pad=styles.BUTTON_PAD)]
        ], element_justification='center', expand_x=True)]
    ]
    
    window = sg.Window('Área do Gerente', layout, element_justification='center', size=styles.DEFAULT_WINDOW_SIZE)

    next_window = 'back_to_main'
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'back_to_main'):
            break
        elif event == 'generate_reports':
            sg.popup('Funcionalidade ainda não implementada.')
        elif event == 'register_fixed_cost':
            _run_register_fixed_cost_form(db_client)

    window.close()
    return next_window

def _run_password_prompt():
    """
    Cria e exibe um popup para solicitar a senha do gerente.
    Retorna a senha digitada ou None se o usuário cancelar.
    """
    layout = [
        [sg.Text('Digite a senha do Gerente:')],
        [sg.Input(key='-PASSWORD-', password_char='*')],
        [sg.Button('OK'), sg.Button('Cancelar')]
    ]
    window = sg.Window('Autenticação', layout, modal=True)
    event, values = window.read()
    window.close()
    if event == 'OK':
        return values['-PASSWORD-']
    return None

def _run_register_fixed_cost_form(db_client: SupabaseClient):
    """
    Cria e exibe o formulário de cadastro de novo custo fixo.
    """
    layout = [
        [sg.Text('Registrar Novo Custo Fixo', font=styles.HEADING_FONT)],
        [sg.Text('Nome:', size=(15, 1)), sg.Input(key='name')],
        [sg.Text('Descrição:', size=(15, 1)), sg.Input(key='description')],
        [sg.Text('Valor:', size=(15, 1)), sg.Input(key='value')],
        [sg.Text('Data:', size=(15, 1)), sg.Input(key='date', size=(20, 1)), sg.CalendarButton('Selecionar Data', target='date', format='%Y-%m-%d')],
        [sg.Button('Salvar'), sg.Cancel('Cancelar')]
    ]

    window = sg.Window('Registrar Custo Fixo', layout, modal=True)
    event, values = window.read()
    window.close()

    if event == 'Salvar':
        try:
            fixed_cost = FixedCost(
                description=values['description'],
                name=values['name'],
                value=float(values['value']),
                date=datetime.strptime(values['date'], '%Y-%m-%d').date()
            )
            db_client.create_fixed_cost(fixed_cost)
            sg.popup('Sucesso', f'Custo fixo registrado com sucesso!')
        except Exception as e:
            sg.popup('Erro', f'Ocorreu um erro ao registrar o custo fixo: {e}')

# funcoes prefixadas com _ nao navegam, sao internas
def _run_register_court_form(db_client: SupabaseClient):
    """
    Cria e exibe o formulário de cadastro de nova quadra.
    """
    layout = [
        [sg.Text('Cadastrar Nova Quadra', font=styles.HEADING_FONT)],
        [sg.Text('Nome:', size=(15, 1)), sg.Input(key='name')],
        [sg.Text('Tipo:', size=(15, 1)), sg.Input(key='court_type')],
        [sg.Text('Descrição:', size=(15, 1)), sg.Multiline(key='description', size=(35, 3))],
        [sg.Text('Capacidade:', size=(15, 1)), sg.Input(key='capacity', size=(5,1))],
        [sg.Text('Preço/Hora:', size=(15, 1)), sg.Input(key='price_per_hour', size=(15,1))],
        [sg.Text('Hora de Abertura:', size=(15, 1)), sg.Input(key='start_hour', size=(5,1))],
        [sg.Text('Hora de Fechamento:', size=(15, 1)), sg.Input(key='end_hour', size=(5,1))],
        [sg.Button('Salvar'), sg.Cancel('Cancelar')]
    ]

    window = sg.Window('Cadastrar Quadra', layout, modal=True)
    event, values = window.read()
    window.close()

    if event == 'Salvar':
        try:
            price = float(values['price_per_hour']) or None
            capacity = int(values['capacity']) or None
            start_hour = f"{int(values['start_hour']):02d}:00:00" or None
            end_hour = f"{int(values['end_hour']):02d}:00:00" or None
            
            new_court = Court(
                id=0,
                name=values['name'],
                court_type=values['court_type'],
                description=values['description'],
                capacity=values['capacity'],
                price_per_hour=values['price'],
                start_hour=values['start_hour'],
                end_hour=values['end_hour'],
            )
            
            db_client.create_court(new_court)
            sg.popup('Sucesso', 'Quadra cadastrada com sucesso!')
        except (ValueError, TypeError) as e:
            sg.popup('Erro ao cadastrar quadra: ', e)

# funcoes prefixadas com _ nao navegam, sao internas
def _run_list_courts_table(db_client: SupabaseClient):
    """
    Cria e exibe uma tabela com a lista de quadras cadastradas.
    """
    courts = db_client.get_courts()
    
    if not courts:
        sg.popup('Nenhuma quadra encontrada.')
        return

    table_data = []
    for court in courts:
        row = [
            court.id, court.name, court.court_type, court.description, 
            court.capacity, f'R$ {court.price_per_hour:.2f}', 
            court.start_hour, court.end_hour
        ]
        table_data.append(row)

    headings = ['ID', 'Nome', 'Tipo', 'Descrição', 'Capacidade', 'Preço/Hora', 'Abertura', 'Fechamento']
    
    layout = [
        [sg.Text('Lista de Quadras Cadastradas', font=styles.HEADING_FONT)],
        [sg.Table(values=table_data, headings=headings, auto_size_columns=False, 
                  col_widths=[5, 20, 15, 20, 10, 10, 10, 10], 
                  justification='left', num_rows=min(len(table_data), 20))],
        [sg.Button('OK')]
    ]

    window = sg.Window('Lista de Quadras', layout, modal=True)
    window.read()
    window.close()
