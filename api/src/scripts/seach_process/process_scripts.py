from time import sleep
import pandas as pd
import pyperclip as pyp
import pyautogui as pya
import keyboard as key
from api.src.scripts.seach_process.audiencia.index import AudienciaProcess
from api.src.scripts.seach_process.citacao.index import CitacaoProcess
from api.src.scripts.seach_process.distribuicao.index import DistribuicaoProcess
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
            
            busc_encont = ScreenImage.wait_and_click('busc', "Tela de busca",)
            
            if not busc_encont:
                ScreenImage.wait_and_click('lupa_seach', "botão de pesquisa",)
            
            # se nao busca a img busc por 8 segundo ele clica novamente no lupa 
            ScreenImage.wait_and_click('busc', "Tela de busca")
            click_and_fill_novo('seach', '_POR NUMERO DE PROCESSO')
            click_and_fill('seach')
            ScreenImage.wait_and_Doubleclick('input_inserir', "Input Pesquisa",)
            key.write(str(self.row['PROCESSO']))
            ScreenImage.wait_and_click('button_ok', "Butão OK",)
            ScreenImage.wait_and_click('one', "ONE",)
            ScreenImage.wait_and_Doubleclick('process', "Processo",)
            log.success('✅ Busca de processo com sucesso') 
             
                     
            SeachProcess.insert_agenda_bcc(self) 
                       

        except Exception as e:
            log.error(f'❌ ERRO ao buscar processo: {e}')
            
            
    def insert_agenda_bcc(self):
        log.info('🔍 Iniciando Abertura de Agenda')
        
        try:
            
            # fazer
            ScreenImage.wait_and_click('agenda', "Agenda",)
            
            
            if not ScreenImage.find_img('adv_agenda', "Tela de Agenda", ""):
                pya.click(792, 292)
                ScreenImage.wait_and_click('agenda', "Agenda",)
                ScreenImage.wait_and_click('adv_agenda', "Tela de Agenda",)
            sleep(2)              
            
            try:
                date_tratativa = format_date(self.row['DATA RECEBIMENTO BCC AVULSO'])
                if date_tratativa and not pd.isna(date_tratativa) and str(date_tratativa).strip().lower() != 'nat':
                    pya.click(1016, 512, button='right')
                    ScreenImage.wait_and_click('novo', "botao novo da agenda",)
                    ScreenImage.wait_and_click('prazo', "botao prazo da agenda",)
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
                    sleep(2)
                    ScreenImage.wait_and_click('ok_azul', "Ok",)
                    if ScreenImage.find_img('yes_agenda', 'Yes', 'click'):
                        sleep(2)
                        ScreenImage.find_img('ok_azul', "Ok", 'click')
                        
                else:
                     log.info('Nota de BCC não existente base')
                    
            except Exception as e:
                log.error(f'❌ ERRO na Agenda BCC: {e}')
            
            try:
                
                date_distribuicao = format_date(self.row['DATA DISTRIBUICAO'])
                if date_distribuicao and not pd.isna(date_distribuicao) and str(date_distribuicao).strip().lower() != 'nat':
                    log.info(f'DATA DISTRIBUIÇÃO:{date_distribuicao}')
                    nota_distribuicao = ScreenImage.find_img('distribuicao', 'Distribuição', "")
                    if nota_distribuicao:
                        log.info('Nota de Distribuição existente, iniciando exclusão')
                        ScreenImage.wait_and_click('distribuicao', 'Distribuição')
                        pya.click(button='right')
                        ScreenImage.wait_and_click('excluir', "Excluir",)
                        ScreenImage.wait_and_click('yes_excluir', "yes",)
                        DistribuicaoProcess.insert_distribuicao(self)
                    else:
                        log.info('Nota de Distribuição não existente')
                        DistribuicaoProcess.insert_distribuicao(self)
                        
                        
                date_citacao = format_date(self.row['DATA CITACAO'])
                if date_citacao and not pd.isna(date_citacao) and str(date_citacao).strip().lower() != 'nat':
                    log.info(f'DATA CITAÇÃO:{date_citacao}')
                    nota_citacao = ScreenImage.find_img('citacao', 'Citação', "")
                    if nota_citacao:
                        log.info('Nota de Citação existente, iniciando exclusão')
                        ScreenImage.wait_and_click('citacao', 'Citação')
                        pya.click(button='right')
                        ScreenImage.wait_and_click('excluir', "Excluir",)
                        ScreenImage.wait_and_click('yes_excluir', "yes",)
                        CitacaoProcess.insert_citacao(self)
                        
                    else:
                        log.info('Nota de Citação não existente')
                        CitacaoProcess.insert_citacao(self)
                        
                    sleep(20)                            
                    
                date_tutela = format_date(self.row['DATA TUTELA'])
                if date_tutela and not pd.isna(date_tutela) and str(date_tutela).strip().lower() != 'nat':
                    log.info(f'DATA tutela:{date_tutela}')
                    TutelaProcess.insert_tutela(self)                 
                    
                audiencia = format_date(self.row['DATA AUDIENCIA'])                
                if audiencia and not pd.isna(audiencia) and str(audiencia).strip().lower() != 'nat':
                    log.info('Audiencia existente iniciando abertura')
                    AudienciaProcess.insert_audiencia(self)  
                    
                             
                
                        
            except Exception as e:
                log.error(f'❌ ERRO na DILIGENCIA: {e}')
                
            # fazer
            ScreenImage.wait_and_click('encerrar', "Encerrar",)
            sleep(5)
            
            ultimo_proc = ScreenImage.wait_and_click('ultimo_processo')
            if not ultimo_proc:
                ScreenImage.wait_and_click('encerrar', "Encerrar",)
            ScreenImage.wait_and_click('ultimo_processo',)
           
 
        except Exception as e:
            log.error(f'❌ ERRO ao detalhes de  processo: {e}')
            
    
    
            
    
        
        

        
        
