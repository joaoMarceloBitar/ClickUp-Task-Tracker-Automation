from fastapi import FastAPI
from app.schemas import DiagnosticoLead
from app.database import salvar_lead
from app.clickup import criar_tarefa

app = FastAPI()

@app.get("/")
def read_root():
    return {"teste"}


@app.post("/webhook/diagnostico")
def receber_diagnostico(lead: DiagnosticoLead):

    resultado_db = salvar_lead(lead)

    resposta_clickup = criar_tarefa(lead)

    return {
        "status": "sucesso",
        "supabase": resultado_db,
        "clickup": resposta_clickup
    }