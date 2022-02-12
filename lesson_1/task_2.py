from ipaddress import ip_address
from task_1 import start_proc, print_nodes

"""
Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
Меняться должен только последний октет каждого адреса.
По результатам проверки должно выводиться соответствующее сообщение.
"""


def host_range_ping():
    address_ip = input('Ввдите начальный ip-адресс: ')
    number_of_addresses = int(input('Сколько адресов проверить: '))
    first_address = ip_address(address_ip)
    ip_addresses_list = []
    last_oct = int(address_ip.split('.')[3])
    while True:
        if last_oct + number_of_addresses > 255:
            number_of_addresses = int(input(f'!!!Можем менять только последний октет, '
                                            f'т.е. максимальное число хостов = {256 - last_oct}!!!\n '
                                            f'Введите число заново:'))
        else:
            for el in range(number_of_addresses):
                ip_addresses_list.append(first_address + el)
            return start_proc(ip_addresses_list)


if __name__ == '__main__':
    print_nodes(host_range_ping())
