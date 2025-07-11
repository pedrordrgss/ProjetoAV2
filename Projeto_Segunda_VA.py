import sys
import sqlite3
import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QTabWidget, QFormLayout, QLineEdit, QTextEdit, QTableWidget, QTableWidgetItem,
    QComboBox, QMessageBox, QHeaderView, QAbstractItemView
)

# --- Configuração do Caminho da Base de Dados ---
# Garante que a base de dados é sempre criada na mesma pasta que o script.
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    script_dir = os.getcwd() # Fallback para ambientes onde __file__ não está definido
DB_NAME = os.path.join(script_dir, 'ReVesteDB.db')


class SistemaVendas(QMainWindow):
    """
    Classe principal da aplicação do Sistema de Vendas.
    Engloba a interface gráfica, a lógica de negócio e a interação com a base de dados.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Vendas ReVeste")
        self.setGeometry(100, 100, 800, 600)

        self.init_db()
        self.init_ui()
        self.carregar_dados_iniciais()

    # --- 1. Inicialização e Configuração ---

    def init_ui(self):
        """Inicializa os componentes da interface gráfica."""
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Criação das abas
        self.init_cadastro_tab()
        self.init_vendas_tab()
        self.init_historico_tab()
        self.init_clientes_tab()

        self.aplicar_estilos()

    def init_db(self):
        """Garante que as tabelas da base de dados existem."""
        schema_queries = [
            """
            CREATE TABLE IF NOT EXISTS Usuario (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                tipo_perfil TEXT NOT NULL DEFAULT 'Consumidor',
                senha TEXT NOT NULL DEFAULT '123'
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Material (
                id_material INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_material TEXT NOT NULL UNIQUE,
                tipo_material TEXT NOT NULL DEFAULT 'roupa',
                condicao TEXT NOT NULL DEFAULT 'novo'
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Transacao (
                id_transacao INTEGER PRIMARY KEY AUTOINCREMENT,
                id_vendedor INTEGER NOT NULL DEFAULT 1,
                id_comprador INTEGER NOT NULL,
                id_material INTEGER NOT NULL,
                detalhes TEXT,
                data_transacao TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pendente',
                FOREIGN KEY (id_comprador) REFERENCES Usuario(id_usuario),
                FOREIGN KEY (id_material) REFERENCES Material(id_material)
            )
            """
        ]
        for query in schema_queries:
            self._executar_query(query)

    def carregar_dados_iniciais(self):
        """Carrega todos os dados da DB para a UI quando a aplicação inicia."""
        self.atualizar_clientes_ui()
        self.atualizar_produtos_ui()
        self.atualizar_historico_ui()

    # --- 2. Criação das Abas da Interface ---

    def init_cadastro_tab(self):
        """Cria a aba de cadastro de clientes e produtos."""
        self.cadastro_tab = QWidget()
        self.tabs.addTab(self.cadastro_tab, "Cadastro")
        layout = QFormLayout(self.cadastro_tab)
        
        self.cliente_input = QLineEdit()
        self.produto_input = QLineEdit()
        self.salvar_btn = QPushButton("Salvar")
        self.salvar_btn.setObjectName("salvarBtn")
        
        layout.addRow("Nome do Cliente:", self.cliente_input)
        layout.addRow("Nome do Produto:", self.produto_input)
        layout.addRow(self.salvar_btn)
        
        self.salvar_btn.clicked.connect(self.handle_salvar_cadastro)

    def init_vendas_tab(self):
        """Cria a aba para registro de vendas."""
        self.vendas_tab = QWidget()
        self.tabs.addTab(self.vendas_tab, "Registro de Vendas")
        layout = QFormLayout(self.vendas_tab)

        # MELHORIA: Data atual como padrão
        self.data_input = QLineEdit(datetime.now().strftime('%d/%m/%Y'))
        self.cliente_combo = QComboBox()
        self.produto_combo = QComboBox()
        self.itens_input = QTextEdit(placeholderText="Detalhes sobre a venda, condição da peça, etc.")
        self.registrar_btn = QPushButton("Registrar Venda")
        self.registrar_btn.setObjectName("registrarBtn")

        layout.addRow("Data (dd/mm/aaaa):", self.data_input)
        layout.addRow("Cliente:", self.cliente_combo)
        layout.addRow("Produto:", self.produto_combo)
        layout.addRow("Detalhes Adicionais:", self.itens_input)
        layout.addRow(self.registrar_btn)
        
        self.registrar_btn.clicked.connect(self.handle_registrar_venda)

    def init_historico_tab(self):
        """Cria a aba de histórico de vendas."""
        self.historico_tab = QWidget()
        self.tabs.addTab(self.historico_tab, "Histórico de Vendas")
        layout = QVBoxLayout(self.historico_tab)
        
        self.tabela_vendas = QTableWidget()
        self.tabela_vendas.setColumnCount(4)
        self.tabela_vendas.setHorizontalHeaderLabels(["Data", "Cliente", "Produto", "Detalhes"])
        self.tabela_vendas.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela_vendas.setSelectionBehavior(QAbstractItemView.SelectRows) # MELHORIA: Selecionar linha inteira
        
        # MELHORIA: Ajuste automático das colunas
        header = self.tabela_vendas.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)

        self.btn_totais = QPushButton("Calcular Totais de Vendas por Período")
        self.btn_totais.setObjectName("totaisBtn")

        layout.addWidget(self.tabela_vendas)
        layout.addWidget(self.btn_totais)
        
        self.btn_totais.clicked.connect(self.handle_calcular_totais)

    def init_clientes_tab(self):
        """Cria a aba de gestão de clientes cadastrados."""
        self.clientes_tab = QWidget()
        self.tabs.addTab(self.clientes_tab, "Clientes Cadastrados")
        layout = QVBoxLayout(self.clientes_tab)
        
        self.tabela_clientes = QTableWidget()
        self.tabela_clientes.setColumnCount(1)
        self.tabela_clientes.setHorizontalHeaderLabels(["Clientes"])
        self.tabela_clientes.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela_clientes.setSelectionBehavior(QAbstractItemView.SelectRows) # MELHORIA: Selecionar linha inteira
        self.tabela_clientes.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch) # MELHORIA: Ajuste automático

        self.btn_remover_cliente = QPushButton("Remover Cliente Selecionado")
        self.btn_remover_cliente.setObjectName("removerClienteBtn")

        layout.addWidget(self.tabela_clientes)
        layout.addWidget(self.btn_remover_cliente)
        
        self.btn_remover_cliente.clicked.connect(self.handle_remover_cliente)

    # --- 3. Lógica de Negócio (Handlers de Eventos) ---

    def handle_salvar_cadastro(self):
        """Lida com o clique do botão 'Salvar' na aba de cadastro."""
        cliente_nome = self.cliente_input.text().strip()
        produto_nome = self.produto_input.text().strip()
        
        if not cliente_nome and not produto_nome:
            self.show_message("Preencha o nome do cliente ou do produto.", error=True)
            return

        try:
            if cliente_nome:
                email_cliente = f'{cliente_nome.lower().replace(" ", ".")}@email.com'
                query = "INSERT INTO Usuario (nome, email) VALUES (?, ?)"
                self._executar_query(query, (cliente_nome, email_cliente))
                self.cliente_input.clear()
                self.show_message(f"Cliente '{cliente_nome}' cadastrado com sucesso!")
                self.atualizar_clientes_ui()

            if produto_nome:
                query = "INSERT INTO Material (nome_material) VALUES (?)"
                self._executar_query(query, (produto_nome,))
                self.produto_input.clear()
                self.show_message(f"Produto '{produto_nome}' cadastrado com sucesso!")
                self.atualizar_produtos_ui()

        except sqlite3.IntegrityError:
            self.show_message("Erro: Cliente ou Produto já existe.", error=True)
        except Exception as e:
            self.show_message(f"Ocorreu um erro inesperado: {e}", error=True)

    def handle_registrar_venda(self):
        """Lida com o clique do botão 'Registar Venda'."""
        data_str = self.data_input.text().strip()
        cliente_nome = self.cliente_combo.currentText()
        produto_nome = self.produto_combo.currentText()
        detalhes = self.itens_input.toPlainText().strip()

        data_db = self._formatar_data_para_db(data_str)
        # MELHORIA: Validação de data mais específica
        if not data_db:
            self.show_message(f"Formato de data inválido: '{data_str}'.\nUse o formato dd/mm/aaaa.", error=True)
            return
        if not (cliente_nome and produto_nome):
            self.show_message("Por favor, selecione um Cliente e um Produto.", error=True)
            return

        try:
            comprador_id = self._get_id_por_nome('Usuario', 'id_usuario', 'nome', cliente_nome)
            material_id = self._get_id_por_nome('Material', 'id_material', 'nome_material', produto_nome)

            if comprador_id is None or material_id is None:
                self.show_message("Erro: Cliente ou Produto não encontrado na base de dados.", error=True)
                return

            query = "INSERT INTO Transacao (id_comprador, id_material, detalhes, data_transacao) VALUES (?, ?, ?, ?)"
            self._executar_query(query, (comprador_id, material_id, detalhes, data_db))
            
            self.itens_input.clear()
            self.show_message("Venda registada com sucesso!")
            self.atualizar_historico_ui()

        except Exception as e:
            self.show_message(f"Ocorreu um erro ao registar a venda: {e}", error=True)

    def handle_remover_cliente(self):
        """Lida com a remoção de um cliente selecionado."""
        selected_items = self.tabela_clientes.selectedItems()
        if not selected_items:
            self.show_message("Por favor, selecione um cliente na tabela para remover.", error=True)
            return

        nome_cliente = selected_items[0].text()
        reply = QMessageBox.question(self, 'Confirmar Remoção',
                                     f"Tem a certeza que deseja remover o cliente '{nome_cliente}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.No:
            return

        try:
            id_cliente = self._get_id_por_nome('Usuario', 'id_usuario', 'nome', nome_cliente)
            if id_cliente is None:
                self.show_message("Cliente não encontrado.", error=True)
                return

            query_check = "SELECT COUNT(*) FROM Transacao WHERE id_comprador = ?"
            transacao_count = self._executar_query(query_check, (id_cliente,), fetch_one=True)[0]

            if transacao_count > 0:
                self.show_message(f"Não é possível remover '{nome_cliente}', pois possui {transacao_count} venda(s) no histórico.", error=True)
                return

            query_delete = "DELETE FROM Usuario WHERE id_usuario = ?"
            self._executar_query(query_delete, (id_cliente,))
            self.show_message(f"Cliente '{nome_cliente}' removido com sucesso!")
            self.atualizar_clientes_ui()

        except Exception as e:
            self.show_message(f"Ocorreu um erro ao remover o cliente: {e}", error=True)

    def handle_calcular_totais(self):
        """Busca na DB e exibe os totais de vendas por períodos."""
        try:
            queries = {
                "DIA": "SELECT strftime('%d/%m/%Y', data_transacao), COUNT(*) FROM Transacao GROUP BY data_transacao ORDER BY data_transacao DESC",
                "SEMANA": "SELECT strftime('%Y-W%W', data_transacao), COUNT(*) FROM Transacao GROUP BY strftime('%Y-W%W', data_transacao) ORDER BY strftime('%Y-W%W', data_transacao) DESC",
                "MÊS": "SELECT strftime('%Y-%m', data_transacao), COUNT(*) FROM Transacao GROUP BY strftime('%Y-%m', data_transacao) ORDER BY strftime('%Y-%m', data_transacao) DESC"
            }
            
            relatorio = []
            for periodo, query in queries.items():
                resultados = self._executar_query(query, fetch_all=True)
                if resultados:
                    relatorio.append(f"📅 Totais por {periodo}:\n" + "\n".join([f"{data}: {total} venda(s)" for data, total in resultados]))

            if not relatorio:
                self.show_message("Nenhuma venda encontrada para calcular os totais.")
                return

            QMessageBox.information(self, "Totais de Vendas", "\n\n".join(relatorio))

        except Exception as e:
            self.show_message(f"Erro ao calcular totais: {e}", error=True)

    # --- 4. Métodos de Atualização da UI ---

    def atualizar_clientes_ui(self):
        """Atualiza a tabela de clientes e a combobox de clientes."""
        clientes = self._executar_query("SELECT nome FROM Usuario ORDER BY nome", fetch_all=True)
        lista_clientes = [c[0] for c in clientes]

        self.tabela_clientes.setRowCount(0)
        self.tabela_clientes.setRowCount(len(lista_clientes))
        for i, cliente in enumerate(lista_clientes):
            self.tabela_clientes.setItem(i, 0, QTableWidgetItem(cliente))

        self.cliente_combo.clear()
        self.cliente_combo.addItems(lista_clientes)

    def atualizar_produtos_ui(self):
        """Atualiza a combobox de produtos."""
        produtos = self._executar_query("SELECT nome_material FROM Material ORDER BY nome_material", fetch_all=True)
        lista_produtos = [p[0] for p in produtos]
        self.produto_combo.clear()
        self.produto_combo.addItems(lista_produtos)

    def atualizar_historico_ui(self):
        """Atualiza a tabela de histórico de vendas."""
        query = """
            SELECT strftime('%d/%m/%Y', t.data_transacao), u.nome, m.nome_material, t.detalhes
            FROM Transacao t
            JOIN Usuario u ON t.id_comprador = u.id_usuario
            JOIN Material m ON t.id_material = m.id_material
            ORDER BY t.data_transacao DESC, t.id_transacao DESC
        """
        vendas = self._executar_query(query, fetch_all=True)
        self.tabela_vendas.setRowCount(0)
        self.tabela_vendas.setRowCount(len(vendas))
        for i, venda in enumerate(vendas):
            for j, dado in enumerate(venda):
                self.tabela_vendas.setItem(i, j, QTableWidgetItem(str(dado)))

    # --- 5. Métodos Auxiliares e Utilitários ---

    def _executar_query(self, query, params=(), fetch_one=False, fetch_all=False):
        """
        Método centralizado para executar todas as queries da base de dados.
        Gere a conexão, o cursor e o tratamento de erros básicos.
        """
        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                if fetch_one:
                    return cursor.fetchone()
                if fetch_all:
                    return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro na Base de Dados: {e}")
            print(f"Query: {query}")
            raise e

    def _get_id_por_nome(self, tabela, campo_id, campo_nome, valor_nome):
        """Retorna o ID de um registo dado o seu nome."""
        query = f"SELECT {campo_id} FROM {tabela} WHERE {campo_nome} = ?"
        resultado = self._executar_query(query, (valor_nome,), fetch_one=True)
        return resultado[0] if resultado else None

    def _formatar_data_para_db(self, data_str):
        """Converte data de dd/mm/aaaa para aaaa-mm-dd para o DB."""
        try:
            return datetime.strptime(data_str, '%d/%m/%Y').strftime('%Y-%m-%d')
        except ValueError:
            return None

    def show_message(self, text, error=False):
        """Exibe uma caixa de mensagem padronizada."""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical if error else QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle("Erro de Operação" if error else "Sucesso")
        msg.exec_()

    def aplicar_estilos(self):
        """Aplica uma folha de estilos (CSS) à aplicação."""
        self.setStyleSheet("""
            QMainWindow { background-color: #f8f9fa; }
            QWidget { font-size: 10pt; }
            QTabWidget::pane { border-top: 2px solid #8635DD; }
            QTabBar::tab {
                background: #e1d4f0; color: #333; padding: 10px;
                border-top-left-radius: 4px; border-top-right-radius: 4px;
            }
            QTabBar::tab:selected { background: #8635DD; color: white; }
            QPushButton {
                color: white; padding: 8px 12px; font-weight: bold;
                border-radius: 5px; border: none;
            }
            QPushButton:hover { background-color: #6a2aa8; }
            QPushButton#salvarBtn { background-color: #8635DD; }
            QPushButton#registrarBtn { background-color: #D45738; }
            QPushButton#registrarBtn:hover { background-color: #b84a2f; }
            QPushButton#totaisBtn { background-color: #17a2b8; }
            QPushButton#totaisBtn:hover { background-color: #138496; }
            QPushButton#removerClienteBtn { background-color: #dc3545; }
            QPushButton#removerClienteBtn:hover { background-color: #c82333; }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #ffffff; padding: 5px;
                border: 1px solid #ccc; border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #8635DD; color: white;
                padding: 4px; font-weight: bold; border: none;
            }
            QTableWidget { 
                border: 1px solid #ccc; 
                selection-background-color: #D45738;
            }
        """)

# --- Ponto de Entrada da Aplicação ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SistemaVendas()
    window.show()
    sys.exit(app.exec_())