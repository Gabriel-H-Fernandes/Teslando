from datetime import datetime
import sqlite3

conexao = sqlite3.connect("gestao_tarefas.db")
cursor = conexao.cursor()

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS tarefas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    titulo TEXT NOT NULL,
    descricao TEXT,
    data_criacao TEXT NOT NULL,
    data_conclusao TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
)
"""
)
conexao.commit()


def criar_usuario(nome, email):
  try:
    cursor.execute(
        "INSERT INTO usuarios (nome, email) VALUES (?, ?)", (nome, email)
    )
    conexao.commit()
    return cursor.lastrowid
  except sqlite3.IntegrityError:
    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
    return cursor.fetchone()[0]


def criar_tarefa():
  print("\n--- CADASTRAR NOVA TAREFA ---")
  nome_usuario = input("Digite seu nome: ")
  email_usuario = input("Digite seu e-mail: ")

  usuario_id = criar_usuario(nome_usuario, email_usuario)

  titulo = input("Título da tarefa: ")
  descricao = input("Descrição da tarefa: ")
  data_criacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  cursor.execute(
      """
        INSERT INTO tarefas (usuario_id, titulo, descricao, data_criacao) 
        VALUES (?, ?, ?, ?)
    """,
      (usuario_id, titulo, descricao, data_criacao),
  )
  conexao.commit()
  print("\n Tarefa cadastrada com sucesso!")


def listar_tarefas():
  cursor.execute("""
        SELECT t.id, u.nome, t.titulo, t.descricao, t.data_criacao, t.data_conclusao 
        FROM tarefas t
        JOIN usuarios u ON t.usuario_id = u.id
    """)
  tarefas = cursor.fetchall()

  print("\n--- LISTA DE TAREFAS CADASTRADAS ---")
  if not tarefas:
    print("Nenhuma tarefa encontrada.")
  else:
    for t in tarefas:
      status = f"Concluída em {t[5]}" if t[5] else "Pendente"
      print(f"ID: {t[0]} | Usuário: {t[1]} | Título: {t[2]}")
      print(f"   Descrição: {t[3]}")
      print(f"   Criado em: {t[4]} | Status: {status}")
      print("-" * 40)


def atualizar_tarefa():
  listar_tarefas()
  try:
    tarefa_id = int(
        input("\nDigite o ID da tarefa que deseja ATUALIZAR (Título/Descrição): ")
    )
    cursor.execute(
        "SELECT id, titulo, descricao FROM tarefas WHERE id = ?", (tarefa_id,)
    )
    tarefa = cursor.fetchone()

    if not tarefa:
      print("\n Tarefa não encontrada com esse ID.")
      return

    print(f"\nEditando tarefa atual: '{tarefa[1]}'")
    novo_titulo = input(
        "Novo título (deixe em branco para manter o atual): "
    ).strip()
    nova_descricao = input(
        "Nova descrição (deixe em branco para manter a atual): "
    ).strip()

    if novo_titulo:
      cursor.execute(
          "UPDATE tarefas SET titulo = ? WHERE id = ?", (novo_titulo, tarefa_id)
      )
    if nova_descricao:
      cursor.execute(
          "UPDATE tarefas SET descricao = ? WHERE id = ?",
          (nova_descricao, tarefa_id),
      )

    conexao.commit()
    print(f"\n Tarefa ID {tarefa_id} atualizada com sucesso!")
  except ValueError:
    print("\n ID inválido. Digite um número inteiro.")


def concluir_tarefa():
  listar_tarefas()
  try:
    tarefa_id = int(
        input("\nDigite o ID da tarefa que deseja marcar como CONCLUÍDA: ")
    )
    data_conclusao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
            UPDATE tarefas SET data_conclusao = ? WHERE id = ?
        """,
        (data_conclusao, tarefa_id),
    )
    conexao.commit()
    print(f"\n Tarefa ID {tarefa_id} marcada como concluída!")
  except ValueError:
    print("\n ID inválido. Digite um número inteiro.")


def deletar_tarefa():
  listar_tarefas()
  try:
    tarefa_id = int(input("\nDigite o ID da tarefa que deseja EXCLUIR: "))
    cursor.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
    conexao.commit()
    print(f"\n Tarefa ID {tarefa_id} excluída com sucesso!")
  except ValueError:
    print("\n ID inválido. Digite um número inteiro.")


def menu():
  while True:
    print("\n==============================")
    print("   SISTEMA DE GESTÃO DE TAREFAS")
    print("==============================")
    print("1. Cadastrar Tarefa ")
    print("2. Listar Tarefas")
    print("3. Atualizar Tarefa ")
    print("4. Concluir Tarefa")
    print("5. Excluir Tarefa ")
    print("6. Sair")

    opcao = input("\nEscolha uma opção (1 a 6): ")

    if opcao == "1":
      criar_tarefa()
    elif opcao == "2":
      listar_tarefas()
    elif opcao == "3":
      atualizar_tarefa()
    elif opcao == "4":
      concluir_tarefa()
    elif opcao == "5":
      deletar_tarefa()
    elif opcao == "6":
      print("\nSaindo do sistema. Até logo!")
      conexao.close()
      break
    else:
      print("\nOpção inválida! Escolha um número entre 1 e 6.")


if __name__ == "__main__":
  menu()