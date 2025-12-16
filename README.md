# HACKATHON_FLIGHT_ON_TIME

# ✈️ Roteiro de Projeto FlightOnTime (MVP)

O objetivo é criar um pipeline completo:

**Dados Históricos → Modelo Preditor → API REST**

---

## 🎯 Fase 1: Planejamento e Acordo (10% do Tempo)

Esta fase é crítica e deve envolver ambos os times para garantir a compatibilidade.

### 1. 🤝 Contrato de Integração e Dicionário de Features

| Item | Ação | Responsável |
|---|---|---|
| Definição da Alvo | Confirmar a variável alvo: `ARR_DEL15` (0 = Pontual, 1 = Atrasado) | DS |
| Inputs da API | Definir as variáveis de entrada que a API receberá (`companhia`, `origem`, `destino`, `data_partida`, `distancia_km`) | BE + DS |
| Output da API | Definir a estrutura de saída (`previsao`, `probabilidade`) | BE + DS |
| Dicionário de Features | Definir a lista final de features usadas após o processamento (ex: `DAY_OF_WEEK`, `CRS_DEP_HOUR`, `Encoded ORIGIN_AIRPORT_ID`). Garante que o BE replique o pré-processamento corretamente. | DS |

---

## 📊 Fase 2: Data Science – Análise e Modelagem (40% do Tempo)

O time de DS foca em criar o modelo preditivo conforme as colunas definidas na Fase 1.

### 2. 📁 Coleta e Limpeza de Dados *(Notebook: EDA e Limpeza)*

| Passo | Ação | Código Python Principal |
|---|---|---|
| 2.1 Coleta | Baixar o dataset de voo individual (ex: BTS ou Kaggle) | `pd.read_csv()` |
| 2.2 Limpeza | Remover *Data Leakage* (`DEP_TIME`, `ARR_TIME`, `CARRIER_DELAY`, etc.) | `df.drop(columns=...)` |
| 2.3 Alvo | Tratar valores ausentes (NaN) em `ARR_DEL15` e converter para `int` (0 ou 1) | `df.dropna(subset=['ARR_DEL15'])` |
| 2.4 EDA | Análise Exploratória: distribuição da alvo, correlações e desbalanceamento | `df['ARR_DEL15'].value_counts()` |

### 3. ✨ Engenharia de Recursos *(Notebook: Feature Engineering)*

| Passo | Ação | Código Python Principal |
|---|---|---|
| 3.1 Data/Tempo | Converter `FL_DATE` para `datetime`. Criar `DAY_OF_WEEK` e `MONTH` | `pd.to_datetime()`, `dt.dayofweek`, `dt.month` |
| 3.2 Horário | Criar `CRS_DEP_HOUR` a partir de `CRS_DEP_TIME` (`// 100`) | `df['CRS_DEP_TIME'] // 100` |
| 3.3 Codificação | Aplicar One-Hot ou Label Encoding nas variáveis categóricas. Salvar encoder se necessário | `pd.get_dummies(X)` |
| 3.4 Dataset | Criar o dataset final `X` (features) e `Y` (alvo) | `X.drop(columns=['ARR_DEL15'])` |

### 4. 🧠 Modelagem e Exportação *(Notebook: Modelagem e Exportação)*

| Passo | Ação | Código Python Principal |
|---|---|---|
| 4.1 Divisão | Dividir dados em Treino e Teste | `train_test_split(X, Y, test_size=0.2)` |
| 4.2 Treinamento | Treinar um modelo de Classificação (ex: RandomForest ou Logistic Regression) | `model.fit(X_train, Y_train)` |
| 4.3 Avaliação | Avaliar desempenho (Acurácia, F1, Matriz de Confusão) | `classification_report(Y_test, Y_pred)` |
| 4.4 Exportação | Exportar o modelo treinado | `joblib.dump(model, 'flight_model.joblib')` |

---

## 💻 Fase 3: Back-End – Construção da API (40% do Tempo)

O time de Back-End constrói o serviço web que irá hospedar e servir as previsões do modelo.

### 5. 🏗️ Setup e Estrutura da API *(Java / Spring Boot)*

| Passo | Ação | Código Java / Spring Boot |
|---|---|---|
| 5.1 Setup | Criar projeto Spring Boot e configurar dependências básicas | Spring Initializr |
| 5.2 Definição | Criar DTOs de Entrada (`FlightRequest`) e Saída (`PredictionResponse`) | Classes Java com `@RequestBody` / `@ResponseBody` |
| 5.3 Interface | Criar Controller com endpoint `POST /predict` | `@RestController`, `@PostMapping("/predict")` |

### 6. 🔗 Integração do Modelo *(API / Microserviço)*

| Passo | Ação | Detalhe da Integração |
|---|---|---|
| 6.1 Carregamento | Definir mecanismo de integração com o modelo serializado | **Opção 1 (MVP):** Microserviço Python (Flask/FastAPI). **Opção 2:** ONNX/PMML (avançado). |
| 6.2 Pré-Processamento | Replicar exatamente a Engenharia de Recursos do DS | Serviço `FlightFeatureService` no Spring |
| 6.3 Chamada | Implementar chamada ao modelo | `RestTemplate` ou `WebClient` |

### 7. ✅ Funcionalidades Exigidas *(MVP)*

| Passo | Ação | Critério de Sucesso |
|---|---|---|
| 7.1 Validação | Validar campos da entrada JSON | Retornar **HTTP 400** se campos obrigatórios estiverem ausentes |
| 7.2 Resposta | Formatar saída com previsão e probabilidade | `{"previsao": "Atrasado", "probabilidade": 0.78}` |

---

## 🚀 Fase 4: Demonstração e Documentação (10% do Tempo)

### 8. 📝 Documentação e Teste

| Entregável | Ação | Responsável |
|---|---|---|
| Notebook DS | Finalizar e limpar notebook (EDA, FE, Modelagem, Avaliação) | DS |
| README | Criar README com instruções, dependências e exemplos | BE + DS |
| Demonstração | Preparar 3 exemplos (Pontual, Atrasado e Erro de Validação) | BE |

---

> Este roteiro oferece uma visão clara, modular e paralelizável. Após a Fase 1, os times podem trabalhar de forma independente com baixo acoplamento.
