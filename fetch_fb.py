from bs4 import BeautifulSoup
import re
from urllib.parse import unquote, parse_qs, urlparse
import random


class FacebookCrawler():

    def __init__(self):
        __base_url = "https://www.facebook.com"
        self.ual = requests.get("http://p29l26ay4.bkt.gdipper.com/ual.json").json()
        self.adid = ""

        self.proxy_ips = []

    def parse_data(self, text):
        """
           get true content
        """
        soup = BeautifulSoup(text, "lxml")
        fbad = {}
        fbad['content'] = soup.select_one(".bt").text.replace("\n\n", "")
        try: 
            fbad['video_url'] = unquote(re.findall("video_redirect/\?src=(.*?)\"", str(soup))[0])
            fbad['content'] = soup.select_one(".cd.ce").text.replace("\n\n", "")
        except:
            fbad['video_url'] = ""
            fbad['content'] = ""

        try:
            fbad['link'] = parse_qs(urlparse(soup.select_one(".cg a").attrs.get("href", "")).query).get("u")[0]
        except:
            fbad['link'] = ""
        

    def parse_true_url(self, text):
        """
           get true url from first request
        """
        adid = self.adid
        try: 
            true_url = re.findall("(https://.*?%s.*?)\"" % adid, text)[0]
            return 1, true_url
        except:
            return 0, "Not exsit"

    def fetch(self, adid):
        """
        入口
        """
        self.adid = str(adid)
        url = self.__base_url + self.adid
        raw_content = self.req(url=url)
        
    def get_proxy_ips(self):
        """
            get 20 proxy ip list
        """
        if self.proxy_ips:
            return
        print("Start to get proxy ips")
        req = requests.get('https://www.us-proxy.org/', headers=self.headers)
        if req.status_code != 200:
            return False
        html = req.text
        bs4 = BeautifulSoup(html, "lxml")
        for td in bs4.select("#proxylisttable tr"):
            try:
                ip, port, a, b, c, d, h = td.select("td")[:6]
                is_https = 'https' if 'yes' in h.text.lower() else 'http'
                iport = [is_https, ip.text, port.text]
                self.proxy_ips.append(iport)
            except:
                print("no ip port")

    def req(self, url):
        ua = random.choice(self.ual)
        headers = {'user-agent': ua}
        self.get_proxy_ips()
        proxy_ips = self.proxy_ips
        for idx, proxy_ip in enumerate(proxy_ips):
            if idx == 3:
                self.proxy_ips = []
                self.get_proxy_ips()
                proxy_ips[idx + 1:] = self.proxy_ips
            if idx == 8:
                print("No product, need check it")
                break
            try:

                req = requests.get(url, headers=headers, proxies={proxy_ip[0]: "%s:%s" % tuple(proxy_ip[1:]]])})
                if not req.ok:
                    continue
                return req.text
            except:
                continue

def __name__ == "__main__":
    fb = FacebookCrawler()
    fb.fetch("")
