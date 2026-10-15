"""Shared presentation shell: laptop slide mode, phone scroll mode, controls, 3D helpers, WebGL globe."""
import json, pathlib

HERE = pathlib.Path(__file__).parent
GLOBE_PTS = (HERE.parent / "map" / "globe.json").read_text()
SOFT = {  # original deck colours -> current palette: ocean blue, warm amber, aqua, coral
 "#0E3640":"#13294B","#17505C":"#1E3A66","#22646F":"#2F5D9E","#2C6670":"#35588C","#0A2026":"#0B1A33","#154A54":"#2A4F87",
 "#1F6570":"#3A69B0","#2E7C86":"#4A7FD0","#336F79":"#3D639C","#061A1F":"#0A1528","#081A1F":"#0D1A2E",
 "#132A30":"#16233A","#566C70":"#5B6B84","#9CB8BB":"#B3C4E0","#E8F0EE":"#F3F6FC","#E3ECEA":"#E6ECF5","#93A9AC":"#9FB0CC",
 "#EDF1EF":"#F2F5FA","#FBFCFB":"#FFFFFF","#C9D5D3":"#D9E1EE","#DDE5E3":"#E4E9F2",
 "#E9A23B":"#FFA94D","#C7852A":"#F08A2C","#9C6519":"#C76F1F","#F7E1B8":"#FFE6C7","#6A4510":"#7A3E06",
 "#C4542A":"#CF432D","#F4D9CD":"#FBDCD5","#F7E6DE":"#FDEEEA","#7A2F13":"#8E2A1A",
 "#9FD3C5":"#4FD1C5","#7FB8AA":"#36B3A8","#5E9A8C":"#2A8F87","#D7EEE7":"#DDF5F2","#DCEAE7":"#E7EEFA","#FFE2A8":"#FFE3C2",
 "0x0b2d35":"0x16335c","0xe9a23b":"0xffa94d","0x9fd3c5":"0x4fd1c5","0x8fd0d2":"0x9cc2ff","0xffe2a8":"0xffe3c2",
 "rgba(14,54,64":"rgba(19,41,75","rgba(10,30,35":"rgba(12,24,48","rgba(8,26,31,.86)":"rgba(12,26,52,.86)",
 "rgba(4,16,20,.55)":"rgba(8,18,38,.5)","rgba(233,162,59":"rgba(255,169,77","rgba(34,100,111":"rgba(47,93,158",
 "rgba(159,211,197":"rgba(120,170,255","rgba(95,163,171":"rgba(91,141,239","rgba(232,240,238":"rgba(243,246,252",
}
WA_NUMBER = "918302192742"
WA_TEXT = "Hi%20Ameck%2C%20I%20saw%20your%20guide%20and%20would%20like%20a%20quote."
WA_URL = f"https://wa.me/{WA_NUMBER}?text={WA_TEXT}"
WA_ICON = '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 20l1.3-3.9A8 8 0 1 1 8 19z"/><path d="M9.2 8.6c.2-.5.6-.5.9-.5h.5c.2 0 .4.1.5.4l.6 1.5c.1.2 0 .4-.1.6l-.5.6c.6 1.1 1.4 1.9 2.5 2.5l.6-.5c.2-.1.4-.2.6-.1l1.5.6c.3.1.4.3.4.5v.5c0 .3 0 .7-.5.9-.9.5-2.4.4-4.3-1.2-1.9-1.5-2.9-3.4-2.7-4.8z"/></svg>'
def soften(html):
    import re
    keys = sorted(SOFT, key=len, reverse=True)
    pat = re.compile("|".join(re.escape(k) for k in keys), re.I)
    low = {k.lower(): v for k, v in SOFT.items()}
    return pat.sub(lambda m: low[m.group(0).lower()], html)

THREE_CDN = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"
HUBS = [[23.1,113.3],[25.0,121.5],[10.8,106.7],[13.75,100.5],[3.1,101.7],[-6.2,106.8],[35.7,139.7],[37.6,127.0],
        [23.8,90.4],[25.2,55.3],[24.7,46.7],[41.0,29.0],[53.55,10.0],[45.5,9.2],[52.2,21.0],[38.7,-9.1],[51.5,-0.1]]

SHELL_CSS = r"""
/* ---------- presentation shell ---------- */
:root{--ui-bg:rgba(8,26,31,.86);--ui-fg:#E8F0EE;--ui-mute:#9CB8BB;--stage-bg:#061A1F;--accent-deep:#E8590C;--wa:#25D366;--wa-dark:#128C4B}
.slide.dark{background:radial-gradient(1100px 620px at 88% -10%,rgba(91,141,239,.45),transparent 62%),radial-gradient(900px 520px at -5% 110%,rgba(255,169,77,.20),transparent 60%),radial-gradient(rgba(243,246,252,.05) 1px,transparent 1.3px) 0 0/22px 22px,var(--sea)}
.slide:not(.dark){background:radial-gradient(900px 520px at 100% 0%,rgba(91,141,239,.12),transparent 62%),radial-gradient(760px 460px at 0% 100%,rgba(79,209,197,.12),transparent 60%),var(--fog)}
.slide.paper{background:radial-gradient(900px 520px at 100% 0%,rgba(255,169,77,.10),transparent 62%),radial-gradient(760px 460px at 0% 100%,rgba(91,141,239,.08),transparent 60%),var(--paper)}
.slide:not(.dark) .num{color:var(--accent-deep)}
.slide .card[style*="background:var(--sea)"] .num{color:var(--marigold)}
html.present-root,body.present{height:100%;overflow:hidden}
body.present{padding:0;background:radial-gradient(1200px 700px at 50% 0%,#1B3A6B,transparent 70%),var(--stage-bg)}
body.present .page-head{display:none}
body.present .deck{position:fixed;inset:0;display:block;max-width:none;margin:0;perspective:2400px}
body.present .slide{position:absolute;left:50%;top:50%;width:1280px;height:720px;aspect-ratio:auto;max-width:none;
  transform:translate(-50%,-50%) scale(var(--k,1)) translateX(var(--tx,0px)) rotateY(var(--ry,0deg));
  opacity:0;visibility:hidden;border-radius:12px;box-shadow:0 40px 90px -30px rgba(0,0,0,.75);
  transition:transform .8s cubic-bezier(.2,.7,.15,1),opacity .5s ease,visibility 0s linear .8s}
body.present .slide.is-before{--tx:-300px;--ry:16deg}
body.present .slide.is-after{--tx:300px;--ry:-16deg}
body.present .slide.is-active{opacity:1;visibility:visible;--tx:0px;--ry:0deg;transition:transform .8s cubic-bezier(.2,.7,.15,1),opacity .5s ease,visibility 0s}
@media (prefers-reduced-motion:reduce){body.present .slide{transition:opacity .2s,visibility 0s linear .2s}body.present .slide.is-before,body.present .slide.is-after{--tx:0px;--ry:0deg}}
@media (prefers-reduced-motion:no-preference){
  body.present .slide.enter .body>*,body.feed .slide.enter .body>*{animation:rise .75s cubic-bezier(.2,.7,.2,1) both}
  body.present .slide.enter .body>*:nth-child(2),body.feed .slide.enter .body>*:nth-child(2){animation-delay:.07s}
  body.present .slide.enter .body>*:nth-child(3),body.feed .slide.enter .body>*:nth-child(3){animation-delay:.14s}
  body.present .slide.enter .body>*:nth-child(4),body.feed .slide.enter .body>*:nth-child(4){animation-delay:.21s}
  body.present .slide.enter .body>*:nth-child(n+5),body.feed .slide.enter .body>*:nth-child(n+5){animation-delay:.28s}
}
@keyframes rise{from{opacity:0;translate:0 18px}to{opacity:1;translate:0 0}}

.ctrl{position:fixed;left:50%;bottom:calc(14px + env(safe-area-inset-bottom,0px));transform:translateX(-50%);z-index:50;display:flex;align-items:center;gap:2px;
  padding:5px;border-radius:999px;background:var(--ui-bg);color:var(--ui-fg);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);
  font-family:var(--f-mono);font-size:12px;letter-spacing:.06em;box-shadow:0 10px 30px -10px rgba(0,0,0,.6);transition:opacity .35s,translate .35s;white-space:nowrap}
.ctrl button{all:unset;cursor:pointer;padding:9px 13px;border-radius:999px;display:inline-flex;align-items:center;gap:6px;text-transform:uppercase}
.ctrl button:hover{background:rgba(232,240,238,.12)}
.ctrl button:focus-visible{outline:2px solid var(--marigold);outline-offset:1px}
.ctrl button[hidden]{display:none}
.ctrl .ic{width:16px;height:16px}
.ctrl #count{padding:0 8px;min-width:5.6em;text-align:center;color:var(--ui-fg)}
body.feed .ctrl .pv,body.feed .ctrl #fs-btn{display:none}
body.present:not(.ui-on) .ctrl:not(:hover):not(:focus-within){opacity:0;translate:0 10px;pointer-events:none}
.bar{position:fixed;left:0;top:0;width:100%;height:3px;z-index:50;display:none;background:rgba(232,240,238,.08)}
body.present .bar{display:block}
.bar i{display:block;height:100%;width:0;background:var(--marigold);transition:width .5s}
.hint{position:fixed;right:18px;bottom:calc(20px + env(safe-area-inset-bottom,0px));z-index:49;font-family:var(--f-mono);font-size:11px;letter-spacing:.08em;
  text-transform:uppercase;color:var(--ui-mute);display:none}
body.present.ui-on .hint{display:block}
#toc{position:fixed;inset:0;z-index:60;background:rgba(4,16,20,.55);display:flex;justify-content:flex-end}
#toc[hidden]{display:none!important}
#toc .panel{width:min(400px,100%);height:100%;overflow:auto;background:#0E3640;color:var(--ui-fg);display:flex;flex-direction:column;gap:6px;
  padding:calc(22px + env(safe-area-inset-top,0px)) max(22px,env(safe-area-inset-right,0px)) 28px 24px;box-shadow:-20px 0 60px -20px rgba(0,0,0,.6)}
#toc h2{font-family:var(--f-display);font-stretch:112%;font-size:22px;margin:0 0 10px;color:var(--ui-fg)}
#toc .close{all:unset;cursor:pointer;align-self:flex-end;font-family:var(--f-mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--ui-mute);padding:6px 8px;border-radius:6px}
#toc .close:focus-visible,#toc .item:focus-visible{outline:2px solid var(--marigold)}
#toc .item{all:unset;cursor:pointer;display:grid;grid-template-columns:2.6em 1fr;gap:10px;align-items:baseline;padding:10px 12px;border-radius:8px;font-size:15px}
#toc .item:hover{background:rgba(232,240,238,.08)}
#toc .item.on{background:rgba(233,162,59,.16)}
#toc .item b{font-family:var(--f-mono);font-weight:500;font-size:12px;color:var(--marigold)}
body.feed{padding-bottom:90px}
body.feed .deck{gap:22px}
@media print{.ctrl,.bar,#toc,.hint{display:none!important}}

/* ---------- interactive depth ---------- */
.card,.stamp,.path,.story{position:relative}
body.present .tiltable{transition:transform .35s cubic-bezier(.2,.7,.2,1),box-shadow .35s;transform-style:preserve-3d;will-change:transform}
body.present .tiltable.tilting{transition:transform .08s linear,box-shadow .3s;box-shadow:0 22px 40px -22px rgba(10,30,35,.55)}
.tiltable::after{content:"";position:absolute;inset:0;border-radius:inherit;pointer-events:none;opacity:0;transition:opacity .3s;
  background:radial-gradient(420px circle at var(--gx,50%) var(--gy,50%),rgba(255,255,255,.22),transparent 55%)}
.tiltable.tilting::after{opacity:1}

/* ---------- 3D scenes (CSS) ---------- */
.fit{position:relative;width:100%;height:calc(var(--dh) * var(--fs,1))}
.fit-in{position:absolute;left:0;top:0;width:var(--dw);height:var(--dh);transform-origin:0 0;transform:scale(var(--fs,1))}
.fit.center .fit-in{left:50%;transform-origin:0 0;transform:translateX(calc(var(--dw) * var(--fs,1) * -.5)) scale(var(--fs,1))}
.stage{position:absolute;inset:0;perspective:var(--persp,1500px);perspective-origin:50% 0%}
.fit{touch-action:pan-y;cursor:grab}
.fit:active{cursor:grabbing}
.node3d.sm{width:38px;height:38px;box-shadow:0 0 0 4px rgba(251,252,251,.75),0 10px 16px -8px rgba(10,30,35,.55)}
.node3d.sm .ic{width:18px;height:18px}
.plane{position:absolute;left:var(--px,0px);top:var(--py,0px);width:var(--pw);height:var(--pd);transform-style:preserve-3d;transform:rotateX(calc(var(--rx) + var(--dx,0deg))) rotateZ(calc(var(--rz) + var(--dz,0deg)));transition:transform .3s ease-out}
.ground{position:absolute;inset:0;border-radius:18px;background-color:var(--g-bg,rgba(14,54,64,.05));
  background-image:linear-gradient(var(--g-line,rgba(14,54,64,.07)) 1px,transparent 1px),linear-gradient(90deg,var(--g-line,rgba(14,54,64,.07)) 1px,transparent 1px);background-size:34px 34px}
.bx{position:absolute;transform-style:preserve-3d;transform:translateZ(calc(var(--z0,0px) + var(--lift3d,0px)));transition:transform .45s cubic-bezier(.2,.7,.2,1)}
.bx>i{position:absolute;display:block}
.bx>.f-t{left:0;top:0;width:100%;height:100%;background:var(--t);transform:translateZ(var(--h));border-radius:3px}
.bx>.f-s{left:0;top:100%;width:100%;height:var(--h);background:var(--s);transform-origin:50% 0;transform:rotateX(90deg)}
.bx>.f-n{left:0;bottom:100%;width:100%;height:var(--h);background:var(--e);transform-origin:50% 100%;transform:rotateX(-90deg)}
.bx>.f-e{left:100%;top:0;width:var(--h);height:100%;background:var(--e);transform-origin:0 50%;transform:rotateY(-90deg)}
.bx>.f-w{right:100%;top:0;width:var(--h);height:100%;background:var(--e);transform-origin:100% 50%;transform:rotateY(90deg)}
.bx.ghost>.f-t{background:rgba(251,252,251,.85);outline:2px dashed var(--sea3);outline-offset:-2px}
.bx.ghost>.f-s,.bx.ghost>.f-e,.bx.ghost>.f-w,.bx.ghost>.f-n{background:rgba(34,100,111,.18)}
.bb{position:absolute;width:0;height:0;transform-style:preserve-3d;
  transform:translateZ(calc(var(--h,0px) + var(--lift,0px))) rotateZ(calc((var(--rz) + var(--dz,0deg)) * -1)) rotateX(calc((var(--rx) + var(--dx,0deg)) * -1));transition:transform .3s ease-out}
.bbc{position:absolute;left:0;bottom:0;transform:translateX(-50%);white-space:nowrap}
.bb.r .bbc{transform:translate(16px,50%);white-space:normal;width:var(--lw,220px)}
.road{position:absolute;height:0;border-top:3px dashed var(--sea3);opacity:.55}
.trav{position:absolute;transform-style:preserve-3d;animation:trav var(--dur,8s) cubic-bezier(.45,0,.55,1) infinite}
@keyframes trav{0%{transform:translateX(0);opacity:0}6%{opacity:1}94%{opacity:1}100%{transform:translateX(var(--dist));opacity:0}}
@media (prefers-reduced-motion:reduce){.trav{animation:none;opacity:1}}
.node3d{width:52px;height:52px;border-radius:50%;background:var(--sea);color:var(--marigold);display:grid;place-items:center;
  box-shadow:0 0 0 5px rgba(251,252,251,.75),0 14px 22px -8px rgba(10,30,35,.55)}
.node3d .ic{width:24px;height:24px}
.node3d.gold{background:var(--marigold);color:var(--ink)}
.tag3d{font-family:var(--f-mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;background:var(--paper);color:var(--ink);border-radius:5px;
  padding:5px 9px;box-shadow:0 8px 18px -8px rgba(10,30,35,.45);font-weight:500}
.lbl3d{display:flex;flex-direction:column;gap:2px;font-size:14px;line-height:1.3;color:var(--ink)}
.lbl3d b{font-family:var(--f-display);font-stretch:108%;font-size:18px;font-weight:700}
.lbl3d span{color:var(--mute)}
.dark .lbl3d{color:var(--on-sea)} .dark .lbl3d span{color:var(--on-sea-mute)}

/* ---------- interactive pieces ---------- */
.bx[data-k]{cursor:pointer}
.bx[data-k]:hover{--lift3d:20px}
.slide:has(.stepcol[data-k="1"]:hover) .bx[data-k="1"]{--lift3d:20px}
.slide:has(.bx[data-k="1"]:hover) .stepcol[data-k="1"]{background:var(--paper);box-shadow:0 10px 26px -16px rgba(10,30,35,.4)}
.slide:has(.stepcol[data-k="2"]:hover) .bx[data-k="2"]{--lift3d:20px}
.slide:has(.bx[data-k="2"]:hover) .stepcol[data-k="2"]{background:var(--paper);box-shadow:0 10px 26px -16px rgba(10,30,35,.4)}
.slide:has(.stepcol[data-k="3"]:hover) .bx[data-k="3"]{--lift3d:20px}
.slide:has(.bx[data-k="3"]:hover) .stepcol[data-k="3"]{background:var(--paper);box-shadow:0 10px 26px -16px rgba(10,30,35,.4)}
.slide:has(.stepcol[data-k="4"]:hover) .bx[data-k="4"]{--lift3d:20px}
.slide:has(.bx[data-k="4"]:hover) .stepcol[data-k="4"]{background:var(--paper);box-shadow:0 10px 26px -16px rgba(10,30,35,.4)}

.stepcol{border-radius:10px;padding:.6cqw .8cqw;margin:-.6cqw -.8cqw;transition:background .3s,box-shadow .3s,opacity .3s}
.grid:has(.stepcol:hover) .stepcol:not(:hover){opacity:.55}
.flip{position:relative;cursor:pointer;perspective:1300px;min-width:0;border-radius:10px;outline:none}
.flip:focus-visible{outline:2px solid var(--marigold);outline-offset:3px}
.flip-in{display:grid;height:100%;transform-style:preserve-3d;transition:transform .75s cubic-bezier(.2,.7,.2,1)}
.flip.flipped .flip-in{transform:rotateY(180deg)}
.flip .face{grid-area:1/1;height:100%;backface-visibility:hidden;-webkit-backface-visibility:hidden;transition:box-shadow .3s,translate .3s}
.flip .face.back{transform:rotateY(180deg)}
.flip:hover .face{translate:0 -3px;box-shadow:0 16px 30px -18px rgba(10,30,35,.5)}
.flip-hint{margin-top:auto;font-family:var(--f-mono);font-size:var(--xs);letter-spacing:.08em;text-transform:uppercase;display:inline-flex;align-items:center;gap:.45em;color:var(--sea3)}
.dark .flip-hint{color:var(--marigold)}
.flip-hint .ic,.jump .ic{width:1.2em;height:1.2em}
.jump{all:unset;cursor:pointer;margin-top:auto;font-family:var(--f-mono);font-size:var(--xs);letter-spacing:.08em;text-transform:uppercase;display:inline-flex;align-items:center;gap:.45em;color:var(--marigold);padding:.3em 0}
.jump:hover{text-decoration:underline;text-underline-offset:.25em}
.jump:focus-visible{outline:2px solid var(--marigold);outline-offset:2px}
.sb{display:flex;flex-direction:column;gap:.15cqw}
.sb b{font-family:var(--f-mono);font-size:var(--xs);letter-spacing:.08em;text-transform:uppercase;color:var(--rust);font-weight:500}
.sb span{font-size:var(--s);line-height:1.38}
@media print{.flip .face.back{display:none}}
.chipbar{display:flex;gap:.5cqw;flex-wrap:wrap;align-items:center}
.chipbar button{all:unset;cursor:pointer;font-family:var(--f-mono);font-size:var(--xs);letter-spacing:.06em;text-transform:uppercase;padding:.42em .95em;border-radius:999px;border:1px solid var(--sea-line);color:var(--on-sea-mute);transition:background .25s,color .25s}
.chipbar button:hover{color:var(--on-sea)}
.chipbar button.on{background:var(--marigold);color:var(--ink);border-color:var(--marigold)}
.chipbar button:focus-visible{outline:2px solid var(--marigold);outline-offset:2px}
svg [data-r]{transition:opacity .45s}
svg[data-f="asia"] [data-r]:not([data-r="asia"]){opacity:.07}
svg[data-f="me"] [data-r]:not([data-r="me"]){opacity:.07}
svg[data-f="eu"] [data-r]:not([data-r="eu"]){opacity:.07}
svg[data-f="am"] [data-r]:not([data-r="am"]){opacity:.07}
svg .pin{cursor:pointer;transition:r .2s}
svg .pin:hover{r:7}
.faq{align-content:start;align-items:start}
.faq details{border-top:1px solid var(--line);padding-top:.8cqw;min-width:0}
.faq summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:flex-start;gap:1em;font-family:var(--f-display);font-stretch:104%;font-weight:650;font-size:var(--b);line-height:1.3}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";flex:none;width:1.5em;height:1.5em;display:grid;place-items:center;border-radius:50%;font-family:var(--f-mono);font-weight:500;color:var(--rust);background:var(--rust-tint);transition:transform .3s}
.faq details[open] summary::after{transform:rotate(45deg)}
.faq details p{font-size:var(--s);color:var(--mute);margin-top:.5cqw}
.faq summary:focus-visible{outline:2px solid var(--marigold);outline-offset:3px;border-radius:4px}
.faq summary:hover{color:var(--sea3)}
.calc label{display:flex;justify-content:space-between;align-items:baseline;gap:1em;font-weight:600;font-size:var(--b)}
.calc output{font-family:var(--f-display);font-stretch:110%;font-weight:760;font-size:var(--l);color:var(--sea);white-space:nowrap}
.calc input[type=range]{-webkit-appearance:none;appearance:none;width:100%;height:30px;background:transparent;cursor:pointer;margin:0}
.calc input[type=range]::-webkit-slider-runnable-track{height:8px;border-radius:99px;background:linear-gradient(90deg,var(--marigold) var(--p,50%),var(--line) var(--p,50%))}
.calc input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:26px;height:26px;border-radius:50%;background:var(--paper);border:4px solid var(--sea);margin-top:-9px;box-shadow:0 6px 14px -6px rgba(10,30,35,.6)}
.calc input[type=range]::-moz-range-track{height:8px;border-radius:99px;background:var(--line)}
.calc input[type=range]::-moz-range-progress{height:8px;border-radius:99px;background:var(--marigold)}
.calc input[type=range]::-moz-range-thumb{width:20px;height:20px;border-radius:50%;background:var(--paper);border:4px solid var(--sea)}
.calc input[type=range]:focus-visible{outline:2px solid var(--marigold);outline-offset:4px;border-radius:8px}
.presets{display:flex;gap:.5cqw;flex-wrap:wrap}
.presets button{all:unset;cursor:pointer;font-family:var(--f-mono);font-size:var(--xs);letter-spacing:.06em;text-transform:uppercase;padding:.45em .95em;border-radius:999px;background:var(--mint-soft);color:var(--sea);transition:background .25s,color .25s}
.presets button.on{background:var(--sea);color:var(--on-sea)}
.presets button:focus-visible{outline:2px solid var(--marigold);outline-offset:2px}
.calc-big{font-family:var(--f-display);font-weight:780;font-stretch:112%;font-size:clamp(24px,3.2cqw,41px);line-height:1.06;color:var(--marigold);text-wrap:balance}
.calc .kv{display:flex;flex-direction:column;gap:.3cqw;border-top:1px solid var(--sea-line);padding-top:.8cqw;min-width:0}
.calc .kv span{font-size:var(--s);color:var(--on-sea-mute)}
.calc .kv b{font-size:var(--b);font-weight:600}
.ratio{display:flex;flex-direction:column;gap:.6cqw}
.ratio .rb{display:grid;grid-template-columns:7.5em 1fr;gap:1em;align-items:center;font-size:var(--s)}
.ratio .track{height:16px;border-radius:5px;background:rgba(232,240,238,.1);position:relative;overflow:hidden}
.ratio .track i{position:absolute;left:0;top:0;bottom:0;border-radius:5px}

/* ---------- 3D phone (problem slide) ---------- */
.phone{transform:perspective(1100px) rotateY(17deg) rotateX(5deg) rotateZ(-1.5deg);
  box-shadow:-10px 10px 0 -2px #0A2026,-26px 34px 50px -16px rgba(10,30,35,.45)}
@media (prefers-reduced-motion:no-preference){.phone{animation:bob 6s ease-in-out infinite}}
@keyframes bob{50%{translate:0 -8px}}

/* ---------- WebGL globe ---------- */
.globe{position:relative;width:100%;aspect-ratio:1/1;max-width:100%}
.globe canvas{position:absolute;inset:0;width:100%;height:100%;display:block;touch-action:pan-y;cursor:grab}
.globe canvas:active{cursor:grabbing}
.globe-fallback{display:none}
.globe.no-gl canvas{display:none}
.globe.no-gl .globe-fallback{display:block}
.globe-cap{font-family:var(--f-mono);font-size:var(--xs);letter-spacing:.1em;text-transform:uppercase;color:var(--on-sea-mute);text-align:center}

/* ---------- WhatsApp ---------- */
.wa-fab{position:fixed;right:calc(18px + env(safe-area-inset-right,0px));bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:55;display:inline-flex;align-items:center;gap:8px;
  padding:12px 16px;border-radius:999px;background:var(--wa);color:#06321A;font-family:var(--f-body);font-weight:600;font-size:14px;text-decoration:none;
  box-shadow:0 12px 30px -10px rgba(18,140,75,.65),0 0 0 0 rgba(37,211,102,.5);animation:wapulse 2.8s ease-out infinite}
.wa-fab .ic{width:20px;height:20px}
.wa-fab:hover{background:#2EE673}
.wa-fab:focus-visible{outline:3px solid var(--marigold);outline-offset:3px}
@keyframes wapulse{0%{box-shadow:0 12px 30px -10px rgba(18,140,75,.65),0 0 0 0 rgba(37,211,102,.45)}70%{box-shadow:0 12px 30px -10px rgba(18,140,75,.65),0 0 0 16px rgba(37,211,102,0)}100%{box-shadow:0 12px 30px -10px rgba(18,140,75,.65),0 0 0 0 rgba(37,211,102,0)}}
@media (prefers-reduced-motion:reduce){.wa-fab{animation:none}}
body.present .hint{right:auto;left:18px}
.wa-cta{display:inline-flex;align-items:center;gap:.6em;padding:.8em 1.3em;border-radius:999px;background:var(--wa);color:#06321A;font-weight:700;font-size:var(--l);text-decoration:none;
  box-shadow:0 18px 36px -16px rgba(18,140,75,.8);transition:transform .25s,box-shadow .25s;align-self:flex-start}
.wa-cta .ic{width:1.3em;height:1.3em}
.wa-cta:hover{transform:translateY(-2px) scale(1.02);box-shadow:0 24px 40px -16px rgba(18,140,75,.9)}
.wa-cta:focus-visible{outline:3px solid var(--marigold);outline-offset:3px}
@media print{.wa-fab{display:none!important}}

/* ---------- 3D floating container (closing slide) ---------- */
.crate{width:220px;height:200px;position:relative;margin:0 auto;perspective:900px}
.crate .cr{position:absolute;left:50%;top:50%;width:150px;height:84px;transform-style:preserve-3d;transform:translate(-50%,-50%) rotateX(-18deg) rotateY(-32deg)}
@media (prefers-reduced-motion:no-preference){.crate .cr{animation:crate 9s ease-in-out infinite}}
@keyframes crate{50%{transform:translate(-50%,-58%) rotateX(-14deg) rotateY(28deg)}}
.crate .cr i{position:absolute;display:block;background:repeating-linear-gradient(90deg,rgba(0,0,0,.14) 0 3px,transparent 3px 9px),var(--c,#FFA94D);border:2px solid rgba(0,0,0,.18);border-radius:3px}
.crate .fr{width:150px;height:84px;transform:translateZ(42px)}
.crate .bk{width:150px;height:84px;transform:rotateY(180deg) translateZ(42px)}
.crate .rt{width:84px;height:84px;left:33px;transform:rotateY(90deg) translateZ(75px);--c:#F08A2C}
.crate .lt{width:84px;height:84px;left:33px;transform:rotateY(-90deg) translateZ(75px);--c:#F08A2C}
.crate .tp{width:150px;height:84px;transform:rotateX(90deg) translateZ(42px);--c:#FFC27F}
.crate .bt{width:150px;height:84px;transform:rotateX(-90deg) translateZ(42px);--c:#C76F1F}
.crate .fr::after{content:"AMECK";position:absolute;inset:0;display:grid;place-items:center;font-family:var(--f-display);font-weight:800;font-stretch:125%;letter-spacing:.18em;color:#3A1A02;font-size:20px}
.crate-shadow{position:absolute;left:50%;bottom:4px;width:150px;height:18px;transform:translateX(-50%);border-radius:50%;background:radial-gradient(closest-side,rgba(0,0,0,.35),transparent)}

/* ---------- phone and narrow screens ---------- */
.m-only{display:none}
.swipe-hint{display:none}
.cwrap{max-width:100%}
@media (max-width:820px){
  .s-in{--xs:11px;--s:13.5px;--b:15px;--l:17px;--h2:25px;--h1:40px;--stat:40px;--g:14px}
  .slide{border-radius:14px}
  .chrome{font-size:10px}
  h2{max-width:none}
  .cwrap{overflow-x:auto;-webkit-overflow-scrolling:touch;padding-bottom:4px}
  svg.chart.wide{min-width:560px}
  svg.chart.wide-xl{min-width:720px}
  .phone{transform:none;box-shadow:0 20px 40px -16px rgba(10,30,35,.45)}
  .globe{max-width:420px;margin:0 auto}
  div:has(> svg.chart.wide),div:has(> svg.chart.wide-xl){overflow-x:auto;-webkit-overflow-scrolling:touch}
  .m-only{display:block}
  .d-only,.m-hide{display:none!important}
  .slide .s-in>.chrome:last-child{display:none}
  .s-in{padding:20px 18px 22px;gap:16px}
  .m-swipe{display:flex!important;grid-template-columns:none!important;flex-direction:row!important;overflow-x:auto;scroll-snap-type:x mandatory;gap:12px!important;
    margin-inline:-18px;padding:4px 18px 12px!important;scrollbar-width:none;-webkit-overflow-scrolling:touch;align-items:stretch}
  .m-swipe::-webkit-scrollbar{display:none}
  .m-swipe>*{flex:0 0 80%;scroll-snap-align:center;min-width:0;grid-column:auto!important}
  .m-swipe>.flip>.flip-in{height:100%}
  .m-grid2{display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:12px!important}
  .swipe-hint{display:flex;align-items:center;gap:6px;justify-content:flex-end;font-family:var(--f-mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute);margin-top:-6px}
  .dark .swipe-hint{color:var(--on-sea-mute)}
  .swipe-hint i{display:inline-block;width:22px;height:2px;background:currentColor;border-radius:2px;animation:nudge 1.6s ease-in-out infinite}
  @keyframes nudge{50%{transform:translateX(6px)}}
  table.t.mcards,table.t.mcards tbody{display:block}
  table.t.mcards thead{display:none}
  table.t.mcards tbody{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:12px;margin-inline:-18px;padding:4px 18px 12px;scrollbar-width:none}
  table.t.mcards tbody::-webkit-scrollbar{display:none}
  table.t.mcards tr{flex:0 0 80%;scroll-snap-align:center;display:flex;flex-direction:column;gap:8px;background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:14px;box-shadow:0 14px 26px -20px rgba(12,24,48,.5)}
  table.t.mcards td{display:block;border:none!important;padding:0!important;width:auto!important}
  table.t.mcards td:first-child{font-family:var(--f-display);font-weight:700;font-size:17px}
  table.t.mcards td.diy,table.t.mcards td.ame{border-radius:10px;padding:10px 12px!important}
  table.t.mcards td[data-l]::before{content:attr(data-l);display:block;font-family:var(--f-mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;margin-bottom:4px;opacity:.75}
  .tablewrap{overflow:visible!important}
  .wa-fab{padding:13px;right:calc(14px + env(safe-area-inset-right,0px))}
  .wa-fab span{display:none}
}
"""

def box(x, y, w, d, h, colors, z=0, inner="", cls="", attrs=""):
    t, s, e = colors
    return (f'<div class="bx {cls}" {attrs} style="left:{x}px;top:{y}px;width:{w}px;height:{d}px;--h:{h}px;--z0:{z}px;--t:{t};--s:{s};--e:{e}">'
            f'<i class="f-n"></i><i class="f-e"></i><i class="f-w"></i><i class="f-s"></i><i class="f-t"></i>{inner}</div>')

def bb(html, left="50%", top="50%", lift=0, cls="", lw=None):
    st = f"left:{left};top:{top};--lift:{lift}px" + (f";--lw:{lw}px" if lw else "")
    return f'<div class="bb {cls}" style="{st}"><div class="bbc">{html}</div></div>'

def scene(dw, dh, plane_html, pw, pd, px, py, rx, rz, persp=1500, cls="", label=""):
    return (f'<div class="fit {cls}" style="--dw:{dw}px;--dh:{dh}px" role="img" aria-label="{label}"><div class="fit-in">'
            f'<div class="stage" style="--persp:{persp}px"><div class="plane" style="--pw:{pw}px;--pd:{pd}px;--px:{px}px;--py:{py}px;--rx:{rx}deg;--rz:{rz}deg">'
            f'{plane_html}</div></div></div></div>')

TEAL = ("#22646F", "#17505C", "#0E3640")
TEAL_L = ("#2E7C86", "#1F6570", "#154A54")
GOLD = ("#E9A23B", "#C7852A", "#9C6519")
MINT = ("#9FD3C5", "#7FB8AA", "#5E9A8C")

def globe_html(fallback_svg, cap):
    return (f'<div class="globe" data-globe><canvas role="img" aria-label="Rotating globe showing Ameck trade routes from 17 sourcing hubs into Jaipur"></canvas>'
            f'<div class="globe-fallback">{fallback_svg}</div></div><p class="globe-cap">{cap}</p>')

SHELL_JS = r"""
(()=>{
const D=document,B=D.body,R=D.documentElement;
const slides=[...D.querySelectorAll('.slide')],N=slides.length;
const printMode=/[?&]print/.test(location.search);window.__printMode=printMode;
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
let cur=0,mode=null,forced=null;
try{forced=localStorage.getItem('ameck-view')}catch(e){}
const hm=/^#s(\d+)$/.exec(location.hash);if(hm)cur=Math.min(N,Math.max(1,+hm[1]))-1;
const $=id=>D.getElementById(id);
const count=$('count'),bar=D.querySelector('.bar i'),toc=$('toc'),viewBtn=$('view-btn'),fsBtn=$('fs-btn');
function wantPresent(){if(printMode)return false;if(forced==='slides')return innerWidth>=480;if(forced==='scroll')return false;
  const r=innerWidth/innerHeight;return (innerWidth>=860&&r>=1.2)||(innerWidth>=560&&r>=1.6)}
function fit(){const pad=innerWidth<900?.985:.94;R.style.setProperty('--k',(Math.min(innerWidth/1280,innerHeight/720)*pad).toFixed(4))}
function apply(){const p=wantPresent();
  if(p!==mode){mode=p;B.classList.toggle('present',p);B.classList.toggle('feed',!p);R.classList.toggle('present-root',p);
    if(p){fit();show(cur,true)}else{slides.forEach(s=>{s.classList.remove('is-active','is-before','is-after','enter');s.inert=false});
      if(cur>0)requestAnimationFrame(()=>slides[cur].scrollIntoView({block:'start'}))}}
  if(p)fit();fitAll();ui()}
function show(i,instant){i=Math.max(0,Math.min(N-1,i));cur=i;
  slides.forEach((s,j)=>{s.classList.toggle('is-active',j===i);s.classList.toggle('is-before',j<i);s.classList.toggle('is-after',j>i);s.inert=j!==i});
  const s=slides[i];if(!instant){s.classList.remove('enter');void s.offsetWidth;s.classList.add('enter');countUp(s)}
  ui();try{history.replaceState(null,'','#s'+(i+1))}catch(e){}}
function go(d){if(mode)show(cur+d);else{const j=Math.max(0,Math.min(N-1,cur+d));slides[j].scrollIntoView({behavior:reduce?'auto':'smooth',block:'start'})}}
function jump(i){if(mode)show(i);else slides[i].scrollIntoView({behavior:'auto',block:'start'});cur=i;ui()}
function ui(){if(count)count.textContent=String(cur+1).padStart(2,'0')+' / '+String(N).padStart(2,'0');
  if(bar)bar.style.width=((cur+1)/N*100)+'%';
  if(viewBtn){viewBtn.querySelector('span').textContent=mode?'Scroll':'Slides';viewBtn.hidden=!mode&&innerWidth<480}
  if(toc)toc.querySelectorAll('.item').forEach(b=>b.classList.toggle('on',+b.dataset.i===cur))}
/* contents */
if(toc){const list=toc.querySelector('.list');let last='';slides.forEach((s,i)=>{const name=(s.getAttribute('aria-label')||'').replace(/^Slide \d+: /,'');
  if(name===last)return;last=name;const b=D.createElement('button');b.className='item';b.dataset.i=i;b.innerHTML='<b>'+String(i+1).padStart(2,'0')+'</b><span></span>';
  b.querySelector('span').textContent=name;b.addEventListener('click',()=>{closeToc();jump(i)});list.appendChild(b)});
  toc.addEventListener('click',e=>{if(e.target===toc)closeToc()});toc.querySelector('.close').addEventListener('click',closeToc)}
function openToc(){if(!toc)return;toc.hidden=false;ui();const on=toc.querySelector('.item.on')||toc.querySelector('.item');on&&on.focus()}
function closeToc(){if(toc&&!toc.hidden){toc.hidden=true;$('toc-btn')&&$('toc-btn').focus()}}
/* controls */
$('prev')&&$('prev').addEventListener('click',()=>go(-1));
$('next')&&$('next').addEventListener('click',()=>go(1));
$('toc-btn')&&$('toc-btn').addEventListener('click',openToc);
if(viewBtn)viewBtn.addEventListener('click',()=>{forced=mode?'scroll':'slides';try{localStorage.setItem('ameck-view',forced)}catch(e){}apply()});
function fs(){if(!D.fullscreenEnabled)return;const p=D.fullscreenElement?D.exitFullscreen():R.requestFullscreen();p&&p.catch&&p.catch(()=>{})}
if(fsBtn){fsBtn.hidden=!D.fullscreenEnabled;fsBtn.addEventListener('click',fs)}
D.addEventListener('keydown',e=>{if(e.target.closest&&e.target.closest('input,textarea,select'))return;const k=e.key;
  if((k===' '||k==='Enter')&&e.target.closest&&e.target.closest('button,summary,a,[role=button]'))return;
  if(toc&&!toc.hidden){if(k==='Escape')closeToc();return}
  if(['ArrowRight','PageDown',' ','ArrowDown'].includes(k)){if(mode){e.preventDefault();go(1)}}
  else if(['ArrowLeft','PageUp','ArrowUp'].includes(k)){if(mode){e.preventDefault();go(-1)}}
  else if(k==='Home'&&mode){e.preventDefault();show(0)}else if(k==='End'&&mode){e.preventDefault();show(N-1)}
  else if(k==='f'||k==='F')fs();else if(k==='c'||k==='C')openToc()});
let wl=0;addEventListener('wheel',e=>{if(!mode||(toc&&!toc.hidden))return;e.preventDefault();const t=Date.now();if(t<wl||Math.abs(e.deltaY)+Math.abs(e.deltaX)<16)return;
  wl=t+900;go((Math.abs(e.deltaY)>=Math.abs(e.deltaX)?e.deltaY:e.deltaX)>0?1:-1)},{passive:false});
let tx=null,ty=null;D.addEventListener('touchstart',e=>{if(!mode)return;const t=e.touches[0];tx=t.clientX;ty=t.clientY},{passive:true});
D.addEventListener('touchend',e=>{if(!mode||tx===null)return;const t=e.changedTouches[0],dx=t.clientX-tx,dy=t.clientY-ty;tx=null;
  if(e.target.closest&&e.target.closest('canvas,.cwrap,input,.calc,.chipbar,.fit'))return;if(Math.abs(dx)>50&&Math.abs(dx)>Math.abs(dy)*1.3)go(dx<0?1:-1)},{passive:true});
let idle;function wake(){B.classList.add('ui-on');clearTimeout(idle);idle=setTimeout(()=>B.classList.remove('ui-on'),2600)}
addEventListener('mousemove',wake);addEventListener('touchstart',wake,{passive:true});addEventListener('keydown',wake);
/* scroll mode: track the slide in view */
const vis=new Map();
const io=new IntersectionObserver(es=>{es.forEach(en=>{vis.set(en.target,en.isIntersecting);
  if(en.isIntersecting&&!mode&&!en.target.__counted){en.target.__counted=1;countUp(en.target);if(!reduce&&!printMode&&slides.indexOf(en.target)>0)en.target.classList.add('enter')}
  if(!mode&&en.isIntersecting&&en.intersectionRatio>=.45){cur=slides.indexOf(en.target);ui()}})},{threshold:[0,.45]});
slides.forEach(s=>io.observe(s));
window.__slideVisible=s=>printMode||(mode?s.classList.contains('is-active'):!!vis.get(s));
/* scale 3D scenes to their column */
function fitAll(){D.querySelectorAll('.fit').forEach(f=>{const dw=parseFloat(f.style.getPropertyValue('--dw'));const w=f.clientWidth;
  if(dw&&w)f.style.setProperty('--fs',Math.min(1,w/dw).toFixed(4))})}
if(window.ResizeObserver){const ro=new ResizeObserver(fitAll);D.querySelectorAll('.fit').forEach(f=>ro.observe(f))}
/* tilt cards */
if(matchMedia('(pointer:fine)').matches&&!reduce){D.querySelectorAll('.card,.stamp,.path,.svc').forEach(c=>{if(c.closest('.fit,.flip,.calc'))return;c.classList.add('tiltable');
  c.addEventListener('pointermove',e=>{if(!mode)return;const r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;
    c.classList.add('tilting');c.style.transform='perspective(900px) rotateX('+(-y*7).toFixed(2)+'deg) rotateY('+(x*9).toFixed(2)+'deg) translateZ(8px)';
    c.style.setProperty('--gx',((x+.5)*100).toFixed(1)+'%');c.style.setProperty('--gy',((y+.5)*100).toFixed(1)+'%')});
  c.addEventListener('pointerleave',()=>{c.classList.remove('tilting');c.style.transform=''})})}
addEventListener('resize',apply);
/* 3D scenes react: mouse tilt on laptops, drag on any screen, scroll on phones */
(()=>{if(reduce)return;const setT=(p,dx,dz)=>{p.style.setProperty('--dx',dx.toFixed(2)+'deg');p.style.setProperty('--dz',dz.toFixed(2)+'deg')};
  slides.forEach(s=>{const ps=[...s.querySelectorAll('.plane')];if(!ps.length)return;
    s.addEventListener('pointermove',e=>{if(e.pointerType!=='mouse'||drag)return;const r=s.getBoundingClientRect(),nx=(e.clientX-r.left)/r.width-.5,ny=(e.clientY-r.top)/r.height-.5;ps.forEach(p=>setT(p,-ny*12,nx*16))});
    s.addEventListener('pointerleave',()=>{if(!drag)ps.forEach(p=>setT(p,0,0))})});
  let drag=null;
  D.querySelectorAll('.fit').forEach(f=>{const p=f.querySelector('.plane');if(!p)return;
    f.addEventListener('pointerdown',e=>{drag={p,x:e.clientX,y:e.clientY,dz:parseFloat(p.style.getPropertyValue('--dz'))||0,dx:parseFloat(p.style.getPropertyValue('--dx'))||0}})});
  addEventListener('pointermove',e=>{if(!drag)return;const dz=Math.max(-40,Math.min(40,drag.dz+(e.clientX-drag.x)*.3));setT(drag.p,drag.dx,dz)});
  const end=()=>{drag=null};addEventListener('pointerup',end);addEventListener('pointercancel',end);
  const onScroll=()=>{if(mode||drag)return;D.querySelectorAll('.fit').forEach(f=>{const r=f.getBoundingClientRect();if(r.bottom<0||r.top>innerHeight)return;
    const c=(r.top+r.height/2)/innerHeight-.5;const p=f.querySelector('.plane');if(p)setT(p,c*-16,c*22)})};
  addEventListener('scroll',onScroll,{passive:true});onScroll()})();
/* swipe hints under phone carousels */
D.querySelectorAll('.m-swipe,table.mcards').forEach(el=>{const h=D.createElement('p');h.className='swipe-hint';h.setAttribute('aria-hidden','true');h.innerHTML='Swipe <i></i>';
  (el.closest('.tablewrap')||el).insertAdjacentElement('afterend',h)});
/* count-up numbers */
function countUp(s){if(printMode||reduce)return;s.querySelectorAll('[data-count]').forEach(el=>{const to=+el.dataset.count,t0=performance.now();
  const st=now=>{const p=Math.min(1,(now-t0)/1200),e=1-Math.pow(1-p,3);el.textContent=Math.round(to*e);if(p<1)requestAnimationFrame(st)};requestAnimationFrame(st)})}
/* flip cards and jump links */
D.querySelectorAll('.flip').forEach(f=>{const t=()=>{f.classList.toggle('flipped');f.setAttribute('aria-pressed',f.classList.contains('flipped'))};
  f.addEventListener('click',e=>{if(e.target.closest('[data-jump]'))return;t()});
  f.addEventListener('keydown',e=>{if(e.target!==f)return;if(e.key==='Enter'||e.key===' '){e.preventDefault();t()}})});
D.querySelectorAll('[data-jump]').forEach(b=>b.addEventListener('click',e=>{e.stopPropagation();const n=b.dataset.jump;
  const i=slides.findIndex(s=>(s.getAttribute('aria-label')||'').endsWith(': '+n));if(i>=0)jump(i)}));
/* FAQ: everything open in print */
if(printMode)D.querySelectorAll('.faq details').forEach(d=>d.open=true);
/* map region filter */
D.querySelectorAll('.chipbar[data-for]').forEach(cb=>{const sv=D.getElementById(cb.dataset.for);cb.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{
  cb.querySelectorAll('button').forEach(x=>{x.classList.toggle('on',x===b);x.setAttribute('aria-pressed',x===b)});
  if(b.dataset.f==='all')sv.removeAttribute('data-f');else sv.setAttribute('data-f',b.dataset.f)}))});
/* savings estimator */
(()=>{const c=D.getElementById('calc');if(!c)return;const v=c.querySelector('#cv'),n=c.querySelector('#cn'),nf=new Intl.NumberFormat('en-IN');
  const rs=x=>'Rs. '+nf.format(Math.round(x)),set=(id,t)=>{const e=c.querySelector('#'+id);if(e)e.textContent=t};
  function upd(){const V=+v.value,N=+n.value,lo=V*0.30,hi=V*0.50;
    set('cv-o',rs(V));set('cn-o',N+(N===1?' order':' orders'));
    set('o-year',rs(lo*N)+' to '+rs(hi*N));set('o-order',rs(lo)+' to '+rs(hi));set('o-cost',rs(V-hi)+' to '+rs(V-lo));set('o-hours',nf.format(60*N)+' to '+nf.format(120*N));
    set('o-work',rs(V)+' × 30% = '+rs(lo)+' and '+rs(V)+' × 50% = '+rs(hi)+' saved per order. Over '+N+(N===1?' order':' orders')+': '+rs(lo)+' × '+N+' = '+rs(lo*N)+' and '+rs(hi)+' × '+N+' = '+rs(hi*N)+'.');
    c.querySelectorAll('.presets button').forEach(b=>{const on=+b.dataset.v===V;b.classList.toggle('on',on);b.setAttribute('aria-pressed',on)});
    v.style.setProperty('--p',((V-v.min)/(v.max-v.min)*100).toFixed(2)+'%');n.style.setProperty('--p',((N-n.min)/(n.max-n.min)*100).toFixed(2)+'%')}
  v.addEventListener('input',upd);n.addEventListener('input',upd);
  c.querySelectorAll('.presets button').forEach(b=>b.addEventListener('click',()=>{v.value=b.dataset.v;upd()}));upd()})();
addEventListener('hashchange',()=>{const m=/^#s(\d+)$/.exec(location.hash);if(m){const i=Math.min(N,Math.max(1,+m[1]))-1;if(i!==cur)jump(i)}});
function centreMaps(){D.querySelectorAll('svg.chart.wide-xl').forEach(sv=>{const p=sv.parentElement;if(p.scrollWidth>p.clientWidth)p.scrollLeft=(p.scrollWidth-p.clientWidth)*.62})}
setTimeout(centreMaps,60);addEventListener('resize',centreMaps);
apply();if(mode)show(cur,true);else if(cur>0)slides[cur].scrollIntoView({block:'start'});
document.querySelectorAll('[data-globe]').forEach(initGlobe);
})();

function initGlobe(el){
  const T=window.THREE,cv=el.querySelector('canvas');
  if(!T){el.classList.add('no-gl');return}
  let r;try{r=new T.WebGLRenderer({canvas:cv,antialias:true,alpha:true,preserveDrawingBuffer:true})}catch(e){el.classList.add('no-gl');return}
  if(!r.getContext()){el.classList.add('no-gl');return}
  const sc=new T.Scene(),cam=new T.PerspectiveCamera(30,1,.1,50);cam.position.set(0,0,5.3);
  const g=new T.Group();sc.add(g);
  const ll=(la,lo,rr)=>{const p=(90-la)*Math.PI/180,t=(lo+180)*Math.PI/180;return new T.Vector3(-rr*Math.sin(p)*Math.cos(t),rr*Math.cos(p),rr*Math.sin(p)*Math.sin(t))};
  const halo=D_halo();sc.add(halo);
  g.add(new T.Mesh(new T.SphereGeometry(.99,64,48),new T.MeshBasicMaterial({color:0x0b2d35})));
  const P=GLOBE_PTS,pos=new Float32Array(P.length*1.5);
  for(let i=0,j=0;i<P.length;i+=2,j+=3){const v=ll(P[i]/10,P[i+1]/10,1);pos[j]=v.x;pos[j+1]=v.y;pos[j+2]=v.z}
  const dg=new T.BufferGeometry();dg.setAttribute('position',new T.BufferAttribute(pos,3));
  g.add(new T.Points(dg,new T.PointsMaterial({color:0x8fd0d2,size:.027,map:dotTex(),transparent:true,alphaTest:.35,depthWrite:false})));
  const J=ll(26.9,75.8,1),trav=[];
  HUBS.forEach((h,k)=>{const A=ll(h[0],h[1],1),ang=A.angleTo(J),lift=.025+ang*.085,pts=[];
    for(let i=0;i<=60;i++){const t=i/60,v=A.clone().lerp(J,t).normalize();v.multiplyScalar(1+lift*Math.sin(Math.PI*t));pts.push(v)}
    const tube=new T.TubeGeometry(new T.CatmullRomCurve3(pts),80,.0045,6,false);
    g.add(new T.Mesh(tube,new T.MeshBasicMaterial({color:0xe9a23b,transparent:true,opacity:.75})));
    const m=new T.Mesh(new T.SphereGeometry(.016,14,14),new T.MeshBasicMaterial({color:0x9fd3c5}));m.position.copy(A).multiplyScalar(1.004);g.add(m);
    const s=new T.Mesh(new T.SphereGeometry(.017,12,12),new T.MeshBasicMaterial({color:0xffe2a8}));g.add(s);trav.push({s,pts,off:k/HUBS.length,sp:.16+(k%5)*.025})});
  const jm=new T.Mesh(new T.SphereGeometry(.032,20,20),new T.MeshBasicMaterial({color:0xe9a23b}));jm.position.copy(J).multiplyScalar(1.006);g.add(jm);
  const ring=new T.Mesh(new T.RingGeometry(.04,.052,48),new T.MeshBasicMaterial({color:0xe9a23b,transparent:true,side:T.DoubleSide,depthWrite:false}));
  ring.position.copy(J).multiplyScalar(1.008);ring.quaternion.setFromUnitVectors(new T.Vector3(0,0,1),J.clone().normalize());g.add(ring);
  const ind=ll(20,80,1),baseY=Math.atan2(-ind.x,ind.z),baseX=20*Math.PI/180;
  let drag=0,dragging=false,lx=0;
  cv.addEventListener('pointerdown',e=>{dragging=true;lx=e.clientX;try{cv.setPointerCapture(e.pointerId)}catch(_){}});
  cv.addEventListener('pointermove',e=>{if(!dragging)return;drag+=(e.clientX-lx)*.006;lx=e.clientX});
  const stop=()=>{dragging=false};cv.addEventListener('pointerup',stop);cv.addEventListener('pointercancel',stop);
  const slide=el.closest('.slide'),reduce=matchMedia('(prefers-reduced-motion: reduce)').matches,t0=performance.now();
  function size(){const w=cv.clientWidth,h=cv.clientHeight;if(!w||!h)return;
    const k=parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--k'))||1;
    const pr=Math.min(2.5,(window.devicePixelRatio||1)*Math.max(1,k));
    if(cv.width!==Math.round(w*pr)||cv.height!==Math.round(h*pr)){r.setPixelRatio(pr);r.setSize(w,h,false);cam.aspect=w/h;cam.updateProjectionMatrix()}}
  function frame(now){requestAnimationFrame(frame);if(document.hidden)return;if(window.__slideVisible&&!window.__slideVisible(slide))return;size();
    const t=window.__printMode?0:Math.max(0,(now-t0)/1000);g.rotation.x=baseX;g.rotation.y=baseY+(reduce?0:Math.sin(t*.13)*.5)+drag;
    trav.forEach(o=>{const u=((t*o.sp+o.off)%1+1)%1,i=Math.max(0,Math.min(o.pts.length-1,Math.floor(u*o.pts.length)));o.s.position.copy(o.pts[i])});
    const p=(t*.7)%1;ring.scale.setScalar(1+p*1.8);ring.material.opacity=.9*(1-p);
    r.render(sc,cam)}
  requestAnimationFrame(frame);
  function dotTex(){const c=document.createElement('canvas');c.width=c.height=64;const x=c.getContext('2d');x.fillStyle='#fff';x.beginPath();x.arc(32,32,26,0,Math.PI*2);x.fill();return new T.CanvasTexture(c)}
  function D_halo(){const c=document.createElement('canvas');c.width=c.height=256;const x=c.getContext('2d');
    const gr=x.createRadialGradient(128,128,70,128,128,128);gr.addColorStop(0,'rgba(159,211,197,0)');gr.addColorStop(.42,'rgba(159,211,197,.28)');gr.addColorStop(.62,'rgba(95,163,171,.12)');gr.addColorStop(1,'rgba(95,163,171,0)');
    x.fillStyle=gr;x.fillRect(0,0,256,256);const sp=new T.Sprite(new T.SpriteMaterial({map:new T.CanvasTexture(c),transparent:true,depthWrite:false}));sp.scale.set(3.05,3.05,1);sp.position.z=-.6;return sp}
}
"""

CTRL_HTML = """<div class="bar" aria-hidden="true"><i></i></div>
<nav class="ctrl" aria-label="Slide controls">
 <button class="pv" id="prev" aria-label="Previous slide"><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 5l-7 7 7 7"/></svg></button>
 <span id="count" aria-live="polite">01 / 01</span>
 <button class="pv" id="next" aria-label="Next slide"><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 5l7 7-7 7"/></svg></button>
 <button id="toc-btn" aria-label="Open contents"><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h16M4 12h16M4 18h10"/></svg>Contents</button>
 <button id="view-btn" aria-label="Switch view"><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/></svg><span>Slides</span></button>
 <button id="fs-btn" aria-label="Full screen"><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg></button>
</nav>
<p class="hint">Arrow keys or swipe to move / F for full screen</p>
<div id="toc" hidden role="dialog" aria-label="Contents"><div class="panel"><button class="close">Close</button><h2>Contents</h2><div class="list"></div></div></div>"""

WA_FAB = f'<a class="wa-fab" href="{WA_URL}" target="_blank" rel="noopener" aria-label="Chat with Ameck on WhatsApp">{WA_ICON}<span>WhatsApp</span></a>'

def assemble(slides, title, brand_left, footer_left, head_label, base_css, sprite, three_src=THREE_CDN, whatsapp=False):
    N = len(slides)
    parts = []
    for i, (theme, section, body) in enumerate(slides, 1):
        parts.append(f'''<section class="slide {theme}" id="slide-{i}" aria-label="Slide {i}: {section}"><div class="s-in">
<div class="chrome"><span class="mark"><i></i>{brand_left}</span><span>{i:02d} / {N:02d}</span></div>
<div class="body">{body}</div>
<div class="chrome"><span>{footer_left}</span><span>{section}</span></div>
</div></section>''')
    return soften(f'''<title>{title}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>{base_css}{SHELL_CSS}</style>
{sprite}
<header class="page-head"><b>AMECK HOUSE</b><span>{head_label}</span></header>
<main class="deck">
{"".join(parts)}
</main>
{CTRL_HTML}
{WA_FAB if whatsapp else ''}
<script src="{three_src}"></script>
<script>const GLOBE_PTS={GLOBE_PTS};const HUBS={json.dumps(HUBS)};
{SHELL_JS}</script>
''')
