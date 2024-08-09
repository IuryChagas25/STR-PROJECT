import threading
import time
import random

# Configurações do salão
NUM_BARBEIROS = 3
NUM_CADEIRAS_ESPERA = 5

# Semáforos e mutexes
mutex = threading.Lock()  # Para garantir a exclusão mútua
barbeiro_sem = threading.Semaphore(0)  # Semáforo para acordar barbeiros (inicialização em 0 pois o semafaro precisa iniciar bloqueado (barbeiros não funcionam sem clientes))
cadeira_espera_sem = threading.Semaphore(NUM_CADEIRAS_ESPERA)  # Cadeiras de espera disponíveis

# Fila de espera
clientes_espera = []

class BarberShop:
    def __init__(self, num_barbeiros, num_cadeiras_espera):
        self.barbeiros = [Barber(i+1) for i in range(num_barbeiros)]
        self.num_cadeiras_espera = num_cadeiras_espera

    def open_shop(self):
        print("O salão está aberto.")
        for barbeiro in self.barbeiros:
            threading.Thread(target=barbeiro.work).start()

    def customer_arrives(self, customer_id):
        print(f"Cliente {customer_id} chegou.")
        with mutex:
            if len(clientes_espera) < self.num_cadeiras_espera:
                clientes_espera.append(customer_id)
                print(f"Cliente {customer_id} sentou na cadeira de espera.")
                barbeiro_sem.release()  # Acorda um barbeiro
            else:
                print(f"Cliente {customer_id} foi embora sem ser atendido, não há cadeiras de espera disponíveis.")

class Barber:
    def __init__(self, barber_id):
        self.barber_id = barber_id

    def work(self):
        while True:
            print(f"Barbeiro {self.barber_id} está dormindo.")
            barbeiro_sem.acquire()  # Espera por um cliente
            self.cut_hair()

    def cut_hair(self):
        with mutex:
            #Caso possua clientes em espera executa a função que chama o release para liberar uma cadeira na fila de espera
            if clientes_espera:
                customer_id = clientes_espera.pop(0)  #remoção de usuário de posição 0 da fila de espera
                print(f"Barbeiro {self.barber_id} está atendendo o cliente {customer_id}.")
                cadeira_espera_sem.release()  # Libera uma cadeira de espera

        time.sleep(random.randint(1, 7))  # Simula o tempo para cortar o cabelo
        print(f"Barbeiro {self.barber_id} terminou de atender o cliente {customer_id} e está pronto para o próximo cliente.")

# Função para simular a chegada de clientes
def customer_simulation(barber_shop):
    customer_id = 1
    while True:
        time.sleep(random.randint(0, 3))  # Intervalo aleatório entre a chegada dos clientes
        barber_shop.customer_arrives(customer_id)
        customer_id += 1

if __name__ == "__main__":
    barber_shop = BarberShop(NUM_BARBEIROS, NUM_CADEIRAS_ESPERA) #inicialização de construtor de barbearia
    barber_shop.open_shop() #inicialização de função para abrir o salão através do objeto barber_shop

    # Simula a chegada dos clientes em uma thread separada
    threading.Thread(target=customer_simulation, args=(barber_shop,)).start()
