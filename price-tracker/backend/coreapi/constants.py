
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
            {"url": "/39-cartes-graphiques", "type": CATEGORIES["GPU"]}
        ],
        "scraper": "ultrapc"
    },
    "https://nextlevelpc.ma": {
        "categories": [
            {"url": "/144-carte-graphique-video-gpu", "type": CATEGORIES["GPU"]}
        ],
        "scraper": "nextlevelpc"
    },
    "https://techspace.ma": {
        "categories": [
            {"url": "/collections/carte-graphique", "type": CATEGORIES["GPU"]}
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

IMAGE_PRIORITY_RETAILERS = [
    'techspace', # Best images
    'ultrapc',      
    'nextlevelpc', # Worst
]


