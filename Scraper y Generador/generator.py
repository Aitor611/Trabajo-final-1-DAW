import psycopg2
import os
import shutil
from jinja2 import Environment, FileSystemLoader

# Configuración
DB_CONFIG = {
    'host': '192.168.100.10',
    'database': 'SQL',
    'user': 'postgres',
    'password': 'trabajofindecurso',
    'port': 5432
}

# Directorios relativos a la ubicación de este script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')


def get_products():
    """Fetch all products from database."""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT id, product_name, price, release_date, image_url FROM products ORDER BY id;")
    products = cur.fetchall()
    cur.close()
    conn.close()
    return products

def generate_site():
    """Main function: reads DB, processes templates, copies static files, writes output."""

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for file_name in os.listdir(STATIC_DIR):
        src = os.path.join(STATIC_DIR, file_name)
        dst = os.path.join(OUTPUT_DIR, file_name)
        if os.path.isfile(src):
            shutil.copy(src, dst)
            print(f"Copied static file: {file_name}")

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

    products = get_products()
    if not products:
        print("No products found in database. Please run the scraper first.")
        return


    index_template = env.get_template('index_template.html')
    index_html = index_template.render(products=products)
    index_path = os.path.join(OUTPUT_DIR, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_html)
    print("Generated index.html")



    product_template = env.get_template('product_template.html')
    for prod in products:
        prod_id = prod[0]
        product_dict = {
            'id': prod[0],
            'name': prod[1],
            'price': prod[2] if prod[2] else "Free",
            'release_date': prod[3] if prod[3] else "Unknown",
            'image_url': prod[4] if prod[4] else ""
        }
        detail_html = product_template.render(product=product_dict)
        detail_path = os.path.join(OUTPUT_DIR, f'product_{prod_id}.html')
        with open(detail_path, 'w', encoding='utf-8') as f:
            f.write(detail_html)
    print(f"Generated {len(products)} detail pages")


if __name__ == "__main__":
    generate_site()
