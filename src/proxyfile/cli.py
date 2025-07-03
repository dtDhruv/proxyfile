# SPDX-License-Identifier: MIT
import argparse
import pathlib
from .core import download_via_proxy


def main() -> None:
    p = argparse.ArgumentParser(
        prog="proxyfile",
        description="Download files through random free proxies from spys.me",
    )
    p.add_argument("url", help="File URL to download")
    p.add_argument("-o", "--outfile", type=pathlib.Path)
    p.add_argument("-c", "--country", metavar="CC", help="Filter by country code")
    p.add_argument(
        "-r",
        "--max-retries",
        type=int,
        default=5,
        help="Number of different proxies to try (default: 5)",
    )
    args = p.parse_args()
    download_via_proxy(
        url=args.url,
        outfile=args.outfile,
        country=args.country,
        max_retries=args.max_retries,
    )


if __name__ == "__main__":
    main()
