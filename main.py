import FreeSimpleGUI as sg
import os
import logging
from dotenv import load_dotenv
import supabase
from database.court_service import CourtService
from database.client_service import ClientService
from database.reservation_service import ReservationService
from database.manager_service import ManagerService
from ui.reservation_management import ReservationUI
from ui.client_management import ClientUI
from ui.court_management import CourtUI
from ui.manager_area import ManagerAreaUI
from ui.main_menu import MainMenuUI

from ui import main_menu, court_management, client_management, reservation_management, manager_area

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)

def main():
    """
    Função principal que executa a aplicação.
    Gerencia a navegação entre as janelas e inicializa o cliente Supabase.
    """
    sg.theme('Reddit')

    # criar clientes do BD
    db_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)
    court_service = CourtService(db_client)
    client_service = ClientService(db_client)
    reservation_service = ReservationService(db_client)
    manager_service = ManagerService(db_client)

    #instanciar UIs
    main_menu_ui = MainMenuUI()
    court_ui = CourtUI()
    client_ui = ClientUI()
    manager_area_ui = ManagerAreaUI()
    reservation_ui = ReservationUI()

    next_window = 'main_menu'

    while True:
        match next_window:
            case 'main_menu':
                next_window = main_menu_ui.run_main_menu()
            case 'manage_courts':
                next_window = court_ui.run_manage_courts(court_service, reservation_service)
            case 'manage_clients':
                next_window = client_ui.run_manage_clients(client_service)
            case 'manage_reservations':
                next_window = reservation_ui.run_manage_reservations(reservation_service)
            case 'manager_area':
                next_window = manager_area_ui.run_manager_area(manager_service)
            case 'back_to_main':
                next_window = 'main_menu'
            case None | 'exit':
                break
            case _:
                break


if __name__ == "__main__":
    main()
