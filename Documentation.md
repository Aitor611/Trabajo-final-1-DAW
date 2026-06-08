## Architecture
Our architecture uses two virtual machines connected via a private network. The host machine runs development tools and the browser. The web virtual machine runs Nginx and serves the static files. The database virtual machine runs PostgreSQL. Communication between the virtual machines occurs over internal IP addresses. We have included a diagram in the repository.

## Virtual Machines Setup
Both virtual machines run Linux Mint 22.3 Cinnamon. The database VM has 1 GB of RAM, 10 GB of disk, and two CPU cores. The web VM has the same specifications. We assigned each VM a static IP address in the same subnet to allow communication. The network is configured as Host-Only or NAT Network. Our installation process included setting up the operating system, creating a regular user, and verifying network connectivity.

## Database (PostgreSQL)
We installed PostgreSQL on the database VM. We created a database and a dedicated user. The products table contains columns for id, product name, price, release date, and image URL. The scraper automatically creates the table. We enabled remote access by modifying PostgreSQL configuration files to listen on all interfaces and accept connections from the private network. We restarted the service after making changes.

## Scraping (Data Extraction)
Our scraper is written in Python and uses the Requests library to fetch Steam search pages and BeautifulSoup to parse the HTML. It extracts the title, price, release date, and image URL for each game. The scraper iterates through search result pages, collecting up to 200 games. The extracted data is stored in the PostgreSQL table. We added a short delay between requests to avoid overloading the server. The scraper can be run from any machine that has network access to the database.

## Static Site Generator
The generator is a Python script that connects to the database, reads all products, and produces a complete static website. It creates an index.html file with a grid of product cards. It also creates individual detail pages for each product. The generator copies external style and script files from a static folder into the output directory. The output is organized inside a folder named "output". We run the generator after the database has been populated.

## Frontend Features
Our website includes pagination showing nine products per page with previous and next buttons. A live search input allows filtering products by name as the user types. A clear button resets the search. Product images are displayed in the cards and on the detail pages; images are centered and maintain their aspect ratio. The design is responsive, adapting to different screen sizes, and uses a dark color scheme inspired by Steam.

## Web Server (Nginx)
We installed Nginx on the web virtual machine. We configured the default server block to listen on port 80, set the document root to the directory containing the static files, and specified index.html as the default file. After copying the generated website files into the document root, we reloaded Nginx to serve the new content.

## Deployment Instructions
First, we set up the virtual machines with the described network configuration. Second, we installed and configured PostgreSQL on the database VM. Third, we ran the scraper to populate the database. Fourth, we ran the generator to create the static files inside the output folder. Fifth, we copied the entire content of the output folder to the Nginx document root on the web VM. Finally, we reloaded Nginx and accessed the site using the web VM's IP address from a browser.

## Security Notes
We researched HTTPS and two-factor authentication but did not implement them because the site is static and runs on a local network for educational purposes. For a production environment, HTTPS should be enabled with Let's Encrypt, and firewall rules should restrict database access to trusted IP addresses. We recommend using strong passwords and the principle of least privilege.

## Troubleshooting
If the image_url column is missing from the database, we can add it with an SQL command. If Nginx returns a 404 error, we verify the document root. If images do not appear, we check that the scraper collected the image URLs. If CSS or JavaScript files are not loaded, we ensure they exist in the output folder and that the paths in the HTML are correct. If pagination or search does not work, we verify that the script.js file is properly included and that the product cards have the required data attributes.

## Repository and Documentation
Our GitHub repository contains all source code and this documentation. The documentation is published via GitHub Pages. We will submit a PDF with screenshots of the process, configuration, and final website as required.

[go to document start](README.md)
