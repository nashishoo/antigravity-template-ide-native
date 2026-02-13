# AMVGG Scraper

This script extracts pet values from `amvgg.com` using Playwright.

## Prerequisites

- Node.js (v16+)
- `npm install` (to install dependencies: playwright, typescript, ts-node)

## Usage

Run the scraper with the following command:

```bash
npx ts-node src/scrapers/amvgg.ts
```

## Output

The script will:
1.  Launch a headless browser.
2.  Navigate to `https://amvgg.com/values`.
3.  Scroll automatically to load all pets.
4.  Save the data to `data/amvgg_dump.json`.

## Configuration

- **Categories**: You can modify the `CATEGORIES` array in `src/scrapers/amvgg.ts` to scrape other sections (e.g., `eggs`, `vehicles`).
- **Timeouts**: If your internet is slow, you may need to increase the `timeout` in `page.goto` or `waitForSelector`.
