# 🧠 Project Context: Catapaz Adopt Me Bot

## 1. Executive Summary
**Project:** Catapaz Adopt Me Bot (PWA)
**Architect:** Catapaz (AI)
**Client:** Dolan (Human)
**Mission:** Create an offline-capable, AI-powered trading assistant for Adopt Me.
**Template:** [Antigravity Workspace Template](https://github.com/nashishoo/antigravity-template-ide-native.git)

## 2. Architecture & Data Flow

### A. Core Engine (Client)
-   **Tech:** React + Vite + TypeScript.
-   **State:** Zustand with LocalStorage Persistence (`zustand/middleware`).
-   **Features:**
    -   Value Calculation: `(Base * Variant) + Potions * Demand`.
    -   PWA: Offline support via `vite-plugin-pwa`.
    -   UI: Tailwind CSS + Lucide Icons (Holographic Theme).

### B. Data Layer (Scraper)
-   **Source:** AMVGG.com.
-   **Technique:** Playwright Scraper (`src/scrapers/amvgg.ts`).
-   **Data Points:** Name, Base Value, Image, Demand (1-3 Stars).
-   **Output:** `client/src/data/items.json` (Static JSON for speed).

### C. Intelligence Layer (Server)
-   **Brain:** Gemini 2.0 Flash.
-   **Gateway:** Node.js Express Server (`server/index.js`).
-   **Endpoint:** `POST /analyze`.
-   **Role:** Analyzes trade fairness and suggests negotiation tactics.

## 3. Key Directories
-   `client/`: Frontend application.
-   `server/`: Backend API for Gemini.
-   `src/scrapers/`: Data ingestion scripts.
-   `docs/`: Project documentation and reviews.
-   `artifacts/`: Workflow artifacts (`task.md`, `worker_prompts.md`).

## 4. Coding Standards
-   **Strict Separation:** Logic (Calculations) vs UI (Components).
-   **Zero External DB:** Persistence must be local-first for reliability.
-   **Agentic Workflow:** All major changes must pass through the Architect -> Worker flow.

## 5. Credits
Built using the **Antigravity Workspace Template**.
Forked and Evolved by **Catapaz** (Gemini 3 Pro + Opus 4.6).
