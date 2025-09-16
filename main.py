import FreeSimpleGUI as sg
from supabase_client import SupabaseClient
from views import get_main_layout, get_manage_courts_layout, register_court, list_courts

DEFAULT_WINDOW_SIZE = (800, 600)

def main():
    sg.theme('Reddit')
    supabase_client = SupabaseClient()

    layout = [[sg.Column(get_main_layout(), key='-MAIN-'), sg.Column(get_manage_courts_layout(), key='-MANAGE_COURTS-', visible=False)]]

    window = sg.Window('Menu Principal', layout, element_justification='center', size=DEFAULT_WINDOW_SIZE)

    active_layout = '-MAIN-'

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'exit'):
            break

        if event == 'manage_courts':
            window['-MAIN-'].update(visible=False)
            window['-MANAGE_COURTS-'].update(visible=True)
            active_layout = '-MANAGE_COURTS-'
        
        elif event == 'back_to_main':
            window['-MANAGE_COURTS-'].update(visible=False)
            window['-MAIN-'].update(visible=True)
            active_layout = '-MAIN-'

        elif event == 'register_court':
            register_court(supabase_client)
        
        elif event == 'list_courts':
            list_courts(supabase_client)

    window.close()


if __name__ == "__main__":
    main()
