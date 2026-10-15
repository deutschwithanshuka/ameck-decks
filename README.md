# How Ameck Works: sales deck

A 30-slide interactive guide to how Ameck Business House sources, checks, ships and delivers products for Indian businesses. Salespeople can open it on a laptop or a phone and pitch straight from the browser.

## Open it

The deck is live at **https://decks.ameckhouse.com**

Setup, done once:

1. DNS for ameckhouse.com has a CNAME record: `decks` pointing to `deutschwithanshuka.github.io`.
2. GitHub Pages is on: Settings, then Pages, deploy from the `main` branch, root folder.
3. Custom domain in Pages is `decks.ameckhouse.com`, with Enforce HTTPS ticked. The `CNAME` file in this repo holds the same domain.

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
