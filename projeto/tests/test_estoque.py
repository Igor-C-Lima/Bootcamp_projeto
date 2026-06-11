import pytest
from src.estoque.funcoes import cadastrar_produto, remover_produto


#Testes função cadastrar produto
def test_cadastrar_produto_nome_vazio(estoque_testes):
    with pytest.raises(ValueError,
                       match="o nome nao pode ser vazio"):
        cadastrar_produto("", 10, 5, estoque_testes)


def test_cadastrar_produto_nome_so_espacos(estoque_testes):
    with pytest.raises(ValueError, 
                       match="o nome nao pode ser vazio"):
        cadastrar_produto("   ", 10, 5, estoque_testes)


def test_cadastrar_produto_ja_existente(estoque_testes):
    with pytest.raises(ValueError, 
                       match="o produto já existe"):
        cadastrar_produto("açai", 10, 5, estoque_testes)


def test_cadastrar_produto_quantidade_negativa(estoque_testes):
    with pytest.raises(ValueError, 
                       match="nao sao permitidos valores negativos"):
        cadastrar_produto("melancia", -1, 5, estoque_testes)


def test_cadastrar_produto_limite_minimo_negativo(estoque_testes):
    with pytest.raises(ValueError, 
                       match="nao sao permitidos valores negativos"):
        cadastrar_produto("melancia", 10, -1, estoque_testes)


def test_cadastrar_produto_ambos_negativos(estoque_testes):
    with pytest.raises(ValueError, 
                       match="nao sao permitidos valores negativos"):
        cadastrar_produto("melancia", -5, -5, estoque_testes)


#Testes função remover produto
def test_remover_produto_nao_existente(estoque_testes):
    with pytest.raises(ValueError, 
                       match="o produto nao existe"):
        remover_produto("banana", estoque_testes)


def test_remover_produto_nome_vazio(estoque_testes):
    with pytest.raises(ValueError, 
                       match="o produto nao existe"):
        remover_produto("", estoque_testes)