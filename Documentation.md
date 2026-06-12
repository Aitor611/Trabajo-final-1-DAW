# Project Documentation: Architecture and Web Deployment

## 1. System Architecture
Our architecture relies on a distributed model utilizing **two virtual machines (VMs)** interconnected via a private virtual network.

* **Host Machine:** Houses the development tools and the web browser for testing.
* **Web VM:** Runs an **Nginx** server responsible for serving the static files of the website.
* **Database VM:** Hosts the **PostgreSQL** engine where all the data is stored.

> **Note:** Communication between both virtual machines occurs exclusively over their internal IP addresses. A detailed infrastructure diagram is included in the repository.

---

## 2. Virtual Machines Setup
Both virtual machines share the same base operating system and hardware specifications, configured within the same subnet using a **Host-Only** or **NAT Network** adapter.

### Hardware Specifications (Per VM)
| Component | Specification |
| :--- | :--- |
| **Operating System** | Linux Mint 22.3 Cinnamon |
| **RAM Memory** | 1 GB |
| **Storage** | 10 GB Hard Disk |
| **Processor** | 2 CPU Cores |

### Initialization Process
1. Base operating system installation.
2. Creation of a regular user with standard privileges.
3. Assignment of **static IP addresses** within the same network range.
4. Network connectivity verification using ping tests.

---

## 3. Database (PostgreSQL)
PostgreSQL was installed and configured on the **Database VM**. The scraping script handles the automatic generation of the database schema.

### `products` Table Structure
* `id` (Primary Key)
* `product_name` (Game Title)
* `price` (Price)
* `release_date` (Release Date)
* `image_url` (Link to the image asset)

### Remote Access Configuration
To allow the website and the scraper to connect, PostgreSQL configuration files were modified to:
* Listen on all network interfaces (`listen_addresses = '*'`).
* Accept external connections originating from the private network range.
* *The service was restarted after applying these changes.*

---

## 4. Scraping (Data Extraction)
The extraction component is a script developed in **Python** tasked with gathering information from the Steam store.

* **Technologies:** `Requests` (for HTTP requests) and `BeautifulSoup` (for HTML parsing).
* **Workflow:** It iterates through the search result pages until collecting a **maximum of 200 games**.
* **Best Practices:** A short delay was implemented between requests to avoid overloading the target server.
* **Flexibility:** The scraper can be executed from any machine that has network access to the PostgreSQL database.

---

## 5. Static Site Generator (SSG)
A Python script acts as a static generator, processing data from the database and transforming it into a production-ready web interface.
The script reads the records from the database, renders the templates, and packages all the content inside the `/output` directory.

---

## 6. Frontend Features
The user interface has been designed drawing inspiration from Steam's visual aesthetics, prioritizing responsiveness and user experience:

* **Pagination:** Displays exactly **9 products per page** with navigation buttons (`Previous` / `Next`).
* **Live Search:** Real-time product filtering by name as the user types, including a clear button to reset the search.
* **Visual Design:** Adaptable layout (*Responsive Design*) with a dark color scheme (*Dark Mode*). Product images are centered and always maintain their original aspect ratio.

---

## 7. Web Server (Nginx)
The **Web VM** utilizes Nginx optimized for high-performance static content delivery.

* **Port:** Listens on the standard port `80`.
* **Document Root:** Points directly to the local directory where the static files are hosted.
* **Default File:** Configured to resolve `index.html` automatically.
* **Update:** After moving the files to the root directory, an Nginx service *reload* is executed to apply changes without server downtime.

---

## 8. Deployment Instructions
Follow this strict order to deploy the project from scratch:
1. **Step 1:** Spin up the VMs and configure the internal network.
2. **Step 2:** Install and configure PostgreSQL on the Database VM.
3. **Step 3:** Run the Python Scraper to populate the database.
4. **Step 4:** Run the Static Generator to create the `/output` folder.
5. **Step 5:** Transfer the entire content of `/output` to the Nginx Document Root on the Web VM.
6. **Step 6:** Reload Nginx and access the site using the Web VM's IP address.
---

## 9. Security Notes
> **Project Context:** Since this is a purely educational and local environment, features such as HTTPS or two-factor authentication (2FA) were not implemented in this phase.

If this environment were to be moved to **Production**, the following measures should be applied:
* Enable **HTTPS** using valid certificates via *Let's Encrypt*.
* Configure strict **Firewall** rules to restrict database access exclusively to trusted IP addresses.
* Implement robust password policies and the **principle of least privilege** for all system users.

---

## 10. Troubleshooting

| Symptom / Error | Probable Cause | Suggested Solution |
| :--- | :--- | :--- |
| Missing `image_url` column | Outdated database table | Add the column manually using SQL commands (`ALTER TABLE`). |
| Nginx **404 Not Found** Error | Incorrect path configuration | Verify the *Document Root* directive inside the Nginx configuration file. |
| Images do not appear | Data extraction failure | Check if the scraper successfully saved the image URLs into the database. |
| CSS or JS styles fail to load | Broken links | Ensure that the files exist in `/output` and that their relative paths in the HTML are correct. |
| Search or pagination doesn't work | Script integration error | Verify that `script.js` is properly included and that the product cards have the required data attributes. |

---

## 11. Repository and Documentation
* **Source Code:** All source code and this documentation are centralized in our GitHub repository.
* **Web Access:** The documentation is publicly available via **GitHub Pages**.
* **Submission:** A complementary PDF document will be submitted, including screenshots of the entire setup process, executed commands, and the final look of the website.

[go to document start](README.md)
