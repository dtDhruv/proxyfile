# proxyfile

A command-line tool to download files through random free proxies from spys.me.

## Installation

```bash
pip install proxyfile
```

## Usage

To download a file, simply provide the URL:

```bash
proxyfile <URL>
```

For example:

```bash
proxyfile http://speed.hetzner.de/100MB.bin
```

This will download the file `100MB.bin` into your current directory.

### Options

You can specify an output file, filter proxies by country, and set the number of retries.

-   `-o, --outfile`: Specify the output file name.
-   `-c, --country`: Use proxies from a specific country (e.g., `US`, `DE`).
-   `-r, --max-retries`: Set the maximum number of proxies to try.

**Example:**

Download a file using a proxy from the United States and save it as `my_file.zip`, trying up to 10 different proxies:

```bash
proxyfile http://example.com/file.zip -o my_file.zip -c US -r 10
```

## How it Works

`proxyfile` fetches a list of free proxies from `spys.me`. It then tries to download the requested file through a randomly selected proxy. If the download fails, it will try another proxy until the download is successful or the maximum number of retries is reached.

## License

This project is licensed under the MIT License.
