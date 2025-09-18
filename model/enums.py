from enum import Enum

class ReservationStatus(Enum):
    AGUARDANDO_PAGAMENTO = "Aguardando Pagamento"
    CONFIRMADA = "Confirmada"
    CONCLUIDA = "Concluída"
    CANCELADA = "Cancelada"

class CourtType(Enum):
    FUTEBOL = "Futebol"
    BASQUETE = "Basquete"
    VOLEI = "Volei"
    TENIS = "Tenis"
    POLIESPORTIVA = "Poliesportiva"

class ReportType(Enum):
    FATURAMENTO = "Faturamento"
    OCUPACAO = "Ocupacao"
