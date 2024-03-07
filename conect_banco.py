from mysql import connector

#Conecta o servidor MYSQL

conexao = connector.connect(
    host="localhost",
    user="root",
    password="senai"
)

# Cria um cursor para executar comando SQL
cursor = conexao.cursor()

#Criao banco de dados 'pwbe_escola" se ele ainda não existe
cursor.execute("CREATE DATABASE IF NOT EXISTS pwbe_escola")

#Seleciona o banco de dados 'pwbe_escola' 
cursor.execute("USE pwbe_escola")

# Cria tabela 'dados_login'
cursor.execute("CREATE TABLE IF NOT EXISTS dados_login (id_professor INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), login VARCHAR(255), senha VARCHAR(255))")

# Cria tabela 'turmas'
cursor.execute("CREATE TABLE IF NOT EXISTS turmas (id_turma INT AUTO_INCREMENT PRIMARY KEY, descricao VARCHAR(255))")

# Cria tabela 'atividades'
cursor.execute("CREATE TABLE IF NOT EXISTS atividades (id_atividade INT AUTO_INCREMENT PRIMARY KEY, descricao VARCHAR(255))")


#Criar tabela 'turmas-professor' com o relacionamento entre 'dados_login' e 'turmas'
cursor.execute('CREATE TABLE IF NOT EXISTS turma_professor (id INT AUTO_INCREMENT PRIMARY KEY, id_professor INT, id_turma INT, FOREIGN KEY (id_professor) REFERENCES dados_login(id_professor), FOREIGN KEY (id_turma) REFERENCES turmas(id_turma))')

#Criar tabela 'atividades_turma' com o relacionamento entre 'atividade' e 'turmas''
cursor.execute('CREATE TABLE IF NOT EXISTS atividades_turma (id INT AUTO_INCREMENT PRIMARY KEY, id_turma INT, id_atividade INT, FOREIGN KEY (id_turma) REFERENCES turmas(id_turma), FOREIGN KEY (id_atividade) REFERENCES atividades(id_atividade))')

#Fecha o cursor e a conexão 
cursor.close()
conexao.close()

print("Banco de dados e tabelas criadas com sucesso")