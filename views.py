import FreeSimpleGUI as sg
from supabase_client import SupabaseClient
from model.Court import Court

#FIXME: talvez a gente possa criar um arquivo só com essas configs de estilo, como se fosse css
DEFAULT_WINDOW_SIZE = (800, 600)
BUTTON_SIZE = (25, 1)

def get_main_layout():
    return [
        [sg.Text('Sistema de Reserva de Quadras', font=('Helvetica', 18, 'bold'), pad=((0,0),(20,20)))],
        [sg.Column([
            [sg.Button('Gerenciar Quadras', key='manage_courts', size = BUTTON_SIZE)],
            [sg.Button('Gerenciar Clientes', key='manage_clients', size = BUTTON_SIZE)],
            [sg.Button('Sair', key='exit', size = BUTTON_SIZE)]
        ], element_justification='center', expand_x=True)]
    ]

def get_manage_courts_layout():
    return [
        [sg.Column([
            [sg.Text('Gerenciar Quadras', font=('Helvetica', 18, 'bold'), pad=((0,0),(20,20)))],
            [sg.Button('Cadastrar Nova Quadra', key='register_court', size = BUTTON_SIZE)],
            [sg.Button('Listar Quadras', key='list_courts', size = BUTTON_SIZE)],
            [sg.Button('Voltar', key='back_to_main', size = BUTTON_SIZE)]
        ], element_justification='center', expand_x=True)]

    ]

def register_court(supabase_client):
    layout = [
        [sg.Text('Cadastrar Nova Quadra', font=('Helvetica', 16))],
        [sg.Text('Nome:', size=(15, 1)), sg.Input(key='name')],
        [sg.Text('Tipo:', size=(15, 1)), sg.Input(key='court_type')],
        [sg.Text('Descrição:', size=(15, 1)), sg.Multiline(key='description', size=(35, 3))],
        [sg.Text('Capacidade:', size=(15, 1)), sg.Input(key='capacity', size=(5,1))],
        [sg.Text('Preço/Hora:', size=(15, 1)), sg.Input(key='price_per_hour', size=(15,1))],
        [sg.Text('Hora de Abertura:', size=(15, 1)), sg.Input(key='start_hour', size=(5,1))],
        [sg.Text('Hora de Fechamento:', size=(15, 1)), sg.Input(key='end_hour', size=(5,1))],
        [sg.Button('Salvar'), sg.Cancel('Cancelar')]
    ]

    window = sg.Window('Cadastrar Quadra', layout, modal=True, size=DEFAULT_WINDOW_SIZE)
    event, values = window.read()
    window.close()

    if event == 'Salvar':
        try:
            price = float(values['price_per_hour'])
            capacity = int(values['capacity'])
            start_hour = f"{int(values['start_hour']):02d}:00:00"
            end_hour = f"{int(values['end_hour']):02d}:00:00"
            new_court = Court(
                id=0,  # ID vai ser definido pelo banco de dados
                name=values['name'],
                court_type=values['court_type'],
                description=values['description'],
                capacity=capacity,
                price_per_hour=price,
                start_hour=start_hour,
                end_hour=end_hour,
            )
            supabase_client.create_court(new_court)
            sg.popup('Sucesso', 'Quadra cadastrada com sucesso!')
        except (ValueError, TypeError) as e:
            sg.popup('Erro', f'Ocorreu um erro ao cadastrar: {e}')

def list_courts(supabase_client):
    courts = supabase_client.get_courts()
    table_data = []
    for court in courts:
        row = [court.id, court.name, court.court_type, court.description, court.capacity, f'R$ {court.price_per_hour:.2f}', court.start_hour, court.end_hour]
        table_data.append(row)

    headings = ['ID', 'Nome', 'Tipo', 'Descrição', 'Capacidade', 'Preço/Hora', 'Abertura', 'Fechamento']
    layout = [
        [sg.Text('Lista de Quadras Cadastradas', font=('Helvetica', 16))],
        [sg.Table(values=table_data, headings=headings, auto_size_columns=False, col_widths=[5, 20, 15, 20, 10, 10, 10, 10], justification='left', num_rows=10)],
        [sg.Button('OK')]
    ]

    window = sg.Window('Lista de Quadras', layout, modal=True, size=DEFAULT_WINDOW_SIZE)
    window.read()
    window.close()
