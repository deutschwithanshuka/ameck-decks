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
<meta name="theme-color" content="#10352E">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%2310352E'/%3E%3Ccircle cx='16' cy='16' r='7' fill='%23E3A1AD'/%3E%3C/svg%3E">
<style>html{-webkit-text-size-adjust:100%}body{margin:0}</style>
</head>
<body>
'''
out=D.parent
(out/'index.html').write_text(head+html+'\n</body>\n</html>\n')
shutil.copy(D/'Ameck-How-We-Work.pdf', out/'Ameck-How-We-Work.pdf')
(out/'.nojekyll').write_text('')
# README.md is maintained by hand in the repo root; the build no longer overwrites it.
print("site built")
