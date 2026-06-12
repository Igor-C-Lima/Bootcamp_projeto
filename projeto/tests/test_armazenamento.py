from unittest.mock import patch, MagicMock
from src.storage.estoque_armazenamento import (
    listar_itens,
    adicionar_item,
    atualizar_quantidade,
    remover_item
)

# Fizemos o "mock" (simulação) do supabase para não alterar o banco real
@patch("src.storage.estoque_armazenamento.supabase")
def test_listar_itens(mock_supabase):
    # Simulando o retorno do banco de dados
    mock_response = MagicMock()
    mock_response.data = [
        {"nome": "AÇAI", "quantidade": 15, "limite_minimo": 5, "status": "Ok"},
        {"nome": "COPO", "quantidade": 2, "limite_minimo": 10, "status": "Repor"}
    ]
    # Simulando a cadeia de chamadas: supabase.table().select().execute()
    (mock_supabase
     .table.return_value
     .select.return_value.execute.return_value) = mock_response

    resultado = listar_itens()

    # Verifica se a conversão do JSON legado foi feita corretamente
    assert "AÇAI" in resultado
    assert "COPO" in resultado
    assert resultado["AÇAI"]["quantidade"] == 15
    assert resultado["COPO"]["status"] == "Repor"
    mock_supabase.table.assert_called_with("produto")


@patch("src.storage.estoque_armazenamento.supabase")
def test_adicionar_item(mock_supabase):
    mock_response = MagicMock()
    mock_response.data = [
        {"nome": "MORANGO", 
         "quantidade": 100, 
         "limite_minimo": 20, 
         "status": "Ok"}
        ]
    (mock_supabase
     .table.return_value
     .insert.return_value
     .execute.return_value) = mock_response

    resultado = adicionar_item("MORANGO", 100, 20)

    # Verifica se o método de inserção foi chamado 
    # com os dados corretos e cálculo de status
    mock_supabase.table.return_value.insert.assert_called_once_with({
        "nome": "MORANGO",
        "quantidade": 100,
        "limite_minimo": 20,
        "status": "Ok"
    })
    assert resultado == mock_response.data


@patch("src.storage.estoque_armazenamento.supabase")
def test_atualizar_quantidade(mock_supabase):
    mock_response = MagicMock()
    mock_response.data = [
        {"nome": "AÇAI", 
         "quantidade": 4, 
         "limite_minimo": 5, 
         "status": "Repor"}
        ]
    
    # Simulando: supabase.table().update().eq().execute()
    mock_table = mock_supabase.table.return_value
    mock_update = mock_table.update.return_value
    mock_eq = mock_update.eq.return_value
    mock_eq.execute.return_value = mock_response

    resultado = atualizar_quantidade("AÇAI", 4, 5)

    # Verifica se atualizou os dados corretos e recalculou o status 
    # (4 é menor que o limite 5 -> Repor)
    mock_table.update.assert_called_once_with({
        "quantidade": 4,
        "status": "Repor"
    })
    mock_update.eq.assert_called_once_with("nome", "AÇAI")
    assert resultado == mock_response.data


@patch("src.storage.estoque_armazenamento.supabase")
def test_remover_item(mock_supabase):
    mock_response = MagicMock()
    mock_response.data = []
    
    mock_table = mock_supabase.table.return_value
    mock_delete = mock_table.delete.return_value
    mock_eq = mock_delete.eq.return_value
    mock_eq.execute.return_value = mock_response

    resultado = remover_item("AÇAI")

    # Verifica se a deleção foi chamada apontando para o nome correto
    mock_delete.eq.assert_called_once_with("nome", "AÇAI")
    assert resultado == mock_response.data