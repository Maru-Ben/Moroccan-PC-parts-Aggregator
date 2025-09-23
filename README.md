# Moroccan PC parts Aggregator

## What We're Building

 A centralized platform that aggregates and compares PC parts prices from various Moroccan e-commerce websites. The goal is to simplify the shopping experience for PC enthusiasts, gamers, and professionals by providing real-time price data, product availability, and deal alerts in one place.

## What We Want to Achieve

* Users can search for PC parts using a search bar
* System displays relevant products from our database
* When a user clicks on a specific product, they see price and availability information from all stores that carry that item
* Essentially creating a comprehensive price comparison tool for the Moroccan PC parts market

## Technical Stack

* Framework: Django
* Database: PostgreSQL
* Data Collection: Custom Django management command for web scraping

## Project Structure

```text
Moroccan-PC-parts-Aggregator/
├── .gitattributes
├── .gitignore
├── LICENSE
├── README.md
├── price-tracker/
│   ├── backend/
│   │   └── tracker/
│   │       ├── manage.py
│   │       ├── requirements.txt
│   │       ├── coreapi/
│   │       │   ├── __init__.py
│   │       │   ├── admin.py
│   │       │   ├── apps.py
│   │       │   ├── models.py
│   │       │   ├── serializers.py
│   │       │   ├── tests.py
│   │       │   ├── urls.py
│   │       │   ├── views.py
│   │       │   ├── management/
│   │       │   │   ├── __init__.py
│   │       │   │   └── commands/
│   │       │   │       └── scrape.py
│   │       │   ├── migrations/
│   │       │   └── scraper/
│   │       │       ├── __init__.py
│   │       │       ├── logger.py
│   │       │       ├── main.py
│   │       │       ├── scapers.py
│   │       │       ├── utils.py
│   │       │       └── logs/
│   │       └── tracker/
│   │           ├── __init__.py
│   │           ├── asgi.py
│   │           ├── settings.py
│   │           ├── urls.py
│   │           └── wsgi.py
```

## What We've Accomplished

* Complete web scraping system that successfully extracts product data from multiple Moroccan PC parts websites
* Data storage pipeline that stores all scraped information in PostgreSQL
* Django management command that handles the scraping process
* Working data collection infrastructure - we can reliably gather product information from various stores

## TODO

* [ ] Modify the scraper to get the full product name, would mean to go into the product page.
* [ ] add a way to hold the config.

## Improvements

* [ ] add a logic in the scraping to change scrape agent if one fails
* [ ] AI PC builder to help users build their PC based on their needs and budget
* [ ] add refresh stock status when user clicks on a product
