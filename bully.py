import threading
import random
import time

# Definindo variáveis globais
processos = []
lock = threading.Lock()
coordenador_atual = None
mensagens_eleicao = []

class Processo(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id
        self.vivo = True

    def run(self):
        global coordenador_atual
        while self.vivo:
            with lock:
                # Verifica se é necessário iniciar uma eleição
                if coordenador_atual is None or not coordenador_atual.vivo:
                    self.iniciar_eleicao()
            time.sleep(1)  # Aguarda um pouco antes de verificar novamente

    def iniciar_eleicao(self):
        global coordenador_atual, mensagens_eleicao
        mensagem = f"Processo {self.id} iniciando eleição."
        mensagens_eleicao.append(mensagem)
        candidatos = [p for p in processos if p.vivo]
        coordenador_atual = max(candidatos, key=lambda p: p.id)
        mensagem = f"Processo {coordenador_atual.id} é o novo coordenador."
        mensagens_eleicao.append(mensagem)
        print(mensagem)

    def parar(self):
        self.vivo = False

def mostrar_processos():
    vivos = [p.id for p in processos if p.vivo]
    print(f"Processos ativos: {vivos}")
    if coordenador_atual:
        print(f"Coordenador atual: {coordenador_atual.id}")

def falhar_coordenador():
    if coordenador_atual:
        coordenador_atual.parar()
        mensagem = f"Coordenador {coordenador_atual.id} falhou."
        mensagens_eleicao.append(mensagem)
        print(mensagem)
        coordenador_atual.iniciar_eleicao()

def ressuscitar_coordenador():
    global coordenador_atual
    if coordenador_atual:
        # Encontra o último coordenador que falhou, se houver
        coordenador_falho = max(processos, key=lambda p: p.id)
        if coordenador_falho.vivo is False:
            coordenador_falho.vivo = True
            mensagem = f"Processo {coordenador_falho.id} ressuscitado como coordenador."
            mensagens_eleicao.append(mensagem)
            print(mensagem)
            coordenador_falho.iniciar_eleicao()
        else:
            print("Nenhum coordenador está falho.")

def main(numero_de_threads):
    global processos, coordenador_atual, mensagens_eleicao

    # Criar e iniciar processos
    for _ in range(numero_de_threads):
        novo_processo = Processo(random.randint(1, 100))
        processos.append(novo_processo)
        novo_processo.start()

    time.sleep(2)  # Espera um pouco para a inicialização

    # Definir o processo com o maior ID como coordenador inicial
    coordenador_inicial = max(processos, key=lambda p: p.id)
    coordenador_atual = coordenador_inicial
    mensagem = f"Processo {coordenador_atual.id} é o coordenador inicial."
    mensagens_eleicao.append(mensagem)
    print(mensagem)

    while True:
        print("\nOpções:")
        print("1 - Mostrar Processos")
        print("2 - Falhar Coordenador")
        print("3 - Ressuscitar Coordenador Falho")
        print("4 - Sair")
        opcao = input("Escolha a opção: ")

        if opcao == '1':
            mostrar_processos()
        elif opcao == '2':
            falhar_coordenador()
        elif opcao == '3':
            ressuscitar_coordenador()
        elif opcao == '4':
            print("Finalizando todos os processos.")
            for p in processos:
                p.parar()
            break
        else:
            print("Opção inválida. Escolha novamente.")


if __name__ == "__main__":
    num_threads = int(input("Número de threads: "))
    main(num_threads)
