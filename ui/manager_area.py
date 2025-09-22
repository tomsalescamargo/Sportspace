"""
Este módulo define a janela da área do gerente.
"""
import FreeSimpleGUI as sg
from database.manager_service import ManagerService
from model.FixedCost import FixedCost
import ui.styles as styles
from utils.exceptions import FormValidationException


def run_manager_area(manager_service):
    """
    Cria e exibe a janela da área do gerente.
    """
    layout = [
        [sg.Text('Área do Gerente', font=styles.HEADING_FONT,
                 pad=styles.HEADING_PAD)],
        [sg.Column([
            [sg.Button('Gerar Relatorios', key='generate_reports',
                       **styles.main_button_style)],
            [sg.Button('Registrar Custo Fixo',
                       key='register_fixed_cost', **styles.main_button_style)],
            [sg.Button('Voltar', key='back_to_main',
                       **styles.main_button_style)]
        ], element_justification='center', expand_x=True)]
    ]

    window = sg.Window('Área do Gerente', layout, **styles.main_window_style)

    next_window = 'back_to_main'
    while True:
        event, _ = window.read()
        if event in (sg.WIN_CLOSED, 'back_to_main'):
            break
        elif event == 'generate_reports':
            sg.popup('Funcionalidade ainda não implementada.')
        elif event == 'register_fixed_cost':
            _run_register_fixed_cost_form(manager_service)

    window.close()
    return next_window


def _run_register_fixed_cost_form(manager_service):
    """
    Cria e exibe o formulário de cadastro de novo custo fixo.
    """
    values = {}
    while True:
        layout = [
            [sg.Text('Registrar Novo Custo Fixo', font=styles.HEADING_FONT)],
            [sg.Text('Nome:', size=styles.INPUT_LABEL_SIZE), sg.Input(
                key='name', default_text=values.get('name', ''))],
            [sg.Text('Descrição:', size=styles.INPUT_LABEL_SIZE), sg.Input(
                key='description', default_text=values.get('description', ''))],
            [sg.Text('Valor:', size=styles.INPUT_LABEL_SIZE), sg.Input(
                key='value', default_text=values.get('value', ''))],
            [sg.Button('Salvar', **styles.form_button_style),
             sg.Cancel('Cancelar', **styles.form_button_style)]
        ]

        window = sg.Window('Registrar Custo Fixo', layout, modal=True)
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Cancelar'):
            window.close()
            break

        if event == 'Salvar':
            try:
                fixed_cost = FixedCost(
                    description=values['description'],
                    name=values['name'],
                    value=values['value'],
                )
                manager_service.create_fixed_cost(fixed_cost)
                sg.popup('Sucesso', f'Custo fixo registrado com sucesso!')
                break
            except FormValidationException as e:
                sg.popup('Erro de Validação', str(e))
            except Exception as e:
                sg.popup('Erro no Banco de Dados',
                         f'Ocorreu um erro ao registrar o custo fixo: {e}')
            finally:
                window.close()
    window.close()
