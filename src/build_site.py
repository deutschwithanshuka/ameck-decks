import pathlib, shutil
D=pathlib.Path(__file__).parent
html=(D/'how-ameck-works.html').read_text()
pdfbtn='<a id="pdf-btn" href="Ameck-How-We-Work.pdf" download aria-label="Download PDF" style="all:unset;cursor:pointer;padding:9px 13px;border-radius:999px;display:inline-flex;align-items:center;gap:6px;text-transform:uppercase"><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 4v11M7 10l5 5 5-5M5 20h14"/></svg>PDF</a>\n <button id="fs-btn"'
assert html.count('<button id="fs-btn"')==1
html=html.replace('<button id="fs-btn"',pdfbtn,1)
head='''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="How Ameck Business House finds, checks, ships and delivers products for Indian businesses. A visual guide for customers.">
<meta property="og:title" content="How Ameck Works">
<meta property="og:description" content="We find the product you want anywhere in the world, buy it at the best price, check its quality and deliver it to your door.">
<meta property="og:type" content="website">
<meta name="theme-color" content="#27505A">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%2327505A'/%3E%3Crect x='8' y='8' width='16' height='16' rx='3' fill='%23E6B36F'/%3E%3C/svg%3E">
<style>html{-webkit-text-size-adjust:100%}body{margin:0}</style>
</head>
<body>
'''
out=D.parent
(out/'index.html').write_text(head+html+'\n</body>\n</html>\n')
shutil.copy(D/'Ameck-How-We-Work.pdf', out/'Ameck-How-We-Work.pdf')
(out/'.nojekyll').write_text('')
(out/'README.md').write_text('''# How Ameck Works: sales deck

A 30-slide interactive guide to how Ameck Business House sources, checks, ships and delivers products for Indian businesses. Salespeople can open it on a laptop or a phone and pitch straight from the browser.

## Open it

Once GitHub Pages is on (Settings, then Pages, then deploy from the `main` branch, root folder), the deck is live at:

`https://<your-github-username>.github.io/<this-repo-name>/`

## Presenting

| On a laptop | On a phone |
| --- | --- |
| Opens as full slides, one at a time | Opens as a scrolling page, slides stacked |
| Arrow keys, space, mouse wheel or the arrows in the bar | Swipe up and down |
| F for full screen, C for contents | Turn the phone sideways for full slides |
| Contents button jumps to any section | Contents button jumps to any section |

Link straight to a slide by adding `#s` and its number, for example `#s26` opens the savings estimator.

## Things to tap during a pitch

- **Cover globe:** drag to spin it.
- **Our network (slide 6):** filter the map by region.
- **How we work and Grow with us:** point at a step to lift it.
- **Seven ways we help (slide 9):** tap a card for its key terms, then jump to its detail slide.
- **Customer stories (slides 21 and 22):** tap a story for the problem, what we did and the result.
- **Estimate your saving (slide 26):** set the client's order value and orders per year to show their estimated saving, with the working.
- **Questions (slide 29):** tap a question to open the answer.

The PDF button in the bar downloads `Ameck-How-We-Work.pdf`, which you can email or send on WhatsApp.

## Files

- `index.html`: the deck, one self-contained page. Fonts are built in. The rotating globe loads three.js from cdnjs.
- `Ameck-How-We-Work.pdf`: the same slides as a PDF.
''')
print("site built")
