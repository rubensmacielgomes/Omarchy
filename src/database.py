"""
Módulo de banco de dados para o Gerenciador de Despesas.
Gerencia todas as operações CRUD usando SQLite3.
"""

import sqlite3
import os


# Caminho do banco de dados no mesmo diretório do projeto
DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "despesas.db")


# ─── Categorias padrão ───────────────────────────────────────────────
CATEGORIAS_PADRAO = [
    "🏠 Moradia",
    "🍔 Alimentação",
    "🚗 Transporte",
    "💡 Energia/Água/Gás",
    "📱 Telefone/Internet",
    "🏥 Saúde",
    "📚 Educação",
    "🎮 Lazer/Entretenimento",
    "👕 Vestuário",
    "🛒 Compras Diversas",
    "💳 Cartão de Crédito",
    "📋 Assinaturas",
    "🐾 Pet",
    "🎁 Presentes",
    "📦 Outros",
]


def conectar():
    """Cria e retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def inicializar_banco():
    """Cria as tabelas necessárias caso não existam."""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS despesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            data TEXT NOT NULL,
            categoria_id INTEGER NOT NULL,
            observacao TEXT DEFAULT '',
            paga INTEGER DEFAULT 0,
            criado_em TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )
    """)

    # Adicionar coluna 'paga' caso o banco já exista sem ela
    cursor.execute("PRAGMA table_info(despesas)")
    colunas = [info[1] for info in cursor.fetchall()]
    if 'paga' not in colunas:
        cursor.execute("ALTER TABLE despesas ADD COLUMN paga INTEGER DEFAULT 0")

    # Inserir categorias padrão se a tabela estiver vazia
    cursor.execute("SELECT COUNT(*) FROM categorias")
    if cursor.fetchone()[0] == 0:
        for cat in CATEGORIAS_PADRAO:
            cursor.execute("INSERT INTO categorias (nome) VALUES (?)", (cat,))

    conn.commit()
    conn.close()


# ─── Operações com Categorias ────────────────────────────────────────

def listar_categorias():
    """Retorna lista de tuplas (id, nome) de todas as categorias."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM categorias ORDER BY nome")
    categorias = cursor.fetchall()
    conn.close()
    return categorias


def adicionar_categoria(nome):
    """Adiciona uma nova categoria ao banco."""
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO categorias (nome) VALUES (?)", (nome,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


# ─── Operações com Despesas ──────────────────────────────────────────

def adicionar_despesa(descricao, valor, data, categoria_id, observacao="", paga=0):
    """Adiciona uma nova despesa ao banco de dados."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO despesas (descricao, valor, data, categoria_id, observacao, paga)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (descricao, valor, data, categoria_id, observacao, paga)
    )
    conn.commit()
    despesa_id = cursor.lastrowid
    conn.close()
    return despesa_id


def editar_despesa(despesa_id, descricao, valor, data, categoria_id, observacao="", paga=0):
    """Atualiza uma despesa existente."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE despesas
           SET descricao=?, valor=?, data=?, categoria_id=?, observacao=?, paga=?
           WHERE id=?""",
        (descricao, valor, data, categoria_id, observacao, paga, despesa_id)
    )
    conn.commit()
    alterados = cursor.rowcount
    conn.close()
    return alterados > 0


def excluir_despesa(despesa_id):
    """Remove uma despesa pelo ID."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM despesas WHERE id=?", (despesa_id,))
    conn.commit()
    removidos = cursor.rowcount
    conn.close()
    return removidos > 0


def listar_despesas(mes=None, ano=None):
    """
    Retorna todas as despesas, opcionalmente filtradas por mês e ano.
    Retorna lista de dicionários com dados da despesa + nome da categoria.
    """
    conn = conectar()
    cursor = conn.cursor()

    query = """
        SELECT d.id, d.descricao, d.valor, d.data, c.nome as categoria,
               d.categoria_id, d.observacao, d.paga
        FROM despesas d
        JOIN categorias c ON d.categoria_id = c.id
    """
    params = []

    if mes is not None and ano is not None:
        query += " WHERE strftime('%m', d.data) = ? AND strftime('%Y', d.data) = ?"
        params = [f"{mes:02d}", str(ano)]

    query += " ORDER BY d.data DESC, d.id DESC"
    cursor.execute(query, params)

    colunas = ["id", "descricao", "valor", "data", "categoria", "categoria_id", "observacao", "paga"]
    despesas = [dict(zip(colunas, row)) for row in cursor.fetchall()]
    conn.close()
    return despesas


def resumo_por_categoria(mes=None, ano=None):
    """
    Retorna o total gasto por categoria em um determinado mês/ano.
    Retorna lista de tuplas (categoria_nome, total).
    """
    conn = conectar()
    cursor = conn.cursor()

    query = """
        SELECT c.nome, COALESCE(SUM(d.valor), 0) as total
        FROM categorias c
        LEFT JOIN despesas d ON d.categoria_id = c.id
    """
    params = []

    if mes is not None and ano is not None:
        query += " AND strftime('%m', d.data) = ? AND strftime('%Y', d.data) = ?"
        params = [f"{mes:02d}", str(ano)]

    query += " GROUP BY c.id HAVING total > 0 ORDER BY total DESC"
    cursor.execute(query, params)
    resultado = cursor.fetchall()
    conn.close()
    return resultado


def total_mensal(mes, ano):
    """Retorna o total gasto em um mês/ano específico."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT COALESCE(SUM(valor), 0)
           FROM despesas
           WHERE strftime('%m', data) = ? AND strftime('%Y', data) = ?""",
        (f"{mes:02d}", str(ano))
    )
    total = cursor.fetchone()[0]
    conn.close()
    return total


def meses_disponiveis():
    """Retorna lista de meses/anos com despesas registradas."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT strftime('%m', data) as mes, strftime('%Y', data) as ano
        FROM despesas
        ORDER BY ano DESC, mes DESC
    """)
    resultado = cursor.fetchall()
    conn.close()
    return [(int(r[0]), int(r[1])) for r in resultado]


def buscar_despesa(despesa_id):
    """Busca uma despesa específica pelo ID."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT d.id, d.descricao, d.valor, d.data, c.nome, d.categoria_id, d.observacao, d.paga
           FROM despesas d
           JOIN categorias c ON d.categoria_id = c.id
           WHERE d.id = ?""",
        (despesa_id,)
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        colunas = ["id", "descricao", "valor", "data", "categoria", "categoria_id", "observacao", "paga"]
        return dict(zip(colunas, row))
    return None
