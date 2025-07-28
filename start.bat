@echo off
REM Definir o diretório do projeto
cd "%USERPROFILE%\Documents\automation-avulsos-rj-ce"

REM Ativar o ambiente virtual
REM call .venv\Scripts\activate

REM Executar o script Python
start cmd /k "cd %cd% && .venv\Scripts\activate && python monitor.py"

REM Pausar a janela para visualizar mensagens
pause
