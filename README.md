# WEB-001 v1.0 - Automatic Newspaper Website

Project code: WEB-001 | Version: v1.0 | Author: Mr. Pankaj Fulpagare

## How it works
1. `feeds.json` lists the news sources (RSS) by section. Edit it to add or remove sources.
2. `update_news.py` reads every feed and writes `news.json` (headline, short summary, link, source).
3. `index.html` shows `news.json` and re-checks it every 5 minutes. Sections, search, dark mode, mobile friendly.
4. `.github/workflows/update.yml` runs the updater every 30 minutes on GitHub and saves the new `news.json`.

## Go live (free)
1. Create a GitHub repository and upload this whole folder (keep the `.github` folder).
2. Settings > Pages > deploy from the main branch (or create a Render "Static Site" from the repo).
3. Settings > Actions > allow workflows. Run "update-news" once from the Actions tab.
4. The site now updates itself every 30 minutes.

## Test on your PC
    python update_news.py
    python -m http.server 8000
Then open http://localhost:8000

## Notes
- Check each source's RSS terms before launching publicly; keep the link-back to the original story.
- Next versions: Hindi/Marathi sections (v1.1), fact-check badge using Loom (v1.2), ads or newsletter signup (v1.3).
