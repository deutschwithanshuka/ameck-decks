import asyncio, pathlib, sys
from playwright.async_api import async_playwright

HERE = pathlib.Path(__file__).parent
import os
CHROME = os.environ.get("CHROME_PATH") or None
THREE = HERE.parent / "map" / "node_modules" / "three" / "build" / "three.min.js"
ARGS = ["--no-sandbox", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"]

async def route3(page):
    # Use a local copy of three.js when present (npm install three@0.128.0 inside map/), otherwise the CDN.
    if THREE.exists():
        await page.route("**/three.min.js", lambda r: r.fulfill(path=str(THREE), content_type="application/javascript"))

async def main():
    pdf_name = sys.argv[1] if len(sys.argv) > 1 else "Ameck-How-We-Work.pdf"
    shots = HERE / (sys.argv[2] if len(sys.argv) > 2 else "shots"); shots.mkdir(exist_ok=True)
    mode = sys.argv[3] if len(sys.argv) > 3 else "pdf"
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME, args=ARGS) if CHROME else await p.chromium.launch(args=ARGS)
        if mode == "pdf":
            pg = await b.new_page(viewport={"width": 1280, "height": 720})
            msgs = []; pg.on("console", lambda m: msgs.append(m.text)); pg.on("pageerror", lambda e: msgs.append("ERR " + str(e)))
            await route3(pg)
            await pg.goto((HERE / "print.html").as_uri() + "?print=1")
            await pg.emulate_media(media="print")
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(2500)
            gl = await pg.evaluate("[...document.querySelectorAll('[data-globe]')].map(g=>g.classList.contains('no-gl')?'no-gl':'gl')")
            issues = await pg.evaluate("""() => {const out=[];document.querySelectorAll('.slide').forEach((s,i)=>{const r=s.getBoundingClientRect();const body=s.querySelector('.s-in');
              if(body.scrollHeight>body.clientHeight+1) out.push(`slide ${i+1}: taller by ${body.scrollHeight-body.clientHeight}px`);});return out;}""")
            print("globe:", gl); print("\n".join(issues) or "no overflow"); print("console:", [m for m in msgs if 'ERR' in m or 'rror' in m][:5])
            for i, s in enumerate(await pg.query_selector_all(".slide"), 1):
                await s.screenshot(path=str(shots / f"s{i:02d}.png"))
            await pg.pdf(path=str(HERE / pdf_name), width="1280px", height="720px", print_background=True,
                         margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        elif mode == "present":
            pg = await b.new_page(viewport={"width": 1440, "height": 860})
            await route3(pg)
            idx = [int(x) for x in sys.argv[4].split(",")]
            for i in idx:
                pg = await b.new_page(viewport={"width": 1440, "height": 860}); await route3(pg)
                await pg.goto((HERE / "print.html").as_uri() + f"#s{i}")
                await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(1800)
                await pg.mouse.move(700, 400)
                await pg.screenshot(path=str(shots / f"p{i:02d}.png"))
        elif mode == "phone":
            ctx = await b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
            pg = await ctx.new_page(); await route3(pg)
            await pg.goto((HERE / "print.html").as_uri())
            await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(2000)
            wide = await pg.evaluate("document.documentElement.scrollWidth")
            print("phone scrollWidth", wide)
            for i, s in enumerate(await pg.query_selector_all(".slide"), 1):
                await s.scroll_into_view_if_needed(); await pg.wait_for_timeout(1000)
                await s.screenshot(path=str(shots / f"m{i:02d}.png"))
        await b.close()

asyncio.run(main())
