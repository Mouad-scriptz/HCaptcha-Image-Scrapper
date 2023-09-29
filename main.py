import hashlib, time, random, os, threading, tls_client, requests, os, subprocess, json, string, httpx
from colorama import Fore, init

init(convert=True,autoreset=True)
os.system("cls")
print_lock      = threading.Lock()
open_lock       = threading.Lock()
v               = tls_client.Session(client_identifier="chrome_111").get("https://js.hcaptcha.com/1/api.js").text.split('nt="')[1].split('"')[0]
accept_language = 'en-GB,en;q=0.9'
sec_ch_ua       = '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"'
user_agent      = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"

def print_wl(text):
    with print_lock:
        print(text)

class colors:
    reset   = Fore.RESET
    cyan    = Fore.CYAN
    magenta = Fore.MAGENTA
    yellow  = Fore.YELLOW; lyellow = Fore.LIGHTYELLOW_EX
    red     = Fore.RED;    lred    = Fore.LIGHTRED_EX
    blue    = Fore.BLUE;   lblue   = Fore.LIGHTBLUE_EX
    green   = Fore.GREEN;  lgreen  = Fore.LIGHTGREEN_EX

class console:
    def input(text:str=None):
        content = input(
            f"({colors.cyan}>{colors.reset}) {colors.lblue}{text if text else 'Input'}{colors.reset} >> {Fore.CYAN}"
        )
        print(colors.reset)
        return content
    
    def success(text:str,content:str=None):
        print_wl(
            f"({colors.lgreen}+{colors.reset}) {colors.cyan}{text}{colors.reset}{': '+content if content else ''}"
        )

    def error(text:str):
        print_wl(
            f"({colors.lred}-{colors.reset}) {colors.lred}{text}{colors.reset}"
        )

    def info(text:str,content:str=None):
        print_wl(
            f"({colors.lyellow}~{colors.reset}) {colors.lyellow}{text}{colors.reset}{': '+content if content else ''}"
        )

def scrape_proxies():
    os.system("cls")
    urls_to_scrape=[
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt"
    ]
    with open("proxies.txt","w") as f:
        f.write("")
        f.close()
    for i in urls_to_scrape:
        proxies = requests.get(url=i).text
        with open("proxies.txt","a+") as f:
            f.write(proxies)
            f.close()
        num = len(proxies.split('\n'))
        console.success("Scraped",f"{i} | {num}")
    time.sleep(1)
    main()

def get_proxy():
    while True:
        with open("proxies.txt","r") as f:
            proxy = random.choice(f.read().splitlines())
            f.close()
            if proxy != "" and proxy != "\n":
               break 
    return proxy

class Scraper():
    def __init__(self, site_key: str, host: str):
        self.site_key = site_key
        self.host     = host 
        self.session  = tls_client.Session(
            "chrome_"+user_agent.split("Chrome/")[1].split(".")[0],
            random_tls_extension_order=True
        )
        self.session.headers = {
            'authority'       : 'hcaptcha.com',
            'accept-language' : accept_language,
            'sec-ch-ua'       : sec_ch_ua,
            'user-agent'      : user_agent
        }
        self.proxy = get_proxy()
        self.session.proxies = {
            "http"  : "http://"+self.proxy,
            "https" : "http://"+self.proxy,
        }
    
    def get_c(self):
        headers = {
            'accept'             : 'application/json',
            'content-type'       : 'text/plain',
            'origin'             : 'https://newassets.hcaptcha.com',
            'sec-ch-ua-mobile'   : '?0',
            'sec-ch-ua-platform' : '"Windows"',
            'sec-fetch-dest'     : 'empty',
            'sec-fetch-mode'     : 'cors',
            'sec-fetch-site'     : 'same-site'
        }
        params = {
            'v'       : v,
            'host'    : self.host,
            'sitekey' : self.site_key,
            'sc'      : '1',
            'swa'     : '1',
            'spst'    : '1'
        }
        try:
            response = self.session.post('https://hcaptcha.com/checksiteconfig',params=params,headers=headers,timeout_seconds=10)
            self.c = response.json()["c"]
            return True
        except:
            return False
        
    def get_challenge(self):
        headers = {
            'accept'             : 'application/json',
            'content-type'       : 'application/x-www-form-urlencoded',
            'origin'             : 'https://newassets.hcaptcha.com',
            'referer'            : 'https://newassets.hcaptcha.com/',
            'sec-ch-ua-mobile'   : '?0',
            'sec-ch-ua-platform' : '"Windows"',
            'sec-fetch-dest'     : 'empty',
            'sec-fetch-mode'     : 'cors',
            'sec-fetch-site'     : 'same-site'
        }
        widget_id = '0'+''.join(random.choice("0123456789") for _ in range(11))
        now = int(time.time()*1000)
        payload = {
            "v"          : v,
            "sitekey"    : self.site_key,
            "host"       : self.host,
            "hl"         : "en",
            "motionData" : {
                "st":now,
                "mm":[[160,3,1696008726528],[152,8,1696008726544],[146,12,1696008726560],[139,16,1696008726576],[131,21,1696008726592],[121,27,1696008726608],[111,32,1696008726624],[101,36,1696008726640],[93,39,1696008726656],[87,41,1696008726672],[85,42,1696008726688]],
                "mm-mp":8,
                "md":[[85,42,1696008726729]],
                "md-mp":0,
                "mu":[[85,42,1696008726856]],
                "mu-mp":0,
                "v":1,
                "topLevel":{
                    "inv":False,
                    "st":now+random.randint(10,100),
                    "sc":{"availWidth":1600,"availHeight":900,"width":1600,"height":900,"colorDepth":24,"pixelDepth":24,"availLeft":0,"availTop":0,"onchange":None,"isExtended":False},
                    "nv":{"vendorSub":"","productSub":"20030107","vendor":"Google Inc.","maxTouchPoints":0,"scheduling":{},"userActivation":{},"doNotTrack":None,"geolocation":{},"connection":{},"pdfViewerEnabled":True,"webkitTemporaryStorage":{},"hardwareConcurrency":random.choice([4,8,16]),"cookieEnabled":True,"appCodeName":"Mozilla","appName":"Netscape","appVersion":user_agent.replace("Mozilla/",""),"platform":"Win32","product":"Gecko","userAgent":user_agent,"language":"en-GB","languages":["en-GB","en"],"onLine":True,"webdriver":False,"bluetooth":{},"clipboard":{},"credentials":{},"keyboard":{},"managed":{},"mediaDevices":{},"storage":{},"serviceWorker":{},"virtualKeyboard":{},"wakeLock":{},"deviceMemory":8,"ink":{},"hid":{},"locks":{},"gpu":{},"mediaCapabilities":{},"mediaSession":{},"permissions":{},"presentation":{},"usb":{},"xr":{},"serial":{},"windowControlsOverlay":{},"userAgentData":{"brands":[{"brand":"Google Chrome","version":"117"},{"brand":"Not;A=Brand","version":"8"},{"brand":"Chromium","version":"117"}],"mobile":False,"platform":"Windows"},"plugins":["internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer"]},
                    "dr":"",
                    "exec":False,
                    "wn":[],
                    "wn-mp":5869,
                    "xy":[],
                    "xy-mp":0,
                    "mm":[[669,157,1696008726280],[634,172,1696008726296],[591,185,1696008726312],[522,202,1696008726335],[476,214,1696008726351],[432,223,1696008726368],[394,227,1696008726384],[359,227,1696008726400],[328,227,1696008726416],[299,227,1696008726432],[263,227,1696008726456],[242,230,1696008726472],[216,237,1696008726495],[203,244,1696008726511]],
                    "mm-mp":7.709677419354839
                },
                "session":[],
                "widgetList":[widget_id],
                "widgetId":widget_id,
                "href":"https://discord.com",
                "prev":{"escaped":False,"passed":False,"expiredChallenge":False,"expiredResponse":False}
            },
            "pdc"        : json.dumps({"s":now,"n":0,"p":1,"gcs":random.randint(100,200)},separators=(",",":")),
            "pst"        : False,
            "n"          : subprocess.check_output(["node", './proof.js', self.c['req'], user_agent]).decode().strip(),
            "c"          : json.dumps(self.c,separators=(",",":"))
        }
        try:
            response = self.session.post(f'https://hcaptcha.com/getcaptcha/{self.site_key}',headers=headers,data=payload,timeout_seconds=10)
            return response.json()
        except:
            return False
        
def thread():
    while True:
        start = time.time()

        scraper = Scraper("4c672d35-0701-42b2-88c3-78380b0db560","discord.com")
        success = scraper.get_c()
        if success == False:
            return
        challenge = scraper.get_challenge()
        if challenge == False:
            return
        tasklist       = challenge['tasklist']
        challenge_type = challenge['request_type']
        question       = challenge["requester_question"]["en"]
        folder_name    = question.lower().replace(".","")

        if folder_name not in os.listdir(f"images/{challenge_type}"):
            os.mkdir(f"images/{challenge_type}/{folder_name}")

        def download_image(image_url, challenge_type):
            folder = os.listdir(f"images/{challenge_type}/{folder_name}/")
            headers = {
                'authority'          : 'imgs.hcaptcha.com',
                'accept'             : 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
                'accept-language'    : accept_language,
                'referer'            : 'https://newassets.hcaptcha.com/',
                'sec-ch-ua'          : sec_ch_ua,
                'sec-ch-ua-mobile'   : '?0',
                'sec-ch-ua-platform' : '"Windows"',
                'sec-fetch-dest'     : 'image',
                'sec-fetch-mode'     : 'no-cors',
                'sec-fetch-site'     : 'same-site',
                'user-agent'         : user_agent
            }
            image = httpx.get(image_url, headers=headers).content
            if challenge_type == "image_label_binary":
                image_name = hashlib.md5(image).hexdigest()
                if image_name in folder:
                    return
            else:
                while True:
                    image_name = ''.join(random.choice(string.digits+string.ascii_letters) for _ in range(20))
                    if image_name not in folder:
                        break
            try:
                f = open(f"images/{folder_name}/{image_name}.jpg","wb")
                f.write(image)
                f.close()
            except:
                pass
        threads = []
        for task in tasklist:
            thread = threading.Thread(
                target = download_image, 
                args   = (task["datapoint_uri"],challenge_type)
            )
            threads.append(thread)
            thread.start()
        for t in threads:
            t.join()
        with open_lock:
            with open("questions.txt", "a+") as f:
                f.seek(0)
                if question not in f.read():
                    f.write(question + "\n")
                f.close()
        console.success(
            "Label", f"{folder_name} | {colors.lblue}Images{colors.reset}: {len(tasklist)} | {colors.cyan}Total{colors.reset}: {len(os.listdir(f'images/{folder_name}'))} | {colors.magenta}{round(time.time()-start)}{colors.reset}s"
        )

def scrape_images():
    threads = int(console.input("Threads"))
    for i in range(threads):
        threading.Thread(target=thread).start()
        console.info("Started thread",str(i+1))

def main():
    os.system("cls")
    print("{ Super-Nova | Scraper } ".center(os.get_terminal_size().columns))
    print("1 - [ Image Scraper ]".center(os.get_terminal_size().columns))
    print("2 - [ Proxy Scraper ]".center(os.get_terminal_size().columns))
    inputed = int(console.input())
    if inputed == 2:
        scrape_proxies()
    elif inputed == 1:
        scrape_images()
        if not "images" in os.listdir(os.curdir):
            os.mkdir("images")
        if open("proxies.txt").read() == "<# Free proxies work. #>":
            print("(-) No proxies detected in proxies.txt")
            input("(#) Press ENTER to continue.")
            main()
    else:
        print("(-) Invalid input.")
        input("(#) Press ENTER to return.")
        main()
main()