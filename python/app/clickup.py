import os
import requests
from dotenv import load_dotenv
from app.schemas import DiagnosticoLead

load_dotenv()
CLICKUP_API_TOKEN = os.getenv("CLICKUP_API_TOKEN")
CLICKUP_LIST_ID = os.getenv("CLICKUP_LIST_ID")


def criar_tarefa(lead: DiagnosticoLead):
    url = f"https://api.clickup.com/api/v2/list/{CLICKUP_LIST_ID}/task"

    headers = {
        "Authorization": CLICKUP_API_TOKEN,
        "Content-Type": "application/json"
    }

    payload = {
        "name": f"Lead - {lead.nome}",
        "description": f"""
Nome: {lead.nome}
Telefone: {lead.telefone}
Email: {lead.email}
Especialidade: {lead.especialidade}

Desafio:
{lead.principal_desafio}
"""
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers
    )

    print("STATUS:", response.status_code)
    print("RESPOSTA:", response.text)

    return response.json()