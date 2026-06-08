# Project Documentation: Static Steam Catalog
## Overview

This project implements a static product catalog for Steam games. Data is extracted from Steam using web scraping with Python, Requests, and BeautifulSoup. Products are stored in a PostgreSQL database on a dedicated virtual machine. A static site generator written in Python reads the database and generates HTML, CSS, and JavaScript files. The static site is served by Nginx on another virtual machine. The catalog includes pagination, live search, and product images.

## Team and Product
The team consists of Pablo, Sofía, and Aitor. The chosen product category is video games from Steam. The data source is the Steam search page.

[go to documentation](Documentation.md)
