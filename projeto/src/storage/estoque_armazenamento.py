import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def listar_itens():
    """Busca da nuvem e converte para o formato JSON original esperado pela API."""
    resposta = supabase.table("produto").select("*").execute()

#Recria a estrutura original do JSON: 
# {"NOME": {"quantidade": X, "limite_minimo": Y}}
    estoque_legado = {}
    for item in resposta.data:
        estoque_legado[item["nome"]] = {
            "quantidade": item["quantidade"],
            "limite_minimo": item["limite_minimo"],
            "status": item["status"] 
        }

    return estoque_legado

def adicionar_item(nome: str, quantidade: int, limite_minimo: int):
    """Insere o produto no PostgreSQL."""
    status_calculado = "Repor" if quantidade <= limite_minimo else "Ok"

    novo_produto = {
        "nome": nome,
        "quantidade": quantidade,
        "limite_minimo": limite_minimo,
        "status": status_calculado
    }

    resposta = supabase.table("produto").insert(novo_produto).execute()
    return resposta.data

def atualizar_quantidade(nome_produto: str, nova_quantidade: int, limite_minimo: int):
    """Atualiza buscando pelo nome, já que o JSON original usava o nome como chave."""
    status_calculado = "Repor" if nova_quantidade <= limite_minimo else "Ok"

    dados_atualizados = {
        "quantidade": nova_quantidade,
        "status": status_calculado
    }
#Atualiza a linha onde a coluna 'nome' for igual ao nome_produto
    resposta = (
        supabase.table("produto")
        .update(dados_atualizados)
        .eq("nome", nome_produto)
        .execute())
    return resposta.data

def remover_item(nome_produto: str):
    """Remove o produto do banco de dados pelo nome."""
    resposta = supabase.table("produto").delete().eq("nome", nome_produto).execute()
    return resposta.data