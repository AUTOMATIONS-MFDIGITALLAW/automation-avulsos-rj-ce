from time import sleep
import pyperclip as pyp
import pyautogui as pya
import keyboard as key
from api.src.utils.functions.format_date import format_date
from api.src.utils.functions.capture_img import ScreenImage
from api.src.utils.functions.click_position import click_and_fill_novo
from api.src.utils.logs.index import log
from api.src.scripts.base.base_scripts import BaseTask

class AllSeach(BaseTask):
    def __init__(self, row):
        super().__init__(row)
        self.screen = ScreenImage()
        
    def execute(self):
        return super().execute()
    
    
class TutelaProcess(AllSeach):
    def __init__(self, row):
        super().__init__(row)


    def insert_tutela(self):
        log.info('🔍 Iniciando Agenda de Tutela')     
        
        try:  
            pya.click(1016, 512, button='right')
            ScreenImage.wait_and_click('novo', "botao novo da agenda",)
            ScreenImage.wait_and_click('decisao', "Botao Decisão",)
            
            date_tutela = format_date(self.row['DATA TUTELA'])
            log.info(f'DATA TUTELA:{date_tutela}')
            pyp.copy(date_tutela)
            sleep(3)
            click_and_fill_novo('data_tutela')
            pya.hotkey('ctrl', 'a')
            sleep(2)
            pya.hotkey('ctrl', 'v')
            ScreenImage.wait_and_click('etiqueta', "Etiqueta Verde",)
            ScreenImage.wait_and_click('filtrar', "Filtrar",)
            sleep(2)
            key.write('TUTELA')
            sleep(2)
            ScreenImage.wait_and_click('checkbox', "Checkbox",)
            ScreenImage.wait_and_click('yes_agenda', "Yes",)
            ScreenImage.wait_and_click('ok_azul', "Ok",)
            descricao = self.row['OBF TUTELA']
            pyp.copy(descricao)
            ScreenImage.wait_and_click('descricao_tutela', 'Descrição Tutela')
            key.write(' - ')
            pya.hotkey('ctrl', 'v')
            sleep(2)
            ScreenImage.wait_and_click('ok_azul', "Ok",)
            if ScreenImage.find_img('yes_agenda', 'Yes', 'click'):
                sleep(2)
            if ScreenImage.find_img('ok_azul', "Ok", 'click'):
                sleep(2)
                
            log.success('Agenda de Tutela inserido com sucesso')
            
            
            
        except Exception as e:
            log.error(f'❌ ERRO ao detalhes de  processo: {e}')
        