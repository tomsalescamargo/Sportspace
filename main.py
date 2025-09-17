import FreeSimpleGUI as sg
from supabase_client import SupabaseClient
import ui.views as ui

def main():
    """
    Função principal que executa a aplicação.
    Gerencia a navegação entre as janelas e inicializa o cliente Supabase.
    """
    sg.theme('Reddit')
    db_client = SupabaseClient()

    next_window = 'main_menu' #janela inicial

    while True:
        match next_window:
            case 'main_menu':
                next_window = ui.run_main_menu()
            case 'manage_courts':
                next_window = ui.run_manage_courts(db_client)
            case 'manager_area':
                next_window = ui.run_manager_area(db_client)
            case 'back_to_main':
                next_window = 'main_menu'
            case None | 'exit':
                break
            case _:
                break 

if __name__ == "__main__":
    main()
