# 📊 Projeto de Engenharia de Dados – Pipeline End-to-End

Este projeto tem como objetivo implementar, na prática, um **pipeline completo de Engenharia de Dados**, seguindo uma arquitetura moderna utilizada no mercado, desde a ingestão dos dados até a disponibilização para consumo analítico.

O foco principal é **engenharia de dados**, com extensões planejadas para **análise de dados e ciência de dados**, permitindo uma visão clara de todo o ciclo de vida dos dados e das responsabilidades de cada etapa.

---

## 🎯 Objetivos do Projeto

- Construir um pipeline de dados **end-to-end**
- Aplicar boas práticas de Engenharia de Dados
- Separar claramente as camadas de dados:
  - ingestão
  - armazenamento
  - transformação
  - consumo
- Criar um projeto **reprodutível**, organizado e adequado para portfólio

---

## 🧱 Arquitetura Geral

Fluxo de dados implementado no projeto:

1°- (API + Dados Simulados) (Fontes de Dados)
2°- Ingestão (Python)
3°- Data Lake (MinIO / S3-like)
4°- Staging (Postgres - JSONB)
5°- Camada Silver (dbt)
6°- Camada Gold (planejada)
7°- BI / Análise / Ciência de Dados (planejado)

---

## 📌 Fontes de Dados

- **API externa**: dados de produtos (Fake Store API)
- **Dados simulados**:
  - clientes
  - pedidos

Essa combinação simula um cenário realista, integrando:
- dados internos (sistemas transacionais)
- dados externos (APIs de terceiros)

---

## 🗂️ Camadas de Dados

### [X] Data Lake (Landing / Bronze)
- Armazenamento de dados brutos
- Versionamento por data (`dt=YYYY-MM-DD`)
- Implementado com **MinIO**, simulando um ambiente S3 (AWS)

### [X] Staging
- Banco relacional **PostgreSQL**
- Dados armazenados em formato **JSONB**
- Camada intermediária para flexibilidade, auditoria e reprocessamento

### [ ] Silver
- Transformações realizadas com **dbt**
- Tipagem e normalização dos dados
- Dados limpos e estruturados, prontos para modelagem analítica

### [ ] Gold
- Modelo dimensional (Star Schema)
- Tabelas fato e dimensões
- Dados prontos para consumo por BI e análises

---

## 🛠️ Tecnologias Utilizadas

- **Python** – ingestão e integração de dados
- **Docker & Docker Compose** – infraestrutura local
- **PostgreSQL** – staging e camadas analíticas
- **MinIO** – Data Lake (S3 local)
- **dbt** – transformações e modelagem analítica
- **WSL (Linux)** – ambiente de desenvolvimento

---

## ✅ Etapas Concluídas

- [x] Configuração da infraestrutura com Docker
- [x] Implementação do Data Lake (MinIO)
- [x] Pipeline de ingestão em Python
- [x] Staging no Postgres com JSONB
- [x] Configuração do dbt
- [x] Criação dos primeiros models da camada Silver

---

## 🚧 Próximas Etapas Planejadas

- [ ] Finalizar camada Silver
- [ ] Criar camada Gold (Star Schema)
- [ ] Implementar testes de qualidade de dados (dbt tests)
- [ ] Orquestrar o pipeline (Airflow ou Prefect)
- [ ] Criar dashboards de BI
- [ ] Realizar análise exploratória dos dados
- [ ] Extensão para Ciência de Dados (opcional)
