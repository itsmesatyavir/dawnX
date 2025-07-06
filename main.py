import httpx
from fake_useragent import FakeUserAgent
from datetime import datetime
from colorama import *
import asyncio, json, os, pytz, uuid

wib = pytz.timezone('Asia/Jakarta')

class Dawn:
    def __init__(self) -> None:
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "chrome-extension://fpdkjdnhkakefebpekbdhillbhonfjjp",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": FakeUserAgent().random
        }
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Ping - FORESTARMY {Fore.BLUE + Style.BRIGHT}Dawn - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}USE ON 2ND ACCOUNT ONLY {Fore.YELLOW + Style.BRIGHT} CODE RESHARED BY AIRDROPSCRIPTFA 
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    def load_accounts(self):
        filename = "accounts.json"
        try:
            if not os.path.exists(filename):
                self.log(f"{Fore.RED}File {filename} Not Found.{Style.RESET_ALL}")
                return []
            with open(filename, 'r') as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []

    async def load_proxies(self, use_proxy_choice: int):
        filename = "proxy.txt"
        try:
            if use_proxy_choice == 1:
                async with httpx.AsyncClient() as client:
                    response = await client.get("https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt")
                response.raise_for_status()
                content = response.text
                with open(filename, 'w') as f:
                    f.write(content)
                self.proxies = content.splitlines()
            else:
                if not os.path.exists(filename):
                    self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                    return
                with open(filename, 'r') as f:
                    self.proxies = f.read().splitlines()

            if not self.proxies:
                self.log(f"{Fore.RED + Style.BRIGHT}No Proxies Found.{Style.RESET_ALL}")
                return

            self.log(f"{Fore.GREEN + Style.BRIGHT}Proxies Total  : {Style.RESET_ALL}{Fore.WHITE + Style.BRIGHT}{len(self.proxies)}{Style.RESET_ALL}")
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed To Load Proxies: {e}{Style.RESET_ALL}")
            self.proxies = []

    def check_proxy_schemes(self, proxy):
        if proxy.startswith(('http://', 'https://', 'socks4://', 'socks5://')):
            return proxy
        return f"socks5://{proxy}"

    def get_next_proxy_for_account(self, email):
        if email not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[email] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[email]

    def rotate_proxy_for_account(self, email):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[email] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy

    def generate_app_id(self):
        prefix = "67"
        app_id = prefix + uuid.uuid4().hex[len(prefix):]
        return app_id

    def mask_account(self, account):
        if "@" in account:
            local, domain = account.split('@', 1)
            mask_account = local[:3] + '*' * 3 + local[-3:]
            return f"{mask_account}@{domain}"
        return account[:3] + '*' * 3 + account[-3:]

    def print_message(self, email, proxy, color, message):
        self.log(
            f"{Fore.CYAN + Style.BRIGHT}[ Account:{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} {self.mask_account(email)} {Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT} Proxy: {Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT}{proxy}{Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}Status:{Style.RESET_ALL}"
            f"{color + Style.BRIGHT} {message} {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}"
        )

    def print_question(self):
        while True:
            try:
                print("1. Run With Monosans Proxy")
                print("2. Run With Private Proxy")
                print("3. Run Without Proxy")
                choose = int(input("Choose [1/2/3] -> ").strip())
                if choose in [1, 2, 3]:
                    return choose
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2 or 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2 or 3).{Style.RESET_ALL}")

    async def user_data(self, app_id: str, email: str, token: str, proxy=None, retries=5):
        url = f"https://ext-api.dawninternet.com/api/atom/v1/userreferral/getpoint?appid={app_id}"
        headers = {**self.headers, "Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        for attempt in range(retries):
            try:
                async with httpx.AsyncClient(proxies=proxy, timeout=120) as client:
                    response = await client.get(url, headers=headers)
                    response.raise_for_status()
                    return response.json()["data"]
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(email, proxy, Fore.YELLOW, f"GET Earning Data Failed: {Fore.RED+Style.BRIGHT}{str(e)}")
                return None

    async def send_keepalive(self, app_id: str, email: str, token: str, use_proxy: bool, proxy=None, retries=5):
        url = f"https://ext-api.dawninternet.com/chromeapi/dawn/v1/userreward/keepalive?appid={app_id}"
        data = json.dumps({"username": email, "extensionid": "fpdkjdnhkakefebpekbdhillbhonfjjp", "numberoftabs": 0, "_v": "1.1.5"})
        headers = {**self.headers, "Authorization": f"Bearer {token}", "Content-Length": str(len(data)), "Content-Type": "application/json"}

        for attempt in range(retries):
            try:
                async with httpx.AsyncClient(proxies=proxy, timeout=120) as client:
                    response = await client.post(url, headers=headers, content=data)
                    response.raise_for_status()
                    return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(email, proxy, Fore.RED, f"PING Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")
                proxy = self.rotate_proxy_for_account(email) if use_proxy else None
                return None

    async def process_user_earning(self, app_id: str, email: str, token: str, use_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(email) if use_proxy else None
            user = await self.user_data(app_id, email, token, proxy)
            if user:
                referral_point = user.get("referralPoint", {}).get("commission", 0)
                reward_point = user.get("rewardPoint", {})
                reward_points = sum(value for key, value in reward_point.items() if "points" in key.lower() and isinstance(value, (int, float)))
                total_points = referral_point + reward_points
                self.print_message(email, proxy, Fore.WHITE, f"Earning {total_points:.0f} PTS")
            await asyncio.sleep(5 * 60)

    async def process_send_keepalive(self, app_id: str, email: str, token: str, use_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(email) if use_proxy else None
            keepalive = await self.send_keepalive(app_id, email, token, use_proxy, proxy)
            if keepalive:
                self.print_message(email, proxy, Fore.GREEN, f"PING Success")
            await asyncio.sleep(5 * 60)

    async def process_accounts(self, app_id: str, email: str, token: str, use_proxy: bool):
        tasks = [
            asyncio.create_task(self.process_user_earning(app_id, email, token, use_proxy)),
            asyncio.create_task(self.process_send_keepalive(app_id, email, token, use_proxy))
        ]
        await asyncio.gather(*tasks)

    async def main(self):
        try:
            accounts = self.load_accounts()
            if not accounts:
                self.log(f"{Fore.RED + Style.BRIGHT}No Accounts Loaded.{Style.RESET_ALL}")
                return

            use_proxy_choice = self.print_question()
            use_proxy = use_proxy_choice in [1, 2]

            self.clear_terminal()
            self.welcome()
            self.log(f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}{Fore.WHITE + Style.BRIGHT}{len(accounts)}{Style.RESET_ALL}")

            if use_proxy:
                await self.load_proxies(use_proxy_choice)

            self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}" * 75)

            tasks = []
            for account in accounts:
                app_id = self.generate_app_id()
                email = account.get('Email')
                token = account.get('Token')
                if app_id and "@" in email and token:
                    tasks.append(asyncio.create_task(self.process_accounts(app_id, email, token, use_proxy)))

            await asyncio.gather(*tasks)
        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        bot = Dawn()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{Fore.RED + Style.BRIGHT}[ EXIT ] Dawn - BOT{Style.RESET_ALL}")
