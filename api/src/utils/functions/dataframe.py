from time import sleep
import pandas as pd
import os
from api.src.scripts.seach_process.process_scripts import SeachProcess
from api.src.utils.logs.index import log

class DataFrameUtils:
    
    @staticmethod
    def data_frame(file_path: str, colunas_esperadas=None):
    
        if colunas_esperadas is None:
            colunas_esperadas = ["DATA RECEBIMENTO BCC AVULSO","HORA RECEBIMENTO BCC AVULSO", "PROCESSO"]

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"O arquivo '{file_path}' não foi encontrado.")

        try:
            df = pd.read_excel(file_path)  # Lê a planilha
        except Exception as e:
            raise ValueError(f"Erro ao ler o arquivo Excel: {e}")

        colunas_existentes = df.columns.tolist()
        colunas_faltantes = [col for col in colunas_esperadas if col not in colunas_existentes]

        return len(colunas_faltantes) == 0, colunas_faltantes, df  # Retorna o DataFrame lido
    
    @staticmethod
    def execute_data_frame(file_path):
        try:
            # Obtém o DataFrame e verifica se as colunas estão presentes
            todas_colunas_presentes, colunas_faltantes, df = DataFrameUtils.data_frame(file_path)

            if not todas_colunas_presentes:
                log.error(f"⚠️ As seguintes colunas estão ausentes: {', '.join(colunas_faltantes)}")
                return
            
            log.info("✅ Todas as colunas obrigatórias estão presentes!")
            
            # Garantindo que a coluna "Status" exista no DataFrame
            if "Status" not in df.columns:
                df["Status"] = ""
            
            # Iterando sobre cada linha do DataFrame
            for index, row in df.iterrows():
                if row["Status"] == 'Concluído':
                    log.success(f"⏭️ Linha {index + 1} já concluída. Pulando...")
                    continue  # Pula para a próxima linha sem processar
                
                
                log.info(f"📌 Processando linha {index + 1}: {row.to_dict()}")

                process = SeachProcess(row)  # Criando a instância corretamente
                process.process()  # Chamando a função process()
                sleep(15)
                
                 # Atualiza a coluna "Status" da linha correspondente
                df.at[index, "Status"] = "Concluído"

                # Salva no arquivo a cada iteração para garantir que os dados sejam preservados
                df.to_excel(file_path, index=False)
                log.success(f"✅ Linha {index + 1} processada e marcada como 'Concluído'.")
                
            log.sucesso("Automaçao Conluida com sucesso!")

        except FileNotFoundError as e:
            log.error(f"Erro: {e}")
        except ValueError as e:
            log.error(f"Erro ao ler o arquivo: {e}")
