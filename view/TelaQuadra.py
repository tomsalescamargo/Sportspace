import PySimpleGUI as sg

class TelaQuadra:
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
            [sg.Text('Gerenciamento de Quadras', font=('Helvetica', 18, 'bold'), pad=((0,0),(20,20)))],
            [sg.Radio('Cadastrar Nova Quadra', 'OPCOES', key='1', font=('Helvetica', 12))],
            [sg.Radio('Listar Quadras Cadastradas', 'OPCOES', key='2', font=('Helvetica', 12))],
            [sg.Radio('Voltar', 'OPCOES', key='0', font=('Helvetica', 12), default=True)],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]
        self.__window = sg.Window('Menu de Quadras', layout, element_justification='center')

        button, values = self.open()

        opcao = 0
        if values['1']:
            opcao = 1
        elif values['2']:
            opcao = 2

        if button in (None, 'Cancelar'):
            opcao = 0

        self.close()
        return opcao

    def pega_dados_quadra(self):
        layout = [
            [sg.Text('Cadastro de Nova Quadra', font=('Helvetica', 16))],
            [sg.Text('Nome:', size=(10, 1)), sg.Input(key='nome')],
            [sg.Text('Tipo:', size=(10, 1)), sg.Input(key='tipo')],
            [sg.Text('Descrição:', size=(10, 1)), sg.Multiline(key='descricao', size=(35, 3))],
            [sg.Text('Preço/Hora:', size=(10, 1)), sg.Input(key='preco_hora', size=(15,1))],
            [sg.Button('Salvar'), sg.Cancel('Cancelar')]
        ]
        self.__window = sg.Window('Cadastrar Quadra', layout, modal=True)

        button, values = self.open()
        self.close()
        
        if button == 'Salvar':
            return values
        return None

    def mostra_lista_quadras(self, lista_quadras):
        dados_tabela = []
        for quadra in lista_quadras:
            linha = [quadra.id, quadra.nome, quadra.tipo, f"R$ {quadra.preco_hora:.2f}"]
            dados_tabela.append(linha)

        headings = ['ID', 'Nome', 'Tipo', 'Preço/Hora']
        layout = [
            [sg.Text('Lista de Quadras Cadastradas', font=('Helvetica', 16))],
            [sg.Table(values=dados_tabela, headings=headings, auto_size_columns=False, col_widths=[5, 20, 15, 10], justification='left', num_rows=10)],
            [sg.Button('OK')]
        ]
        self.__window = sg.Window('Lista de Quadras', layout, modal=True)
        self.open()
        self.close()

    def mostra_mensagem(self, titulo: str, mensagem: str):
        sg.popup(mensagem, title=titulo)