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
                [sg.Button('Alterar Cliente',
                           key='update_client', **styles.main_button_style)],
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
                self._run_client_form(client_service, None)
            elif event == 'update_client': # FLUXO ADICIONADO
                self._run_update_delete_client_flow(client_service)
            elif event == 'list_clients':
                self._run_list_clients_table(client_service)

        window.close()
        return next_window


    def _run_client_form(self, client_service, client_to_edit=None):
        is_editing = client_to_edit is not None
        window_title = 'Editar Cliente' if is_editing else 'Cadastrar Novo Cliente'

        if is_editing:
            default_values = {
                'name': client_to_edit.name,
                'phone': client_to_edit.phone,
                'cpf': client_to_edit.cpf,
            }
        else:
            default_values = {}

        layout = [
            [sg.Text(window_title, font=styles.HEADING_FONT)],
            [sg.Text('Nome Completo:', size=styles.INPUT_LABEL_SIZE), sg.Input(
                key='name', default_text=default_values.get('name', ''))],
            [sg.Text('Telefone:', size=styles.INPUT_LABEL_SIZE), sg.Input(
                key='phone', default_text=default_values.get('phone', ''))],
            [sg.Text('CPF:', size=styles.INPUT_LABEL_SIZE), sg.Input(
                key='cpf', default_text=default_values.get('cpf', ''))],
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
                        client_to_edit.name = values['name']
                        client_to_edit.phone = values['phone']
                        client_to_edit.cpf = values['cpf']

                        client_service.update_client(client_to_edit)
                        sg.popup('Sucesso', 'Cliente alterado com sucesso!')
                    else:
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

            if event == 'Excluir':
                if sg.popup_yes_no('Você tem CERTEZA que deseja excluir este cliente? Esta ação não pode ser desfeita.', title='Confirmação de Exclusão') == 'Yes':
                    try:
                        client_service.delete_client(client_to_edit.id)
                        sg.popup('Cliente excluído com sucesso!')
                        break # Fecha o formulário após excluir
                    except Exception as e:
                        sg.popup('Erro', f'Ocorreu um erro ao excluir o cliente: {e}')

        window.close()

    def _run_update_delete_client_flow(self, client_service):
        client_to_edit = self._run_client_search_window(client_service)

        if client_to_edit:
            self._run_client_form(client_service, client_to_edit)

    def _run_client_search_window(self, client_service):
        clients = client_service.get_clients()
        if not clients:
            sg.popup('Nenhum cliente encontrado.')
            return None

        headings = ['ID', 'Nome', 'CPF']
        table_data = [[c.id, c.name, c.cpf] for c in clients]

        layout = [
            [sg.Text('Selecione o Cliente', font=styles.HEADING_FONT)],
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

        window = sg.Window('Buscar Cliente', layout, modal=True)
        selected_client = None

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Cancelar'):
                selected_client = None
                break

            if event == 'Selecionar':
                selected_rows = values['-TABLE-']
                if selected_rows:
                    selected_index = selected_rows[0]
                    selected_client = clients[selected_index]
                    break
                else:
                    sg.popup_error('Por favor, selecione um cliente na tabela.')

        window.close()
        return selected_client

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