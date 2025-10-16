"""
Este módulo define a janela de gerenciamento de clientes.
"""
import FreeSimpleGUI as sg
from model.Client import Client
import ui.styles as styles
from utils.exceptions import FormValidationException

class ClientUI:
    def run_manage_clients(self, client_service):
        layout = [
            [sg.Text('Gerenciar Clientes', font=styles.HEADING_FONT,
                     pad=styles.HEADING_PAD)],
            [sg.Column([
                [sg.Button('Cadastrar Novo Cliente',
                           key='register_client', **styles.main_button_style)],
                [sg.Button('Listar Clientes', key='list_clients',
                           **styles.main_button_style)],
                [sg.Button('Voltar', key='back_to_main',
                           **styles.main_button_style)]
            ], element_justification='center', expand_x=True)]
        ]

        window = sg.Window('Gerenciar Clientes', layout,
                           **styles.main_window_style)

        next_window = 'back_to_main'
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'back_to_main'):
                break
            elif event == 'register_client':
                self._run_register_client_form(client_service)
            elif event == 'list_clients':
                self._run_list_clients_table(client_service)

        window.close()
        return next_window


    def _run_register_client_form(self, client_service):
        values = {}
        while True:
            layout = [
                [sg.Text('Cadastrar Novo Cliente', font=styles.HEADING_FONT)],
                [sg.Text('Nome Completo:', size=styles.INPUT_LABEL_SIZE), sg.Input(
                    key='name', default_text=values.get('name', ''))],
                [sg.Text('Telefone:', size=styles.INPUT_LABEL_SIZE), sg.Input(
                    key='phone', default_text=values.get('phone', ''))],
                [sg.Text('CPF:', size=styles.INPUT_LABEL_SIZE), sg.Input(
                    key='cpf', default_text=values.get('cpf', ''))],
                [sg.Push(), sg.Button('Salvar', **styles.form_button_style),
                 sg.Cancel('Cancelar', **styles.form_button_style)]
            ]

            window = sg.Window('Cadastrar Cliente', layout, modal=True)
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window.close()
                break

            if event == 'Salvar':
                try:
                    new_client = Client(
                        id=0,
                        name=values['name'],
                        phone=values['phone'],
                        cpf=values['cpf']
                    )

                    client_service.create_client(new_client)
                    sg.popup('Sucesso', 'Cliente cadastrado com sucesso!')
                    break
                except FormValidationException as e:
                    sg.popup('Erro de Validação', str(e))
                except Exception as e:
                    sg.popup('Erro no Banco de Dados',
                             f'Ocorreu um erro ao salvar o cliente: {e}')
                finally:
                    window.close()


    def _run_list_clients_table(self, client_service):
        clients = client_service.get_clients()

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
            [sg.Button('OK', **styles.form_button_style)]
        ]

        window = sg.Window('Lista de Clientes', layout, modal=True)
        window.read()
        window.close()
