# Análise de Dados Ambientais do Pantanal

Aplicação interativa para leitura, tratamento e visualização de dados 
ambientais em séries temporais. O usuário pode carregar um arquivo CSV 
próprio ou explorar o conjunto de dados de exemplo incluído.

---

## Funcionalidades

- Upload de arquivo CSV com validação automática de colunas
- Diagnóstico de dados faltantes por variável
- Tratamento por interpolação linear (adequado para séries temporais contínuas)
- Cálculo de estatísticas descritivas (média por variável)
- Visualização interativa da evolução temporal de temperatura, nível do rio e NDVI

---

## Formato esperado do CSV

| Coluna         | Tipo     | Descrição                                      |
|----------------|----------|------------------------------------------------|
| data           | datetime | Data da observação                             |
| temperatura_c  | float    | Temperatura em graus Celsius                   |
| nivel_rio_m    | float    | Nível do rio em metros                         |
| ndvi           | float    | Índice de Vegetação por Diferença Normalizada  |

---

## Como executar

**Pré-requisitos:** Python 3.8+

```bash
$ git clone https://github.com/RebecaLameira/inpp-pantanal.git
$ cd inpp-pantanal
$ pip install -r requirements.txt
$ streamlit run app.py
```

Acesse em: `http://localhost:8501`

---

## Estrutura do projeto

```
├── app.py               # Aplicação principal
├── dados_pantanal.csv   # Dataset de exemplo
├── requirements.txt     # Dependências
└── README.md
```

## Decisões técnicas

**Streamlit** — escolhido por permitir construir interfaces orientadas 
a dados diretamente em Python, sem necessidade de frontend separado. 
Adequado para protótipos e ferramentas científicas.

**Interpolação linear** — adotada para preenchimento de valores ausentes 
por ser matematicamente apropriada para séries temporais ambientais com 
variação gradual. Alternativas como média global ou mediana foram 
descartadas por não preservarem a tendência temporal dos dados.

**Plotly** — utilizado para visualização por gerar gráficos interativos 
(zoom, hover, exportação) sem configuração adicional, aumentando a 
usabilidade da ferramenta.

---

## Possíveis evoluções

- Detecção automática de anomalias na série temporal
- Exportação dos dados tratados em CSV
- Integração com APIs de dados ambientais em tempo real
- Análise de correlação entre variáveis (temperatura × NDVI × nível do rio)
