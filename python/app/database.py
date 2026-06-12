import os
from app.schemas import DiagnosticoLead
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("URL:", os.getenv("SUPABASE_URL"))
print("KEY:", os.getenv("SUPABASE_KEY"))

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)        


def salvar_lead(lead: DiagnosticoLead):

    payload = {
        "nome": lead.nome,
        "telefone": lead.telefone,
        "email": lead.email,
        "especialidade": lead.especialidade,
        "principal_desafio": lead.principal_desafio,
    }

    try:
        result = (
            supabase
            .table("diagnosticoCliente")
            .insert(payload)
            .execute()
        )

        print("RESULTADO:", result)

        return result

    except Exception as e:
        print("ERRO:", e)
        raise
