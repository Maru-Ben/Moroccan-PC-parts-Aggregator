
CATEGORIES = {
    "CPU": "cpu",
    "GPU": "gpu",
    "RAM": "ram",
    "STORAGE": "storage",
    "MOTHERBOARD": "motherboard",
    "PSU": "psu",
    "CASE": "case"
}

# TODO ADD WEBSITES
SCRAPING_URLS = {
    "https://www.ultrapc.ma": {
        "categories": [
            {"url": "/20-composants", "type": COMPONENTS},
            {"url": "/58-peripheriques", "type": PERIPHERALS}
        ],
        "scraper": "ultrapc"
    },
    "https://nextlevelpc.ma": {
        "categories": [
            {"url": "/143-composants", "type": COMPONENTS},
            {"url": "/148-peripherique-pc", "type": PERIPHERALS},
            {"url": "/189-ecran-pc", "type": PERIPHERALS}
        ],
        "scraper": "nextlevelpc"
    },
    "https://techspace.ma": {
        "categories": [
            {"url": "/collections/composants", "type": COMPONENTS},
            {"url": "/collections/peripheriques", "type": PERIPHERALS}
        ],
        "scraper": "techspace"
    }
}


SCRAPING_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}
 
SCRAPING_WAIT = { # assuming they have bad servers
    "min_seconds": 2,
    "max_seconds": 6
}

