import os # Permite que Python "converse" com o sistema operacional
import json # Permite troca de dados na entre sistemas
import logging # Grava as ações da aplicação no arquivo
import random # Gera números aleatórios
import pandas as pd
import joblib # Carregar o modelo treinado

from datetime import datetime # Acessar o relógio do sistema operacional
from dotenv import load_dotenv # Importa o carregador de arquivo .env e injetar as variáveis
from fastapi import FastAPI, Request, Depends, HTTPException, status # Criar APIs
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials # Implementação de padrões de segurança
from fastapi.middleware.cors import CORSMiddleware

import signal # Para shutdown
from pydantic import BaseModel # Definir quais campos o Python deve esperar e validar no JSON recebido.

# 1. Carrega as variáveis do arquivo .env para o sistema
load_dotenv()

# Carregamento do Dataset encontrado no link de download RAW (bruto).
url = 'df_final.csv'
df = pd.read_csv( url,  sep=',' )

# 2. Captura as variáveis usando os nomes definidos no .env
APP_TITLE = os.getenv("APP_TITLE")
USERS_FILE = os.getenv("USERS_JSON_PATH")
LOG_FILE = os.getenv("LOG_FILE_PATH")

# Configuração de Log usando a variável do .env
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(message)s'
)

# CARREGAMENTO DO MODELO E SCALER (Régua Mágica)
# Certifique-se de que os nomes dos arquivos coincidem com os que você salvou
try:
    modelo = joblib.load('model_churn.pkl')
    scaler = joblib.load('scaler.pkl')
    colunas_do_modelo = joblib.load('model_columns.pkl') # A lista de nomes e ordem
    print("✅ Todos os 3 arquivos carregados com sucesso!")
except Exception as e:
    print(f"❌ Erro ao carregar arquivos: {e}")


# Limites passado para o modelo:
limites = {
    'tenure': {'min': int(df['tenure'].min()), 'max': int(df['tenure'].max())},
    'MonthlyCharges': {'min': float(df['MonthlyCharges'].min()), 'max': float(df['MonthlyCharges'].max())},
    'TotalCharges': {'min': float(df['TotalCharges'].min()), 'max': float(df['TotalCharges'].max())}
}

app = FastAPI(
    title=APP_TITLE,
    description="API de Predição de Churn para o Hackathon One",
    version="1.0.0",
    openapi_url="/openapi.json", # Caminho interno
    docs_url="/docs",           # Caminho interno
    root_path="/python"         # <--- ESTA É A CHAVE!
    ) # Criando o "servidor" que vai ouvir as requisições na internet.

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Em produção, substitua pelo domínio do seu frontend
    allow_credentials=True,
    allow_methods=["*"],      # Permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],      # Permite todos os headers
)

security = HTTPBearer()

# Estrutura dos dados à receber. Seus valores padrões.
class ClienteSchema(BaseModel):
    tenure: int = 0
    MonthlyCharges: float = 0
    TotalCharges: float = 0
    gender_Male: int = 0
    Partner_Yes: int = 0
    Dependents_Yes: int = 0
    PhoneService_Yes: int = 0
    MultipleLines_Yes: int = 0
    InternetService_Fiber_optic: int = 0  # Note: Pydantic troca espaços por _
    InternetService_No: int = 1
    OnlineSecurity_Yes: int = 0
    OnlineBackup_Yes: int = 0
    DeviceProtection_Yes: int = 0
    TechSupport_Yes: int = 0
    StreamingTV_Yes: int = 0
    StreamingMovies_Yes: int = 0
    Contract_One_year: int = 0
    Contract_Two_year: int = 0
    PaperlessBilling_Yes: int = 0
    PaymentMethod_Credit_card_automatic: int = 0
    PaymentMethod_Electronic_check: int = 0
    PaymentMethod_Mailed_check: int = 0

# Mapeamento para lertura correta das colunas conforme o modelo treinado
MAPA_NOMES_COLUNAS = {
    "PaymentMethod_Credit_card_automatic": "PaymentMethod_Credit card (automatic)",
    "PaymentMethod_Bank_transfer_automatic": "PaymentMethod_Bank transfer (automatic)",
    "PaymentMethod_Mailed_check": "PaymentMethod_Mailed check",
    "PaymentMethod_Electronic_check": "PaymentMethod_Electronic check",
    "Contract_One_year": "Contract_One year",
    "Contract_Two_year": "Contract_Two year",
    "InternetService_Fiber_optic": "InternetService_Fiber optic"
}

 # --- FUNÇÕES AUXILIARES ---
def carregar_usuarios():
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def get_current_user(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    usuarios = carregar_usuarios()
    token = credentials.credentials
    if token in usuarios:
        request.state.user_name = usuarios[token]
        return usuarios[token]
    request.state.user_name = "ANÔNIMO"
    raise HTTPException(status_code=401, detail="Token inválido")

# --- ENDPOINTS ---

@app.get("/metadata")
def get_metadata():
    """Retorna os limites máximos e mínimos para validação no Frontend"""
    return limites

@app.post("/predict")
def predict(input_data: ClienteSchema, user: str = Depends(get_current_user)):

    try:
        # 1. Converte o Pydantic para dicionário
        dados = input_data.dict()

        # 2. TRADUÇÃO INTELIGENTE
        dados_formatados = {}
        for chave, valor in dados.items():
            # Tenta tradução específica primeiro, senão faz o replace padrão
            nova_chave = MAPA_NOMES_COLUNAS.get(chave, chave.replace('_', ' '))
            dados_formatados[nova_chave] = valor
        
        # 3. Cria o DataFrame
        df = pd.DataFrame([dados_formatados])

        # 4. Alinhamento com model_columns (Garante ordem e TotalCharges)
        df = df.reindex(columns=colunas_do_modelo, fill_value=0)

        # 5. Escalonamento (Agora o scaler reconhece os nomes!)
        df_scaled = scaler.transform(df)

        # 6. Predição
        probabilidades = modelo.predict_proba(df_scaled)[0] # [prob_nao_cancelar, prob_cancelar]
        classe_predita = modelo.predict(df_scaled)[0]
        
        # Pega a probabilidade da classe que o modelo escolheu
        confianca = probabilidades[classe_predita]
        
        res = "Vai cancelar" if classe_predita == 1 else "Não vai cancelar"
        
        return {
            "previsao": res,
            "probabilidade": float(round(confianca * 100, 2))
        }

    except Exception as e:
        return {"detail": f"Erro no processamento: {str(e)}"}

@app.get("/shutdown")
def shutdown(user: str = Depends(get_current_user)):
    if user != "Luciano":
        raise HTTPException(status_code=403, detail="Acesso negado")
    os.kill(os.getpid(), signal.SIGTERM)
    return {"message": "Reiniciando..."}