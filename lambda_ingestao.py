import json
import os
import urllib.request
import urllib.parse
from datetime import datetime
import boto3

s3_client = boto3.client('s3')

BUCKET_BRONZE = "open-weather-clima-bronze"  
CIDADES = ["Sao Paulo,BR", "Rio de Janeiro,BR", "Brasilia,BR", "Lisbon,PT"]
API_KEY = os.environ.get("OPENWEATHER_API_KEY")

def lambda_handler(event, context):
    agora = datetime.utcnow()
    timestamp_epoch = int(agora.timestamp())
    
    for cidade in CIDADES:
        cidade_limpa = cidade.split(',')[0].replace(' ', '_').lower()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={urllib.parse.quote(cidade)}&appid={API_KEY}&units=metric"
        
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                dados = json.loads(response.read().decode('utf-8'))
                dados['_ingestion_timestamp'] = agora.isoformat()
                
                # S3 Key particionado: clima/ano=YYYY/mes=MM/dia=DD/
                s3_key = (
                    f"clima/ano={agora.year}/mes={agora.strftime('%m')}/dia={agora.strftime('%d')}/"
                    f"{cidade_limpa}_{timestamp_epoch}.json"
                )
                
                s3_client.put_object(
                    Bucket=BUCKET_BRONZE,
                    Key=s3_key,
                    Body=json.dumps(dados),
                    ContentType='application/json'
                )
                print(f"Salvo Bronze: {s3_key}")
        except Exception as e:
            print(f"Erro em {cidade}: {str(e)}")

    return {"statusCode": 200, "body": "Ingestão Bronze Concluída!"}
