"""
Este módulo define os estilos visuais da aplicação, como fontes, 
dimensões de janelas e botões, e preenchimento (padding).
"""

# Fonte da aplicacão
FONT = 'Arial'

# Dimensoes de janela e botoes
DEFAULT_WINDOW_SIZE = (800, 600)
MAIN_BUTTON_SIZE = (25, 1)
FORM_BUTTON_SIZE = (10, 1)
INPUT_LABEL_SIZE = (15, 1)

# Fontes
HEADING_FONT = (FONT, 20, 'bold')
BODY_FONT = (FONT, 12)
LABEL_FONT = (FONT, 10)
MAIN_BUTTON_FONT = (FONT, 12)
FORM_BUTTON_FONT = (FONT, 10)

# Cores
BUTTON_COLOR = 'black'

# Paddings (preenchimento)
HEADING_PAD = ((0, 0), (20, 20))
MAIN_BUTTON_PAD = (5, 8)
FORM_BUTTON_PAD = (2, 10)

# Estilos
main_button_style = {'size': MAIN_BUTTON_SIZE, 'button_color': ('white', BUTTON_COLOR), 'pad': MAIN_BUTTON_PAD, 'font':MAIN_BUTTON_FONT, 'auto_size_button': False}
form_button_style = {'size': FORM_BUTTON_SIZE, 'button_color': ('white', BUTTON_COLOR), 'pad': FORM_BUTTON_PAD, 'font':FORM_BUTTON_FONT}
main_window_style = {'element_justification': 'center', 'size': DEFAULT_WINDOW_SIZE}
