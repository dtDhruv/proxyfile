import re
import requests
from dataclasses import dataclass
from typing import List


@dataclass(slots=True)
class ProxyEntry:
    host: str
    port: int
    country_code: str  # "US", "DE", …


def spys_me() -> List[ProxyEntry]:
    """
    Parse https://spys.me/proxy.txt and return a list of ProxyEntry objects.

    Each line in the feed looks like:
        <IP>:<PORT>  <CC>-<flags>  <more flags…>

    Example:
        104.238.232.210:999  PR-N   -
             ^--------------^  ^^
                 host:port     |__ two‑letter country code
    """
    text = requests.get("https://spys.me/proxy.txt", timeout=10).text

    pattern = re.compile(
        r"^(?P<ip>\d{1,3}(?:\.\d{1,3}){3}):(?P<port>\d+)\s+"
        r"(?P<cc>[A-Z]{2})-",  # grab cc before the first “-”
        re.MULTILINE,
    )

    return [
        ProxyEntry(m["ip"], int(m["port"]), m["cc"]) for m in pattern.finditer(text)
    ]
