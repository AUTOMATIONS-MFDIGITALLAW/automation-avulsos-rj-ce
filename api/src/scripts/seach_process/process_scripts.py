from time import sleep
import pandas as pd
import pyperclip as pyp
import pyautogui as pya
import keyboard as key
from api.src.scripts.seach_process.audiencia.index import AudienciaProcess
from api.src.scripts.seach_process.citacao.index import CitacaoProcess
from api.src.scripts.seach_process.sentenca.index import SentencaProcess
from api.src.scripts.seach_process.tutela.index import TutelaProcess
from api.src.utils.functions.format_date import format_date, format_hora
from api.src.utils.functions.capture_img import ScreenImage
from api.src.utils.functions.click_position import click_and_fill, click_and_fill_novo
from api.src.utils.logs.index import log
from api.src.scripts.base.base_scripts import BaseTask

class AllSeach(BaseTask):
    def __init__(self, row):
        super().__init__(row)
        self.screen = ScreenImage()
        
    def execute(self):
        return super().execute()
    
    
class SeachProcess(AllSeach):
    def __init__(self, row):
        super().__init__(row)
        
    def process(self):
        log.info('🔍 Iniciando Busca de Processo')

        try:
            # Busca e clica na imagem "lupa_seach"
            ScreenImage.wait_and_click('lupa_seach', "botão de pesquisa")
            ScreenImage.wait_and_click('busc', "Tela de busca")
            click_and_fill_novo('seach', '_POR NUMERO DE PROCESSO')
            click_and_fill('seach')
            ScreenImage.wait_and_Doubleclick('input_inserir', "Input Pesquisa",)
            key.write(str(self.row['PROCESSO']))
            ScreenImage.wait_and_click('button_ok', "Butão OK",)
            ScreenImage.wait_and_click('one', "ONE",)
            ScreenImage.wait_and_Doubleclick('process', "Processo",)
            log.success('✅ Busca de processo com sucesso')
            date_tratativa = format_date(self.row['DATA RECEBIMENTO BCC AVULSO'])
            if date_tratativa and not pd.isna(date_tratativa) and str(date_tratativa).strip().lower() != 'nat':
                SeachProcess.insert_agenda_bcc(self)
            else:
                SeachProcess.insert_agenda(self)



        except Exception as e:
            log.error(f'❌ ERRO ao buscar processo: {e}')
            
            
    def insert_agenda_bcc(self):
        log.info('🔍 Iniciando Abertura de Agenda')
        
        try:

            ScreenImage.wait_and_click('agenda', "Agenda",)
            ScreenImage.wait_and_click('adv_agenda', "Tela de Agenda",)
            
            nota_citacao = ScreenImage.find_img('citacao', 'Citação', "")
            
            pya.click(1016, 512, button='right')
            ScreenImage.wait_and_click('novo', "botao novo da agenda",)
            ScreenImage.wait_and_click('prazo', "botao prazo da agenda",)
            date_tratativa = format_date(self.row['DATA RECEBIMENTO BCC AVULSO'])
            hora_tratativa = self.row['HORA RECEBIMENTO BCC AVULSO']
            log.info(f'DATA CAPTURADA:{date_tratativa} hora: {hora_tratativa}')
            pyp.copy(date_tratativa)
            sleep(3)
            click_and_fill_novo('data_nota')
            pya.hotkey('ctrl', 'a')
            sleep(2)
            pya.hotkey('ctrl', 'v')
            sleep(2)
            key.press('Tab')
            sleep(2)
            pyp.copy(hora_tratativa)
            sleep(2)
            pya.hotkey('ctrl', 'v')
            sleep(2)
            ScreenImage.wait_and_click('etiqueta', "Etiqueta Verde",)
            ScreenImage.wait_and_click('filtrar', "Filtrar",)
            sleep(2)
            key.write('DATA DE RECEBIMENTO NO BACKOFFICE - AVULSO')
            sleep(2)
            ScreenImage.wait_and_click('checkbox', "Checkbox",)
            ScreenImage.wait_and_click('yes_agenda', "Yes",)
            ScreenImage.wait_and_click('ok_azul', "Ok",)
            
            
            try:
                deligencia = self.row['DILIGÊNCIA']
                audiencia = self.row['AUDIÊNCIA?']
                log.info(f'{deligencia} {audiencia}')
                if deligencia in ['CITACAO', 'CITAÇÃO', 'CITAÇÃO COM TUTELA']:
                    if not nota_citacao:
                        log.info('Nota de Citação não existente')
                        ScreenImage.wait_and_click('altra_nota', "Altrar Nota",)
                        ScreenImage.find_img('yes_agenda', 'Yes', 'click')
                        sleep(2)
                        ScreenImage.wait_and_click('ok_azul', "Ok",)
                        CitacaoProcess.insert_citacao(self)
                    else:
                        ScreenImage.wait_and_click('ok_azul', "Ok",)
                        if ScreenImage.find_img('yes_agenda', 'Yes', 'click'):
                            sleep(2)
                        if ScreenImage.wait_and_click('ok_azul', "Ok"):
                            sleep(3)
                else:
                    ScreenImage.wait_and_click('ok_azul', "Ok",)
                    if ScreenImage.find_img('yes_agenda', 'Yes', 'click'):
                        ScreenImage.wait_and_click('ok_azul', "Ok")
                        sleep(3)
                            
                    
                    
                if deligencia in ['LIMINAR DEFERIDA', 'TUTELA', 'CITAÇÃO COM TUTELA']:
                    log.info('Chamando a funçao de inserir tutela')
                    TutelaProcess.insert_tutela(self)
            
                     
                
                if audiencia == 'SIM':
                    log.info('Audiencia existente iniciando abertura')
                    AudienciaProcess.insert_audiencia(self)
                        
            except Exception as e:
                log.error(f'❌ ERRO na DILIGENCIA: {e}')
                
            
            ScreenImage.wait_and_click('encerrar', "Encerrar",)
           
 
        except Exception as e:
            log.error(f'❌ ERRO ao detalhes de  processo: {e}')
            
    
    def insert_agenda(self):
        log.info('🔍 Iniciando Abertura de Agenda')
        
        try:

            ScreenImage.wait_and_click('agenda', "Agenda",)
            ScreenImage.wait_and_click('adv_agenda', "Tela de Agenda",)
            
            nota_citacao = ScreenImage.find_img('citacao', 'Citação', "")
            
            pya.click(1016, 512, button='right')
            ScreenImage.wait_and_click('novo', "botao novo da agenda",)
            ScreenImage.wait_and_click('prazo', "botao prazo da agenda",)
            
            try:
                deligencia = self.row['DILIGÊNCIA']
                audiencia = self.row['AUDIÊNCIA?']
                log.info(f'{deligencia} {audiencia}')
                if deligencia in ['CITACAO', 'CITAÇÃO', 'CITAÇÃO COM TUTELA']:
                    if not nota_citacao:
                        log.info('Nota de Citação não existente')
                        # ScreenImage.wait_and_click('altra_nota', "Altrar Nota",)
                        # ScreenImage.find_img('yes_agenda', 'Yes', 'click')
                        # sleep(2)
                        # ScreenImage.wait_and_click('ok_azul', "Ok",)
                        CitacaoProcess.insert_citacao(self)
                    else:
                        ScreenImage.wait_and_click('ok_azul', "Ok",)
                        if ScreenImage.find_img('yes_agenda', 'Yes', 'click'):
                            sleep(2)
                        if ScreenImage.wait_and_click('ok_azul', "Ok"):
                            sleep(3)
                else:
                    ScreenImage.wait_and_click('anular_azul', "Anular",)
                    ScreenImage.find_img('yes_agenda', 'Yes', 'click')
                            
                    
                    
                if deligencia in ['LIMINAR DEFERIDA', 'TUTELA', 'CITAÇÃO COM TUTELA']:
                    log.info('Chamando a funçao de inserir tutela')
                    TutelaProcess.insert_tutela(self)
            
                     
                
                if audiencia == 'SIM':
                    log.info('Audiencia existente iniciando abertura')
                    AudienciaProcess.insert_audiencia(self)
                        
            except Exception as e:
                log.error(f'❌ ERRO na DILIGENCIA: {e}')
                
            
            ScreenImage.wait_and_click('encerrar', "Encerrar",)
           
 
        except Exception as e:
            log.error(f'❌ ERRO ao detalhes de  processo: {e}')
            
    
        
        

        
        
