import requests
from bs4 import BeautifulSoup
import time
import psycopg2


def save_to_db(games):
    try:   
        connection = psycopg2.connect(
            host='192.168.100.10',
            database='SQL',
            user='postgres',
            password='trabajofindecurso',
            port=5432
        )
        cursor = connection.cursor()
        # Add image_url column
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                product_name VARCHAR(255),
                price VARCHAR(100),
                release_date VARCHAR(100),
                image_url TEXT
            );
        ''')
        cursor.executemany('''
            INSERT INTO products (product_name, price, release_date, image_url)
            VALUES (%(product_name)s, %(price)s, %(release_date)s, %(image_url)s);
        ''', games)
        
        connection.commit()
        cursor.close()
        connection.close()
        print('Data saved successfully (including images)')
    except Exception as e:
        print(f"ERROR SAVING TO DB: {e}")


def extract_games():
    MAX_GAMES = 200 
    GAMES_PER_PAGE = 50


    games_list = []
    start = 0


    print("Searching for results from Steam...")


    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    }


    while start < MAX_GAMES:
        params = {
            'term': '',       
            'start': start, 
            'count': GAMES_PER_PAGE
        }
        
        response = requests.get('https://store.steampowered.com/search/', params=params, headers=headers)
        
        if response.status_code != 200:
            print(f"Error connecting to Steam at offset {start}")
            break
            
        soup = BeautifulSoup(response.text, "html.parser")
        game_blocks = soup.find_all("a", class_="search_result_row")
        
        for block in game_blocks:
            # Title
            title_tag = block.find("span", class_="title")
            title = title_tag.text.strip() if title_tag else "No title"
            
            # Price
            price_tag = block.find("div", class_="discount_prices")
            price = price_tag.text.strip().replace('\n', ' ') if price_tag else "Free or no price"
            
            # Release date
            date_tag = block.find("div", class_="search_released responsive_secondrow")
            release_date = date_tag.text.strip() if date_tag else "No release date"
            
            # Image
            img_tag = block.find("img", class_="search_capsule")
            if img_tag and img_tag.get('src'):
                image_url = img_tag['src']
            else:
                # fallback: any img inside the block
                img_fallback = block.find("img")
                image_url = img_fallback['src'] if img_fallback and img_fallback.get('src') else ""
            
            game_data = {
                "product_name": title,
                "price": price,
                "release_date": release_date,
                "image_url": image_url
            }
            
            games_list.append(game_data)
            print(f"Extracted: {title} | {price} | {release_date} | Image: {image_url[:60]}...")
            
        start += GAMES_PER_PAGE
        time.sleep(1)
        
    print(f"\nProcess completed! Collected {len(games_list)} games.")
    return games_list


if __name__ == "__main__":
    games_data = extract_games()
    if games_data:
        save_to_db(games_data)