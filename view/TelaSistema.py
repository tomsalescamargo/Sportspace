import PySimpleGUI as sg

class TelaSistema:
    def __init__(self):
        self.__window = None
        sg.theme('Reddit')

    def open(self):
        button, values = self.__window.Read()
        return button, values

    def close(self):
        if self.__window:
            self.__window.Close()
            self.__window = None

    def tela_opcoes(self):
        layout = [
            [sg.Text('Sistema de Reservas de Quadras', font=('Helvetica', 18, 'bold'), pad=((0,0),(20,20)))],
            [sg.Radio('Gerenciar Quadras', 'OPCOES', key='1', font=('Helvetica', 12))],
            [sg.Radio('Gerenciar Clientes', 'OPCOES', key='2', font=('Helvetica', 12), disabled=True)],
            [sg.Radio('Sair do Sistema', 'OPCOES', key='0', font=('Helvetica', 12), default=True)],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]
        self.__window = sg.Window('Menu Principal', layout, element_justification='center')

        button, values = self.open()

        opcao = 0
        if values['1']:
            opcao = 1
        # Quando tiverem outras opções:
        # elif values['2']:
        #     opcao = 2

        if button in (None, 'Cancelar'):
            opcao = 0

        self.close()
        return opcao