import threading
import time
import random

# Configurações do salão
NUM_BARBEIROS = 3
NUM_CADEIRAS_ESPERA = 5

# Semáforos e mutexes
mutex = threading.Lock()  # Para garantir a exclusão mútua
barbeiro_sem = threading.Semaphore(0)  # Semáforo para acordar barbeiros (inicialização em 0 pois o semafaro precisa iniciar bloqueado (barbeiros não funcionam sem clientes))
cadeira_espera_vazia = threading.Semaphore(NUM_CADEIRAS_ESPERA)  # Cadeiras de espera disponíveis
cadeira_espera_cheia = threading.Semaphore(0) # Cadeiras de espera ocupadas

# Fila de espera
clientes_espera = []

class Barbearia:
    def __init__(self, num_barbeiros, num_cadeiras_espera):
        self.barbeiros = [Barbeiro(i+1) for i in range(num_barbeiros)]
        self.num_cadeiras_espera = num_cadeiras_espera

    def abrir_barbearia(self):
        print("O salão está aberto.")
        for barbeiro in self.barbeiros:
            threading.Thread(target=barbeiro.work).start()

    def cliente_chega(self, cliente_id):
        print(f"Cliente {cliente_id} chegou.")
        with mutex:
            if len(clientes_espera) < self.num_cadeiras_espera:
                clientes_espera.append(cliente_id)
                print(f"Cliente {cliente_id} sentou na cadeira de espera.")
                cadeira_espera_vazia.acquire()
                cadeira_espera_cheia.release()
                barbeiro_sem.release()  # Acorda um barbeiro
            else:
                print(f"Cliente {cliente_id} foi embora sem ser atendido, não há cadeiras de espera disponíveis.")

class Barbeiro:
    def __init__(self, barbeiro_id):
        self.barbeiro_id = barbeiro_id
        print(f"Barbeiro {self.barbeiro_id} está dormindo.")

    def work(self):
        while True:
            barbeiro_sem.acquire()  # Espera por um cliente
            print(f"Barbeiro {self.barbeiro_id} acordou.")
            self.cortar_cabelo()
            #if cadeira_espera_cheia.acquire(blocking=False):
            if clientes_espera:
                self.cortar_cabelo()
            else:
                print(f"Barbeiro {self.barbeiro_id} está dormindo.")

    def cortar_cabelo(self):
        with mutex:
            #Caso possua clientes em espera executa a função que chama o release para liberar uma cadeira na fila de espera
            if clientes_espera:
                cliente_id = clientes_espera.pop(0) #remoção de usuário de posição 0 da fila de espera
                print(f"Barbeiro {self.barbeiro_id} está atendendo o cliente {cliente_id}.")
                cadeira_espera_cheia.acquire()  # Acupa uma cadeira de espera
                cadeira_espera_vazia.release()  # Libera uma cadeira de espera
                time.sleep(random.randint(1, 7))  # Simula o tempo para cortar o cabelo
                print(f"Barbeiro {self.barbeiro_id} terminou de atender o cliente {cliente_id} e está pronto para o próximo cliente.")

        

# Função para simular a chegada de clientes
def simular_chegada_cliente(barber_shop):
    cliente_id = 1
    while True:
        time.sleep(random.randint(0, 2))  # Intervalo aleatório entre a chegada dos clientes
        barber_shop.cliente_chega(cliente_id)
        cliente_id += 1

if __name__ == "__main__":
    barber_shop = Barbearia(NUM_BARBEIROS, NUM_CADEIRAS_ESPERA) #inicialização de construtor de barbearia
    barber_shop.abrir_barbearia() #inicialização de função para abrir o salão através do objeto barber_shop

    # Simula a chegada dos clientes em uma thread separada
    threading.Thread(target=simular_chegada_cliente, args=(barber_shop,)).start()
