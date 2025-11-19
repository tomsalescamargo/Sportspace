"""
Este módulo define a janela da área do gerente.
"""
from datetime import datetime

import FreeSimpleGUI as sg
from model.FixedCost import FixedCost
import ui.styles as styles
from utils.exceptions import FormValidationException

class ManagerAreaUI:
    def run_manager_area(self, manager_service):
        """
        Cria e exibe a janela da área do gerente.
        """
        layout = [
            [sg.Text('Área do Gerente', font=styles.HEADING_FONT,
                     pad=styles.HEADING_PAD)],
            [sg.Column([
                [sg.Button('Gerar Relatorios', key='generate_reports',
                           **styles.main_button_style)],
                [sg.Button('Listar Custos Fixos', key='list_fixed_costs',
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
                self._run_reports_menu(manager_service)
            elif event == 'list_fixed_costs':
                self._show_fixed_costs_list(manager_service)
            elif event == 'register_fixed_cost':
                self._run_register_fixed_cost_form(manager_service)

        window.close()
        return next_window


    def _run_register_fixed_cost_form(self, manager_service):
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

    def _show_fixed_costs_list(self, manager_service):
        fixed_costs = manager_service.get_fixed_costs()
        if not fixed_costs:
            sg.popup('Informação', 'Nenhum custo fixo cadastrado.')
            return

        table_data = self._format_fixed_costs_table_data(fixed_costs)
        headings = ['Nome', 'Descrição', 'Valor']
        num_rows = max(5, min(len(table_data), 15)) if table_data else 5

        layout = [
            [sg.Text('Custos Fixos Registrados', font=styles.HEADING_FONT)],
            [sg.Table(
                values=table_data,
                headings=headings,
                auto_size_columns=False,
                col_widths=[20, 30, 12],
                justification='left',
                num_rows=num_rows,
                key='-FIXED_COSTS_LIST-',
                enable_events=True
            )],
            [
                sg.Button('Fechar', key='close_fixed_costs', **styles.form_button_style),
                sg.Button('Excluir', key='delete_fixed_cost',
                          **{**styles.form_button_style, 'button_color': ('white', 'red')})
            ]
        ]

        window = sg.Window('Custos Fixos', layout, modal=True)

        selected_cost = None
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'close_fixed_costs'):
                break

            if event == '-FIXED_COSTS_LIST-':
                if values['-FIXED_COSTS_LIST-']:
                    selected_index = values['-FIXED_COSTS_LIST-'][0]
                    selected_cost = fixed_costs[selected_index]

            if event == 'delete_fixed_cost':
                if not selected_cost:
                    sg.popup('Selecione um custo fixo para excluir.')
                    continue

                if sg.popup_yes_no('Tem certeza que deseja excluir este custo fixo?') != 'Yes':
                    continue

                try:
                    manager_service.delete_fixed_cost(selected_cost['id'])
                    sg.popup('Sucesso', 'Custo fixo excluído com sucesso!')
                    fixed_costs = manager_service.get_fixed_costs()
                    table_data = self._format_fixed_costs_table_data(fixed_costs)
                    window['-FIXED_COSTS_LIST-'].update(values=table_data)
                    selected_cost = None
                    if not fixed_costs:
                        sg.popup('Informação', 'Nenhum custo fixo restante para exibir.')
                        break
                except Exception as exc:
                    sg.popup('Erro ao excluir custo fixo', str(exc))

        window.close()

    def _run_reports_menu(self, manager_service):
        menu_button_style = styles.main_button_style.copy()
        menu_button_style['size'] = (40, 1)

        layout = [
            [sg.Text('Relatórios Disponíveis', font=styles.HEADING_FONT, pad=(0, 20))],
            [sg.Button('Relatório de Ocupação de Quadras', key='report_occupancy',
                       **menu_button_style)],
            [sg.Button('Relatório de Faturamento Mensal', key='report_monthly_revenue',
                       **menu_button_style)],
            [sg.Push(), sg.Cancel('Fechar', **styles.form_button_style)]
        ]

        window = sg.Window(
            'Gerar Relatórios',
            layout,
            modal=True,
            size=(600, 350),
            element_justification='center'
        )

        while True:
            event, _ = window.read()
            if event in (sg.WIN_CLOSED, 'Fechar'):
                break

            if event == 'report_occupancy':
                self._run_court_occupancy_report(manager_service)
            elif event == 'report_monthly_revenue':
                self._run_monthly_revenue_report(manager_service)

        window.close()

    def _run_court_occupancy_report(self, manager_service):
        report_rows = manager_service.get_court_occupancy_report()
        table_data = self._format_occupancy_table_data(report_rows)
        num_rows = max(5, min(len(table_data), 15)) if table_data else 5

        headings = ['Quadra', 'Horas Utilizadas']
        layout = [
            [sg.Text('Relatório de Ocupação de Quadras', font=styles.HEADING_FONT)],
            [sg.Table(
                values=table_data,
                headings=headings,
                key='-OCCUPANCY_TABLE-',
                auto_size_columns=False,
                col_widths=[35, 15],
                justification='left',
                num_rows=num_rows
            )],
            [sg.Text(self._build_occupancy_summary(report_rows),
                     key='-OCCUPANCY_SUMMARY-', font=styles.BODY_FONT)],
            [sg.Cancel('Fechar', **styles.form_button_style)]
        ]

        window = sg.Window('Relatório de Ocupação', layout, modal=True, finalize=True)

        while True:
            event, _ = window.read()
            if event in (sg.WIN_CLOSED, 'Fechar'):
                break

        window.close()

    def _run_monthly_revenue_report(self, manager_service):
        current_date = datetime.now()
        months = [
            ('Janeiro', 1), ('Fevereiro', 2), ('Março', 3), ('Abril', 4),
            ('Maio', 5), ('Junho', 6), ('Julho', 7), ('Agosto', 8),
            ('Setembro', 9), ('Outubro', 10), ('Novembro', 11), ('Dezembro', 12)
        ]
        default_month_name = next(name for name, value in months if value == current_date.month)

        layout = [
            [sg.Text('Relatório de Faturamento Mensal', font=styles.HEADING_FONT)],
            [sg.Text('Mês:', size=styles.INPUT_LABEL_SIZE),
             sg.Combo([name for name, _ in months], key='month', default_value=default_month_name,
                      readonly=True, size=(20, 1))],
            [sg.Text('Ano:', size=styles.INPUT_LABEL_SIZE),
             sg.Input(key='year', default_text=str(current_date.year), size=(10, 1))],
            [sg.Button('Gerar', **styles.form_button_style),
             sg.Cancel('Cancelar', **styles.form_button_style)]
        ]

        window = sg.Window('Selecionar Período', layout, modal=True)

        try:
            while True:
                event, values = window.read()
                if event in (sg.WIN_CLOSED, 'Cancelar'):
                    break

                if event == 'Gerar':
                    selected_month = values.get('month')
                    if not selected_month:
                        sg.popup('Erro de Validação', 'Selecione um mês para gerar o relatório.')
                        continue

                    try:
                        month_value = next(value for name, value in months if name == selected_month)
                    except StopIteration:
                        sg.popup('Erro', 'Mês selecionado inválido.')
                        continue

                    try:
                        year = int(values.get('year'))
                        if year < 1900:
                            raise ValueError
                    except (TypeError, ValueError):
                        sg.popup('Erro de Validação', 'Informe um ano válido (>= 1900).')
                        continue

                    try:
                        report_data = manager_service.get_monthly_revenue_report(year, month_value)
                    except Exception as exc:  # pragma: no cover - interface visual
                        sg.popup('Erro ao gerar relatório', str(exc))
                        continue

                    window.close()
                    window = None
                    self._show_monthly_revenue_summary(report_data)
                    break
        finally:
            if window is not None:
                window.close()

    def _show_monthly_revenue_summary(self, report_data: dict):
        month = report_data.get('month', 1)
        year = report_data.get('year', datetime.now().year)
        formatted_period = f"{month:02d}/{year}"
        fixed_costs = report_data.get('fixed_costs') or []
        fixed_costs_table_data = [
            [item.get('name', 'N/D'), f"R$ {item.get('value', 0):.2f}"]
            for item in fixed_costs
        ]
        num_rows = max(3, min(len(fixed_costs_table_data), 10)) if fixed_costs_table_data else 3

        layout = [
            [sg.Text('Resumo do Faturamento Mensal', font=styles.HEADING_FONT)],
            [sg.Text(f'Período: {formatted_period}', font=styles.BODY_FONT)],
            [sg.Text(f"Faturamento total (reservas pagas): R$ {report_data.get('total_revenue', 0):.2f}",
                     font=styles.BODY_FONT)],
            [sg.Text(f"Custos fixos registrados: R$ {report_data.get('total_fixed_costs', 0):.2f}",
                     font=styles.BODY_FONT)],
            [sg.Text(f"Resultado líquido: R$ {report_data.get('net_result', 0):.2f}",
                     font=styles.BODY_FONT)],
            [sg.Text('Detalhamento dos Custos Fixos', font=styles.BODY_FONT, pad=(0, 10))]
        ]

        if fixed_costs_table_data:
            layout.append([
                sg.Table(
                    values=fixed_costs_table_data,
                    headings=['Nome', 'Valor'],
                    auto_size_columns=False,
                    col_widths=[35, 15],
                    justification='left',
                    num_rows=num_rows,
                    key='-FIXED_COSTS_TABLE-'
                )
            ])
        else:
            layout.append([
                sg.Text('Nenhum custo fixo cadastrado.', font=styles.BODY_FONT)
            ])

        layout.append([sg.Cancel('Fechar', **styles.form_button_style)])

        window = sg.Window('Relatório de Faturamento Mensal', layout, modal=True)

        while True:
            event, _ = window.read()
            if event in (sg.WIN_CLOSED, 'Fechar'):
                break

        window.close()

    def _format_occupancy_table_data(self, report_rows: list[dict]):
        table_data = []
        for row in report_rows:
            table_data.append([
                row.get('court_name', 'N/D'),
                row.get('hours_used', 0)
            ])
        return table_data

    def _build_occupancy_summary(self, report_rows: list[dict]):
        if not report_rows:
            return 'Nenhuma quadra cadastrada para gerar o relatório.'
        total_hours = sum(int(row.get('hours_used', 0)) for row in report_rows)
        total_courts = len(report_rows)
        return f'Total de quadras: {total_courts} | Horas totais utilizadas: {total_hours}'

    def _format_fixed_costs_table_data(self, fixed_costs: list[dict]):
        table_data = []
        for cost in fixed_costs:
            name = cost.get('name', 'N/D')
            description = cost.get('description', '-')
            try:
                value = float(cost.get('value', 0))
            except (TypeError, ValueError):
                value = 0
            table_data.append([name, description, f"R$ {value:.2f}"])
        return table_data
