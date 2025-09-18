"""
Este módulo define a janela do menu principal da aplicação.
"""
import FreeSimpleGUI as sg
import os
from dotenv import load_dotenv
import ui.styles as styles

load_dotenv()

MANAGER_PASSWORD = os.getenv("MANAGER_PASSWORD")

def run_main_menu():
    """
    Cria e exibe a janela do menu principal.
    Retorna o nome da próxima janela a ser exibida.
    """
    layout = [
        [sg.Text('Sistema de Reserva de Quadras', font=styles.HEADING_FONT, pad=styles.HEADING_PAD)],
        [sg.Column([
            [sg.Button('Gerenciar Quadras', key='manage_courts', **styles.main_button_style)],
            [sg.Button('Gerenciar Clientes', key='manage_clients', **styles.main_button_style)],
            [sg.Button('Área do Gerente', key='manager_area', **styles.main_button_style)],
            [sg.Button('Sair', key='exit', **styles.main_button_style)]
        ], element_justification='center', expand_x=True)]
    ]

    window = sg.Window('Menu Principal', layout, **styles.main_window_style)
    
    next_window = 'exit'
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'exit'):
            break
        if event == 'manage_courts':
            next_window = 'manage_courts'
            break
        elif event == 'manage_clients':
            next_window = 'manage_clients'
            break
        elif event == 'manager_area':
            password = _run_password_prompt()
            if password == MANAGER_PASSWORD:
                next_window = 'manager_area'
                break
            elif password is not None:
                sg.popup("Senha incorreta.")
            
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
        [sg.Button('OK', **styles.form_button_style), sg.Button('Cancelar', **styles.form_button_style)]
    ]
    window = sg.Window('Autenticação', layout, modal=True)
    event, values = window.read()
    window.close()
    if event == 'OK':
        return values['-PASSWORD-']
    return None
