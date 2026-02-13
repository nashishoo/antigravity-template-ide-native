
import { chromium } from 'playwright';
import * as fs from 'fs';
import * as path from 'path';

interface Item {
    name: string;
    base_value: number;
    image_url: string;
    category: string;
    demand: number;
}

const CATEGORIES = ['pets']; // Can be expanded to ['pets', 'eggs', 'vehicles', etc.]
const BASE_URL = 'https://amvgg.com/values';
const OUTPUT_DIR = path.join(__dirname, '../../data');
const OUTPUT_FILE = path.join(OUTPUT_DIR, 'amvgg_dump.json');

async function scrape() {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
        userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    });
    const page = await context.newPage();

    const allItems: Item[] = [];
    const uniqueNames = new Set<string>();

    try {
        for (const category of CATEGORIES) {
            console.log(`Navigating to ${category}...`);
            await page.goto(`${BASE_URL}/${category}`, { waitUntil: 'domcontentloaded', timeout: 60000 });

            // Wait for at least one item to load
            try {
                await page.waitForSelector('div.rounded-2xl.cursor-pointer', { timeout: 10000 });
            } catch (e) {
                console.log('Timeout waiting for selector, seeing if content exists anyway...');
            }

            // Handle cookies/modals if they appear (Generic wait)
            try {
                await page.waitForTimeout(2000);
            } catch (e) { }

            // Infinite scroll loop
            let previousHeight = 0;
            let noChangeCount = 0;

            console.log('Starting auto-scroll...');
            while (noChangeCount < 3) {
                const currentHeight = await page.evaluate(() => document.body.scrollHeight);
                await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
                await page.waitForTimeout(1500); // Wait for load

                const newHeight = await page.evaluate(() => document.body.scrollHeight);
                if (newHeight === previousHeight) {
                    noChangeCount++;
                } else {
                    noChangeCount = 0;
                    previousHeight = newHeight;
                }

                const itemCount = await page.locator('h2').count();
                process.stdout.write(`\rLoaded ${itemCount} items...`);
            }
            console.log('\nFinished scrolling.');

            // Extract data
            const items = await page.evaluate((cat) => {
                const results: any[] = [];
                const unique = new Set();

                // Strategy: specific containers based on inspection
                // The subagent found items are in div.rounded-2xl.cursor-pointer
                // We look for h2 (name) and spans (value) inside these.

                const cards = document.querySelectorAll('div.rounded-2xl.cursor-pointer');

                cards.forEach(card => {
                    const nameEl = card.querySelector('h2');
                    if (!nameEl) return;

                    const name = nameEl.innerText.trim();
                    if (!name) return;

                    // Value: Find a span that looks like a number
                    const spans = Array.from(card.querySelectorAll('span'));
                    const valueSpan = spans.find(s => /^\d+(\.\d+)?$/.test(s.innerText.trim()));
                    const valueText = valueSpan ? valueSpan.innerText.trim() : '0';
                    const base_value = parseFloat(valueText);

                    // Image
                    const imgEl = card.querySelector('img');
                    let image_url = imgEl ? imgEl.src : '';

                    // Demand
                    // Look for 'Demand' span, then get the stars from the next sibling
                    const demandLabel = spans.find(el => el.textContent?.trim() === 'Demand');
                    const starsSpan = demandLabel ? demandLabel.nextElementSibling : null;
                    const demand = starsSpan ? (starsSpan.textContent?.match(/★/g) || []).length : 0;

                    results.push({
                        name,
                        base_value,
                        image_url,
                        category: cat.charAt(0).toUpperCase() + cat.slice(1), // Capitalize
                        demand
                    });
                });

                return results;
            }, category);

            console.log(`Extracted ${items.length} items from ${category}.`);

            for (const item of items) {
                // filter duplicates across categories if any, though unlikely if strictly separated
                if (!uniqueNames.has(item.name)) {
                    uniqueNames.add(item.name);
                    allItems.push(item);
                }
            }
        }

        // Ensure output directory exists
        if (!fs.existsSync(OUTPUT_DIR)) {
            fs.mkdirSync(OUTPUT_DIR, { recursive: true });
        }

        fs.writeFileSync(OUTPUT_FILE, JSON.stringify(allItems, null, 2));
        console.log(`Successfully saved ${allItems.length} items to ${OUTPUT_FILE}`);

    } catch (error) {
        console.error('Error scraping AMVGG:', error);
    } finally {
        await browser.close();
    }
}

scrape();
