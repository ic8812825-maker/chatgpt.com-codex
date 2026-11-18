"""Download the public HistData Generic ASCII archive using the advertised form."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
from html.parser import HTMLParser
from pathlib import Path
from urllib import parse,request


class DownloadForm(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active=False
        self.fields={}

    def handle_starttag(self,tag,attrs):
        attributes=dict(attrs)
        if tag=="form":
            self.active=attributes.get("id")=="file_down"
        if tag=="input" and self.active and "name" in attributes:
            self.fields[attributes["name"]]=attributes.get("value","")

    def handle_endtag(self,tag):
        if tag=="form":
            self.active=False


def fetch(month):
    year,number=month[:4],int(month[4:])
    ref=("https://www.histdata.com/download-free-forex-historical-data/"
         f"?/ascii/tick-data-quotes/EURUSD/{year}/{number}")
    headers={"User-Agent":"Mozilla/5.0"}
    form=DownloadForm()
    with request.urlopen(request.Request(ref,headers=headers),timeout=25) as response:
        form.feed(response.read().decode("latin1"))
    if not form.fields:
        raise ValueError("advertised download form absent")
    headers["Referer"]=ref
    post=request.Request("https://www.histdata.com/get.php",
                         parse.urlencode(form.fields).encode(),headers)
    with request.urlopen(post,timeout=60) as response:
        data=response.read(60_000_001)
    if not data.startswith(b"PK") or len(data)>60_000_000:
        raise ValueError(f"unexpected archive response of {len(data)} bytes")
    Path(f"historical-{month}.zip").write_bytes(data)
    return month,len(data),hashlib.sha256(data).hexdigest()


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("months",nargs="+")
    with ThreadPoolExecutor(3) as pool:
        for row in pool.map(fetch,parser.parse_args().months):
            print(*row,flush=True)
