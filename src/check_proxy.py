import threading
import queue
import requests

q = queue.Queue()
valid_proxies = []
with open('../proxy/proxy_list.txt', 'r') as file:
    proxies = file.read().split("\n")
    for p in proxies:
        q.put(p)

def check_proxy():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            response = requests.get("https://www.google.com", proxies={"http": proxy, "https": proxy})
            if response.status_code == 200:
                valid_proxies.append(proxy)
                with open('../proxy/valid_proxies.txt', 'a') as file:
                    file.write(proxy + "\n")
                    print(f"Valid proxy found and saved: {proxy}")
        except:
            continue


for _ in range(10):
    threading.Thread(target=check_proxy).start()