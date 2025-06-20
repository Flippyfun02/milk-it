from recipe_scrapers import scrape_me
from grocery_list import GroceryList

def main():
    grocery_list = GroceryList()
    MENU = "---\n1. Add Recipe \n2. Add Item\n3. See Grocery List \n4. Quit\n---"
    choice = 0
    print(MENU)
    while choice != 4:
        try:
            choice = int(input("Select an Option (1-4): "))
        except ValueError:
            continue
        match (choice):
            case 1:
                try:
                    url = input("URL: ").strip()
                    scraper = scrape_me(url)
                    grocery_list.add_all(scraper.ingredients())
                    print("Success!")
                except ValueError as e:
                    print("Failed,", e)
            case 2:
                item = input("Item: ")
                try:
                    grocery_list.add(item)
                    print("Success!")
                except ValueError: 
                    print("Failed!")
            case 3:
                print(grocery_list)
            case _:
                continue
        print(MENU)

if __name__ == "__main__":
    main()