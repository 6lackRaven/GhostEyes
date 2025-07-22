import re
import tldextract
from collections import defaultdict
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def extract_domain(url: str) -> str:
    """Extract root domain from URL"""
    extracted = tldextract.extract(url)
    return f"{extracted.domain}.{extracted.suffix}"

def is_valid_url(url: str) -> bool:
    """Validate URL format"""
    pattern = re.compile(
        r'^(https?://)?'  # http:// or https://
        r'([a-zA-Z0-9.-]+)'  # domain
        r'(\.[a-zA-Z]{2,63})'  # TLD
        r'(:[0-9]{1,5})?'  # port
        r'(/[^\s]*)?$'  # path
    )
    return bool(pattern.match(url))

def get_robots_txt(url: str) -> list:
    """Fetch and parse robots.txt"""
    robots_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}/robots.txt"
    try:
        response = requests.get(robots_url, timeout=5)
        if response.status_code == 200:
            return [line.split(": ")[1].strip() 
                    for line in response.text.splitlines() 
                    if line.startswith("Disallow:")]
    except:
        return []
