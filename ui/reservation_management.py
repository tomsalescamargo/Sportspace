"""
Este módulo define a janela de gerenciamento de reservas.
"""
import ui.styles as styles
from model.Reservation import Reservation
from model.Payment import Payment
from utils.exceptions import FormValidationException
from utils.reservations_helper import populate_reservations_table
from utils.enums import PaymentMethod, ReservationStatus

from datetime import datetime
import FreeSimpleGUI as sg

class ReservationUI:
    def run_manage_reservations(self, reservation_service):
        """
        Cria e exibe a janela de gerenciamento de reservas.
        """
        layout = [
            [sg.Text('Gerenciar Reservas', font=styles.HEADING_FONT,
                     pad=styles.HEADING_PAD)],
            [sg.Column([
                [sg.Button('Criar Reserva', key='create_reservation',
                           **styles.main_button_style)],
                [sg.Button('Listar Reservas', key='list_reservations',
                           **styles.main_button_style)],
                [sg.Button('Histórico por Cliente', key='client_history',
                           **styles.main_button_style)],
                [sg.Button('Voltar', key='back_to_main',
                           **styles.main_button_style)]
            ], element_justification='center', expand_x=True)]
        ]

        window = sg.Window('Gerenciar Reservas', layout,
                           **styles.main_window_style)

        next_window = 'back_to_main'
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'back_to_main'):
                break
            elif event == 'create_reservation':
                self._run_register_reservation_form(reservation_service)
            elif event == 'list_reservations':
                self._run_list_reservations_table(reservation_service)
            elif event == 'client_history':
                self._run_client_reservation_history(reservation_service)

        window.close()
        return next_window


    def _run_register_reservation_form(self, reservation_service):
        """
        Cria e exibe o formulário de cadastro de nova reserva.
        """

        # Fazer a busca e setup dos dados no inicio para fazer tudo somente uma vez
        courts = reservation_service.get_courts()

        if not courts:
            sg.popup(
                'Nenhuma quadra cadastrada.')
            return

        clients = reservation_service.get_clients()

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
             sg.Input(key='date', size=(16, 1), readonly=True,
                      disabled_readonly_background_color='white'),
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
                    client = self._run_client_search_window(clients)
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
                        date_time = datetime.strptime(
                            date_time_str, '%Y-%m-%d %H:%M')

                        new_reservation = Reservation(
                            client_id=selected_client.id,
                            court_id=court_hash[values['court_name']],
                            date_time=date_time,
                            status=ReservationStatus.AGUARDANDO_PAGAMENTO
                        )

                        # reservation client da throw em FormValidationException caso algo esteja errado
                        reservation_service.validate_reservation(new_reservation)
                        reservation_service.create_reservation(new_reservation)

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


    def _run_client_reservation_history(self, reservation_service):
        clients = reservation_service.get_clients()

        if not clients:
            sg.popup('Nenhum cliente cadastrado.')
            return

        selected_client = self._run_client_search_window(clients)

        if not selected_client:
            return

        reservations = reservation_service.get_reservations_by_client(selected_client.id)

        if not reservations:
            sg.popup('Nenhuma reserva encontrada para este cliente.')
            return

        headings = ['ID', 'Cliente', 'Quadra', 'Data e Hora', 'Status']
        table_data = populate_reservations_table(reservations)

        layout = [
            [sg.Text(f'Histórico de Reservas - {selected_client.name}', font=styles.HEADING_FONT)],
            [sg.Table(
                values=table_data,
                headings=headings,
                auto_size_columns=False,
                col_widths=[3, 20, 20, 15, 18],
                justification='left',
                num_rows=15,
                alternating_row_color='lightblue',
                key='-TABLE-',
                row_height=25
            )],
            [sg.Button('Voltar', **styles.form_button_style)]
        ]

        window = sg.Window('Histórico de Reservas', layout, modal=True)
        window.read()
        window.close()


    def _run_list_reservations_table(self, reservation_service):
        reservations = reservation_service.get_reservations()

        headings = ['ID', 'Cliente', 'Quadra', 'Data e Hora', 'Status']
        table_data = populate_reservations_table(reservations)

        layout = [
            [sg.Text('Lista de Reservas', font=styles.HEADING_FONT)],
            [sg.Table(
                values=table_data,
                headings=headings,
                auto_size_columns=False,
                col_widths=[3, 20, 20, 15, 18],
                justification='left',
                num_rows=15,
                alternating_row_color='lightblue',
                key='-TABLE-',
                row_height=25,
                enable_events=True
            )],
            [
                sg.Button('Registrar Pagamento', key='btn_pay', **styles.form_button_style),
                sg.Button('Serviços', key='btn_service', **styles.form_button_style),
                sg.Button('Concluir', key='btn_conclude', **styles.form_button_style),
                sg.Button('Cancelar', key='btn_cancel',
                          **{**styles.form_button_style, 'button_color': ('white', 'red')})
            ],
            [sg.HorizontalSeparator()],
            [sg.Button('Voltar', **styles.form_button_style),
             sg.Button('Editar', **styles.form_button_style),
             sg.Button('Excluir', **{**styles.form_button_style, 'button_color': ('white', 'red')})
             ]
        ]

        window = sg.Window('Lista de Reservas', layout, modal=True)

        selected_reservation = None
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Voltar'):
                break
            
            if event == '-TABLE-':
                if values['-TABLE-']:
                    selected_index = values['-TABLE-'][0]
                    selected_reservation = reservations[selected_index]

            if event == 'Editar':
                if selected_reservation:
                    self._run_edit_reservation_form(reservation_service, selected_reservation)
                    reservations = reservation_service.get_reservations()
                    table_data = populate_reservations_table(reservations)
                    window['-TABLE-'].update(values=table_data)
                else:
                    sg.popup('Por favor, selecione uma reserva para editar.')

            if event == 'Excluir':
                if selected_reservation:
                    if sg.popup_yes_no('Tem certeza que deseja excluir esta reserva?') == 'Yes':
                        try:
                            reservation_service.delete_reservation(selected_reservation['id'])
                            sg.popup('Sucesso', 'Reserva excluída com sucesso!')
                            reservations = reservation_service.get_reservations()
                            table_data = populate_reservations_table(reservations)
                            window['-TABLE-'].update(values=table_data)
                        except Exception as e:
                            sg.popup('Erro ao excluir', e)
                else:
                    sg.popup('Por favor, selecione uma reserva para excluir.')
            if event == 'btn_pay':
                if not selected_reservation:
                    sg.popup("Selecione uma reserva primeiro.")
                    continue
                self._run_payment_form(reservation_service, selected_reservation)
                reservations = reservation_service.get_reservations()
                window['-TABLE-'].update(values=populate_reservations_table(reservations))

            elif event == 'btn_service':
                if not selected_reservation:
                    sg.popup("Selecione uma reserva primeiro.")
                    continue
                self._run_manage_reservation_services(reservation_service, selected_reservation)
                reservations = reservation_service.get_reservations()
                window['-TABLE-'].update(values=populate_reservations_table(reservations))

            elif event == 'btn_conclude':
                if self._confirm_action(selected_reservation, "Concluir"):
                    try:
                        reservation_service.update_status(
                            selected_reservation['id'],
                            ReservationStatus.CONCLUIDA.value
                        )
                        sg.popup("Reserva concluída com sucesso!")
                        reservations = reservation_service.get_reservations()
                        window['-TABLE-'].update(values=populate_reservations_table(reservations))
                    except Exception as e:
                        sg.popup_error(f"Erro: {e}")

            elif event == 'btn_cancel':
                if self._confirm_action(selected_reservation, "CANCELAR"):
                    try:
                        reservation_service.update_status(
                            selected_reservation['id'],
                            ReservationStatus.CANCELADA.value
                        )
                        sg.popup("Reserva cancelada!")
                        reservations = reservation_service.get_reservations()
                        window['-TABLE-'].update(values=populate_reservations_table(reservations))
                    except Exception as e:
                        sg.popup_error(f"Erro: {e}")

        window.close()

    def _run_edit_reservation_form(self, reservation_service, reservation):
        courts = reservation_service.get_courts()
        clients = reservation_service.get_clients()

        court_hash = {court.name: court.id for court in courts}
        court_names = list(court_hash.keys())

        client_hash = {client.name: client.id for client in clients}
        client_names = list(client_hash.keys())

        reservation_datetime = datetime.strptime(reservation['date_time'], '%Y-%m-%dT%H:%M:%S')

        hours = [f'{h:02d}:00' for h in range(24)]

        layout = [
            [sg.Text('Editar Reserva', font=styles.HEADING_FONT)],
            [sg.Text('Quadra:', size=styles.INPUT_LABEL_SIZE),
             sg.Combo(court_names, key='court_name', default_value=reservation['courts']['name'], readonly=True, size=(30, 1))],
            [sg.Text('Cliente:', size=styles.INPUT_LABEL_SIZE),
                sg.Combo(client_names, key='client_name', default_value=reservation['clients']['name'], readonly=True, size=(30, 1))],
            [sg.Text('Data:', size=styles.INPUT_LABEL_SIZE),
             sg.Input(key='date', size=(16, 1), readonly=True, default_text=reservation_datetime.strftime('%Y-%m-%d'),
                      disabled_readonly_background_color='white'),
             sg.CalendarButton('Selecionar', target='date', format='%Y-%m-%d', **styles.form_button_style)],
            [sg.Text('Hora:', size=styles.INPUT_LABEL_SIZE),
             sg.Combo(hours, key='time', default_value=reservation_datetime.strftime('%H:%M'), readonly=True, size=(10, 1))],
            [sg.Push(), sg.Button('Salvar', **styles.form_button_style),
             sg.Cancel('Cancelar', **styles.form_button_style)]
        ]

        window = sg.Window('Editar Reserva', layout, modal=True)

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Cancelar'):
                break

            if event == 'Salvar':
                try:
                    date_time_str = f"{values['date']} {values['time']}"
                    date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')

                    updated_reservation = Reservation(
                        client_id = client_hash[values['client_name']],
                        court_id = court_hash[values['court_name']],
                        date_time = date_time,
                        status = reservation['status']
                    )

                    reservation_service.validate_reservation(updated_reservation)
                    reservation_service.update_reservation(reservation['id'], updated_reservation)
                    sg.popup('Sucesso', 'Reserva atualizada com sucesso!')
                    break
                except FormValidationException as e:
                    sg.popup('Erro de validação', e)
                except Exception as e:
                    sg.popup('Erro ao salvar', e)

        window.close()

    def _run_client_search_window(self, clients):
        headings = ['ID', 'Nome', 'CPF']
        table_data = [[client.id, client.name, client.cpf] for client in clients]
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
                if event == '-SEARCH-':
                    search_term = values['-SEARCH-'].lower().strip()

                    if search_term:
                        filtered_clients = [
                            client for client in clients
                            if search_term in client.name.lower()
                        ]
                        current_table_data = [
                            [client.id, client.name, client.cpf] for client in filtered_clients]
                        original_clients = filtered_clients
                    else:
                        current_table_data = table_data.copy()
                        original_clients = clients.copy()

                    window['-TABLE-'].update(values=current_table_data)

                if event == '-TABLE-':
                    selected_rows = values['-TABLE-']
                    if selected_rows:
                        selected_index = selected_rows[0]
                        return original_clients[selected_index]

        finally:
            window.close()

    def _confirm_action(self, reservation, action_name):
        if not reservation:
            sg.popup(f"Selecione uma reserva para {action_name}.")
            return False
        return sg.popup_yes_no(f"Deseja realmente {action_name} a reserva #{reservation['id']}?") == 'Yes'

    def _run_payment_form(self, reservation_service, reservation):
        methods = [m.value for m in PaymentMethod]

        try:
            balance = reservation_service.calculate_reservation_balance(reservation['id'])
            default_value = f"{balance['remaining_balance']:.2f}"

            summary_text = (
                f"Quadra: R$ {balance['court_price']:.2f}\n"
                f"Serviços Extras: R$ {balance['services_total']:.2f}\n"
                f"Total Geral: R$ {balance['total_cost']:.2f}\n"
                f"Já Pago: R$ {balance['total_paid']:.2f}"
            )
        except Exception as e:
            sg.popup_error(f"Erro ao calcular valores: {e}")
            default_value = "0.00"
            summary_text = "Erro ao carregar valores."

        layout = [
            [sg.Text(f"Novo Pagamento - Reserva {reservation['id']}", font=styles.HEADING_FONT)],

            [sg.Frame("Resumo da Conta", [
                [sg.Text(summary_text, font=styles.BODY_FONT)]
            ], pad=(0, 10))],

            [sg.Text("Valor a Pagar (R$):", size=styles.INPUT_LABEL_SIZE),
             sg.Input(default_text=default_value, key='value', size=(15, 1))],

            [sg.Text("Método:", size=styles.INPUT_LABEL_SIZE),
             sg.Combo(methods, key='method', default_value=methods[0], readonly=True)],

            [sg.Button("Confirmar", **styles.form_button_style),
             sg.Cancel("Cancelar", **styles.form_button_style)]
        ]

        window = sg.Window('Pagamento', layout, modal=True)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Cancelar'):
                break

            if event == 'Confirmar':
                try:
                    payment_val = float(values['value'])
                    if payment_val > balance['remaining_balance'] + 0.01:  # +0.01 margem erro float
                        if sg.popup_yes_no("O valor é maior que o restante. Confirmar troco/crédito?") != 'Yes':
                            continue

                    payment = Payment(
                        reservation_id=reservation['id'],
                        method=values['method'],
                        value=payment_val
                    )
                    reservation_service.add_payment(payment)
                    sg.popup("Pagamento registrado!")
                    new_balance = reservation_service.calculate_reservation_balance(reservation['id'])
                    if new_balance['remaining_balance'] <= 0.01:
                        reservation_service.update_status(reservation['id'], ReservationStatus.CONFIRMADA.value)
                        sg.popup("Reserva totalmente paga! Status alterado para Confirmada.")

                    break
                except ValueError:
                    sg.popup_error("Valor inválido.")
                except FormValidationException as e:
                    sg.popup_error(str(e))
                except Exception as e:
                    sg.popup_error(f"Erro no banco: {e}")

        window.close()

    def _run_add_service_form(self, reservation_service, reservation):
        try:
            available_services = reservation_service.get_available_extra_services()
        except Exception as e:
            sg.popup_error(f"Erro ao buscar serviços: {e}")
            return

        if not available_services:
            sg.popup("Nenhum serviço extra cadastrado no sistema.")
            return

        service_names = [str(s) for s in available_services]

        layout = [
            [sg.Text(f"Adicionar Serviço - Reserva {reservation['id']}", font=styles.HEADING_FONT)],
            [sg.Text("Serviço:", size=styles.INPUT_LABEL_SIZE),
             sg.Combo(service_names, key='service_idx', readonly=True, size=(30, 1), default_value=service_names[0])],
            [sg.Text("Quantidade:", size=styles.INPUT_LABEL_SIZE),
             sg.Input("1", key='qty', size=(5, 1))],
            [sg.Button("Adicionar", **styles.form_button_style), sg.Cancel("Cancelar", **styles.form_button_style)]
        ]

        window = sg.Window('Serviços Extras', layout, modal=True)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Cancelar'):
                break

            if event == 'Adicionar':
                try:
                    selected_text = values['service_idx']
                    idx = service_names.index(selected_text)
                    service_obj = available_services[idx]

                    qty = int(values['qty'])
                    if qty < 1: raise ValueError("Qtd deve ser > 0")

                    reservation_service.add_service_to_reservation(
                        reservation_id=reservation['id'],
                        service_id=service_obj.id,
                        quantity=qty
                    )
                    sg.popup(f"Adicionado: {qty}x {service_obj.service}")
                    break
                except ValueError:
                    sg.popup_error("Quantidade inválida.")
                except Exception as e:
                    sg.popup_error(f"Erro ao salvar: {e}")

        window.close()

    def _run_manage_reservation_services(self, reservation_service, reservation):

        while True:
            items = reservation_service.get_reservation_services(reservation['id'])
            table_data = []
            total_services = 0.0

            for item in items:
                svc_name = item['extra_services']['service']
                price = float(item['extra_services']['value'])
                qty = int(item['quantity'])
                subtotal = price * qty
                total_services += subtotal

                table_data.append([
                    item['service_id'],
                    f"{qty}x",
                    svc_name,
                    f"R$ {price:.2f}",
                    f"R$ {subtotal:.2f}"
                ])

            headings = ['ID', 'Qtd', 'Serviço', 'Unit.', 'Subtotal']

            layout = [
                [sg.Text(f"Serviços - Reserva #{reservation['id']}", font=styles.HEADING_FONT)],
                [sg.Table(
                    values=table_data,
                    headings=headings,
                    auto_size_columns=False,
                    col_widths=[5, 5, 20, 10, 10],
                    justification='left',
                    num_rows=6,
                    key='-SVC_TABLE-',
                    enable_events=True,
                    alternating_row_color='lightblue'
                )],
                [sg.Text(f"Total em Serviços: R$ {total_services:.2f}", font=styles.BODY_FONT)],
                [
                    sg.Button('Adicionar Item', key='add', **styles.form_button_style),
                    sg.Button('Remover Item', key='remove',
                              **{**styles.form_button_style, 'button_color': ('white', 'red')}),
                    sg.Button('Fechar', key='close', **styles.form_button_style)
                ]
            ]

            window = sg.Window('Gerenciar Serviços da Reserva', layout, modal=True)
            selected_service_id = None

            while True:
                event, values = window.read()

                if event in (sg.WIN_CLOSED, 'close'):
                    window.close()
                    return

                if event == '-SVC_TABLE-':
                    if values['-SVC_TABLE-']:
                        idx = values['-SVC_TABLE-'][0]
                        selected_service_id = table_data[idx][0]

                if event == 'add':
                    window.hide()
                    self._run_add_service_form(reservation_service, reservation)
                    window.close()
                    break

                if event == 'remove':
                    if selected_service_id:
                        if sg.popup_yes_no("Remover este item da reserva?") == 'Yes':
                            try:
                                reservation_service.remove_service_from_reservation(
                                    reservation['id'],
                                    selected_service_id
                                )
                                sg.popup("Item removido!")
                                window.close()
                                break
                            except Exception as e:
                                sg.popup_error(f"Erro: {e}")
                    else:
                        sg.popup("Selecione um item na lista para remover.")