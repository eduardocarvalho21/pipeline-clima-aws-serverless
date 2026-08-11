# 🌤️ Pipeline de Dados Climáticos Serverless na AWS (Free Tier)

![AWS Lambda](https://img.shields.io/badge/AWS_Lambda-Serverless-orange?logo=awslambda)
![Amazon S3](https://img.shields.io/badge/Amazon_S3-Data_Lake-green?logo=amazons3)
![Amazon Athena](https://img.shields.io/badge/Amazon_Athena-SQL-blue?logo=amazonathena)
![Python](https://img.shields.io/badge/Python-3.12-yellow?logo=python)
![Architecture](https://img.shields.io/badge/Architecture-Medallion-purple)

Pipeline de Engenharia de Dados *Serverless* e *Event-Driven* construído na AWS utilizando exclusivamente a **camada gratuita (Free Tier)**. O projeto realiza a ingestão, tratamento e disponibilização de dados meteorológicos globais em tempo real sob o conceito de **Arquitetura Medallion (Camadas Bronze e Silver)**.

---

## 📐 Arquitetura da Solução

```text
[ API OpenWeatherMap ]
         │
      (HTTPS)
         ▼
[ AWS Lambda (Ingestão) ] ◄── (Trigger: EventBridge Cron - 1h)
         │
      (JSON Bruto)
         ▼
[ Amazon S3 (Camada Bronze) ]
         │
   (S3 Event Notification)
         ▼
[ AWS Lambda (Transformação) ]
         │
     (NDJSON Limpo)
         ▼
[ Amazon S3 (Camada Silver) ]
         │
      (DDL Schema)
         ▼
[ Amazon Athena ] ──► Consultas SQL Analíticas
