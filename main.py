import sys
import requests
import pandas as pd

def fetch_menu_data(restaurant_id):
    # Construct the URL with the provided restaurant_id
    url = f"https://www.swiggy.com/dapi/menu/pl?page-type=REGULAR_MENU&complete-menu=true&lat=18.56&lng=73.95&restaurantId={restaurant_id}"
    try:
        # Send a GET request to the Swiggy API
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for 4xx or 5xx status codes
        return response.json()  # Return JSON response if successful
    except requests.exceptions.RequestException as e:
        # Handle any request exceptions (e.g., network issues)
        print(f"Failed to fetch menu data: {e}")
        return None

def extract_menu_details(menu_data):
    # Check if the received data has the expected structure
    if 'data' not in menu_data:
        print("Unexpected data format received.")
        return []

    # Extract relevant details from the menu data
    menu_items = []
    for category in menu_data['data'].get('sections', []):
        for item in category.get('items', []):
            menu_items.append({
                'Name': item.get('name', ''),
                'Price': item.get('price', ''),
                'Description': item.get('description', ''),
                'Category': category.get('title', '')
            })
    return menu_items

def main():
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py <restaurant_id>")
        sys.exit(1)

    # Extract restaurant_id from command-line arguments
    restaurant_id = sys.argv[1]
    
    # Fetch menu data from Swiggy API
    menu_data = fetch_menu_data(restaurant_id)
    if menu_data:
        # Extract menu details if data is successfully fetched
        menu_items = extract_menu_details(menu_data)
        if menu_items:
            # Convert extracted data into a DataFrame and save it as CSV
            df = pd.DataFrame(menu_items)
            df.to_csv(f"{restaurant_id}_menu.csv", index=False)
            print("Menu data extracted and saved to CSV successfully.")
        else:
            print("No menu items found.")
    else:
        print("Failed to fetch menu data.")

if __name__ == "__main__":
    main()
