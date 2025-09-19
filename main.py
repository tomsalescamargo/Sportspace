import FreeSimpleGUI as sg
from ui import main_menu, court_management, client_management, reservation_management, manager_area

def main():
    """
    Função principal que executa a aplicação.
    Gerencia a navegação entre as janelas e inicializa o cliente Supabase.
    """
    sg.theme('Reddit')

    next_window = 'main_menu' #janela inicial

    while True:
        match next_window:
            case 'main_menu':
                next_window = main_menu.run_main_menu()
            case 'manage_courts':
                next_window = court_management.run_manage_courts()
            case 'manage_clients':
                next_window = client_management.run_manage_clients()
            case 'manage_reservations':
                next_window = reservation_management.run_manage_reservations()
            case 'manager_area':
                next_window = manager_area.run_manager_area()
            case 'back_to_main':
                next_window = 'main_menu'
            case None | 'exit':
                break
            case _:
                break 

if __name__ == "__main__":
    main()
