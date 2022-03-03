from ipaddress import ip_address
from subprocess import PIPE, DEVNULL, Popen
from socket import gethostbyname, gaierror
from threading import Thread
from queue import Queue

"""
Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения
(«Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().
"""


def host_ping(address, data):
    try:
        address_ip = ip_address(address)
    except ValueError:
        address_ip = get_host_name(address)
    ping = Popen(f"ping {address_ip} -w 1 -n 1", shell=True, stdout=PIPE, stderr=DEVNULL)
    try:
        if b'TTL=' in ping.stdout.readlines()[2]:
            data.put(['Доступен', f'{address}'])
        else:
            data.put(['Недоступен', f'{address}'])
    except IndexError:
        data.put(['Недоступен', f'{address}'])


def get_host_name(address):
    try:
        return gethostbyname(address)
    except gaierror:
        print(f'Не удалось получить ip-адресс хоста {address}')


def start_proc(my_list):
    data = Queue()
    nodes = {'Доступные узлы': [], 'Недоступные узлы': []}
    for el in my_list:
        process = Thread(target=host_ping, args=(el, data))
        process.start()
        process.join()
    for i in range(len(data.queue)):
        element = data.get()
        if element[0] == 'Доступен':
            nodes['Доступные узлы'].append(f'{element[1]}')
        elif element[0] == 'Недоступен':
            nodes['Недоступные узлы'].append(f'{element[1]}')
    return nodes


def print_nodes(data):
    for num in range(len(data.get('Доступные узлы'))):
        print(f'Узел {data.get("Доступные узлы")[num]} доступен')
    for num in range(len(data.get('Недоступные узлы'))):
        print(f'Узел {data.get("Недоступные узлы")[num]} недоступен')


if __name__ == '__main__':
    ip_addresses_list = ['yandex.ru', '192.168.1.253', 'google.com', 'gogdflrkle.com', 'gosuslugi.ru']
    print_nodes(start_proc(ip_addresses_list))
