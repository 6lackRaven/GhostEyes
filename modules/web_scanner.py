import aiohttp
from bs4 import BeautifulSoup
import dns.resolver

class WebScanner:
    def __init__(self):
        self.session = aiohttp.ClientSession()
        
    async def subdomain_scan(self, domain, wordlist):
        """Async subdomain enumeration"""
        valid_subdomains = []
        async with self.session:
            for sub in wordlist:
                target = f"{sub}.{domain}"
                try:
                    await dns.resolver.resolve(target, 'A')
                    valid_subdomains.append(target)
                except:
                    continue
        return valid_subdomains
    
    async def tech_detect(self, url):
        """Identify web technologies"""
        async with self.session.get(url) as response:
            headers = response.headers
            html = await response.text()
            
        tech_stack = []
        if "X-Powered-By" in headers:
            tech_stack.append(headers["X-Powered-By"])
        if "Server" in headers:
            tech_stack.append(headers["Server"])
            
        soup = BeautifulSoup(html, 'html.parser')
        if soup.find('meta', attrs={'name': 'generator'}):
            tech_stack.append(soup.find('meta', 
                          attrs={'name': 'generator'})['content'])
        return list(set(tech_stack))
