import requests, jwt, hashlib, math, time, random, os
from python_ghost_cursor import path
from datetime import datetime
from json import dumps
if not "images" in os.listdir(__path__):
    os.mkdir("images")
def generate_hsl(req):
    x = "0123456789/:abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    req = jwt.decode(req,options={"verify_signature":False})
    def a(r):
        for t in range(len(r) - 1, -1, -1):
            if r[t] < len(x) - 1:
                r[t] += 1
                return True
            r[t] = 0
        return False
    def i(r):
        t = ""
        for n in range(len(r)):
            t += x[r[n]]
        return t
    def o(r, e):
        n = e
        hashed = hashlib.sha1(e.encode())
        o = hashed.hexdigest()
        t = hashed.digest()
        e = None
        n = -1
        o = []
        for n in range(n + 1, 8 * len(t)):
            e = t[math.floor(n / 8)] >> n % 8 & 1
            o.append(e)
        a = o[:r]
        def index2(x,y):
            if y in x:
                return x.index(y)
            return -1
        return 0 == a[0] and index2(a, 1) >= r - 1 or -1 == index2(a, 1)
    def get():
        for e in range(25):
            n = [0 for i in range(e)]
            while a(n):
                u = req["d"] + "::" + i(n)
                if o(req["s"], u):
                    return i(n)
    result = get()
    hsl = ":".join([
        "1",
        str(req["s"]),
        datetime.now().isoformat()[:19] \
            .replace("T", "") \
            .replace("-", "") \
            .replace(":", ""),
        req["d"],
        "",
        result
    ])
    return hsl

class Scrapper():
    def __init__(self, site_key: str, host: str):
        self.sk = site_key
        self.host = host 
        self.v = requests.get("https://js.hcaptcha.com/1/api.js").text.split('nt="')[1].split('"')[0]
        self.session = requests.Session()
    def get_c(self):
        headers = {
            'authority': 'hcaptcha.com',
            'accept': 'application/json',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,ar;q=0.7',
            'cache-control': 'no-cache',
            'content-type': 'text/plain',
            'origin': 'https://newassets.hcaptcha.com',
            'pragma': 'no-cache',
            'referer': 'https://newassets.hcaptcha.com/',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        }
        params = {'v':self.v,'host':self.host,'sitekey':self.sk,'sc':'1','swa':'1'}
        r = self.session.post('https://hcaptcha.com/checksiteconfig',params=params,headers=headers)
        c = r.json()["c"]
        c["type"] = "hsl"
        return c
    def get_captcha(self,c,hsl):
        headers = {
            'authority': 'hcaptcha.com',
            'accept': 'application/json',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,ar;q=0.7',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://newassets.hcaptcha.com',
            'pragma': 'no-cache',
            'referer': 'https://newassets.hcaptcha.com/',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        }
        start = {'x': 100, 'y': 100}
        end = {'x': 600, 'y': 700}
        timestamp = int((time.time() * 1000) + round(random.random() * (120 - 30) + 30))
        mm = [[int(p['x']), int(p['y']), int(time.time() * 1000) + round(random.random() * (5000 - 2000) + 2000)] for p in path(start, end)]
        payload = {
            "v": self.v,
            "sitekey": self.sk,
            "host": self.host,
            "hl": "en",
            "motionData": dumps({"st":timestamp,"dct":timestamp,"mm":mm},separators=(",",":")),
            "n": hsl,
            "c": dumps(c,separators=(",",":"))
        }
        r = requests.post(f'https://hcaptcha.com/getcaptcha/{self.sk}',headers=headers,data=payload)
        return r.json()
    def scrape_challenge(self):
        c = self.get_c()
        captcha_data = self.get_captcha(c,generate_hsl(c["req"]))
        question = captcha_data["requester_question"]["en"]
        folder_name = question.replace("Please click each image containing ","")
        if not folder_name in os.listdir("images"):
            os.mkdir(f"images/{folder_name}")
        for i in captcha_data["tasklist"]:
            image_name = i["task_key"]
            image = requests.get(i["datapoint_uri"])
            f = open(f"images/{folder_name}/{image_name}.png","wb")
            f.write(image.content)
            f.close()
        f = open("questions.txt","a+")
        if not question in f.read().splitlines():
            f.write(question+"\n")
            f.close()
        return question, len(captcha_data["tasklist"])
while True:
    question, images = Scrapper("4c672d35-0701-42b2-88c3-78380b0db560","discord.com").scrape_challenge()
    print(f"Question: {question} | Number of images: {images}")