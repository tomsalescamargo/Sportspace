from view.TelaQuadra import TelaQuadra
from model.Quadra import Quadra

class ControladorQuadra:
    def __init__(self, controlador_sistema):
        self.__quadras = []
        self.__proximo_id = 1
        self.__tela_quadra = TelaQuadra()
        self.__controlador_sistema = controlador_sistema

    def cadastrar_quadra(self):
        dados_quadra = self.__tela_quadra.pega_dados_quadra()

        if dados_quadra:
            try:
                preco = float(dados_quadra['preco_hora'])
                nova_quadra = Quadra(self.__proximo_id,
                                     dados_quadra['nome'],
                                     dados_quadra['tipo'],
                                     dados_quadra['descricao'],
                                     preco)
                
                self.__quadras.append(nova_quadra)
                self.__proximo_id += 1
                self.__tela_quadra.mostra_mensagem("Sucesso", "Quadra cadastrada com sucesso!")
            
            except (ValueError, TypeError) as e:
                self.__tela_quadra.mostra_mensagem("Erro", f"Ocorreu um erro ao cadastrar: {e}")

    def listar_quadras(self):
        self.__tela_quadra.mostra_lista_quadras(self.__quadras)

    def voltar(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        lista_opcoes = {
            1: self.cadastrar_quadra,
            2: self.listar_quadras,
            0: self.voltar
        }

        while True:
            opcao_escolhida = self.__tela_funcionario.tela_opcoes()
            funcao_escolhida = lista_opcoes[opcao_escolhida]
            funcao_escolhida()