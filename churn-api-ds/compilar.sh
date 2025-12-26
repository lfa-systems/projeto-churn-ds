#!/bin/bash

APP_NAME="run_server"
ENTRY_POINT="run_server.py"

mostrar_ajuda() {
    echo "Uso: ./compilar.sh [OPÇÃO]"
    echo ""
    echo "Opções:"
    echo "  --run          Executa em modo dev (com reload)."
    echo "  --build        Compila o executável (terminal visível)."
    echo "  --build-hide   Compila o executável (modo noconsole)."
    echo "  --start        Inicia o binário em SEGUNDO PLANO (Background)."
    echo "  --stop         Para o servidor que está em background."
    echo "  --status       Verifica se o servidor está rodando."
    echo "  --help         Mostra esta ajuda."
    exit 0
}

# --- LOGICA DE EXECUÇÃO ---

case "$1" in
    --run)
        echo "[DEV] Iniciando com Uvicorn..."
        uvicorn main:app --reload
        ;;
    --build)
        pyinstaller --onefile --hidden-import=uvicorn.logging --hidden-import=uvicorn.loops.auto --hidden-import=uvicorn.protocols.http.auto --hidden-import=uvicorn.lifespan.on $ENTRY_POINT
        cp .env usuarios.json dist/ 2>/dev/null
        ;;
    --build-hide)
        pyinstaller --onefile --noconsole --hidden-import=uvicorn.logging --hidden-import=uvicorn.loops.auto --hidden-import=uvicorn.protocols.http.auto --hidden-import=uvicorn.lifespan.on $ENTRY_POINT
        cp .env usuarios.json dist/ 2>/dev/null
        ;;
    --start)
        if [ ! -f "dist/$APP_NAME" ]; then
            echo "[ERRO] Executável não encontrado em dist/. Compile primeiro."
            exit 1
        fi
        # O segredo do background real no Linux:
        nohup ./dist/$APP_NAME > /dev/null 2>&1 &
        echo "[OK] Servidor iniciado em background. PID: $!"
        ;;
    --stop)
        PID=$(pgrep -f $APP_NAME)
        if [ -z "$PID" ]; then
            echo "[AVISO] Nenhum servidor encontrado rodando."
        else
            kill $PID
            echo "[OK] Servidor (PID $PID) encerrado."
        fi
        ;;
    --status)
        PID=$(pgrep -f $APP_NAME)
        if [ -z "$PID" ]; then
            echo "[-] Servidor está PARADO."
        else
            echo "[+] Servidor está RODANDO (PID: $PID)."
        fi
        ;;
    *)
        mostrar_ajuda
        ;;
esac