from recipe_scrapers import scrape_me

def main():
    url = input("URL: ").strip()
    scraper = scrape_me(url)
    print(scraper.ingredients())

if __name__ == "__main__":
    main()