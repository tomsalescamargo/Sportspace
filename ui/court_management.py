"""
Este módulo define a janela de gerenciamento de quadras.
"""
import FreeSimpleGUI as sg
from model.Court import Court
import ui.styles as styles
from utils.enums import CourtType
from utils.exceptions import FormValidationException

# TODO: validação correta de horas e atributos (para todos os modelos)


def run_manage_courts(court_service):
    """
    Creates and displays the court management window.
    """
    layout = [
        [sg.Text('Gerenciar Quadras', font=styles.HEADING_FONT,
                 pad=styles.HEADING_PAD)],
        [sg.Column([
            [sg.Button('Cadastrar Nova Quadra', key='register_court',
                       **styles.main_button_style)],
            [sg.Button('Alterar Quadra', key='update_court',
                       **styles.main_button_style)],
            [sg.Button('Listar Quadras', key='list_courts',
                       **styles.main_button_style)],
            [sg.Button('Voltar', key='back_to_main',
                       **styles.main_button_style)]
        ], element_justification='center', expand_x=True)]
    ]

    window = sg.Window('Gerenciar Quadras', layout, **styles.main_window_style)

    next_window = 'back_to_main'
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'back_to_main'):
            break
        elif event == 'register_court':
            _run_court_form(court_service, None)
        elif event == 'update_court':
            _run_update_delete_court_flow(court_service)
        elif event == 'list_courts':
            _run_list_courts_table(court_service)

    window.close()
    return next_window


def _run_court_form(court_service, court_to_edit=None):
    """
    Creates and displays the court registration/edit form, depending on the action chosen by the user.
    """
    is_editing = court_to_edit is not None
    window_title = 'Editar Quadra' if is_editing else 'Cadastrar Nova Quadra'

    court_types = [court_type.value for court_type in CourtType]
    hours = [f'{h:02d}:00' for h in range(24)]

    if is_editing:
        default_values = {
            'name': court_to_edit.name,
            'court_type': court_to_edit.court_type,
            'description': court_to_edit.description,
            'capacity': court_to_edit.capacity,
            'price_per_hour': court_to_edit.price_per_hour,
            'start_hour': court_to_edit.start_hour,
            'end_hour': court_to_edit.end_hour,
        }
    else:
        default_values = {}

    layout = [
        [sg.Text(window_title, font=styles.HEADING_FONT)],
        [sg.Text('Nome:', size=styles.INPUT_LABEL_SIZE), sg.Input(
            key='name', size=(25, 1), default_text=default_values.get('name', ''))],
        [sg.Text('Tipo:', size=styles.INPUT_LABEL_SIZE), sg.Combo(court_types, key='court_type',
                                                                    default_value=default_values.get('court_type', court_types[0]), readonly=True, size=(10, 1))],
        [sg.Text('Descrição:', size=styles.INPUT_LABEL_SIZE), sg.Multiline(
            key='description', size=(35, 3), default_text=default_values.get('description', ''))],
        [sg.Text('Capacidade:', size=styles.INPUT_LABEL_SIZE), sg.Input(
            key='capacity', size=(5, 1), default_text=default_values.get('capacity', ''))],
        [sg.Text('Preço/Hora:', size=styles.INPUT_LABEL_SIZE), sg.Input(
            key='price_per_hour', size=(5, 1), default_text=default_values.get('price_per_hour', ''))],
        [sg.Text('Hora de Abertura:', size=styles.INPUT_LABEL_SIZE), sg.Combo(hours, key='start_hour', default_value=default_values.get('start_hour', hours[0]), readonly=True, size=(5, 1)),
            sg.Text('Hora de Fechamento:', size=(17, 1)), sg.Combo(hours, key='end_hour', default_value=default_values.get('end_hour', hours[0]), readonly=True, size=(5, 1))],
        [  
            sg.Push(), 
            sg.Button('Salvar', **styles.form_button_style),
            sg.Button('Excluir', button_color='red') if is_editing else sg.Text(),
            sg.Cancel('Cancelar', **styles.form_button_style)
        ]
    ]

    window = sg.Window(window_title, layout, modal=True)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Cancelar'):
            break

        if event == 'Salvar':
            try:

                if is_editing:
                    court_to_edit.name = values['name']
                    court_to_edit.court_type = values['court_type']
                    court_to_edit.description = values['description']
                    court_to_edit.capacity = values['capacity']
                    court_to_edit.price_per_hour = values['price_per_hour']
                    court_to_edit.start_hour = values['start_hour']
                    court_to_edit.end_hour = values['end_hour']

                    court_service.update_court(court_to_edit)
                    sg.popup('Quadra alterada com sucesso!')
                else:
                    new_court = Court(
                        id=0, #The ID will be generated by the database
                        name=values['name'],
                        court_type=values['court_type'],
                        description=values['description'],
                        capacity=values['capacity'],
                        price_per_hour=values['price_per_hour'],
                        start_hour=values['start_hour'],
                        end_hour=values['end_hour']
                    )
                    court_service.create_court(new_court)
                    sg.popup('Quadra cadastrada com sucesso!')

                break

            except FormValidationException as e:
                sg.popup('Dados inseridos inválidos', str(e))
            except Exception as e:
                sg.popup('Erro no Banco de Dados',
                         f'Ocorreu um erro ao salvar a quadra: {e}')

        if event == 'Excluir':
            if sg.popup_yes_no('Você tem CERTEZA que deseja excluir esta quadra? Esta ação não pode ser desfeita.', title='Confirmação de Exclusão') == 'Yes':
                try:
                    court_service.delete_court(court_to_edit.id)
                    sg.popup('Quadra excluída com sucesso!')
                    break
                except Exception as e:
                    sg.popup('Erro', f'Ocorreu um erro ao excluir a quadra: {e}')

    window.close()


def _run_update_delete_court_flow(court_service):
    """
    Executes the flow of selecting a court and then opening the form for editing or deletion
    """
    court_to_edit = _run_court_search_window(court_service)

    if court_to_edit:
        _run_court_form(court_service, court_to_edit)

def _run_court_search_window(court_service):
    """
    Creates and displays a court search window.
    Returns the selected court or None.
    """
    courts = court_service.get_courts()
    if not courts:
        sg.popup('Nenhuma quadra encontrada.')
        return None

    headings = ['ID', 'Nome', 'Tipo']
    table_data = [[c.id, c.name, c.court_type] for c in courts]

    layout = [
        [sg.Text('Selecione a Quadra', font=styles.HEADING_FONT)],
        [sg.Table(
            values=table_data,
            headings=headings, 
            key='-TABLE-',
            enable_events=True,
            auto_size_columns=False,
            col_widths=[8, 25, 18],
            justification='left',
            num_rows=12,
            selected_row_colors=('white', 'blue')
        )],
        [sg.Push(), sg.Button('Selecionar', **styles.form_button_style), sg.Cancel('Cancelar', **styles.form_button_style)]
    ]

    window = sg.Window('Buscar Quadra', layout, modal=True)
    selected_court = None

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Cancelar'):
            selected_court = None
            break

        if event == 'Selecionar':
            selected_rows = values['-TABLE-']
            if selected_rows:
                selected_index = selected_rows[0]
                selected_court = courts[selected_index]
                break
            else:
                sg.popup_error('Por favor, selecione uma quadra na tabela.')

    window.close()
    return selected_court


def _run_list_courts_table(court_service):
    """
    Creates and displays a table containing the list of registered courts.
    """
    courts = court_service.get_courts()

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

    headings = ['ID', 'Nome', 'Tipo', 'Descrição',
                'Capacidade', 'Preço/Hora', 'Abertura', 'Fechamento']

    layout = [
        [sg.Text('Lista de Quadras Cadastradas', font=styles.HEADING_FONT)],
        [sg.Table(values=table_data, headings=headings, auto_size_columns=False,
                  col_widths=[5, 20, 15, 20, 10, 10, 10, 10],
                  justification='left', num_rows=min(len(table_data), 20))],
        [sg.Button('OK', **styles.form_button_style)]
    ]

    window = sg.Window('Lista de Quadras', layout, modal=True)
    window.read()
    window.close()
