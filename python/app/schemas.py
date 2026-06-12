from pydantic import BaseModel, Field, field_validator
import re   

class DiagnosticoLead(BaseModel):
    nome: str = Field(...,min_length=3, max_length=100)
    telefone: str = Field(...,min_length=10, max_length=15)
    email: str = Field(...,pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    especialidade: str = Field(...,min_length=2, max_length=100)
    principal_desafio: str = Field(...,min_length=10, max_length=200)

    @field_validator('nome')
    @classmethod
    def padronizar_nome(cls, valor: str) -> str:
        return " ".join(valor.split()).title()
    
    @field_validator('email')
    @classmethod
    def padronizar_email(cls, valor: str) -> str:
        return valor.strip()
    
    @field_validator('telefone')
    @classmethod
    def padronizar_telefone(cls, valor: str) -> str:
        numeros = re.sub(r'\D', '', valor)
        
        if len(numeros) < 10 or len(numeros) > 11:
            raise ValueError('O telefone deve conter 10 ou 11 dígitos, incluindo o DDD.')
        
        if len(numeros) == 11:
            return f"({numeros[:2]}) {numeros[2:7]}-{numeros[7:]}"
        
        return f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:]}"
    

    @field_validator('especialidade', 'principal_desafio')
    @classmethod
    def limpar_textos(cls, valor: str) -> str:
        return " ".join(valor.split()).capitalize()