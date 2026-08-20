import mysql.connector

class Component: # Classe para representar um componente do inventário espacial
    """Classe que representa um componente do inventário espacial.
    Cada componente possui um código único, nome, categoria, massa e consumo de energia.
    Args:
        cod_invent (str): Código único do componente.
        nome (str): Nome do componente.
        categoria (str): Categoria do componente (ex: "Propulsão", "Comunicação").
        massa (float): Massa do componente em kg.
        consumo (float): Consumo de energia do componente em Watts.
    """
    def __init__(self, cod_invent, nome, categoria, massa, consumo): # Inicializa um componente do inventário espacial
        self.cod_invent = cod_invent # Código único do componente
        self.nome = nome # Nome do componente
        self.categoria = categoria # Categoria do componente (ex: "Propulsão", "Comunicação")
        self.massa = massa # Massa do componente em kg
        self.consumo = consumo # Consumo de energia do componente em Watts

    def __repr__(self): # Método para representar o componente como string
        return f"{self.cod_invent} - {self.nome} ({self.categoria})" # Representa o componente como uma string formatada


class LogMissao: # Classe para representar um log de missão
    def __init__(self, data, mensagem): # Inicializa um log de missão com data e mensagem
        self.data = data # Data do log
        self.mensagem = mensagem # Mensagem do log

class InventoryManager: # Classe para gerenciar o inventário espacial
    def __init__(self): # Inicializa o gerenciador de inventário espacial
        import mysql.connector # Importa o conector MySQL para interagir com o banco de dados
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mysql",  # Atualize conforme necessário
            database="astrosim"
        ) # Conecta ao banco de dados AstroSim
        self.cursor = self.conn.cursor() # Cria um cursor para executar comandos SQL

    def add_component(self, component): # Método para adicionar um componente ao inventário
        sql = """ 
            INSERT INTO inventario_espacial (cod_invent, nome, categoria, massa, consumo)
            VALUES (%s, %s, %s, %s, %s)
        """ # Comando SQL para inserir um novo componente no inventário
        dados = (
            component.cod_invent,
            component.nome,
            component.categoria,
            component.massa,
            component.consumo
        ) # Dados do componente a serem inseridos
        self.cursor.execute(sql, dados) # Executa o comando SQL com os dados do componente
        self.conn.commit() # Confirma a transação no banco de dados

    def get_all_components(self): # Método para obter todos os componentes do inventário
        self.cursor.execute("SELECT cod_invent, nome, categoria, massa, consumo FROM inventario_espacial") # Executa um comando SQL para selecionar todos os componentes do inventário
        resultados = self.cursor.fetchall() # Obtém todos os resultados da consulta
        return [Component(*linha) for linha in resultados] # Retorna uma lista de objetos Component a partir dos resultados da consulta
    
    def get_all_logs(self): # Método para obter todos os logs de missão
        self.cursor.execute("SELECT data, mensagem FROM logs_missao") # Executa um comando SQL para selecionar todos os logs de missão
        resultados = self.cursor.fetchall() # Obtém todos os resultados da consulta
        return [LogMissao(data, mensagem) for data, mensagem in resultados] # Retorna uma lista de objetos LogMissao a partir dos resultados da consulta

    def close(self): # Método para fechar a conexão com o banco de dados
        self.cursor.close() # Fecha o cursor
        self.conn.close() # Fecha a conexão com o banco de dados
