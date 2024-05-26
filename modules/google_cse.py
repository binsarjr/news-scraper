from urllib.parse import *
import json, re, requests


def get_params(cx: str):
    resp = requests.get(f"https://cse.google.com/cse.js?cx={cx}")
    text = resp.text

    cse_token = re.search(r'"cse_token":\s+"([^\"]+)"', text, re.DOTALL).group(1)
    cselibv = re.search(r'"cselibVersion":\s+"([^\"]+)"', text, re.DOTALL).group(1)

    import random
    import string

    # Membuat string acak sebanyak 4 karakter
    random_string = "".join(random.choices(string.digits, k=4))

    return {
        "q": None,
        "num": None,
        "start": None,
        "rsz": "filtered_cse",
        "hl": "en",
        "source": "gcsc",
        "gss": ".com",
        "cselibv": cselibv,
        "cx": cx,
        "safe": "active",
        "cse_tok": cse_token,
        "lr": "",
        "cr": "",
        "gl": "",
        "filter": "0",
        "sort": "",
        "as_oq": "",
        "as_sitesearch": "",
        "exp": "cc",
        "callback": f"google.search.cse.api{random_string}",
    }


def make_request_args(
    keyword: str, limit=20, page=1, params={}, headers={}, cookies={}, **kwargs
):
    if limit > 20:
        limit = 20

    params["q"] = keyword
    params["num"] = limit
    params["start"] = (page - 1) * limit

    return {
        "url": "https://cse.google.com/cse/element/v1?" + urlencode(params),
        "headers": headers,
        "cookies": cookies,
        **kwargs,
    }


def extract_google_search_cse(text: str):
    pattern = r"google\.search\.cse\.[^\(]+\((.*?)\);"

    # Find the match using regex
    data = json.loads(re.search(pattern, text, re.DOTALL).group(1))
    return data
