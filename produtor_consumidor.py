import threading
import time
import random

# Definição das constantes
BUFFER_SIZE = 5
NUM_PRODUTORES = 2
NUM_CONSUMIDORES = 3

# Buffer e índices
buffer = [None] * BUFFER_SIZE
in_index = 0
out_index = 0

# Semáforos
mutex = threading.Semaphore(1)  # Exclusão mútua
cheio = threading.Semaphore(0)  # Contador de itens no buffer
vazio = threading.Semaphore(BUFFER_SIZE)  # Contador de espaços vazios
# Função do produtor
def produtor(id):
    global in_index
    while True:
        time.sleep(random.randint(1, 3))  # Tempo de produção

        item = random.randint(1, 100)  # Valor do item produzido

        vazio.acquire()  # Espera até que haja espaço no buffer
        mutex.acquire()  # Obtém acesso exclusivo ao buffer

        buffer[in_index] = item
        print(f"Produtor {id} produziu: {item}")
        in_index = (in_index + 1) % BUFFER_SIZE  # Atualiza o índice circular

        mutex.release()  # Libera o acesso ao buffer
        cheio.release()  # Sinaliza que há um item a mais no buffer

# Função do consumidor
def consumidor(id):
    global out_index
    while True:
        time.sleep(random.randint(1, 2))  # Tempo de processamento

        cheio.acquire()  # Espera até que haja um item no buffer
        mutex.acquire()  # Obtém acesso exclusivo ao buffer

        item = buffer[out_index]
        print(f"Consumidor {id} consumiu: {item}")
        out_index = (out_index + 1) % BUFFER_SIZE  # Atualiza o índice circular
        print(f"cheio {cheio._value}")
        mutex.release()  # Libera o acesso ao buffer
        vazio.release()  # Sinaliza que há uma posição vazia no buffer

# Função principal
def main():
    # Cria as threads dos produtores
    produtores = []
    for i in range(NUM_PRODUTORES):
        t = threading.Thread(target=produtor, args=(i,))
        t.start()
        produtores.append(t)

    # Cria as threads dos consumidores
    consumidores = []
    for i in range(NUM_CONSUMIDORES):
        t = threading.Thread(target=consumidor, args=(i,))
        t.start()
        consumidores.append(t)

    # Aguarda as threads terminarem (nunca vai terminar com o loop infinito)
    for t in produtores:
        t.join()
    for t in consumidores:
        t.join()

if __name__ == "__main__":
    main()
