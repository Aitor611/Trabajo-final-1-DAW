## Architecture
The architecture uses two virtual machines connected via a private network. The host machine runs the development tools and browser. The web virtual machine runs Nginx and serves the static files. The database virtual machine runs PostgreSQL. The communication between VMs happens over internal IP addresses. A diagram is included in the repository.

## Virtual Machines Setup
Both virtual machines run Linux Mint 22.3 Cinnamon. The database VM has 1 GB of RAM, 10 GB of disk, and two CPU cores. The web VM has the same specifications. Each VM is assigned a static IP address in the same subnet to allow communication. The network is configured as Host-Only or NAT Network. The installation process includes setting up the operating system, creating a regular user, and verifying network connectivity.

## Database (PostgreSQL)
PostgreSQL is installed on the database VM. A database and a dedicated user are created. The products table contains columns for identifier, product name, price, release date, and image URL. The table is created automatically by the scraper. Remote access is enabled by modifying the PostgreSQL configuration files to listen on all interfaces and accept connections from the private network. The service is restarted after changes.

## Scraping (Data Extraction)
The scraper is written in Python and uses the Requests library to fetch Steam search pages and BeautifulSoup to parse the HTML. It extracts the title, price, release date, and image URL of each game. The scraper iterates through search result pages, collecting up to 200 games. The extracted data is stored in the PostgreSQL table. A short delay is added between requests to avoid overloading the server. The scraper can be run from any machine that has network access to the database.

## Static Site Generator
The generator is a Python script that connects to the database, reads all products, and produces a complete static website. It creates an index.html file with a grid of product cards. It also creates individual detail pages for each product. The generator copies external style and script files from a static folder into the output directory. The output is organized inside a folder named output. The generator is executed after the database has been populated.

## Frontend Features
The website includes pagination showing nine products per page with previous and next buttons. A live search input allows filtering products by name as the user types. A clear button resets the search. Product images are displayed in the cards and on the detail pages; images are centered and maintain their aspect ratio. The design is responsive, adapting to different screen sizes, and uses a dark color scheme inspired by Steam.

## Web Server (Nginx)
Nginx is installed on the web virtual machine. The default server block is configured to listen on port 80, set the document root to the directory containing the static files, and specify index.html as the default file. After copying the generated website files into the document root, Nginx is reloaded to serve the new content.

## Deployment Instructions
First, set up the virtual machines with the described network configuration. Second, install and configure PostgreSQL on the database VM. Third, run the scraper to populate the database. Fourth, run the generator to create the static files inside the output folder. Fifth, copy the entire content of the output folder to the Nginx document root on the web VM. Finally, reload Nginx and access the site using the web VM's IP address from a browser.

## Security Notes
HTTPS and two-factor authentication were researched but not implemented because the site is static and runs on a local network for educational purposes. For a production environment, HTTPS should be enabled with Let's Encrypt, and firewall rules should restrict access to the database to trusted IP addresses. Strong passwords and principle of least privilege are recommended.

## Troubleshooting
If the database column image_url is missing, it can be added with an SQL command. If Nginx returns a 404 error, the document root should be verified. If images do not appear, the scraper output should be checked to confirm that image URLs were collected. If CSS or JavaScript files are not loaded, ensure they exist in the output folder and that the paths in the HTML are correct. If pagination or search does not work, verify that the script.js file is properly included and that the product cards have the required data attributes.

## Repository and Documentation
The GitHub repository contains all source code and this documentation. The documentation is published via GitHub Pages. A PDF with screenshots of the process, configuration, and final website is submitted as required. 

[go to document start](README.md)
