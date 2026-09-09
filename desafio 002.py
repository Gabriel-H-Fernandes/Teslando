import os
import shutil
import shlex
from pathlib import Path

def comando_help(args):
    print("=== Comandos Disponíveis ===")
    print("  ls [caminho]              - Lista arquivos ou o conteúdo de um diretório")
    print("  cat <arquivo1> [arq2...]  - Exibe o conteúdo de um ou mais arquivos")
    print("  cp <origem> <destino>     - Copia um arquivo ou diretório")
    print("  rm [-r] <alvo1> [alvo2..] - Remove arquivos ou pastas (-r para pastas)")
    print("  touch <arquivo1> ...      - Cria um ou mais arquivos vazios")
    print("  echo \"texto\" [> arquivo]  - Imprime texto ou salva em um arquivo com '>")

def comando_ls(args):
    caminho = args[0] if args else "."
    if not os.path.exists(caminho):
        print(f"ls: impossível acessar '{caminho}': Arquivo ou diretório não encontrado")
        return

    if not os.path.isdir(caminho):
        print(caminho)
        return
    
    for item in Path(caminho).iterdir():
        nome = f"{item.name}/" if item.is_dir() else item.name
        print(nome)

def comando_cat(args):
    if not args:
        print("Uso: cat <arquivo1> [arquivo2...]")
        return

    for arquivo in args:
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                print(f.read(), end="")
        except FileNotFoundError:
            print(f"cat: {arquivo}: Arquivo ou diretório não encontrado")
        except IsADirectoryError:
            print(f"cat: {arquivo}: É um diretório")


def comando_cp(args):
    if len(args) < 2:
        print("Uso: cp <Arquivo que vai ser copiado> <Nome do novo arquivo>")
        return

    origem, destino = args[0], args[1]

    try:
        if os.path.isdir(origem):
            shutil.copytree(origem, destino)  
        else:
            shutil.copy2(origem, destino)     
    except Exception as e:
        print(f"cp: erro ao copiar: {e}")

def comando_rm(args):
    if not args:
        print("Uso: rm [-r] <alvo1> [alvo2...]")
        return

    recursivo = "-r" in args
    if recursivo:
        args.remove("-r")

    for alvo in args:
        if not os.path.exists(alvo):
            print(f"rm: impossível remover '{alvo}': Arquivo ou diretório não encontrado")
            continue

        if os.path.isdir(alvo):
            if recursivo:
                shutil.rmtree(alvo)  
            else:
                print(f"rm: não foi possível remover '{alvo}': É um diretório")
        else:
            os.remove(alvo)          

def comando_touch(args):
    if not args:
        print("Uso: touch <nome_do_arquivo1> [nome_do_arquivo2...]")
        return

    for caminho in args:
        try:
            
            Path(caminho).touch()
            print(f"Arquivo '{caminho}' criado com sucesso.")
        except Exception as e:
            print(f"touch: não foi possível criar '{caminho}': {e}")

def comando_echo(args):
    
    if ">" in args:
        pos_redirecionamento = args.index(">")
        texto = " ".join(args[:pos_redirecionamento])
        arquivos_destino = args[pos_redirecionamento + 1:]

        if not arquivos_destino:
            print("Uso: echo \"seu texto\" > <arquivo>")
            return

        arquivo = arquivos_destino[0]
        try:
            with open(arquivo, "w", encoding="utf-8") as f:
                f.write(texto + "\n")
            print(f"Texto gravado no arquivo '{arquivo}'.")
        except Exception as e:
            print(f"echo: erro ao escrever no arquivo: {e}")
    else:
        
        print(" ".join(args))

def main():
    print("=== Terminal Python Iniciado ===")
    print("Comandos disponíveis: ls, cat, cp, rm, help, echo, touch | Digite 'sair' ou 'exit' para fechar.\n")

    while True:
        try:
            
            entrada = input("meu_terminal> ").strip()

            if not entrada:
                continue

            
            partes = shlex.split(entrada)
            comando = partes[0].lower()
            argumentos = partes[1:]

            
            if comando in ["sair", "exit", "quit"]:
                print("Encerrando o programa...")
                break

            if comando == "ls":
                comando_ls(argumentos)
            elif comando == "cat":
                comando_cat(argumentos)
            elif comando == "cp":
                comando_cp(argumentos)
            elif comando == "rm":
                comando_rm(argumentos)
            elif comando == "touch":
                comando_touch(argumentos)
            elif comando == "echo":
                comando_echo(argumentos)
            elif comando == "help":
                comando_help(argumentos)
            else:
                print(f"Comando '{comando}' não reconhecido. Comandos disponiveis: ls, cat, cp, rm. Caso queira sair digite 'Sair'")

            print() 

        except (KeyboardInterrupt, EOFError):
            print("\nEncerrando o programa...")
            break

if __name__ == "__main__":
    main()