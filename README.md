This project implements a web crawler designed to discover and list all product URLs across multiple e-commerce websites. The crawler efficiently handles pagination and dynamically loaded content to gather unique product URLs.

Features
Asynchronous scraping for improved performance using asyncio.
Integration of Selenium for handling dynamic content and JavaScript-rendered pages.
Concurrency control using semaphores to limit the number of simultaneous requests.
Output of product URLs to a structured JSON file.

Implementation Details
Domain-Specific Scrapers
Amazon: Utilizes Selenium to navigate through product pages, handles pagination, and extracts product URLs that match specific patterns.
Flipkart: Placeholder for implementing scraping logic; can be expanded in a similar manner as Amazon.
Myntra: Placeholder for implementing infinite scroll handling.

like that can integrate more ecommerce.

Concurrency Control
A semaphore is used to limit the number of concurrent requests, ensuring that the crawler operates efficiently without overwhelming the target servers.

Future Improvements
Implement Auto-Learning of URL Patterns:

Data Collection: As we scrape each website, collect and store the product URLs and their associated patterns (e.g., regex patterns or parts of the URL).

Pattern Extraction:

Use regex or string manipulation techniques to identify common structures in the collected URLs.
For example, if we find URLs like /dp/B07XYZ1234 and /gp/product/B07XYZ1234, we might deduce that the pattern involves /dp/ or /gp/product/.
Pattern Storage:

Maintain a dictionary or database to store learned patterns for each domain.
For each new URL encountered, will update the storage with its corresponding pattern.

Pattern Matching:

Before scraping, will check if there are existing patterns for a domain.  Will use these patterns to filter potential product URLs dynamically as we scrape the site.
If we discover a new URL pattern while scraping, add it to the storage for future use.

