import json
import sys
from datetime import datetime
from types import SimpleNamespace

import requests


def main():
    r = requests.Session()
    while True:
        try:
            resp = r.get("https://api.github.com/repos/JCWasmx86/mesonlsp/releases")
            if resp.status_code != 200:
                continue
        except Exception as exc:
            print(f"{exc}", file=sys.stderr)
            continue
        break
    data_obj = json.loads(resp.text, object_hook=lambda d: SimpleNamespace(**d))
    release = data_obj[0]
    date_str = datetime.today().strftime("%Y-%m-%d")
    time_str = datetime.today().time().hour
    result_obj = {
        "date": date_str,
        "hour": time_str,
        "version": release.tag_name,
    }
    for asset in release.assets:
        result_obj[asset.name] = asset.download_count
    with open(f"{date_str}--{time_str}.json", "w") as filep:
        json.dump(result_obj, filep)


if __name__ == "__main__":
    main()
