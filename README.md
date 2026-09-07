# CodeAlpha Data Analytics Internship — Task 1: Web Scraping

This project completes **Task 1: Web Scraping** from the CodeAlpha Data Analytics internship instructions.

## Objective
Use Python and BeautifulSoup to extract structured data from a public web page and save it as a custom CSV dataset.

## Tools
- Python 3.10+
- requests
- BeautifulSoup4
- pandas

## Project structure
```
CodeAlpha_Task1_Web_Scraping/
├── scraper.py
├── requirements.txt
├── README.md
├── data/
│   └── books.csv          # generated after running the scraper
└── output/
    └── scraping_summary.txt
```

## How to run
1. Open this folder in VS Code.
2. Create/activate a virtual environment (optional but recommended).
3. Install dependencies:
   `pip install -r requirements.txt`
4. Run:
   `python scraper.py`
5. The script creates `data/books.csv` and `output/scraping_summary.txt`.

The scraper uses the public **Books to Scrape** practice website, which is designed for web-scraping exercises.

## What is extracted
For each book:
- title
- price
- availability
- rating
- product URL

The script navigates through multiple pages and collects the available book records.

## Internship submission
The CodeAlpha instructions ask interns to upload complete source code to GitHub using a repository named `CodeAlpha_ProjectName` and submit the completed task through the provided submission form. The PDF also says that at least 2 or 3 tasks must be completed for internship completion. 
