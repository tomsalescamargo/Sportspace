"""
Este módulo define a janela de gerenciamento de quadras.
"""
import FreeSimpleGUI as sg
from model.Court import Court
import ui.styles as styles
from database.supabase_client import db_client

#TODO: validação correta de horas e atributos (para todos os modelos)

def run_manage_courts():
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
            _run_register_court_form()
        elif event == 'list_courts':
            _run_list_courts_table()
            
    window.close()
    return next_window

def _run_register_court_form():
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
            price_per_hour = float(values['price_per_hour'])
            capacity = int(values['capacity'])
   
            new_court = Court(
                id=0,
                name=values['name'],
                court_type=values['court_type'],
                description=values['description'],
                capacity=capacity,
                price_per_hour=price_per_hour,
                start_hour=values['start_hour'],
                end_hour=values['end_hour'],
            )
            
            db_client.create_court(new_court)
            sg.popup('Sucesso', 'Quadra cadastrada com sucesso!')
        except (ValueError, TypeError) as e:
            sg.popup('Erro ao cadastrar quadra: ', e)

def _run_list_courts_table():
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
