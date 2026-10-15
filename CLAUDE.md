# Ameck sales deck: guide for Claude

This repo is the public sales deck "How Ameck Works" for Ameck Business House, served by GitHub Pages at https://decks.ameckhouse.com. Every push to `main` goes live in about a minute.

## Never touch
- `CNAME` must stay `decks.ameckhouse.com`.
- Do not edit `index.html` by hand. It is generated; change the source in `src/` and rebuild.
- DNS lives in the owner's Shopify admin (record `decks` CNAME to `deutschwithanshuka.github.io`). Leave it alone.
- Never add the internal vision deck or any internal plans to this public repo.

## How it is built
- `src/gen.py`: all slide content (one `slide(theme, section, body)` call per slide, in order). Edit text and slides here.
- `src/shell.py`: shared look and behaviour: colour palette (`SOFT` map, applied over the original hex codes), laptop slide mode, phone scroll mode, controls, 3D helpers (`box`, `bb`, `scene`), WebGL globe, WhatsApp button (`WA_NUMBER`, `WA_TEXT`).
- `src/render.py`: renders the PDF and screenshots with Playwright, and checks every slide fits.
- `src/build_site.py`: writes the final `index.html` (adds the PDF button and page metadata) and copies the PDF to the repo root.
- `fonts/` (Bodoni Moda for headings, Figtree for text, OFL licence) and `map/` (world map and globe points) are build inputs.

Rebuild after any change, from `src/` (needs Python 3.12 or newer):

```
pip install playwright && python -m playwright install chromium   # first time only
cd map && npm install three@0.128.0 && cd ..                       # first time only, for the globe in the PDF
cd src
python gen.py
python render.py Ameck-How-We-Work.pdf shots pdf      # must print "no overflow"
python render.py x shots phone                        # phone screenshots in src/shots/m*.png
python build_site.py
```

Then check the screenshots, commit `index.html`, the PDF and the source, and push.

## House rules for the copy
- No em dashes or en dashes anywhere in the text. Use full stops or commas.
- Money in Indian format with "Rs.", for example Rs. 5,00,000. Triple-check every price calculation and show the working.
- Plain, short sentences written for the customer.
- Business facts to keep correct: minimum 25 units and 20 kg per import or export shipment (any mix); customers need only GST, Ameck works under its own IEC and does 100% of the paperwork; product cost is paid 100% upfront, shipping is billed at actual cost after landing; no credit.
- Contact: WhatsApp and phone +91 83021 92742, info@ameckhouse.com, websites ameckhouse.in and ameckhouse.com, catalogue.ameckhouse.com. No office address.

## Check before pushing
- Laptop: slides fit 1280 x 720 with "no overflow".
- Phone (390 px wide): nothing scrolls sideways, carousels swipe, text is not crowded.
- Interactive parts still work: flip cards, map filter, savings estimator, FAQ, WhatsApp button.
