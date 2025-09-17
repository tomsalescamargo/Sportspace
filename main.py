import FreeSimpleGUI as sg
from supabase_client import SupabaseClient
import views

def main():
    """
    Função principal que executa a aplicação.
    Gerencia a navegação entre as janelas e inicializa o cliente Supabase.
    """
    sg.theme('Reddit')
    supabase_client = SupabaseClient()

    next_window = 'main_menu' #janela inicial

    while True:
        match next_window:
            case 'main_menu':
                next_window = views.run_main_menu()
            case 'manage_courts':
                next_window = views.run_manage_courts(supabase_client)
            case 'manager_area':
                next_window = views.run_manager_area()
            case 'back_to_main':
                next_window = 'main_menu'
            case None | 'exit':
                break
            case _:
                break 

if __name__ == "__main__":
    main()
