
from view.TelaSistema import TelaSistema
from controller.ControladorQuadras import ControladorQuadra
# Importar outros controladores aqui no futuro


class ControladorSistema:
    __instance = None

    def __init__(self):
        self.__tela_sistema = TelaSistema()
        self.__controlador_quadras = ControladorQuadra(self)
        # Adicionar outros controladores

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(ControladorSistema, cls).__new__(cls)
        return cls.__instance

    @property
    def controlador_quadras(self):
        return self.__controlador_quadras

    def gerenciar_quadras(self):
        self.__controlador_quadras.abre_tela()

    def encerrar_sistema(self):
        exit(0)

    def abre_tela(self):
        lista_opcoes = {
            1: self.gerenciar_quadras,
            # 2: self.gerenciar_clientes,
            0: self.encerrar_sistema
        }

        while True:
            opcao_escolhida = self.__tela_sistema.tela_opcoes()
            funcao_escolhida = lista_opcoes[opcao_escolhida]
            funcao_escolhida()
