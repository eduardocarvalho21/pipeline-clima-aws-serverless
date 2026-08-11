import json
import boto3
import urllib.parse
from datetime import datetime

s3_client = boto3.client('s3')
BUCKET_SILVER = "open-weather-clima-silver"  

def lambda_handler(event, context):
    # Pode ser disparada via evento do S3 ou varredura de lote
    for record in event.get('Records', []):
        bucket_origem = record['s3']['bucket']['name']
        key_origem = urllib.parse.unquote_plus(record['s3']['object']['key'])
        
        # Lê o JSON do Bronze
        response = s3_client.get_object(Bucket=bucket_origem, Key=key_origem)
        conteudo = json.loads(response['Body'].read().decode('utf-8'))
        
        # Extrai e achata os dados da API
        registro_limpo = {
            "cidade": conteudo.get("name"),
            "pais": conteudo.get("sys", {}).get("country"),
            "lat": conteudo.get("coord", {}).get("lat"),
            "lon": conteudo.get("coord", {}).get("lon"),
            "temp": conteudo.get("main", {}).get("temp"),
            "sensacao_termica": conteudo.get("main", {}).get("feels_like"),
            "umidade": conteudo.get("main", {}).get("humidity"),
            "pressao": conteudo.get("main", {}).get("pressure"),
            "vento_velocidade": conteudo.get("wind", {}).get("speed"),
            "condicao_tempo": conteudo.get("weather", [{}])[0].get("description"),
            "data_medicao": datetime.utcfromtimestamp(conteudo.get("dt", 0)).strftime('%Y-%m-%d %H:%M:%S'),
            "ingestion_timestamp": conteudo.get("_ingestion_timestamp")
        }
        
        # Salva o arquivo em formato JSON Orientado a Linhas (NDJSON) na Silver
        # mantendo a mesma estrutura de partições de data
        filename = key_origem.split('/')[-1].replace('.json', '_processed.json')
        particao_caminho = "/".join(key_origem.split('/')[:-1])
        s3_key_silver = f"{particao_caminho}/{filename}"
        
        s3_client.put_object(
            Bucket=BUCKET_SILVER,
            Key=s3_key_silver,
            Body=json.dumps(registro_limpo) + "\n",
            ContentType='application/json'
        )
        print(f"Salvo Silver: {s3_key_silver}")

    return {"statusCode": 200, "body": "Transformação Concluída!"}
