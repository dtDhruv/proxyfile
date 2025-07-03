# SPDX-License-Identifier: MIT
from __future__ import annotations
import pathlib
import random
import time
from contextlib import suppress
from urllib.parse import urlsplit
import requests
from tqdm import tqdm
from .proxylist import spys_me, ProxyEntry


def _proxy_is_alive(proxy: str, timeout: int = 5) -> bool:
    try:
        requests.head(
            "https://www.google.com",
            proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"},
            timeout=timeout,
        )
        return True
    except Exception:
        return False


def _get_proxies(cc: str | None = None, need: int = 200) -> list[str]:
    raw: list[ProxyEntry] = spys_me()
    if cc:
        raw = [p for p in raw if p.country_code.lower() == cc.lower()]
    pool = [f"{p.host}:{p.port}" for p in raw]
    random.shuffle(pool)
    return pool[:need]


def download_via_proxy(
    url: str,
    outfile: pathlib.Path | None = None,
    *,
    country: str | None = None,
    max_retries: int = 5,
) -> None:
    """Download *url* through random live proxies from spys.me."""
    outfile = outfile or pathlib.Path(urlsplit(url).path.split("/")[-1] or "download")
    tmpfile = outfile.with_suffix(".part")

    proxies = _get_proxies(country)
    if not proxies:
        raise RuntimeError("No proxies matched your criteria.")

    for attempt, proxy in enumerate(proxies, 1):
        if attempt > max_retries:
            raise RuntimeError("All proxies failed.")

        print(f"[{attempt}/{max_retries}] probing {proxy} …", end="", flush=True)
        if not _proxy_is_alive(proxy):
            print(" dead")
            continue
        print(" ok")

        try:
            with requests.get(
                url,
                proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"},
                timeout=30,
                stream=True,
            ) as r:
                r.raise_for_status()
                total = int(r.headers.get("content-length", 0))
                with (
                    tmpfile.open("wb") as fh,
                    tqdm(
                        total=total,
                        unit="B",
                        unit_scale=True,
                        unit_divisor=1024,
                        desc=str(outfile.name),
                    ) as bar,
                ):
                    for chunk in r.iter_content(chunk_size=8192):
                        fh.write(chunk)
                        bar.update(len(chunk))
            tmpfile.rename(outfile)
            print(f"✓ Downloaded via {proxy} → {outfile}")
            return
        except KeyboardInterrupt:
            with suppress(FileNotFoundError):
                tmpfile.unlink(missing_ok=True)
            raise
        except Exception as exc:
            print("×", exc)
            with suppress(FileNotFoundError):
                tmpfile.unlink(missing_ok=True)
            time.sleep(2)
