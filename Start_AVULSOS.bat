@echo off
REM Definir o diretório do projeto
cd "%USERPROFILE%\Documents\automation-avulsos-rj-ce"

REM Ativar o ambiente virtual
call .venv\Scripts\activate

REM Executar o script Python
python main.py

REM Pausar a janela para visualizar mensagens
pause
