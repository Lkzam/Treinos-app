import jwt
import datetime

secret_key = 'lkzam'

# Payload
payload = {
    'id': 1,  # Exemplo de ID de aluno
    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Expiração em 1 hora
}

# Gerar o token
token = jwt.encode(payload, secret_key, algorithm='HS256')

print("Token gerado:", token)
