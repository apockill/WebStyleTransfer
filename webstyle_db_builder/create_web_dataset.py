import random
import hashlib
from pathlib import Path
from argparse import ArgumentParser

import requests
import tldextract

from crawler import Webpage, create_basic_driver

DMOZ_URL = "https://www.kaggle.com/shawon10/url-classification-dataset-dmoz/version/2#URL%20Classification.csv"

DEFAULT_DIMS = [480, 720, 900, 960, 1024, 1050, 1080,
                1280, 1440, 1500, 1600, 1700, 1800, 1900]


def main():
    parser = ArgumentParser()
    parser.add_argument("-p", "--dmoz-urls", required=True,
                        help="Path to URL Classification dataset in DMOZ format"
                             f". Downloadable from here: {DMOZ_URL}"
                             " seperated by newline characters.")
    parser.add_argument("-d", "--driver-path", required=True,
                        help="Path to the chromedriver file")
    parser.add_argument("-s", "--save-dir", required=True,
                        help="Directory to save scraped images")
    parser.add_argument("-r", "--render-dims", nargs="+", type=int,
                        default=DEFAULT_DIMS,
                        help="Different dimensions to render the pages at")
    parser.add_argument("-n", "--renders-per-page", type=int, required=True,
                        help="Number of times to render each page")

    args = parser.parse_args()

    with open(args.dmoz_urls, "r") as file:
        lines = file.readlines()


    save_dir = Path(args.save_dir)
    existing = [str(f.name).split("_")[0] for f in save_dir.glob("*.png")]

    for line in lines:
        url_rank, url = [s.strip() for s in line.split('\t')]
        if url == "Hidden profile":
            continue
        url = "http://" + url

        if str(url_rank) in existing:
            print(f"Skipping site {url} - has already been crawled.")
            continue

        # Check that the server is up
        try:
            r = requests.get(url, timeout=3)
            assert r.status_code == 200, \
                f"Status code was {r.status_code}"
        except Exception as e:
            print(f"Failed to load {url} because {type(e)}, {e}")
            continue

        browser = create_basic_driver(args.driver_path)
        try:
            page = Webpage(url, browser)
            for _ in range(args.renders_per_page):
                dims = [random.choice(args.render_dims),
                        random.choice(args.render_dims)]

                # Create the save path
                domain = tldextract.extract(url).domain
                path = save_dir / f"{url_rank}_{domain}_" \
                                  f"({dims[0]}x{dims[1]}).png"

                page.save_screenshot(path, dims,
                                     scroll_percent=random.random())

        except Exception as e:
            print(f"Failed to load {url} because {type(e)}, {e}")
        finally:
            browser.quit()



if __name__ == "__main__":
    main()
