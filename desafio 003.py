import csv
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
import requests

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def obter_usuarios_api():

  url = "https://reqres.in/api/users"
  usuarios = []
  pagina = 1

  print("Conectando-se à API para buscar os usuários...")

  try:
    while True:
      resposta = requests.get(f"{url}?page={pagina}")

      if resposta.status_code == 200:
        dados = resposta.json()
        usuarios.extend(dados.get("data", []))

        if pagina >= dados.get("total_pages", 1):
          break
        pagina += 1
      else:
        print(f"Erro ao acessar a API: Status {resposta.status_code}")
        break

    print(f"Total de {len(usuarios)} usuários obtidos com sucesso.")
    return usuarios

  except requests.exceptions.RequestException as e:
    print(f"Erro de conexão com a API: {e}")
    return []


def salvar_dados_csv(usuarios, nome_arquivo="usuarios.csv"):
 
  if not usuarios:
    print("Nenhum dado para salvar.")
    return None

  print(f"Salvando dados no arquivo CSV '{nome_arquivo}'...")
  try:
    cabecalho = usuarios[0].keys()

    with open(
        nome_arquivo, mode="w", newline="", encoding="utf-8"
    ) as arquivo_csv:
      escritor = csv.DictWriter(arquivo_csv, fieldnames=cabecalho)
      escritor.writeheader()
      for usuario in usuarios:
        escritor.writerow(usuario)

    print(f"Arquivo '{nome_arquivo}' gerado com sucesso!")
    return nome_arquivo
  except Exception as e:
    print(f"Erro ao salvar o arquivo CSV: {e}")
    return None


def enviar_email(
    caminho_arquivo, email_remetente, senha_app, email_destinatario
):
  if not caminho_arquivo or not os.path.exists(caminho_arquivo):
    print("Arquivo não encontrado para envio.")
    return

  print(f"Preparando o envio do e-mail para: {email_destinatario}...")

  msg = MIMEMultipart()
  msg["From"] = email_remetente
  msg["To"] = email_destinatario
  msg["Subject"] = "Relatório Automatizado: Listagem de Usuários (CSV)"

  corpo = "Olá,\n\nSegue em anexo o arquivo CSV contendo a listagem atualizada de usuários obtida da API.\n\nAtenciosamente,\nAutomação Python"
  msg.attach(MIMEText(corpo, "plain"))

  try:
    with open(caminho_arquivo, "rb") as anexo:
      parte = MIMEBase("application", "octet-stream")
      parte.set_payload(anexo.read())

    encoders.encode_base64(parte)
    parte.add_header(
        "Content-Disposition", f"attachment; filename= {caminho_arquivo}"
    )
    msg.attach(parte)

    servidor = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    servidor.starttls()
    servidor.login(email_remetente, senha_app)
    servidor.sendmail(email_remetente, email_destinatario, msg.as_string())
    servidor.quit()

    print("E-mail enviado com sucesso!")

    os.remove(caminho_arquivo)
    print(f"Arquivo temporário '{caminho_arquivo}' limpo do sistema.")

  except Exception as e:
    print(f"Erro ao enviar o e-mail: {e}")


def main():

  print("--- Iniciando o processo de integração ---")

  email_remetente = input("Digite o seu e-mail do Gmail (Remetente): ").strip()
  senha_app = input("Digite a senha de aplicativo de 16 dígitos: ").strip()
  email_destinatario = input(
      "Digite o e-mail de destino (Quem vai receber): "
  ).strip()

  if not email_remetente or not senha_app or not email_destinatario:
    print("Dados incompletos. O processo foi cancelado.")
    return

  usuarios = obter_usuarios_api()

  if usuarios:
    arquivo_gerado = salvar_dados_csv(usuarios)

    if arquivo_gerado:

      enviar_email(
          arquivo_gerado, email_remetente, senha_app, email_destinatario
      )
  else:
    print("Processo interrompido devido a falhas na obtenção dos dados.")

  print("--- Processo finalizado ---")


if __name__ == "__main__":
  main()