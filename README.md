# Project Documentation: Static Steam Catalog

---

## Overview
This project implements a **static product catalog** for Steam games. The system operates through an automated pipeline distributed across a virtualized infrastructure:

* **Data Extraction:** Data is extracted from Steam using web scraping powered by **Python**, `Requests`, and `BeautifulSoup`.
* **Storage:** Extracted products are stored in a **PostgreSQL** database hosted on a dedicated virtual machine.
* **Site Generation:** A **Static Site Generator (SSG)** written in Python reads the database to generate production-ready HTML, CSS, and JavaScript files.
* **Web Serving:** The final static site is served by **Nginx** running on a separate virtual machine.
* **User Interface:** The catalog features interactive elements such as client-side **pagination**, **live search**, and responsive product images.

---

## Team and Product
* **Development Team:** Pablo, Sofía, and Aitor.
* **Product Category:** Video games from Steam.
* **Data Source:** Official Steam search pages.

[go to documentation](Documentation.md)
