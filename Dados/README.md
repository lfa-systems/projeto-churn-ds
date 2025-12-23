#### 📘 Dicionário de dados do DataSet
`WA_Fn-UseC_-Telco-Customer-Churn_dicionario.csv`

* `customerID`: número de identificação único de cada cliente
* `gender`: gênero (masculino e feminino) 
* `SeniorCitizen`: informação sobre um cliente ter ou não idade igual ou maior que 65 anos 
* `Partner`:  se o cliente possui ou não um parceiro ou parceira
* `Dependents`: se o cliente possui ou não dependentes
* `tenure`:  meses de contrato do cliente
* `PhoneService`: assinatura de serviço telefônico 
* `MultipleLines`: assisnatura de mais de uma linha de telefone 
* `InternetService`: assinatura de um provedor internet 
* `OnlineSecurity`: assinatura adicional de segurança online 
* `OnlineBackup`: assinatura adicional de backup online 
* `DeviceProtection`: assinatura adicional de proteção no dispositivo 
* `TechSupport`: assinatura adicional de suporte técnico| menos tempo de espera
* `StreamingTV`: assinatura de TV a cabo 
* `StreamingMovies`: assinatura de streaming de filmes 
* `Contract`: tipo de contrato
* `PaperlessBilling`: se o cliente prefere receber online a fatura
* `PaymentMethod`: forma de pagamento
* `MonthlyCharges`: total de todos os serviços do cliente por mês
* `TotalCharges`: total gasto pelo cliente
* `Churn`: se o cliente deixou ou não a empresa 

----
## 🤝 Este dicionário é essencial para o time de Data Science (DS) e para o time de Back-end (Backend) que criará os DTOs.

| Coluna | Descrição |Tipo de Dado (Para Modelagem) | Categorias / Valores Esperados | Observações Críticas (Limpeza) |
| :--- | :--- | :--- | :--- | :--- | 
| `customerID` | Número de identificação único do cliente. |ID (String) | Único para cada linha. | Não usar na modelagem (remover).|
| `gender` | Gênero do cliente. | Categórica (Nominal) |"{'Female', 'Male'}"|Pré-processamento: One-Hot Encoding (OHE).|
| `SeniorCitizen` | Cliente com idade ≥65 anos. | Binária | "{0: Não, 1: Sim}" |"Converter para o formato 0/1| se não estiver assim."|
| `Partner` | O cliente possui parceiro(a).| Binária | "{'Yes', 'No'}" | OHE. |
| `Dependents` | O cliente possui dependentes.| Binária|"{'Yes', 'No'}"|OHE.|
| `tenure` | Meses de contrato do cliente com a empresa.| Numérica (Discreta)|Intervalo de 0 a 72 (máximo de 6 anos).| StandardScaler.|
| `PhoneService` | Assinatura de serviço telefônico.| Binária |"{'Yes', 'No'}"|OHE.|
| `MultipleLines`| Assinatura de mais de uma linha de telefone.|Categórica (Ternária)|"{'Yes', 'No', 'No phone service'}"|OHE.|
| `InternetService`| Provedor de internet assinado.| Categórica (Nominal)|"{'DSL', 'Fiber optic', 'No'}"|OHE.|
| `OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies` | Assinaturas adicionais (segurança, backup, etc.).|Categórica (Ternária)|"{'Yes', 'No', 'No internet service'}"|OHE.|
| `Contract` | Tipo de contrato.|Categórica (Nominal)| "{'Month-to-month', 'One year', 'Two year'}"|OHE.|
| `PaperlessBilling` | Preferência de fatura (online).|Binária|"{'Yes', 'No'}"|OHE.|
| `PaymentMethod` | Forma de pagamento utilizada.| Categórica (Nominal)|"{'Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'}"|OHE.|
| `MonthlyCharges` | Total de todos os serviços do cliente por mês.|Numérica (Contínua)| Valores em dólar.|StandardScaler.|
| `TotalCharges` | Total gasto pelo cliente durante todo o contrato.|Numérica (Contínua)| Valores em dólar.| CRÍTICO: Converter de String/Object para Float. Contém nulos (NaN) que devem ser removidos.|
| `Churn` | Se o cliente cancelou o serviço (Target / Rótulo).| Target Binária (0 ou 1)|"{'Yes': 1, 'No': 0}"|Variável de Saída (Target): Deve ser mapeada para 0 e 1.|

## 🔄 O que é One-Hot Encoding (OHE)?
O One-Hot Encoding (OHE) é uma técnica de pré-processamento essencial em Machine Learning para transformar variáveis categóricas (texto) em um formato numérico que os algoritmos podem processar. É orquestrado pelo objeto ColumnTransformer (do scikit-learn)

### 🧪 Exemplo Prático (Aplicado ao projeto-churn-ds)
Usando a variável `InternetService` do dataset| que possui três categorias:

|Cliente|InternetService|
| :--- | :---|
| A |DSL
| B |Fibra Ótica|
| C |Não|

### 🔢 Após o OHE| a tabela de features fica assim:

|Cliente |InternetService_DSL|InternetService_Fibra_Ótica|InternetService_Não|
|:---|:---|:---|:---|
|A|1|0|0|
|B|0|1|0|
|C|0|0|1|

## 🔄 O que é o StandardScaler?
Se o One-Hot Encoding lida com texto| o StandardScaler lida com números.
O StandardScaler é uma ferramenta do scikit-learn (Python) que transforma as variáveis numéricas. 
Essa transformação é conhecida como padronização Z-score ou normalização Z-score.

### 🧪 Exemplo Prático (Aplicado ao projeto-churn-ds)
Usaremos variáveis numéricas em escalas muito diferentes:

| Variável | Escala Típica |
| :--- | :--- |
| `tenure` (Meses de Contrato) | De 0 a 72 |
| `MonthlyCharges` (Cobrança Mensal) | De 20 a 120 |
| `TotalCharges` (Cobrança Total) | De 0 a $\approx 8600$ |

Se você alimentar essas colunas diretamente em modelos como Regressão Logística| K-Nearest Neighbors (KNN) ou Redes Neurais| **o algoritmo pode dar uma importância desproporcional** à coluna com os valores mais altos| como TotalCharges.

🧪 **Exemplo**: Uma mudança de 1 unidade em `TotalCharges` (8600 $\rightarrow$ 8601) seria interpretada como muito mais significativa do que uma mudança de 1 unidade em `tenure` (3 $\rightarrow$ 4)| mesmo que a mudança no `tenure` seja mais relevante para prever o Churn.


## 🔄 Tabela de Tradução: CSV Original vs. Estrutura do Modelo

|Coluna no CSV Original|Tipo no CSV|O que virou no Modelo (Dicionário)|Regra de Transformação|
|---|---|---|---|
|**customerID**|object|(Removido)|Identidade não importa para o comportamento.|
|**gender**|object|gender_Male|"1 se for Homem| 0 se for Mulher."|
|**SeniorCitizen**|int64|SeniorCitizen|Já é 0 ou 1 (Mantido).|
|**Partner**|object|Partner_Yes|"""Yes"" vira 1| ""No"" vira 0."|
|**Dependents**|object|Dependents_Yes|"""Yes"" vira 1| ""No"" vira 0."|
|**tenure**|int64|tenure|Número de meses (Mantido).|
|**PhoneService**|object|PhoneService_Yes|"""Yes"" vira 1| ""No"" vira 0."|
|**MultipleLines**|object|MultipleLines_Yes|"""Yes"" vira 1| ""No"" vira 0."|
|**InternetService**|object|InternetService_Fiber optic|"Se for ""Fiber optic"" vira 1."|
|**InternetService**|object|InternetService_No|Se não tiver internet vira 1.|
|**OnlineSecurity**|object|OnlineSecurity_Yes|"""Yes"" vira 1| o resto vira 0."|
|**OnlineBackup**|object|OnlineBackup_Yes|"""Yes"" vira 1| o resto vira 0."|
|**DeviceProtection**|object|DeviceProtection_Yes|"""Yes"" vira 1| o resto vira 0."|
|**TechSupport**|object|TechSupport_Yes|"""Yes"" vira 1| o resto vira 0."|
|**StreamingTV**|object|StreamingTV_Yes|"""Yes"" vira 1| o resto vira 0."|
|**StreamingMovies**|object|StreamingMovies_Yes|"""Yes"" vira 1| o resto vira 0."|
|**Contract**|object|Contract_One year|Se for contrato de 1 ano vira 1.|
|**Contract**|object|Contract_Two year|Se for contrato de 2 anos vira 1.|
|**PaperlessBilling**|object|PaperlessBilling_Yes|"""Yes"" vira 1| ""No"" vira 0."|
|**PaymentMethod**|object|PaymentMethod_Electronic check|Se pagar com cheque eletrônico vira 1.|
|**PaymentMethod**|object|PaymentMethod_Mailed check|Se pagar com cheque via correio vira 1.|
|**PaymentMethod**|object|PaymentMethod_Credit card (automatic)|Se for cartão automático vira 1.|
|**MonthlyCharges**|float64|MonthlyCharges|Valor mensal (Mantido).|
|**TotalCharges**|object|TotalCharges|Convertido de Texto para Número.|
|**Churn**|object|y_train / y_test|O gabarito que o robô tenta adivinhar.|



---
## 📜 Informações do Documento

| Campo | Detalhe |
| :--- | :--- |
| **Autor Principal** | Luciano Azevedo |
| **Data da Criação** | 16 de Dezembro de 2025 |
| **Última Atualização** | 16 de Dezembro de 2025 |
| **Versão** | 1.0 |