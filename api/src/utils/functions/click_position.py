import keyboard
import pyautogui as pya
import pyperclip
from time import sleep
from api.src.utils.map_path.index import POSITION_PATH
from api.src.utils.logs.index import log





def click_and_fill(position_name, value:str =None, delay_before: float = 0, delay_after: float = 0.75, command:str='click', interval:float = 0, num_clicks:int = 1):
    
    try:

        x, y = POSITION_PATH[position_name]

        if delay_before > 0:
            sleep(delay_before)

        action_function = getattr(pya, command)
        
        if command == 'doubleClick':  action_function(x, y)
        else: action_function(x, y, num_clicks, interval)
        
        log.debug(f'Clicking at {position_name} ({x}, {y})')
        
        if value is not None:
            sleep(0.5)
            log.debug(f'Writing: {value}')
            pyperclip.copy(value)
            pya.hotkey('Ctrl', 'v')
            sleep(2)
        
        if delay_after > 0:
            sleep(delay_after)
    
    except KeyError as e:
        log.error(f"Nome posição '{position_name}' não encontrada no POSITION_PATH.")
    except ValueError as e:
        log.error(f'Os valores-chave não correspondem. {e}')
    except Exception as e:
        log.error(f"Ocorreu um erro inesperado. {e}")
        
        
def click_and_fill_novo(position_name, value:str =None, delay_before: float = 0, delay_after: float = 0.75, command:str='click', interval:float = 0, num_clicks:int = 1):
    
    try:

        x, y = POSITION_PATH[position_name]

        if delay_before > 0:
            sleep(delay_before)

        action_function = getattr(pya, command)
        
        if command == 'doubleClick':  action_function(x, y)
        else: action_function(x, y, num_clicks, interval)
        
        log.debug(f'Clicking at {position_name} ({x}, {y})')
        
        if value is not None:
            sleep(0.5)
            log.debug(f'Writing: {value}')
            keyboard.write(value)
            sleep(2)
        
        if delay_after > 0:
            sleep(delay_after)
    
    except KeyError as e:
        log.error(f"Nome posição '{position_name}' não encontrada no POSITION_PATH.")
    except ValueError as e:
        log.error(f'Os valores-chave não correspondem. {e}')
    except Exception as e:
        log.error(f"Ocorreu um erro inesperado. {e}")
   
   
