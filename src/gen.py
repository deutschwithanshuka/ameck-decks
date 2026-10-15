import base64, pathlib, sys, os
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from shell import *

HERE = pathlib.Path(__file__).parent
FONTS = HERE.parent / "fonts"

def b64(p):
    return base64.b64encode(p.read_bytes()).decode()

bodoni = next(FONTS.glob("fontsource-variable-bodoni-moda-*/files"))
fig = next(FONTS.glob("fontsource-figtree-*[0-9]/files"))

font_css = "".join(
    f'@font-face{{font-family:"Bodoni Moda";src:url(data:font/woff2;base64,{b64(bodoni / f"bodoni-moda-latin-standard-{st}.woff2")}) format("woff2");font-weight:400 900;font-style:{st};font-display:block}}\n'
    for st in ("normal", "italic")
) + "".join(
    f'@font-face{{font-family:"Figtree";src:url(data:font/woff2;base64,{b64(fig / f"figtree-latin-{w}-normal.woff2")}) format("woff2");font-weight:{w};font-display:block}}\n'
    for w in (400, 500, 600, 700)
)

CSS = r"""
/* Layout: a deck of 16:9 slides; deep emerald and Jaipur sandstone grounds alternate, rose marks the one thing to see */
:root{
  --sea:#0E3640; --sea2:#17505C; --sea3:#22646F; --on-sea:#E8F0EE; --on-sea-mute:#9CB8BB; --sea-line:#2C6670;
  --fog:#EDF1EF; --paper:#FBFCFB; --ink:#132A30; --mute:#566C70; --line:#C9D5D3;
  --marigold:#E9A23B; --marigold-soft:#F7E1B8; --rust:#C4542A; --rust-soft:#F4D9CD; --mint:#9FD3C5; --mint-soft:#D7EEE7; --rust-tint:#F7E6DE; --sea-tint:#DCEAE7;
  --page-bg:#DDE5E3; --page-fg:#132A30; --page-mute:#566C70;
  --f-display:"Bodoni Moda","Didot","Bodoni 72",Georgia,serif;
  --f-body:"Figtree",system-ui,sans-serif;
  --f-mono:"Figtree",system-ui,sans-serif;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--page-bg:#081A1F;--page-fg:#E3ECEA;--page-mute:#93A9AC;color-scheme:dark}}
:root[data-theme="dark"]{--page-bg:#081A1F;--page-fg:#E3ECEA;--page-mute:#93A9AC;color-scheme:dark}

*{box-sizing:border-box}
body{background:var(--page-bg);color:var(--page-fg);font-family:var(--f-body);-webkit-print-color-adjust:exact;print-color-adjust:exact;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:28px 56px}
.page-head{max-width:1280px;margin:0 auto 20px;display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:8px 24px}
.page-head b{font-family:var(--f-display);font-weight:600;letter-spacing:.02em;font-size:15px}
.page-head span{font-family:var(--f-mono);font-size:12px;color:var(--page-mute);letter-spacing:.06em;text-transform:uppercase}
.deck{max-width:1280px;margin:0 auto;display:flex;flex-direction:column;gap:28px}

.slide{container-type:inline-size;container-name:slide;width:100%;max-width:100%;aspect-ratio:16/9;overflow:hidden;border-radius:14px;
  background:var(--fog);color:var(--ink);box-shadow:0 1px 2px rgba(10,30,35,.08),0 12px 32px -12px rgba(10,30,35,.25);position:relative}
.slide.paper{background:var(--paper)}
.slide.dark{background:var(--sea);color:var(--on-sea)}
.s-in{height:100%;display:flex;flex-direction:column;gap:2.1cqw;padding:2.6cqw 4.4cqw 2.4cqw;
  --xs:clamp(10px,.92cqw,12px);--s:clamp(11.5px,1.13cqw,14.5px);--b:clamp(12.5px,1.32cqw,17px);--l:clamp(14px,1.62cqw,20.5px);
  --h2:clamp(21px,3.05cqw,39px);--h1:clamp(32px,6.1cqw,78px);--stat:clamp(30px,5.2cqw,66px);--g:clamp(10px,1.6cqw,20px);
  font-size:var(--b);line-height:1.42}
.chrome{display:flex;justify-content:space-between;gap:12px;font-family:var(--f-mono);font-size:var(--xs);letter-spacing:.16em;text-transform:uppercase;color:var(--mute)}
.dark .chrome{color:var(--on-sea-mute)}
.chrome .mark{display:flex;align-items:center;gap:.6em}
.chrome .mark i{width:.55em;height:.55em;background:var(--rust);display:inline-block;border-radius:50%}
.dark .chrome .mark i{background:var(--marigold)}
.body{flex:1;min-height:0;display:flex;flex-direction:column;gap:var(--g)}
.eyebrow{font-family:var(--f-mono);font-size:var(--xs);letter-spacing:.18em;text-transform:uppercase;color:var(--rust);font-weight:600}
.dark .eyebrow{color:var(--marigold)}
h1,h2,h3{font-family:var(--f-display);margin:0;text-wrap:balance}
h1{font-size:var(--h1);font-weight:500;line-height:1;letter-spacing:-.015em}
h1 em,h2 em{font-style:italic;font-weight:500;color:var(--rust)}
.dark h1 em,.dark h2 em{color:var(--marigold)}
h2{font-size:var(--h2);font-weight:500;line-height:1.08;letter-spacing:-.01em;max-width:30ch}
h3{font-size:var(--l);font-weight:600;line-height:1.15}
p{margin:0}
.lead{font-size:var(--l);line-height:1.4;max-width:46ch}
.mute{color:var(--mute)} .dark .mute{color:var(--on-sea-mute)}
.small{font-size:var(--s)}
.mono{font-family:var(--f-mono);letter-spacing:.04em}
.hd{display:flex;flex-direction:column;gap:.7cqw}
.row{display:flex;gap:var(--g);flex-wrap:wrap}
.grid{display:grid;gap:var(--g)}
.g2{grid-template-columns:repeat(2,minmax(0,1fr))} .g3{grid-template-columns:repeat(3,minmax(0,1fr))}
.g4{grid-template-columns:repeat(4,minmax(0,1fr))} .g6{grid-template-columns:repeat(6,minmax(0,1fr))}
.fill{flex:1;min-height:0}
.ic{width:1.5em;height:1.5em;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round;flex:none}
.icb{width:2.6em;height:2.6em;border-radius:50%;display:grid;place-items:center;background:var(--mint-soft);color:var(--sea);flex:none}
.icb .ic{width:1.35em;height:1.35em}
.dark .icb{background:var(--sea2);color:var(--marigold)}
.card{background:var(--paper);border:1px solid transparent;border-radius:14px;box-shadow:0 1px 2px rgba(10,30,35,.05);padding:1.4cqw 1.5cqw;display:flex;flex-direction:column;gap:.7cqw;min-width:0}
.paper .card{background:var(--fog)}
.dark .card{background:var(--sea2);border-color:var(--sea-line)}
.chip{display:inline-flex;align-items:center;gap:.4em;font-family:var(--f-mono);font-size:var(--xs);letter-spacing:.1em;text-transform:uppercase;
  padding:.4em .85em;border-radius:999px;background:var(--mint-soft);color:var(--sea);font-weight:500;white-space:nowrap}
.chip.gold{background:var(--marigold-soft);color:#6A4510}
.chip.rust{background:var(--rust-soft);color:#7A2F13}
.dark .chip{background:var(--sea3);color:var(--on-sea)}
.dark .chip.gold{background:var(--marigold);color:var(--ink)}
ul.ticks{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:.55cqw}
ul.ticks li{display:flex;gap:.6em;align-items:flex-start}
ul.ticks li::before{content:"";flex:none;width:.5em;height:.5em;margin-top:.5em;background:var(--marigold);border-radius:1px}
.rule{height:1px;background:var(--line)} .dark .rule{background:var(--sea-line)}
svg text{font-family:var(--f-body)}
svg .mono{font-family:var(--f-mono)}
svg.chart{width:100%;height:auto;display:block}

/* cover */
.cover .s-in{padding-top:2.6cqw}
.cover-grid{display:grid;grid-template-columns:1.05fr .95fr;gap:3cqw;align-items:center;flex:1;min-height:0}
.route{display:flex;align-items:center;gap:.8em;font-family:var(--f-mono);font-size:var(--s);letter-spacing:.12em;text-transform:uppercase;color:var(--marigold);flex-wrap:wrap}
.route .ic{width:1.1em;height:1.1em;color:var(--on-sea-mute)}
/* stats */
.stat{border-top:2px solid var(--marigold);padding-top:1.1cqw;display:flex;flex-direction:column;gap:.4cqw}
.stat b{font-family:var(--f-display);font-size:var(--stat);font-weight:600;line-height:1;letter-spacing:-.01em}
.stat b em{font-style:normal;color:var(--marigold)}
/* steps track */
.track{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:var(--g);position:relative}
.track::before{content:"";position:absolute;left:6%;right:6%;top:2.2cqw;border-top:2px dashed var(--sea3);opacity:.5}
.step{display:flex;flex-direction:column;gap:.8cqw;position:relative;min-width:0}
.node{width:4.4cqw;height:4.4cqw;min-width:40px;min-height:40px;border-radius:50%;background:var(--sea);color:var(--marigold);display:grid;place-items:center;box-shadow:0 0 0 .6cqw var(--fog)}
.node .ic{width:48%;height:48%}
.who{display:grid;grid-template-columns:auto 1fr;gap:.25em .6em;font-size:var(--s)}
.who dt{font-family:var(--f-mono);font-size:var(--xs);letter-spacing:.08em;text-transform:uppercase;color:var(--mute);padding-top:.2em}
.who dd{margin:0}
.callout{background:var(--marigold-soft);border-radius:8px;padding:1cqw 1.4cqw;display:flex;gap:.8em;align-items:center;font-weight:500}
.dark .callout{background:var(--sea2)}
/* service cards */
.svc h3{font-size:var(--b)}
.svc .for{font-size:var(--s);color:var(--mute);flex:1}
.card.cta,.paper .card.cta{background:var(--sea);color:var(--on-sea);border-color:var(--sea)}
.cta .icb{background:var(--sea2);color:var(--marigold)}
.cta .for{color:var(--on-sea-mute)}
/* tables */
table.t{width:100%;border-collapse:collapse;font-size:var(--s)}
table.t th{font-family:var(--f-mono);font-size:var(--xs);letter-spacing:.08em;text-transform:uppercase;text-align:left;font-weight:500;color:var(--mute);padding:0 1cqw .6cqw 0;border-bottom:1.5px solid var(--ink)}
table.t td{padding:.62cqw 1cqw .62cqw 0;border-bottom:1px solid var(--line);vertical-align:top}
table.t td:first-child{font-weight:600}
.cell{display:flex;gap:.55em;align-items:flex-start}
.cell .ic{width:1.15em;height:1.15em;margin-top:.12em;stroke-width:2.4}
.x{color:var(--rust)} .ok{color:var(--sea3)}
table.t.vs td{padding-top:.95cqw;padding-bottom:.95cqw}
.vs td.diy{background:var(--rust-tint);padding-left:1cqw}
.vs td.ame{background:var(--sea-tint);padding-left:1cqw;font-weight:500}
.vs th.diy{color:var(--rust);padding-left:1cqw} .vs th.ame{color:var(--sea3);padding-left:1cqw}
.path{border-radius:12px;padding:1.6cqw 1.8cqw;display:flex;flex-direction:column;gap:1cqw;min-width:0}
.path.alone{background:var(--rust-tint);border:1.5px dashed var(--rust)}
.path.us{background:var(--sea);color:var(--on-sea)}
.path ol{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:.55cqw;font-size:var(--s)}
.path li{display:flex;gap:.7em;align-items:flex-start}
.path li .n{flex:none;width:1.7em;height:1.7em;border-radius:50%;display:grid;place-items:center;font-family:var(--f-mono);font-weight:600;font-size:.85em}
.alone li .n{background:var(--rust);color:var(--paper)}
.us li .n{background:var(--marigold);color:var(--ink)}
.us ol{font-size:var(--b);gap:1.2cqw}
.alone ol{font-size:var(--b);gap:.95cqw}
.bigt{white-space:nowrap}
.bigt{font-family:var(--f-display);font-weight:600;font-size:clamp(24px,3.4cqw,44px);line-height:1}
.phone{background:var(--ink);border-radius:22px;padding:1cqw;max-width:30cqw;width:100%;margin:0 auto;box-shadow:0 10px 30px -10px rgba(0,0,0,.4)}
.phone .scr{background:#E9E4DB;border-radius:14px;overflow:hidden;display:flex;flex-direction:column}
.phone .top{background:#2B4A4F;color:#E8F0EE;padding:.8cqw 1.1cqw;display:flex;align-items:center;gap:.7cqw;font-size:var(--s)}
.phone .top i{width:2.2cqw;height:2.2cqw;min-width:20px;min-height:20px;border-radius:50%;background:#8FA5A8;display:inline-block}
.phone .top small{display:block;font-size:var(--xs);color:#B9CDCF}
.phone .msgs{padding:1cqw;display:flex;flex-direction:column;gap:.6cqw;font-size:var(--s);line-height:1.3}
.bub{max-width:82%;padding:.55cqw .8cqw;border-radius:8px;background:#FFFFFF;color:#1C2B2E;box-shadow:0 1px 0 rgba(0,0,0,.08)}
.bub.me{align-self:flex-end;background:#D3EFC8}
.bub.warn{background:#FBE3D9}
.daytag{align-self:center;font-family:var(--f-mono);font-size:var(--xs);letter-spacing:.06em;background:#DCD5C9;color:#4E5A5C;padding:.2cqw .7cqw;border-radius:4px}
.seen{align-self:center;font-size:var(--xs);color:#6B7577;font-style:italic}
.pill4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1.4cqw}
.pillar{border-top:3px solid var(--marigold);padding-top:1cqw;display:flex;flex-direction:column;gap:.5cqw}
.mission{font-family:var(--f-display);font-weight:600;font-size:clamp(22px,3.5cqw,45px);line-height:1.08;max-width:24ch;text-wrap:balance}
.mi{display:flex;flex-direction:column;gap:.7cqw}
.mi .ex{margin-top:auto;border-top:1px dashed var(--line);padding-top:.7cqw;font-size:var(--s)}
.mi .ex b{font-family:var(--f-mono);font-size:var(--xs);letter-spacing:.08em;text-transform:uppercase;color:var(--rust);display:block;margin-bottom:.2cqw}
.stamp{border:1.5px dashed var(--sea3);border-radius:10px;padding:1.2cqw 1.4cqw;display:flex;flex-direction:column;gap:.5cqw;background:var(--paper);position:relative;min-width:0}
.stamp .code{position:absolute;top:1cqw;right:1.2cqw;font-family:var(--f-mono);font-weight:600;font-size:var(--xs);letter-spacing:.1em;color:var(--rust);border:1.5px solid var(--rust);padding:.15em .5em;border-radius:3px;transform:rotate(-6deg)}
.ledger{display:flex;flex-wrap:wrap;gap:.5cqw;align-items:center;border-top:1.5px solid var(--ink);padding-top:1cqw}
.stairs{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1.2cqw;align-items:end}
.stair{display:flex;flex-direction:column;gap:.7cqw}
.stair .blk{border-radius:8px 8px 0 0;background:var(--sea2);display:flex;align-items:flex-start;padding:1cqw 1.2cqw;color:var(--marigold);font-family:var(--f-display);font-weight:600;font-size:var(--h2)}
/* timeline (protection) */
.tl{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:1.2cqw;position:relative}
.tl::before{content:"";position:absolute;left:3%;right:3%;top:1.5cqw;height:2px;background:var(--sea-line)}
.tl .st{display:flex;flex-direction:column;gap:.6cqw;position:relative;min-width:0}
.tl .dot{width:3cqw;height:3cqw;min-width:28px;min-height:28px;border-radius:50%;display:grid;place-items:center;font-family:var(--f-mono);font-weight:600;font-size:var(--s);background:var(--mint);color:var(--ink);box-shadow:0 0 0 .5cqw var(--sea)}
.tl .money .dot{background:var(--marigold)}
.tl .ship .dot{background:var(--on-sea)}
.tl h3{font-size:var(--s);}
.tl p{font-size:var(--s);color:var(--on-sea-mute)}
/* equation */
.eq{display:flex;align-items:stretch;gap:1cqw}
.eq .blk{flex:1;border-radius:10px;padding:1.4cqw;display:flex;flex-direction:column;gap:.6cqw;background:var(--paper);border:1px solid var(--line);min-width:0}
.eq .op{display:grid;place-items:center;font-family:var(--f-display);font-size:var(--h2);font-weight:600;color:var(--mute);flex:none}
.eq .total{background:var(--sea);color:var(--on-sea);border-color:var(--sea)}
.eq .total .mute{color:var(--on-sea-mute)}
.strike{text-decoration:line-through;text-decoration-thickness:2px;text-decoration-color:var(--rust)}
/* stories */
.story b.m{font-family:var(--f-display);font-size:clamp(22px,3.1cqw,40px);font-weight:600;line-height:1;color:var(--marigold)}
.story .where{font-family:var(--f-mono);font-size:var(--xs);letter-spacing:.08em;text-transform:uppercase;color:var(--on-sea-mute)}
.story p{font-size:var(--s)}
.s-span2{grid-column:span 2} .s-span3{grid-column:span 3}
/* faq */
.faq{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1.3cqw 3cqw}
/* phone-only readable lists that replace wide charts */
.mlist{margin:0;display:flex;flex-direction:column}
.mlist .mt{font-family:var(--f-mono);font-size:var(--xs);letter-spacing:.14em;text-transform:uppercase;color:var(--mute);margin-bottom:6px}
.mlist .mr{display:flex;justify-content:space-between;align-items:baseline;gap:12px;padding:9px 0;border-top:1px solid var(--line)}
.mlist dt{font-size:var(--s);color:var(--ink)}
.mlist dd{margin:0;font-weight:600;font-size:var(--s);text-align:right;color:var(--ink)}
.mlist dd small{display:block;font-weight:400;color:var(--mute)}
.faq div{border-top:1px solid var(--line);padding-top:.8cqw;display:flex;flex-direction:column;gap:.3cqw;min-width:0}
.faq b{font-family:var(--f-display);font-weight:600;font-size:var(--b)}
.faq p{font-size:var(--s);color:var(--mute)}
/* contact */
.contact{display:grid;grid-template-columns:auto 1fr;gap:.9cqw 1.6cqw;align-items:baseline}
.contact dt{font-family:var(--f-mono);font-size:var(--xs);letter-spacing:.1em;text-transform:uppercase;color:var(--on-sea-mute)}
.contact dd{margin:0;font-size:var(--l);font-weight:500;user-select:all}
.contact dd.small{font-size:var(--s);font-weight:400;user-select:text}
.num{font-family:var(--f-display);font-weight:600;color:var(--marigold);font-size:var(--h2);line-height:1}
.closer{font-family:var(--f-display);font-weight:600;font-size:clamp(20px,2.6cqw,34px);line-height:1.05}
a{color:inherit;text-decoration-color:var(--marigold);text-underline-offset:.18em}

@media (max-width:820px){
  .pill4,.stairs{grid-template-columns:minmax(0,1fr)} .stair .blk{height:auto!important} .phone{max-width:100%}
  .slide{aspect-ratio:auto}
  .s-in{gap:18px;padding:18px 18px 16px}
  .g2,.g3,.g4,.g6,.cover-grid,.track,.tl,.faq{grid-template-columns:minmax(0,1fr)}
  .s-span2,.s-span3{grid-column:auto}
  .track::before,.tl::before{display:none}
  .eq{flex-direction:column} .eq .op{padding:2px 0}
  .split{grid-template-columns:minmax(0,1fr)!important}
  .tablewrap{overflow-x:auto}
}
@media (prefers-reduced-motion:no-preference){.slide{transition:box-shadow .2s}}
@page{size:1280px 720px;margin:0}
@media print{
  body{background:#fff;padding:0}
  .page-head{display:none}
  .deck{gap:0;max-width:none}
  .slide{width:1280px;height:720px;aspect-ratio:auto;border-radius:0;box-shadow:none;break-after:page;page-break-after:always}
}
"""

ICONS = {
"search":'<circle cx="11" cy="11" r="7"/><path d="M16.5 16.5L21 21"/>',
"shield":'<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6l8-3z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
"ship":'<path d="M3 14h18l-2.2 5.5H5.2z"/><path d="M6 14V9h12v5"/><path d="M9.5 9V5.5h5V9"/><path d="M2 22c2 0 2-1 4-1s2 1 4 1 2-1 4-1 2 1 4 1 2-1 4-1"/>',
"box":'<path d="M3 7.5l9-4 9 4-9 4-9-4z"/><path d="M3 7.5v9l9 4 9-4v-9"/><path d="M12 11.5v9"/>',
"truck":'<path d="M2 6h11v10H2z"/><path d="M13 9h4l4 4v3h-8z"/><circle cx="6.5" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>',
"plane":'<path d="M21 15.5L13.5 11V5.5a1.5 1.5 0 0 0-3 0V11L3 15.5V17l7.5-2.2V19L8.5 20.5V22l3.5-1 3.5 1v-1.5L13.5 19v-4.2L21 17z"/>',
"globe":'<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="3.8" ry="9"/><path d="M3.5 9h17M3.5 15h17"/>',
"tag":'<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8" r="1.4"/>',
"gift":'<path d="M3 8h18v4H3zM5 12h14v9H5zM12 8v13"/><path d="M12 8C10.5 4.5 6.5 4 7 6.7 7.4 8 12 8 12 8zm0 0c1.5-3.5 5.5-4 5-1.3C16.6 8 12 8 12 8z"/>',
"building":'<path d="M4 3h16v18H4z"/><path d="M8 7h2M14 7h2M8 11h2M14 11h2M8 15h2M14 15h2M10 21v-3h4v3"/>',
"store":'<path d="M3.5 9L5 4h14l1.5 5"/><path d="M3 9h18v1.5a3 3 0 0 1-6 0 3 3 0 0 1-6 0 3 3 0 0 1-6 0z"/><path d="M5 13.5V21h14v-7.5M10 21v-5h4v5"/>',
"factory":'<path d="M3 21V10l5 3v-3l5 3v-3l5 3V4h3v17z"/><path d="M7 17h2M12 17h2"/>',
"doc":'<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>',
"rupee":'<circle cx="12" cy="12" r="9"/><path d="M9 8h6M9 11h6M11 8c2.6 0 2.6 3 0 3H9l4.5 5"/>',
"clock":'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 2"/>',
"users":'<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6"/><circle cx="17" cy="9" r="2.5"/><path d="M17 14c2.8 0 4.5 2 4.5 5"/>',
"phone":'<rect x="7" y="2.5" width="10" height="19" rx="2"/><path d="M11 18h2"/>',
"mail":'<rect x="3" y="5" width="18" height="14" rx="1.5"/><path d="M3.5 6.5L12 13l8.5-6.5"/>',
"chat":'<path d="M4 4h16v12H9l-5 4z"/><path d="M8 9h8M8 12h5"/>',
"pin":'<path d="M12 21s-7-6.4-7-12a7 7 0 0 1 14 0c0 5.6-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
"cup":'<path d="M4 8h13v5a6 6 0 0 1-6 6h-1a6 6 0 0 1-6-6z"/><path d="M17 10h1.5a2.5 2.5 0 0 1 0 5H17M8 2.5v3M12 2.5v3"/>',
"home":'<path d="M3 11l9-7 9 7"/><path d="M5 9.5V20h14V9.5M10 20v-5h4v5"/>',
"sparkle":'<path d="M11 3l1.8 5.2L18 10l-5.2 1.8L11 17l-1.8-5.2L4 10l5.2-1.8z"/><path d="M18.5 15.5l.7 2 2 .7-2 .7-.7 2-.7-2-2-.7 2-.7z"/>',
"book":'<path d="M4 5a2 2 0 0 1 2-2h14v15H6a2 2 0 0 0-2 2z"/><path d="M4 20a2 2 0 0 0 2 2h14v-4"/>',
"palette":'<path d="M12 3a9 9 0 1 0 0 18c1.5 0 2-1 2-2s-1-1.5-1-2.5 1-2 2.5-2H18a3 3 0 0 0 3-3C21 7 17 3 12 3z"/><circle cx="7.5" cy="11" r="1"/><circle cx="10" cy="7" r="1"/><circle cx="15" cy="7.5" r="1"/>',
"gear":'<circle cx="12" cy="12" r="3"/><circle cx="12" cy="12" r="6.5"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9L7 7M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/>',
"dumbbell":'<path d="M6.5 6.5v11M17.5 6.5v11M3.5 9v6M20.5 9v6M6.5 12h11"/>',
"leaf":'<path d="M5 19C5 10 11 4 20 4c0 9-6 15-15 15z"/><path d="M5 19l8-8"/>',
"check":'<path d="M5 12.5l4.5 4.5L19 7.5"/>',
"x":'<path d="M6.5 6.5l11 11M17.5 6.5l-11 11"/>',
"arrow":'<path d="M4 12h15M13.5 6.5L19 12l-5.5 5.5"/>',
"eye":'<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
"lock":'<rect x="5" y="11" width="14" height="10" rx="1.5"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
"stamp":'<path d="M9.5 3h5v4.5L13.5 10H19v4H5v-4h5.5L9.5 7.5z"/><path d="M5 18h14v3H5z"/>',
"anchor":'<circle cx="12" cy="5" r="2"/><path d="M12 7v14M5 13a7 7 0 0 0 14 0M8.5 10.5h7"/>',
"layers":'<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>',
}
SPRITE = '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>' + "".join(
    f'<symbol id="i-{k}" viewBox="0 0 24 24">{v}</symbol>' for k, v in ICONS.items()) + '</defs></svg>'

def ic(name, cls="ic"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'

def icb(name):
    return f'<span class="icb">{ic(name)}</span>'

def mlist(title, rows):
    """Phone-only list version of a chart: rows of (label, value[, note])."""
    out = f'<dl class="mlist m-only"><div class="mt">{title}</div>'
    for r in rows:
        note = f"<small>{r[2]}</small>" if len(r) > 2 else ""
        out += f'<div class="mr"><dt>{r[0]}</dt><dd>{r[1]}{note}</dd></div>'
    return out + "</dl>"

SLIDES = []
def slide(theme, section, body):
    SLIDES.append((theme, section, body))

# ---------------- 1 COVER ----------------
containers = []
def container(x, y, fill, label=None, code=None, dark_text=False):
    tcol = "#132A30" if dark_text else "#E8F0EE"
    s = f'<g transform="translate({x},{y})"><rect width="164" height="72" rx="3" fill="{fill}"/>'
    s += '<rect x="5" y="5" width="154" height="62" fill="url(#corr)"/>'
    s += '<path d="M128 6v60M146 6v60" stroke="rgba(0,0,0,.28)" stroke-width="1.6"/>'
    s += '<rect x="134" y="30" width="6" height="14" rx="1" fill="rgba(0,0,0,.25)"/>'
    s += '<rect width="164" height="72" rx="3" fill="none" stroke="rgba(0,0,0,.22)" stroke-width="2"/>'
    if label:
        s += f'<text x="62" y="45" text-anchor="middle" font-family="Bodoni Moda" font-weight="600" font-size="22" letter-spacing="3" fill="{tcol}">{label}</text>'
    if code:
        s += f'<text class="mono" x="10" y="19" font-size="9" letter-spacing="1" fill="{tcol}" opacity=".8">{code}</text>'
    return s + '</g>'

cover_svg = f'''<svg class="chart" viewBox="0 0 520 470" role="img" aria-label="Stacked shipping containers with a trade route to a globe">
<defs>
 <pattern id="corr" width="7" height="10" patternUnits="userSpaceOnUse"><rect width="7" height="10" fill="none"/><rect x="0" width="2.2" height="10" fill="rgba(0,0,0,.14)"/><rect x="2.2" width="1" height="10" fill="rgba(255,255,255,.08)"/></pattern>
 <marker id="dotm" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5"><circle cx="5" cy="5" r="4" fill="#E9A23B"/></marker>
</defs>
<g opacity=".9">
 <circle cx="438" cy="78" r="50" fill="none" stroke="#2C6670" stroke-width="1.5"/>
 <ellipse cx="438" cy="78" rx="21" ry="50" fill="none" stroke="#2C6670" stroke-width="1.5"/>
 <path d="M392 60h92M392 96h92" stroke="#2C6670" stroke-width="1.5" fill="none"/>
 <circle cx="452" cy="64" r="6" fill="#E9A23B"/>
</g>
<path d="M452 64 C 380 40, 300 70, 272 186" fill="none" stroke="#E9A23B" stroke-width="2.2" stroke-dasharray="2 7" stroke-linecap="round"/>
<circle cx="272" cy="190" r="5" fill="#E9A23B"/>
{container(190,196,"#E9A23B","AMECK","AMKU 202614",True)}
{container(105,276,"#22646F",None,"CN-IN")}
{container(275,276,"#9FD3C5",None,"IN-EU",True)}
{container(20,356,"#17505C",None,"VN-IN")}
{container(190,356,"#C4542A",None,"AE-IN")}
{container(360,356,"#E8F0EE",None,"IN-US",True)}
<path d="M0 432h520" stroke="#2C6670" stroke-width="2"/>
<text class="mono" x="0" y="458" font-size="11" letter-spacing="2" fill="#9CB8BB">35+ COUNTRIES  /  500+ FACTORIES  /  ONE PARTNER</text>
</svg>'''

slide("dark cover", "Customer guide", f'''
<div class="cover-grid">
  <div class="hd" style="gap:2.2cqw">
    <span class="eyebrow">Ameck Business House / Customer guide 2026</span>
    <h1>How Ameck works <em>for you</em></h1>
    <p class="lead" style="color:var(--on-sea)">We find the product you want anywhere in the world, buy it at the best price, check its quality and deliver it to your door.</p>
    <div class="route">Find {ic("arrow")} Check {ic("arrow")} Ship {ic("arrow")} Deliver</div>
    <p class="small mute">Global trade and product sourcing, run from Jaipur and Gurgaon, India.</p>
  </div>
  <div class="hd" style="gap:.4cqw">{globe_html(cover_svg, 'Our trade routes: 17 sourcing hubs into Jaipur. Drag to spin.')}</div>
</div>''')


# ---------------- THE PROBLEM ----------------
slide("", "The problem", f"""
<div class="grid fill split" style="grid-template-columns:.8fr 1.2fr;gap:4cqw;align-items:center">
  <div>
    <div class="phone"><div class="scr">
      <div class="top"><i></i><div>+91 9xxxx xxxxx<small>Import agent, unsaved number</small></div></div>
      <div class="msgs">
        <div class="bub me">Need 200 of this bag. Best price?</div>
        <div class="bub">Best rate. Pay cash or UPI to my personal number.</div>
        <div class="bub me">Will I get a GST bill?</div>
        <div class="bub">No bill needed. I will manage customs.</div>
        <span class="daytag">3 weeks later</span>
        <div class="bub warn">Goods stuck at port. Send Rs. 40,000 more to release.</div>
        <div class="bub me">These do not look like the sample at all!</div>
        <span class="seen">Last seen 2 weeks ago</span>
      </div>
    </div></div>
    <p class="small mute m-hide" style="text-align:center;margin-top:2.6cqw">Illustration of a typical informal import</p>
  </div>
  <div class="hd" style="gap:1.4cqw">
    <span class="eyebrow">The problem we exist to solve</span>
    <h2>Too much of India's import trade still runs on WhatsApp</h2>
    <p class="mute">Unregistered agents, no paperwork and no one to hold accountable. Small and growing businesses carry all of the risk.</p>
    <div class="grid g2 m-swipe" style="gap:1cqw">
      {"".join(f'<div class="row" style="flex-wrap:nowrap;gap:.7em;align-items:flex-start;padding:1cqw 1.1cqw;background:var(--rust-tint);border-radius:8px"><span class="x">{ic(i)}</span><span class="small"><b>{t}</b><br><span class="mute">{d}</span></span></div>' for i,t,d in [
        ("rupee","Hidden margins","One brand was paying about 1.8 times the factory price"),
        ("doc","No invoice, no paper trail","No GST bill, no input tax credit, no proof"),
        ("eye","No quality check","Photos on chat, then whatever arrives"),
        ("stamp","Stuck at customs","Paperwork errors, holds and extra payments"),
        ("users","No one accountable","When it goes wrong, the number goes silent"),
        ("factory","Small buyers shut out","Factories ask for 500 to 5,000 units")])}
    </div>
  </div>
</div>""")

# ---------------- OUR MOTIVE ----------------
pillars = [
 ("Formal","Our own IEC, GST-compliant billing and 100% of the paperwork on every order."),
 ("Transparent","Factory price plus actual freight. Zero commission, no hidden margins."),
 ("Accessible","Start from 25 units and 20 kg, any mix. We pool orders to reach factory prices."),
 ("Accountable","Verified suppliers, two inspections, one contact, and a refund if we cannot deliver."),
]
slide("dark", "Our motive", f"""
<div class="hd" style="gap:1.6cqw"><span class="eyebrow">Our motive</span>
<p class="mission">We are taking India's import trade out of WhatsApp chats and making it formal, transparent and accountable.</p>
<p class="lead" style="color:var(--on-sea-mute);max-width:62ch">Any Indian business, however small, should be able to buy from the world's factories at factory prices, with full paperwork, verified suppliers and one partner who answers for the result.</p></div>
<div class="pill4 fill m-swipe" style="align-content:end">
 {"".join(f'<div class="pillar"><h3 style="color:var(--marigold)">{t}</h3><p class="small" style="color:var(--on-sea)">{d}</p></div>' for t,d in pillars)}
</div>""")

# ---------------- WHY AMECK ----------------
why = [
 ("Who you deal with","An unregistered phone number","A registered company with its own IEC, offices in Jaipur and Gurgaon"),
 ("Paperwork","None, or done badly","100% done by us, under our own IEC"),
 ("Price","A hidden margin at every layer","Factory price plus actual freight, zero commission"),
 ("Quality","Photos on a chat","Sample approval plus two factory inspections"),
 ("Payment","Cash or a personal UPI ID","RBI-regulated gateway, refund if we cannot deliver"),
 ("When something goes wrong","Last seen two weeks ago","One accountable contact, reply within one business day"),
 ("Reach","Whatever one trader knows","35+ countries and 500+ verified factories"),
]
slide("paper", "Why Ameck", f"""
<div class="hd"><span class="eyebrow">Why Ameck</span><h2>A WhatsApp trader, or a trade partner</h2></div>
<div class="tablewrap fill"><table class="t vs mcards">
<thead><tr><th style="width:20%"></th><th class="diy" style="width:34%">WhatsApp trader</th><th class="ame">Ameck Business House</th></tr></thead>
<tbody>{"".join(f'<tr><td>{a}</td><td class="diy" data-l="WhatsApp trader"><span class="cell"><span class="x">{ic("x")}</span><span>{d}</span></span></td><td class="ame" data-l="Ameck Business House"><span class="cell"><span class="ok">{ic("check")}</span>{w}</span></td></tr>' for a,d,w in why)}</tbody>
</table></div>
<div class="callout" style="background:var(--sea);color:var(--on-sea)"><span style="color:var(--marigold)">{ic("shield")}</span><span><b>We are not another middleman.</b> We are the formal, accountable way for Indian businesses to trade with the world.</span></div>""")
# ---------------- 2 WHO WE ARE ----------------
promise = [
 ("shield","Full ownership, not just advice","We carry out every step ourselves, from the first conversation to final delivery."),
 ("globe","Global reach, Indian understanding","We know the factories abroad and the market at home."),
 ("users","Built for every size","First-time entrepreneur or established business, we scale to fit you."),
 ("chat","One accountable contact","You never chase suppliers, forwarders or customs. We do, and we keep you updated."),
]
slide("", "Who we are", f'''
<div class="grid g2 fill split" style="grid-template-columns:1fr 1fr;gap:4cqw;align-items:start">
  <div class="hd" style="gap:1.6cqw">
    <span class="eyebrow">Who we are</span>
    <h2>A global trade partner for Indian businesses of every size</h2>
    <p class="lead">Most Indian businesses buy from the same local wholesalers. Same products, same prices, no way to stand out.</p>
    <p>We built Ameck to change that. We give small shops, growing brands and established companies the global factories and factory prices that large corporations take for granted.</p>
    <div class="grid g2" style="margin-top:1cqw">
      <div class="card">{icb("building")}<h3>Gurgaon</h3><p class="small mute">Headquarters. Corporate and strategic leadership.</p></div>
      <div class="card">{icb("pin")}<h3>Jaipur</h3><p class="small mute">Operations. Sourcing, logistics, compliance and client work. Visits by appointment.</p></div>
    </div>
  </div>
  <div class="hd" style="gap:1.4cqw">
    <span class="eyebrow">Our promise to you</span>
    <div class="hd m-swipe" style="gap:1.4cqw">{"".join(f'<div class="row" style="flex-wrap:nowrap;align-items:flex-start;gap:1.4cqw;padding-bottom:1.3cqw;border-bottom:1px solid var(--line)">{icb(i)}<div class="hd" style="gap:.3cqw"><h3>{t}</h3><p class="mute">{d}</p></div></div>' for i,t,d in promise)}</div>
  </div>
</div>''')

# ---------------- 3 NETWORK MAP ----------------
import json as _json
MAP = _json.loads((HERE.parent / "map" / "map.json").read_text())
_dots = "".join(f'<circle cx="{x}" cy="{y}" r="2.3"/>' for x,y in MAP["dots"])
_jx, _jy = MAP["jaipur"]["x"], MAP["jaipur"]["y"]
_arcs = ""; _pins = ""; _moves = []
LABEL = {"China":(10,15,"start"),"Japan":(8,4,"start"),"Vietnam":(8,10,"start"),"Indonesia":(8,10,"start"),"UAE":(-8,12,"end"),"Turkey":(6,-8,"start"),"Germany":(4,-10,"start"),"Italy":(-8,12,"end"),"United States":(0,-10,"middle"),"United Kingdom":(-10,6,"end")}
for h in MAP["hubs"]:
    x,y = h["x"],h["y"]
    mx,my = (x+_jx)/2, (y+_jy)/2
    d = ((x-_jx)**2+(y-_jy)**2)**.5
    cy_ = my - d*0.28
    _arcs += f'<path data-r="{h["region"]}" d="M{x},{y} Q{mx:.1f},{cy_:.1f} {_jx},{_jy}"/>'
    _k = len(_moves)
    _moves.append(f'<circle data-r="{h["region"]}" r="3.4" fill="#FFE2A8"><animateMotion dur="{5+(_k%4)}s" begin="-{(_k*0.7)%5:.1f}s" repeatCount="indefinite" path="M{x},{y} Q{mx:.1f},{cy_:.1f} {_jx},{_jy}"/></circle>')
    _pins += f'<circle class="pin" data-r="{h["region"]}" cx="{x}" cy="{y}" r="4.2" fill="#9FD3C5" stroke="#0E3640" stroke-width="1.5"><title>{h["name"]}</title></circle>'
    if h["name"] in LABEL:
        dx,dy,a = LABEL[h["name"]]
        _pins += f'<text data-r="{h["region"]}" x="{x+dx}" y="{y+dy}" text-anchor="{a}" font-size="12.5" fill="#E8F0EE" font-weight="500">{h["name"]}</text>'
map_svg = f"""<svg id="netmap" class="chart wide-xl" viewBox="0 0 {MAP['w']} {MAP['h']}" role="img" aria-label="World map of Ameck sourcing hubs across Asia, the Middle East, Europe and the United States, all routed to Jaipur">
<g fill="#336F79">{_dots}</g>
<g fill="none" stroke="#E9A23B" stroke-width="1.4" stroke-opacity=".55">{_arcs}</g>
<g>{"".join(_moves)}</g>
{_pins}
<circle cx="{_jx}" cy="{_jy}" r="16" fill="#E9A23B" fill-opacity=".18"/><circle cx="{_jx}" cy="{_jy}" r="7.5" fill="#E9A23B" stroke="#0E3640" stroke-width="2"/>
<text x="{_jx}" y="{_jy+30}" text-anchor="middle" class="mono" font-size="13" font-weight="600" fill="#E9A23B" letter-spacing="2">JAIPUR</text>
</svg>"""
netstats = [('<span data-count="35">35</span><em>+</em>',"Countries we source from"),('<span data-count="500">500</span><em>+</em>',"Verified factory partners"),('<span data-count="25">25</span><em>+</em>',"Industries served"),('<span data-count="100">100</span><em>%</em>',"Orders inspected before shipping"),("&lt;2<em>%</em>","Dispute rate on orders")]
slide("dark", "Our network", f"""
<div class="hd"><span class="eyebrow">Our network</span><h2>Factories across the world, one route to your door</h2></div>
<div class="grid fill split" style="grid-template-columns:2.6fr 1fr;gap:3cqw;align-items:center">
  <div class="hd" style="gap:1cqw"><div class="chipbar" data-for="netmap" role="group" aria-label="Show hubs by region"><span class="mono small mute" style="margin-right:.4cqw">SHOW</span>{"".join(f'<button type="button" data-f="{k}" aria-pressed="{str(k=="all").lower()}" class="{"on" if k=="all" else ""}">{v}</button>' for k,v in [("all","All"),("asia","Asia"),("me","Middle East"),("eu","Europe"),("am","Americas")])}</div><div>{map_svg}</div></div>
  <div class="hd m-grid2" style="gap:1.2cqw">{"".join(f'<div class="stat" style="padding-top:.6cqw"><b style="font-size:clamp(24px,3.2cqw,42px)">{n}</b><span class="small mute">{l}</span></div>' for n,l in netstats)}</div>
</div>
<p class="small mute">Main sourcing hubs shown. Other regions on request. Sourcing and logistics run from our Jaipur operations centre.</p>""")


def iso_row(nodes, heights, colors, label):
    pl='<div class="ground" style="border-radius:20px"></div>'
    for k in range(4):
        pl+=box(18+k*74,62,58,58,heights[k],colors[k],inner=bb(nodes[k],lift=10),attrs=f'data-k="{k+1}"')
    return scene(360,300,pl,320,180,20,90,58,-38,persp=1400,label=label)
# ---------------- 4 FOUR STEPS ----------------
steps = [
 ("search","We find it","Share the product, quantity, budget and deadline","Find and verify a trusted factory, negotiate the price, work out your full landed cost","Real quote in 48 hours"),
 ("eye","We check it","Approve the sample","Inspect mid-production and again before shipping, against your approved sample","During production"),
 ("ship","We ship it","Nothing","Book freight, insure the cargo, prepare every document, clear customs, pay duties","Air 7 to 12, sea 25 to 45 working days"),
 ("home","You get it","Receive your goods","Deliver to your warehouse, office or shop, with tracking at every milestone","Pan-India, or free pickup in Jaipur and Delhi"),
]
_CX=[146,438,730,1022]; _PD=190
_pl='<div class="ground"></div>'
_pl+=f'<div class="road" style="left:{_CX[0]}px;top:{_PD//2+70}px;width:{_CX[3]-_CX[0]}px"></div>'
for n,(i_,t,y_,w_,tm) in enumerate(steps):
    _node=f'<div class="node3d {"gold" if n==3 else ""}">{ic(i_)}</div>'
    _pl+=box(_CX[n]-88,_PD//2-62,176,104,[26,44,62,80][n],GOLD if n==3 else TEAL,inner=bb(_node,lift=14),attrs=f'data-k="{n+1}"')
_pl+=f'<div class="trav" style="left:{_CX[0]-23}px;top:{_PD//2+70-13}px;--dist:{_CX[3]-_CX[0]}px;--dur:9s">{box(0,0,46,26,22,GOLD)}</div>'
steps_scene=scene(1168,176,_pl,1168,_PD,0,10,58,0,persp=1700,label="Four raised platforms for Find, Check, Ship and Deliver, joined by a shipping route with a container moving along it")
slide("", "How we work", f'''
<div class="hd"><span class="eyebrow">How we work</span><h2 style="max-width:none">From your enquiry to your door, in four steps</h2></div>
<div class="d-only">{steps_scene}</div><div class="m-only">{iso_row([f'<div class="node3d sm {chr(103)+chr(111)+chr(108)+chr(100) if n==3 else chr(32)}">{ic(s_[0])}</div>' for n,s_ in enumerate(steps)],[22,40,58,76],[TEAL,TEAL,TEAL,GOLD],'Four rising platforms: find, check, ship, deliver')}</div>
<div class="grid g4 m-swipe" style="gap:var(--g)">
 {"".join(f'''<div class="hd stepcol" data-k="{n+1}" style="gap:.6cqw"><div class="hd" style="gap:.1cqw"><span class="eyebrow" style="color:var(--mute)">Step {n+1}</span><h3>{t}</h3></div>
   <dl class="who"><dt>You</dt><dd>{y}</dd><dt>We</dt><dd>{w}</dd></dl>
   <span class="chip" style="align-self:flex-start;white-space:normal">{ic("clock")} {tm}</span></div>''' for n,(i,t,y,w,tm) in enumerate(steps))}
</div>
<div class="callout">{ic("check")} Your only jobs are to share the requirement and approve the sample. We handle every factory, shipment and customs form in between.</div>''')

# ---------------- MARKET INTELLIGENCE ----------------
mis = [
 ("sparkle","Trend intelligence","We track global trends and spot products 12 to 24 months before they reach Indian wholesale.","Gift store, Bangalore","Became the city's only stockist of Nordic ceramics"),
 ("search","Niche discovery","We match a product category to your capital, city and customers.","First-time importer, Hyderabad","Opened with an underserved range, reordered in 3 months"),
 ("eye","Competitor analysis","We find what drives a rival's growth, then target the categories nobody owns yet.","Kitchenware retailer, Kochi","Two new categories and growing again in 8 months"),
 ("layers","Product strategy","We help you choose what to launch, how to position it and at what order size.","Education store, Pune","First Indian stockist of Scandinavian learning tools"),
]
slide("paper", "Market intelligence", f"""
<div class="row m-stack" style="justify-content:space-between;align-items:flex-end;gap:2cqw;flex-wrap:nowrap">
  <div class="hd"><span class="eyebrow">Market intelligence</span><h2>We also help you decide what to sell</h2></div>
  <div style="text-align:right;flex:none"><b class="num" style="font-size:var(--stat)">12 to 24</b><p class="small mute">months ahead of the Indian mainstream</p></div>
</div>
<p class="mute" style="max-width:72ch">Selling the same products as every shop on your street leaves you competing only on price. Our research finds what your competitors have not found yet.</p>
<div class="grid g4 fill m-swipe" style="grid-auto-rows:1fr">
 {"".join(f'<div class="card mi">{icb(i)}<h3 style="font-size:var(--l)">{t}</h3><p class="mute">{d}</p><div class="ex"><b>{w}</b><span style="font-size:var(--b);font-weight:500">{r}</span></div></div>' for i,t,d,w,r in mis)}
</div>""")

# ---------------- 5 SEVEN SERVICES ----------------
SVC_BACK = {
 "Shipping and Delivery": (["Sea or air freight, customs cleared","From 25 kg, no upper limit","Full cost breakdown in 4 hours"],"Shipping and Delivery"),
 "Import from China": (["25 units and 20 kg per shipment, any mix","Factory price, zero commission","Sample first, then two inspections"],"Import from China"),
 "Export and Global Trade": (["Documentation, freight and compliance","Indian goods to buyers worldwide","Four trade directions covered"],"Export and Global Trade"),
 "Brand Building": (["From an idea to a product ready to sell","Your logo, colours and packaging","Sourcing plan within 48 hours"],"Brand Building and Global Sourcing"),
 "Corporate Solutions": (["Gifts, kits, hampers and supplies","From 50 units, fully branded","Delivered anywhere in India"],"Corporate Solutions"),
 "Global Sourcing": (["35+ countries searched for you","Suppliers vetted, prices negotiated","Inspected before it ships"],"Brand Building and Global Sourcing"),
 "Ready Stock Store": (["Products already imported and checked","Bulk orders from 25 units","Browse at catalogue.ameckhouse.com"],None),
}
def svc_flip(i,t,f,k):
    import re as _re
    plain=_re.sub(r"<[^>]+>","",t)
    pts,jt=SVC_BACK.get(plain,([],None))
    jump=f'<button type="button" class="jump" data-jump="{jt}">See the details {ic("arrow")}</button>' if jt else '<span class="flip-hint" style="color:var(--marigold)">Tap to flip back</span>'
    return (f'<div class="flip" tabindex="0" role="button" aria-pressed="false" aria-label="{plain}: show key terms"><div class="flip-in">'
            f'<div class="card svc face front">{icb(i)}<h3>{t}</h3><p class="for">{f}</p><div class="row" style="justify-content:space-between;align-items:center;gap:.6em;flex-wrap:nowrap"><span class="chip gold">{k}</span><span class="flip-hint">Flip {ic("arrow")}</span></div></div>'
            f'<div class="card face back" style="background:var(--sea);color:var(--on-sea);border-color:var(--sea)"><h3 style="font-size:var(--b)">{t}</h3>'
            f'<ul class="ticks small">{"".join(f"<li>{x}</li>" for x in pts)}</ul>{jump}</div></div></div>')

svcs = [
 ("truck","Shipping and Delivery","Businesses that already have a product and need it moved, door to door","From 25 kg"),
 ("factory","Import from China","First-time and experienced importers wanting factory prices","25 units + 20 kg"),
 ("globe","Export and Global Trade","Indian makers and sellers going global","25 units + 20 kg"),
 ("tag","Brand Building","Entrepreneurs with a product idea but no brand yet","Plan in 48 h"),
 ("gift","Corporate Solutions","HR teams and companies: gifts, kits, hampers, supplies","From 50 units"),
 ("search","Global Sourcing","Buyers who know what they want, not where to find it","Any category"),
 ("store","Ready Stock Store","Buyers ready to purchase products we have already imported","From 25 units"),
]
slide("paper", "Our services", f'''
<div class="hd"><span class="eyebrow">Seven ways we help</span><h2 style="max-width:none">Pick only what you need. Every service works on its own.</h2><p class="small mute">Tap any card to flip it for the key terms.</p></div>
<div class="grid g4 fill m-swipe" style="grid-auto-rows:1fr">
 {"".join(svc_flip(i,t,f,k) for i,t,f,k in svcs)}
 <div class="card svc cta"><span class="icb">{ic("chat")}</span><h3>Not sure which fits?</h3><p class="for">Tell us what you are looking for and we will point you to the right service.</p><span class="mono small" style="color:var(--marigold)">WhatsApp +91 83021 92742</span></div>
</div>''')

# ---------------- 6 IMPORT FROM CHINA ----------------
X0, X1, D = 70, 540, 45
sx = lambda d: X0 + (X1 - X0) * d / D
ticks = "".join(f'<line x1="{sx(t):.1f}" y1="44" x2="{sx(t):.1f}" y2="214" stroke="#C9D5D3" stroke-width="1"/><text x="{sx(t):.1f}" y="236" text-anchor="middle" font-size="13" fill="#566C70">{t}</text>' for t in (0,10,20,30,40))
mode_chart = f'''<svg class="chart wide" viewBox="0 0 560 270" role="img" aria-label="Air freight takes 7 to 12 working days, sea freight 25 to 45 working days">
{ticks}
<line x1="{X0}" y1="214" x2="{X1}" y2="214" stroke="#132A30" stroke-width="1.5"/>
<text x="0" y="100" font-size="16" font-weight="600" fill="#132A30">Air</text>
<rect x="{sx(7):.1f}" y="88" width="{sx(12)-sx(7):.1f}" height="26" rx="5" fill="#E9A23B"/>
<text x="{sx(12)+10:.1f}" y="106" font-size="14" fill="#132A30" font-weight="500">7 to 12 working days</text>
<text x="0" y="172" font-size="16" font-weight="600" fill="#132A30">Sea</text>
<rect x="{sx(25):.1f}" y="160" width="{sx(45)-sx(25):.1f}" height="26" rx="5" fill="#17505C"/>
<text x="{sx(25)-10:.1f}" y="178" text-anchor="end" font-size="14" fill="#132A30" font-weight="500">25 to 45 working days</text>
<text x="{X1}" y="262" text-anchor="end" font-size="12" fill="#566C70" class="mono">WORKING DAYS, DOOR TO DOOR</text>
<text x="0" y="22" font-size="12" fill="#566C70" class="mono">CHOOSE YOUR SHIPPING MODE</text>
</svg>'''
slide("", "Import from China", f'''
<div class="hd"><span class="eyebrow">Service / Import from China</span><h2>Factory-direct from China, with zero commission</h2></div>
<div class="grid fill split" style="grid-template-columns:.9fr 1.1fr;gap:4cqw;align-items:start">
  <div class="hd" style="gap:1.4cqw">
    <div class="hd" style="gap:.8cqw"><span class="eyebrow" style="color:var(--mute)">Minimum per shipment. Both must be met.</span>
    <div class="grid g2" style="gap:1.2cqw">
      <div class="card" style="gap:.4cqw"><b class="num" style="font-size:clamp(26px,4cqw,52px);white-space:nowrap">25</b><span class="small"><b>units minimum</b>, any mix of products</span></div>
      <div class="card" style="gap:.4cqw"><b class="num" style="font-size:clamp(26px,4cqw,52px);white-space:nowrap">20 kg</b><span class="small"><b>weight minimum</b>, whole shipment</span></div>
    </div><p class="small mute">Applies to every import and export shipment.</p></div>
    <ul class="ticks">
      <li>Machinery, furniture and fully custom goods may need more units. We confirm on enquiry.</li>
      <li>You only need GST registration. We work under our own IEC and do 100% of the paperwork.</li>
      <li>Sample approval before bulk, pre-shipment inspection on every order</li>
    </ul>
  </div>
  <div class="card" style="padding:1.6cqw 2cqw"><div class="m-hide">{mode_chart}</div>{mlist('Shipping mode, door to door', [('Air','7 to 12 working days'),('Sea','25 to 45 working days')])}<p class="small mute">Insurance, tracking and customs handling are included with both modes. Samples travel by express courier.</p></div>
</div>''')

# ---------------- 7 SHIPPING ----------------
lanes = [
 ("anchor","World to India","Imports into India",["Freight booking","Customs clearance","Duty management","Door delivery"]),
 ("plane","India to World","Exports from India",["Export documentation","Global freight","Compliance support","International delivery"]),
 ("truck","Warehouse to you","Last mile",["Pan-India delivery","Free self-pickup in Jaipur","Free self-pickup in Delhi"]),
]
goods = ["Apparel","Electronics","Home goods","Food products","Machinery","Raw materials","Furniture","Textiles"]
slide("paper", "Shipping and Delivery", f'''
<div class="hd"><span class="eyebrow">Service / Shipping and Delivery</span><h2>Already have the goods? We move them, cleared and delivered.</h2></div>
<div class="grid g3 m-swipe">
 {"".join(f'<div class="card"><div class="row" style="align-items:center;flex-wrap:nowrap;gap:1cqw">{icb(i)}<div><h3>{t}</h3><span class="small mute">{s}</span></div></div><ul class="ticks small">{"".join(f"<li>{x}</li>" for x in items)}</ul></div>' for i,t,s,items in lanes)}
</div>
<div class="grid g4 m-grid2" style="border-top:1.5px solid var(--ink);padding-top:1.2cqw">
  <div><b class="num" style="font-size:var(--h2)">25 kg</b><p class="small mute">Minimum per shipment</p></div>
  <div><b class="num" style="font-size:var(--h2)">No cap</b><p class="small mute">No upper weight limit</p></div>
  <div><b class="num" style="font-size:var(--h2)">4 h</b><p class="small mute">Full cost breakdown in 4 hours</p></div>
  <div><b class="num" style="font-size:var(--h2)">35+</b><p class="small mute">Countries served</p></div>
</div>
<div class="row" style="align-items:center;gap:.6cqw">
  <span class="mono small mute" style="margin-right:.6cqw">WE SHIP</span>{"".join(f'<span class="chip">{g}</span>' for g in goods)}<span class="chip">And more</span>
  <span class="chip rust">{ic("x")} Hazardous materials only</span>
</div>''')

# ---------------- 8 EXPORT / FOUR DIRECTIONS ----------------
dir_svg = '''<svg class="chart" viewBox="0 0 480 400" role="img" aria-label="Four trade directions around India: world to India, China to India, India to world, Indian goods to global buyers">
<defs>
 <marker id="am" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#9FD3C5"/></marker>
 <marker id="ag" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#E9A23B"/></marker>
</defs>
<path d="M108 118 L 184 172" stroke="#9FD3C5" stroke-width="3" fill="none" marker-end="url(#am)"/>
<path d="M368 104 Q 300 100 276 152" stroke="#9FD3C5" stroke-width="3" fill="none" marker-end="url(#am)"/>
<path d="M298 186 Q 374 182 394 136" stroke="#E9A23B" stroke-width="3" fill="none" marker-end="url(#ag)"/>
<path d="M290 252 Q 330 320 362 322" stroke="#E9A23B" stroke-width="3" fill="none" marker-end="url(#ag)"/>
<circle cx="236" cy="214" r="64" fill="#FBFCFB" stroke="#E9A23B" stroke-width="5"/>
<text x="236" y="210" text-anchor="middle" font-family="Bodoni Moda" font-weight="600" font-size="26" fill="#132A30" letter-spacing="2">INDIA</text>
<text x="236" y="234" text-anchor="middle" font-size="12" fill="#566C70" class="mono">JAIPUR OPS</text>
<circle cx="70" cy="92" r="44" fill="#22646F"/><text x="70" y="98" text-anchor="middle" font-family="Bodoni Moda" font-weight="600" font-size="16" fill="#E8F0EE">CHINA</text>
<circle cx="410" cy="82" r="48" fill="#22646F"/><text x="410" y="78" text-anchor="middle" font-family="Bodoni Moda" font-weight="600" font-size="15" fill="#E8F0EE">WORLD</text><text x="410" y="96" text-anchor="middle" font-size="12" fill="#9CB8BB">markets</text>
<circle cx="412" cy="330" r="48" fill="#22646F"/><text x="412" y="326" text-anchor="middle" font-family="Bodoni Moda" font-weight="600" font-size="15" fill="#E8F0EE">GLOBAL</text><text x="412" y="344" text-anchor="middle" font-size="12" fill="#9CB8BB">buyers</text>
<g font-family="IBM Plex Mono" font-weight="600" font-size="13" text-anchor="middle">
 <circle cx="318" cy="112" r="12" fill="#9FD3C5"/><text x="318" y="117" fill="#132A30">1</text>
 <circle cx="146" cy="134" r="12" fill="#9FD3C5"/><text x="146" y="139" fill="#132A30">2</text>
 <circle cx="366" cy="178" r="12" fill="#E9A23B"/><text x="366" y="183" fill="#132A30">3</text>
 <circle cx="318" cy="300" r="12" fill="#E9A23B"/><text x="318" y="305" fill="#132A30">4</text>
</g>
<g font-size="12" fill="#9CB8BB" class="mono"><rect x="0" y="352" width="22" height="4" fill="#9FD3C5"/><text x="30" y="358">INTO INDIA</text><rect x="0" y="374" width="22" height="4" fill="#E9A23B"/><text x="30" y="380">OUT OF INDIA</text></g>
</svg>'''
dirs = [
 ("1","World to India","Products from global markets brought into India, from factory to your warehouse, duties and all.","mint"),
 ("2","China to India","Factory-direct pricing, zero commission, pre-shipment quality checks.","mint"),
 ("3","India to World","Indian-made goods taken to global buyers. We handle documentation, freight and compliance.","gold"),
 ("4","Indian goods for global buyers","International buyers source authentic Indian textiles, handicrafts, spices and more, for B2B and retail.","gold"),
]
slide("dark", "Export and Global Trade", f'''
<div class="hd"><span class="eyebrow">Service / Export and Global Trade</span><h2>Four trade directions. One partner.</h2></div>
<div class="grid fill split" style="grid-template-columns:.95fr 1.05fr;gap:3.5cqw;align-items:center">
  <div>{dir_svg}</div>
  <div class="hd" style="gap:1.3cqw">
   <div class="hd m-swipe" style="gap:1.3cqw">{"".join(f'<div class="row" style="flex-wrap:nowrap;gap:1.2cqw;align-items:flex-start;padding-bottom:1.1cqw;border-bottom:1px solid var(--sea-line)"><span class="mono" style="flex:none;width:2em;height:2em;border-radius:50%;display:grid;place-items:center;font-weight:600;background:{"var(--mint)" if c=="mint" else "var(--marigold)"};color:var(--ink)">{n}</span><div class="hd" style="gap:.3cqw"><h3>{t}</h3><p class="small mute">{d}</p></div></div>' for n,t,d,c in dirs)}</div>
   <div class="callout" style="gap:1cqw"><b class="num" style="font-size:var(--h2);white-space:nowrap">25 units + 20 kg</b><span class="small">Minimum for every import or export shipment. Both must be met, and you can mix any products.</span></div>
  </div>
</div>''')

# ---------------- 9 BRAND + SOURCING ----------------
CONN = '<span style="flex:1;width:2px;background:var(--line);min-height:.8cqw"></span>'
bsteps = [("Share your idea","Product concept, target market, budget"),("We source it","Right factory, material and price"),("Brand and package","Your logo, colours and packaging applied"),("Market ready","Delivered and ready to sell")]
regions = [("East Asia","China, Taiwan, Vietnam"),("South and Southeast Asia","India, Bangladesh, Indonesia, Thailand"),("Middle East","UAE, Dubai"),("Europe","Germany, Italy, Poland, Portugal")]
slide("", "Brand Building and Global Sourcing", f'''
<div class="grid fill split" style="grid-template-columns:1fr 1.15fr;gap:4cqw">
  <div class="hd" style="gap:1.3cqw">
    <span class="eyebrow">Service / Brand Building</span>
    <h2 style="font-size:clamp(19px,2.5cqw,32px)">From an idea to a product ready to sell</h2>
    <div class="hd" style="gap:0">
     {"".join(f'<div class="row" style="flex-wrap:nowrap;gap:1.2cqw;align-items:stretch"><div style="display:flex;flex-direction:column;align-items:center"><span class="mono" style="width:2.2em;height:2.2em;border-radius:50%;display:grid;place-items:center;background:var(--sea);color:var(--marigold);font-weight:600;flex:none">{n+1}</span>{CONN if n<3 else ""}</div><div style="padding-bottom:1.1cqw"><h3>{t}</h3><p class="small mute">{d}</p></div></div>' for n,(t,d) in enumerate(bsteps))}
    </div>
    <div class="row" style="gap:.5cqw">{"".join(f'<span class="chip">{c}</span>' for c in ["Apparel","Drinkware","Packaging","Private label","Merchandise","Electronics","Home goods"])}</div>
  </div>
  <div class="hd" style="gap:1.3cqw">
    <span class="eyebrow">Service / Global Sourcing</span>
    <h2 style="font-size:clamp(19px,2.5cqw,32px)">Know what you need, but not where to get it?</h2>
    <div class="grid g2 m-grid2">
      {"".join(f'<div class="card" style="gap:.4cqw"><span class="row" style="gap:.5em;align-items:center;flex-wrap:nowrap;color:var(--sea3)">{ic("pin")}<h3 style="color:var(--ink)">{r}</h3></span><p class="small mute">{c}</p></div>' for r,c in regions)}
    </div>
    <p class="small mute m-hide">Other regions on request.</p>
    <div class="grid g4 m-grid2" style="gap:1cqw">
      {"".join(f'<div class="hd" style="gap:.4cqw;align-items:flex-start">{icb(i)}<span class="small">{t}</span></div>' for i,t in [("factory","Factory discovery and vetting"),("rupee","Price negotiation for you"),("eye","Pre-shipment inspection"),("ship","Door delivery, duties handled")])}
    </div>
  </div>
</div>''')

# ---------------- 10 CORPORATE ----------------
corp = [
 ("gift","Corporate gifting",["Employee welcome kits","Diwali and festive hampers","Client appreciation gifts","Work anniversary boxes","Event giveaways"]),
 ("box","Office supplies",["Stationery and pantry items","Hygiene and facility products","Packaging material","IT accessories","Monthly scheduled delivery"]),
 ("tag","Branded merchandise",["Apparel and caps","Bags and backpacks","Drinkware","Tech accessories","Eco and sustainable items"]),
]
cproc = [("Share your brief","Product, quantity, budget, date"),("Proposal in 48 h","Options, pricing, branding, delivery"),("Approve and brand","Your logo, colours, packaging"),("Delivered","To your office, staff or clients")]
slide("paper", "Corporate Solutions", f'''
<div class="hd"><span class="eyebrow">Service / Corporate Solutions</span><h2>Your brand on every product, delivered across India</h2></div>
<div class="grid g3 m-swipe">
 {"".join(f'<div class="card"><div class="row" style="align-items:center;flex-wrap:nowrap;gap:1cqw">{icb(i)}<h3>{t}</h3></div><ul class="ticks small">{"".join(f"<li>{x}</li>" for x in items)}</ul></div>' for i,t,items in corp)}
</div>
<div class="grid g4 m-grid2" style="gap:1.2cqw">
 {"".join(f'<div class="hd" style="gap:.2cqw;border-top:2px solid var(--sea);padding-top:.8cqw"><span class="mono small" style="color:var(--rust);font-weight:600">0{n+1}</span><h3 style="font-size:var(--b)">{t}</h3><p class="small mute">{d}</p></div>' for n,(t,d) in enumerate(cproc))}
</div>
<div class="row" style="gap:.6cqw">
 <span class="chip gold">From 50 units</span><span class="chip gold">Consultant call in 4 to 6 hours</span><span class="chip gold">100% custom branded</span><span class="chip gold">Quality checked before dispatch</span><span class="chip gold">Pan-India delivery</span>
</div>''')

# ---------------- 11 READY STOCK ----------------
cats = [("Handbags","Totes, clutches, crossbody",71),("Footwear","Heels, flats, mules, boots",28),("Eyewear","Sunglasses and optical",18),("Home and utility","Decor, organisers, gadgets",12),("Furnishing studio","Premium furniture",7)]
BX0, BX1, BM = 200, 500, 71
rows = ""
for n,(c,sub,v) in enumerate(cats):
    y = 34 + n*50
    w = (BX1-BX0)*v/BM
    rows += f'<text x="0" y="{y+12}" font-size="15" font-weight="600" fill="#132A30">{c}</text><text x="0" y="{y+29}" font-size="11.5" fill="#566C70">{sub}</text>'
    rows += f'<rect x="{BX0}" y="{y}" width="{w:.1f}" height="24" rx="4" fill="{"#E9A23B" if n==0 else "#22646F"}"/>'
    rows += f'<text x="{BX0+w+8:.1f}" y="{y+17}" font-size="14" font-weight="600" fill="#132A30">{v}</text>'
cat_chart = f'''<svg class="chart" viewBox="0 0 560 300" role="img" aria-label="Styles per catalogue: handbags 71, footwear 28, eyewear 18, home and utility 12, furnishing studio 7">
<text x="0" y="14" font-size="12" fill="#566C70" class="mono">STYLES IN EACH WHOLESALE CATALOGUE</text>
<line x1="{BX0}" y1="28" x2="{BX0}" y2="282" stroke="#132A30" stroke-width="1.5"/>
{rows}
</svg>'''
slide("", "Ready Stock Store", f'''
<div class="grid fill split" style="grid-template-columns:.85fr 1.15fr;gap:4cqw;align-items:center">
  <div class="hd" style="gap:1.4cqw">
    <span class="eyebrow">Service / Ready Stock Store</span>
    <h2>Ready stock, already imported and checked</h2>
    <p class="lead">Browse products we have already sourced and have ready to sell. Order in bulk, or just browse for ideas.</p>
    <div class="row" style="gap:3cqw">
      <div><b class="num">136</b><p class="small mute">Styles across five catalogues</p></div>
      <div><b class="num">25</b><p class="small mute">Units minimum per bulk order</p></div>
    </div>
    <p class="mono small">catalogue.ameckhouse.com</p>
  </div>
  <div class="card" style="padding:1.8cqw 2cqw">{cat_chart}</div>
</div>
<p class="small mute">Catalogue counts as of October 2026. New products are added regularly on ameckhouse.com.</p>''')

# ---------------- 12 PROTECTION TIMELINE ----------------
tl = [
 ("money","1","Product paid upfront","100% of the product cost upfront, through RBI-regulated Cashfree. We never work on credit."),
 ("","2","Supplier verified","Registration, export history, capacity and bank details checked before we buy"),
 ("","3","Sample approved","Your sign-off before any bulk production"),
 ("","4","Mid-production check","Bulk compared with your approved sample"),
 ("","5","Pre-shipment check","Problems fixed at the factory, before shipping"),
 ("ship","6","Insured in transit","Cargo insured and tracked, every document cross-checked"),
 ("money","7","Landed and delivered","Customs in 2 to 3 working days. You pay the actual shipping cost, then we deliver."),
]
slide("dark", "How we protect you", f'''
<div class="hd"><span class="eyebrow">How we protect you</span><h2>Your money and your goods are protected at every stage</h2></div>
<div class="fill" style="display:flex;align-items:center"><div class="tl m-swipe" style="width:100%">
 {"".join(f'<div class="st {c}"><span class="dot">{n}</span><h3>{t}</h3><p>{d}</p></div>' for c,n,t,d in tl)}
</div></div>
<div class="grid g3" style="align-items:stretch">
  <div class="callout" style="flex-direction:column;align-items:flex-start;gap:.2cqw"><b class="num" style="font-size:var(--stat)">&lt;2%</b><span class="small mute">Dispute rate across our orders</span></div>
  <div class="card s-span2" style="justify-content:center;gap:.8cqw"><p><b>You pay for the product upfront. We carry the risk.</b> What arrives matches your quote, and any shortfall is fixed by us. If we cannot deliver for a reason within our control, you get a full refund.</p>
  <div class="row small mute" style="gap:2cqw"><span class="row" style="gap:.4em;align-items:center"><i style="width:.8em;height:.8em;border-radius:50%;background:var(--marigold);display:inline-block"></i>Payment</span><span class="row" style="gap:.4em;align-items:center"><i style="width:.8em;height:.8em;border-radius:50%;background:var(--mint);display:inline-block"></i>Quality check</span><span class="row" style="gap:.4em;align-items:center"><i style="width:.8em;height:.8em;border-radius:50%;background:var(--on-sea);display:inline-block"></i>Shipping</span></div></div>
</div>''')

# ---------------- 13 RISKS TABLE ----------------
risks = [
 ("users","Fake or unreliable supplier","Due diligence before any deal: registration, export history, capacity and banking details"),
 ("rupee","Paying for goods that never come","You pay Ameck, not an unknown supplier. Full refund if we cannot deliver for a reason within our control"),
 ("eye","Bulk order not matching the sample","Sample approval, then mid-production and pre-shipment inspections against it"),
 ("doc","Customs hold over paperwork","Invoice, packing list, Bill of Entry and certificate of origin cross-checked before filing"),
 ("stamp","Wrong duty or classification","Correct HSN code for every product, with duty and IGST worked out upfront"),
 ("shield","Damage or loss in transit","Cargo insurance and tracking on every shipment"),
 ("layers","Missing product licences","FSSAI for food, BIS for electronics, CDSCO for cosmetics and medical products"),
 ("clock","Missed delivery dates","One accountable contact who owns your date and updates you first"),
]
slide("", "How we protect you", f'''
<div class="hd"><span class="eyebrow">How we protect you</span><h2>Eight common import risks, and how we prevent each one</h2></div>
<div class="tablewrap fill"><table class="t mcards">
<thead><tr><th style="width:38%">The risk</th><th>How we prevent it</th></tr></thead>
<tbody>{"".join(f'<tr><td><span class="cell"><span style="color:var(--rust)">{ic(i)}</span>{r}</span></td><td data-l="How we prevent it">{s}</td></tr>' for i,r,s in risks)}</tbody>
</table></div>
<div class="callout">{ic("check")} You never deal with customs authorities or prepare a customs document yourself.</div>''')

# ---------------- COMPLIANCE ----------------
comps = [
 ("cup","Food and ingredients","FSSAI","FSSAI importer licence and Food Import Clearance System"),
 ("phone","Electronics","BIS","BIS certification and quality control orders"),
 ("sparkle","Cosmetics","CDSCO","Drugs and Cosmetics Act, CDSCO registration where needed"),
 ("shield","Medical and pharma","CDSCO","CDSCO registration for devices and pharmaceuticals"),
 ("gear","Capital goods","EPCG","Support with the EPCG duty-saving scheme for machinery"),
 ("box","Raw materials","AA","Support with Advance Authorisation for production inputs"),
]
ledger = ["HSN classification","Basic Customs Duty","Social Welfare Surcharge","IGST","Bill of Entry on ICEGATE","Commercial invoice and packing list","Certificate of origin","Customs KYC"]
slide("", "Licences and compliance", f"""
<div class="hd"><span class="eyebrow">Licences and compliance</span><h2>Every licence and filing, handled under our IEC</h2></div>
<div class="grid g3 fill m-swipe" style="grid-auto-rows:1fr">
 {"".join(f'<div class="stamp"><span class="code">{c}</span>{icb(i)}<h3 style="font-size:var(--b)">{t}</h3><p class="small mute">{d}</p></div>' for i,t,c,d in comps)}
</div>
<div class="ledger"><span class="mono small mute" style="margin-right:.6cqw">ON EVERY SHIPMENT</span>{"".join(f'<span class="chip">{l}</span>' for l in ledger)}</div>""")

# ---------------- 14 WHAT YOU PAY ----------------
_slabs=[("Factory price","Paid upfront, at our negotiated price",0,92,TEAL),("Shipping, duty included","Door to door, per CBM by sea or per kg by air",128,34,MINT),("GST","As applicable, shown on your invoice",200,40,GOLD)]
_tw='<div class="ground" style="border-radius:24px"></div>'
for nm,ds,z,h,col in _slabs:
    _tw+=box(30,30,170,170,h,col,z=z,inner=bb(f'<div class="lbl3d"><b>{nm}</b><span>{ds}</span></div>',left="100%",top="100%",lift=-h//2,cls="r",lw=250))
_tw+=bb('<span class="tag3d" style="background:var(--sea);color:var(--marigold);font-size:14px;padding:7px 12px">= Your landed cost</span>',left="115px",top="115px",lift=300)
_twm='<div class="ground" style="border-radius:24px"></div>'
for nm,ds,z,h,col in _slabs:
    _twm+=box(30,30,170,170,h,col,z=z)
_twm+=bb('<span class="tag3d" style="background:var(--sea);color:var(--marigold);font-size:14px;padding:7px 12px">= Your landed cost</span>',left="115px",top="115px",lift=300)
tower_m=scene(340,430,_twm,230,230,55,190,58,-42,persp=1900,label="A 3D stack of factory price, duty and GST, and freight")
legend_m='<div class="hd" style="gap:8px">'+"".join(f'<div class="row" style="flex-wrap:nowrap;gap:10px;align-items:center"><i style="flex:none;width:14px;height:14px;border-radius:4px;background:{col[0]}"></i><span><b>{nm}</b> <span class="mute small">{ds}</span></span></div>' for nm,ds,z,h,col in reversed(_slabs))+'</div>'
tower=scene(560,470,_tw,230,230,40,215,58,-42,persp=1900,label="A 3D stack: factory price at the base, shipping with duty included in the middle, GST on top, together making your landed cost")
slide("paper", "What you pay", f'''
<div class="hd"><span class="eyebrow">What you pay</span><h2 style="max-width:none">The factory price and the real freight. Nothing hidden.</h2></div>
<div class="grid fill split" style="grid-template-columns:1.05fr .95fr;gap:2.4cqw;align-items:center">
  <div><div class="d-only">{tower}</div><div class="m-only">{tower_m}{legend_m}</div></div>
  <div class="hd" style="gap:1.3cqw">
    <span class="eyebrow" style="color:var(--mute)">What you never pay us for</span>
    <div class="grid g2" style="gap:1cqw">
      {"".join(f'<div class="row" style="flex-wrap:nowrap;gap:.7em;align-items:center;padding:.9cqw 1.1cqw;border:1px dashed var(--rust);border-radius:8px"><span class="x">{ic("x")}</span><span class="strike">{t}</span></div>' for t in ["Sourcing commission","Subscription fees","Forex markup","Agent cuts or hidden margins"])}
    </div>
    <div class="card" style="background:var(--sea);color:var(--on-sea);border-color:var(--sea)"><b class="num" style="font-size:var(--stat)">30 to 45%</b><p>Typical saving on product cost against Indian wholesale, because we buy factory-direct and combine orders across customers.</p></div>
    <p class="small mute">China imports follow this model. Brand building, corporate orders and export work are quoted individually in a written proposal.</p>
  </div>
</div>''')

# ---------------- 15 TIMELINES ----------------
HX0, HX1 = 200, 520
hx = lambda h: HX0 + (HX1-HX0)*h/48
resp = [("Work starts after payment",4),("Logistics quote",4),("Corporate call back",6),("General enquiry reply",24),("Sourcing quote or proposal",48)]
r_rows = ""
for n,(l,h) in enumerate(resp):
    y = 40 + n*46
    r_rows += f'<text x="0" y="{y+16}" font-size="14" fill="#132A30">{l}</text><rect x="{HX0}" y="{y}" width="{hx(h)-HX0:.1f}" height="22" rx="4" fill="#E9A23B"/>'
    lab = "4 to 6 h" if h==6 else f"{h} h"
    tx = hx(h)+8
    anchor = "start"
    if h == 48:
        tx, anchor = hx(h)-8, "end"
    col = "#132A30"
    r_rows += f'<text x="{tx:.1f}" y="{y+16}" font-size="13" font-weight="600" text-anchor="{anchor}" fill="{col}">within {lab}</text>'
r_ticks = "".join(f'<line x1="{hx(t):.1f}" y1="30" x2="{hx(t):.1f}" y2="270" stroke="#C9D5D3"/><text x="{hx(t):.1f}" y="290" text-anchor="middle" font-size="12" fill="#566C70">{t}</text>' for t in (0,12,24,36,48))
resp_chart = f'''<svg class="chart wide" viewBox="0 0 540 310" role="img" aria-label="Response times in hours">
<text x="0" y="14" font-size="12" fill="#566C70" class="mono">HOW FAST WE RESPOND (HOURS)</text>{r_ticks}<line x1="{HX0}" y1="270" x2="{HX1}" y2="270" stroke="#132A30" stroke-width="1.5"/>{r_rows}</svg>'''
DX0, DX1 = 200, 520
dx = lambda d: DX0 + (DX1-DX0)*d/45
trans = [("Customs clearance",2,3,"#9FD3C5"),("Air freight",7,12,"#E9A23B"),("Sea freight",25,45,"#17505C")]
t_rows = ""
for n,(l,a,b,c) in enumerate(trans):
    y = 60 + n*70
    w = max(dx(b)-dx(a), 7)
    t_rows += f'<text x="0" y="{y+16}" font-size="14" fill="#132A30">{l}</text><rect x="{dx(a):.1f}" y="{y}" width="{w:.1f}" height="22" rx="4" fill="{c}"/>'
    if b == 45:
        t_rows += f'<text x="{dx(a)-8:.1f}" y="{y+16}" text-anchor="end" font-size="13" font-weight="600" fill="#132A30">{a} to {b} days</text>'
    else:
        t_rows += f'<text x="{dx(a)+w+8:.1f}" y="{y+16}" font-size="13" font-weight="600" fill="#132A30">{a} to {b} days</text>'
t_ticks = "".join(f'<line x1="{dx(t):.1f}" y1="30" x2="{dx(t):.1f}" y2="270" stroke="#C9D5D3"/><text x="{dx(t):.1f}" y="290" text-anchor="middle" font-size="12" fill="#566C70">{t}</text>' for t in (0,10,20,30,40))
trans_chart = f'''<svg class="chart wide" viewBox="0 0 540 310" role="img" aria-label="Transit and clearance in working days">
<text x="0" y="14" font-size="12" fill="#566C70" class="mono">TRANSIT AND CLEARANCE (WORKING DAYS)</text>{t_ticks}<line x1="{DX0}" y1="270" x2="{DX1}" y2="270" stroke="#132A30" stroke-width="1.5"/>{t_rows}</svg>'''
slide("", "Timelines", f'''
<div class="hd"><span class="eyebrow">Timelines at a glance</span><h2>How fast things move</h2></div>
<div class="grid g2 fill" style="gap:2cqw">
  <div class="card" style="padding:1.6cqw 1.8cqw;justify-content:center"><div class="m-hide">{resp_chart}</div>{mlist("How fast we respond", [(l, "within 4 to 6 h" if h==6 else f"within {h} h") for l,h in resp])}</div>
  <div class="card" style="padding:1.6cqw 1.8cqw;justify-content:center"><div class="m-hide">{trans_chart}</div>{mlist("Transit and clearance", [(l, f"{a} to {b} working days") for l,a,b,c in trans])}</div>
</div>
<p class="small mute">Freight times are door to door. Exact timelines depend on your product, supplier and destination, and your quote states the agreed timeline before you pay.</p>''')

# ---------------- 16 INDUSTRIES ----------------
inds = [
 ("store","Retail, boutiques and D2C","Unique products you will not find in local wholesale"),
 ("cup","Cafes, restaurants and hotels","Specialty coffee gear, kitchen equipment, tableware, ingredients"),
 ("home","Home decor and lifestyle","Japanese homeware, Scandinavian decor, Italian ceramics, glassware"),
 ("sparkle","Beauty and wellness","International formulations and packaging, compliance handled"),
 ("book","Education","Montessori materials, STEM kits, sensory tools, lab supplies"),
 ("palette","Artisans and craft","Specialist raw materials, dyes, pigments, tools and fittings"),
 ("gear","Manufacturing and B2B","Raw materials, components, machinery inputs, pro equipment"),
 ("leaf","Fast-growing categories","Fitness equipment, premium pet products, eco goods"),
]
slide("paper", "Who we work with", f'''
<div class="hd"><span class="eyebrow">Who we work with</span><h2>From a single cafe to a manufacturing unit</h2>
<p class="mute" style="max-width:70ch">Entrepreneurs and startups, retailers and growing brands, established businesses, manufacturers seeking new markets, and importers who want their sourcing managed.</p></div>
<div class="grid g4 fill m-swipe" style="grid-auto-rows:1fr">
 {"".join(f'<div class="card">{icb(i)}<h3 style="font-size:var(--b)">{t}</h3><p class="small mute">{d}</p></div>' for i,t,d in inds)}
</div>''')

# ---------------- 17 STORIES ----------------
STORY_BACK = {
 "Specialty cafe, Jaipur": ("Four months stuck trying to import Japanese pour-over equipment alone.","Confirmed the HSN code and landed cost, checked the maker, filed on ICEGATE and delivered.","Delivered in six weeks. Three repeat orders since."),
 "Home decor retailer, Mumbai": ("800 units arrived with weak stitching, wrong colour and wrong sizes.","Mid-production and pre-shipment inspections against the approved sample, on every order.","A material swap caught halfway through the next order. No faulty shipment since."),
 "Manufacturing unit, Surat": ("Lost Rs. 4.2 lakh to a supplier found online who then disappeared.","Full factory checks, verified bank details and a written contract before any order.","Four orders on time and to specification. Nothing lost."),
 "Lifestyle brand, Chennai": ("Paying about 1.8 times factory price through a trading company.","Sourced direct from the same kind of factory, with a clear, fixed fee.","Landed cost 38% lower, margin up 14 points, two new categories funded."),
 "Gift store, Bangalore": ("Selling the same products as every shop on the street.","Found Nordic ceramics 18 months before Indian wholesale and imported them end to end.","The only stockist in the city, with prices nobody could compare."),
 "D2C brand, Delhi": ("A shipment held three weeks at Nhava Sheva over a packing list mismatch. Peak season missed.","Every document cross-checked against the others before filing on ICEGATE.","The last four shipments cleared within two working days."),
 "Boutique, Mumbai": ("A launch event collapsed when promised goods never arrived.","One accountable contact owning the delivery date, with updates before being asked.","Two launches since, both delivered ahead of the date."),
 "Ceramics artist, Pune": ("Could not meet Italian factory minimums alone, and one shipment was lost.","Found two verified makers, tested samples and pooled orders with other buyers.","Four on-time quarterly deliveries and two referrals."),
 "First-time importer, Hyderabad": ("Six months unsure what to sell, with capital ready.","Niche research matched to their budget, city and customers.","Opened with a range nobody else had. Reordered within three months."),
 "Kitchenware retailer, Kochi": ("Losing ground to a newer rival for three years.","Mapped what drove the rival, then sourced two categories nobody owned yet.","Growing again within eight months."),
}
def story_flip(m,w,d,sp):
    pr,did,res=STORY_BACK[w]
    rows="".join(f'<div class="sb"><b>{a}</b><span>{b}</span></div>' for a,b in (("The problem",pr),("What we did",did),("The result",res)))
    return (f'<div class="flip {sp}" tabindex="0" role="button" aria-pressed="false" aria-label="{w}: show the full story"><div class="flip-in">'
            f'<div class="card story face front"><b class="m">{m}</b><span class="where">{w}</span><p>{d}</p><span class="flip-hint">Tap for the full story {ic("arrow")}</span></div>'
            f'<div class="card face back" style="background:var(--paper);color:var(--ink);border-color:var(--paper);gap:.8cqw">{rows}</div></div></div>')

stories = [
 ("6 weeks","Specialty cafe, Jaipur","From first call to delivered Japanese pour-over equipment, after four months stuck trying alone. Three repeat orders since.","s-span2"),
 ("Caught early","Home decor retailer, Mumbai","An 800-unit order once arrived unlike the sample. Our mid-production check caught the next order's material swap at the factory.","s-span2"),
 ("Rs. 0 lost","Manufacturing unit, Surat","After losing Rs. 4.2 lakh to an online supplier, four orders through us arrived on time and to specification.","s-span2"),
 ("38% lower","Lifestyle brand, Chennai","Total landed cost after replacing a trading company that charged about 1.8 times factory price. Gross margin up 14 points.","s-span3"),
 ("Only stockist","Gift store, Bangalore","Nordic ceramic homeware sourced about 18 months before it reached Indian wholesale. The store became the city's only stockist.","s-span3"),
]
slide("dark", "Customer stories", f'''
<div class="hd"><span class="eyebrow">Customer stories</span><h2>Real problems we have solved</h2></div>
<div class="grid g6 fill m-swipe" style="grid-auto-rows:1fr">
 {"".join(story_flip(m,w,d,sp) for m,w,d,sp in stories)}
</div>''')


# ---------------- STORIES 2 ----------------
stories2 = [
 ("2 days","D2C brand, Delhi","A shipment once sat at Nhava Sheva for three weeks over a paperwork mismatch. Their last four Ameck shipments cleared within two working days.","s-span2"),
 ("Ahead of date","Boutique, Mumbai","A launch event once collapsed when goods never came. Two launches since were timed to our delivery dates, and both arrived early.","s-span2"),
 ("4 quarters","Ceramics artist, Pune","Italian pigments she could not buy alone. We pooled orders to meet factory minimums: four on-time quarterly deliveries and two referrals.","s-span2"),
 ("3 months","First-time importer, Hyderabad","Six months stuck on what to sell. Our niche research found an underserved category, and the second order came within three months of opening.","s-span3"),
 ("8 months","Kitchenware retailer, Kochi","A decade-old store losing to a newer rival. We mapped what drove the rival and sourced two new categories. Growth returned within eight months.","s-span3"),
]
slide("dark", "Customer stories", f"""
<div class="hd"><span class="eyebrow">Customer stories, continued</span><h2>Five more problems we have solved</h2></div>
<div class="grid g6 fill m-swipe" style="grid-auto-rows:1fr">
 {"".join(story_flip(m,w,d,sp) for m,w,d,sp in stories2)}
</div>""")

# ---------------- TWO JOURNEYS ----------------
ALONE = ['Search online directories and hope the supplier is real', 'Pay a supplier you have never met', 'Approve a sample and hope the bulk matches', 'Work out HSN codes, customs duty and IGST', 'Prepare the Bill of Entry, licences and every document', 'Chase freight forwarders, the port and customs', 'Handle customs queries, holds and demurrage', 'Absorb any fraud, defect, delay or penalty yourself']
US = [('Send one message', 'What you need, how many, your budget and date'), ('Approve the sample', 'Your one decision before bulk production'), ('Receive your goods', 'Inspected, insured, cleared and at your door')]
slide("paper", "Ameck vs doing it yourself", f'''
<div class="hd"><span class="eyebrow">Ameck vs doing it yourself</span><h2>Import on your own, or hand it to us</h2></div>
<div class="grid fill split m-swipe" style="grid-template-columns:1.15fr .85fr;gap:2cqw">
  <div class="path alone">
    <div class="row m-stack" style="justify-content:space-between;align-items:flex-end;flex-wrap:nowrap;gap:1cqw">
      <span class="chip rust">On your own: 8 jobs, all yours</span>
      <div style="text-align:right"><b class="bigt" style="color:var(--rust);font-size:clamp(22px,3cqw,38px)">60 to 120 h</b><p class="small mute">of your time per shipment, over 3 to 5 months</p></div>
    </div>
    <ol>{"".join(f'<li><span class="n">{n+1}</span><span>{t}</span></li>' for n,t in enumerate(ALONE))}</ol>
  </div>
  <div class="path us">
    <div class="row m-stack" style="justify-content:space-between;align-items:flex-end;flex-wrap:nowrap;gap:1cqw">
      <span class="chip gold">With Ameck: 3 steps</span>
      <div style="text-align:right"><b class="bigt" style="color:var(--marigold);font-size:clamp(22px,3cqw,38px)">A few hours</b><p class="small" style="color:var(--on-sea-mute)">of your time, in total</p></div>
    </div>
    <ol>{"".join(f'<li><span class="n">{n+1}</span><span><b>{t}</b><br><span class="small" style="color:var(--on-sea-mute)">{d}</span></span></li>' for n,(t,d) in enumerate(US))}</ol>
    <div class="rule" style="margin-top:auto"></div>
    <p class="small">Suppliers, inspections, IEC, customs, freight and the risk all sit with us. You stay focused on selling.</p>
  </div>
</div>''')
# ---------------- 18 DIY ----------------
diy = [
 ("Finding a supplier","Online directories with no way to check them","A verified network, with due diligence on every supplier"),
 ("What to import","What is already sold locally, and already crowded","Trends spotted 12 to 24 months before the Indian mainstream"),
 ("Price","Whatever the supplier quotes","Factory-direct, typically 30 to 45% below wholesale"),
 ("Quality","Approve a sample and hope the bulk matches","Mid-production and pre-shipment inspection on every order"),
 ("Customs and paperwork","IEC, HSN, Bill of Entry, IGST, BIS, FSSAI. One error can cost weeks.","100% handled by us, under our own IEC"),
 ("Your time","60 to 120 hours per shipment, over 3 to 5 months","A few hours in total"),
 ("Risk","Fraud, quality failure and penalties fall on you","Managed through supplier checks, inspections and insurance"),
]
slide("", "Ameck vs doing it yourself", f'''
<div class="hd"><span class="eyebrow">Ameck vs doing it yourself</span><h2>The same import, two very different experiences</h2></div>
<div class="tablewrap fill"><table class="t vs mcards">
<thead><tr><th style="width:18%"></th><th class="diy" style="width:41%">On your own</th><th class="ame">With Ameck</th></tr></thead>
<tbody>{"".join(f'<tr><td>{a}</td><td class="diy" data-l="On your own"><span class="cell"><span class="x">{ic("x")}</span><span>{d}</span></span></td><td class="ame" data-l="With Ameck"><span class="cell"><span class="ok">{ic("check")}</span>{w}</span></td></tr>' for a,d,w in diy)}</tbody>
</table></div>
<div class="callout">{ic("chat")} Not sure which route suits you? Tell us what you want to import. We will give you an honest landed cost estimate.</div>''')


# ---------------- COST EXAMPLE ----------------
CX0, CK = 250, 1.12   # x origin, px per Rs. thousand (500k -> 560px)
cx = lambda k: CX0 + CK*k
crow = [
 ("Product cost", (500,500,"Rs. 5,00,000"), (325,350,"Rs. 3,25,000 to 3,50,000")),
 ("Freight", (40,60,"Rs. 40,000 to 60,000"), (35,50,"Rs. 35,000 to 50,000")),
 ("Customs agent and handling", (8,15,"Rs. 8,000 to 15,000"), None),
]
cbars = ""
for n,(lab,d,a) in enumerate(crow):
    y = 58 + n*92
    cbars += f'<text x="0" y="{y+26}" font-size="15" font-weight="600" fill="#132A30">{lab}</text>'
    lo,hi,t = d
    cbars += f'<rect x="{CX0}" y="{y}" width="{CK*lo:.1f}" height="22" rx="3" fill="#C4542A"/>'
    if hi>lo: cbars += f'<rect x="{cx(lo):.1f}" y="{y}" width="{CK*(hi-lo):.1f}" height="22" rx="3" fill="#C4542A" opacity=".4"/>'
    tx = cx(hi)+10
    if hi == 500: cbars += f'<text x="{cx(hi)-10:.1f}" y="{y+16}" text-anchor="end" font-size="13" font-weight="600" fill="#FBFCFB">{t}</text>'
    else: cbars += f'<text x="{tx:.1f}" y="{y+16}" font-size="13" fill="#132A30">{t}</text>'
    y2 = y+30
    if a:
        lo,hi,t = a
        cbars += f'<rect x="{CX0}" y="{y2}" width="{CK*lo:.1f}" height="22" rx="3" fill="#17505C"/>'
        cbars += f'<rect x="{cx(lo):.1f}" y="{y2}" width="{CK*(hi-lo):.1f}" height="22" rx="3" fill="#17505C" opacity=".4"/>'
        cbars += f'<text x="{cx(hi)+10:.1f}" y="{y2+16}" font-size="13" font-weight="600" fill="#132A30">{t}</text>'
    else:
        cbars += f'<text x="{CX0+6}" y="{y2+16}" font-size="13" font-weight="600" fill="#17505C">Included in our service</text>'
cticks = "".join(f'<line x1="{cx(k):.1f}" y1="44" x2="{cx(k):.1f}" y2="318" stroke="#C9D5D3"/><text x="{cx(k):.1f}" y="338" text-anchor="middle" font-size="12" fill="#566C70">{lab}</text>' for k,lab in [(0,"0"),(100,"1 L"),(200,"2 L"),(300,"3 L"),(400,"4 L"),(500,"5 L")])
cost_chart = f'''<svg class="chart wide" viewBox="0 0 840 350" role="img" aria-label="Rs. 5 lakh order: product cost Rs. 5,00,000 on your own vs Rs. 3,25,000 to 3,50,000 with Ameck">
<text x="0" y="16" font-size="12" fill="#566C70" class="mono">COST OF A RS. 5 LAKH FACTORY-PRICE ORDER (RS., L = LAKH)</text>
<g class="mono" font-size="12" fill="#566C70"><rect x="560" y="5" width="14" height="14" rx="2" fill="#C4542A"/><text x="580" y="16">ON YOUR OWN</text><rect x="690" y="5" width="14" height="14" rx="2" fill="#17505C"/><text x="710" y="16">WITH AMECK</text></g>
{cticks}<line x1="{CX0}" y1="318" x2="{cx(500)}" y2="318" stroke="#132A30" stroke-width="1.5"/>
<line x1="{CX0}" y1="44" x2="{CX0}" y2="318" stroke="#132A30" stroke-width="1.5"/>
{cbars}</svg>'''
slide("", "Ameck vs doing it yourself", f'''
<div class="hd"><span class="eyebrow">Ameck vs doing it yourself</span><h2>What a Rs. 5 lakh order really costs</h2></div>
<div class="grid fill split" style="grid-template-columns:1.5fr .7fr;gap:2cqw">
  <div class="card" style="padding:1.6cqw 1.8cqw;justify-content:center"><div class="m-hide">{cost_chart}</div>{mlist("A Rs. 5 lakh order", [(lab, d[2], ("With Ameck: " + a[2]) if a else "With Ameck: included in our service") for lab,d,a in crow])}</div>
  <div class="hd m-swipe" style="gap:1.2cqw">
    <div class="card" style="background:var(--sea);color:var(--on-sea);border-color:var(--sea);gap:.5cqw"><b class="bigt" style="color:var(--marigold)">Rs. 1.5 to 1.75 lakh</b><p class="small">saved on product cost alone, about 30 to 35% lower, because we buy factory-direct and combine orders</p></div>
    <div class="card" style="gap:.4cqw"><h3 style="font-size:var(--b)">Lower duty too</h3><p class="small mute">Customs duty and IGST are charged on the product cost, so a lower price means lower duty.</p></div>
    <div class="card" style="gap:.4cqw"><h3 style="font-size:var(--b)">And your time back</h3><p class="small mute">60 to 120 hours on your own, against a few hours with us.</p></div>
  </div>
</div>
<p class="small mute">Illustrative example from the Ameck guide to importing on your own. Your quote gives the exact figures for your order. Lighter bar ends show the range.</p>''')
# ---------------- SAVINGS ESTIMATOR ----------------
slide("paper", "Estimate your saving", f'''
<div class="hd"><span class="eyebrow">Estimate your saving</span><h2 style="max-width:none">See what factory-direct pricing could save you</h2></div>
<div class="grid fill split calc" id="calc" style="grid-template-columns:.92fr 1.08fr;gap:2.2cqw;align-items:stretch">
  <div class="card" style="gap:1.6cqw;justify-content:center;padding:1.8cqw 2cqw">
    <div class="hd" style="gap:.7cqw">
      <label for="cv"><span>Your typical order value today</span><output id="cv-o" for="cv">Rs. 5,00,000</output></label>
      <input type="range" id="cv" min="50000" max="5000000" step="10000" value="500000" style="--p:9.09%" aria-describedby="cv-h">
      <div class="presets">{"".join(f'<button type="button" data-v="{v}" aria-pressed="{str(v==500000).lower()}" class="{"on" if v==500000 else ""}">{l}</button>' for v,l in [(100000,"Rs. 1 lakh"),(500000,"Rs. 5 lakh"),(1000000,"Rs. 10 lakh"),(2500000,"Rs. 25 lakh")])}</div>
      <p class="small mute" id="cv-h">What you pay a wholesaler or trader for one order, before freight and tax.</p>
    </div>
    <div class="hd" style="gap:.7cqw">
      <label for="cn"><span>Orders per year</span><output id="cn-o" for="cn">4 orders</output></label>
      <input type="range" id="cn" min="1" max="24" step="1" value="4" style="--p:13.04%">
    </div>
  </div>
  <div class="card" style="background:var(--sea);color:var(--on-sea);border-color:var(--sea);gap:1.1cqw;justify-content:center;padding:1.8cqw 2cqw">
    <span class="eyebrow">Estimated saving on product price, a year</span>
    <b class="calc-big" id="o-year" aria-live="polite">Rs. 6,00,000 to Rs. 9,00,000</b>
    <div class="ratio" aria-hidden="true">
      <div class="rb"><span>Wholesale today</span><div class="track"><i style="width:100%;background:var(--rust)"></i></div></div>
      <div class="rb"><span>With Ameck</span><div class="track"><i style="width:70%;background:var(--marigold);opacity:.45"></i><i style="width:55%;background:var(--marigold)"></i></div></div>
    </div>
    <div class="grid g3" style="gap:1.2cqw">
      <div class="kv"><span>Saved per order</span><b id="o-order">Rs. 1,50,000 to Rs. 2,25,000</b></div>
      <div class="kv"><span>Product price with Ameck</span><b id="o-cost">Rs. 2,75,000 to Rs. 3,50,000</b></div>
      <div class="kv"><span>Hours back a year</span><b id="o-hours">240 to 480</b></div>
    </div>
    <p class="small" style="color:var(--on-sea-mute)"><b style="color:var(--on-sea)">Working:</b> <span id="o-work">Rs. 5,00,000 × 30% = Rs. 1,50,000 and Rs. 5,00,000 × 45% = Rs. 2,25,000 saved per order on product price. Over 4 orders: Rs. 1,50,000 × 4 = Rs. 6,00,000 and Rs. 2,25,000 × 4 = Rs. 9,00,000.</span></p>
  </div>
</div>
<p class="small mute">An illustrative estimate. We buy premium goods direct from the factory and cut out the middlemen, which typically lowers the product price by 30 to 45% against Indian wholesale. Shipping is not included: it is charged by weight or volume, door to door, with customs duty included for most products. Time saved assumes 60 to 120 hours for each self-managed shipment. Your quote gives the exact figures.</p>''')

# ---------------- GROW WITH US ----------------
stairs = [
 ("1","First order","One product, one shipment, from 25 units and 20 kg",34),
 ("2","Repeat orders","The same verified factory, faster quotes, better prices",52),
 ("3","Recurring supply","Scheduled monthly or quarterly deliveries, pooled with other buyers",70),
 ("4","Your own brand","Private label, packaging and new markets, India and abroad",88),
]
_SD=190
_st='<div class="ground"></div>'
for k,(n,t,d,h) in enumerate(stairs):
    _st+=box(_CX[k]-95,_SD//2-60,190,120,[40,78,116,154][k],GOLD if k==3 else TEAL_L if k==2 else TEAL,inner=bb(f'<div class="node3d {"gold" if k==3 else ""}" style="font-family:var(--f-display);font-weight:600;font-size:24px">{n}</div>',lift=14),attrs=f'data-k="{k+1}"')
stair_scene=scene(1168,300,_st,1168,_SD,0,108,58,0,persp=1700,label="A rising 3D staircase of four steps: first order, repeat orders, recurring supply, your own brand")
slide("paper", "Grow with us", f"""
<div class="hd"><span class="eyebrow">Grow with us</span><h2 style="max-width:none">From your first import to a full supply chain</h2></div>
<div class="d-only">{stair_scene}</div><div class="m-only">{iso_row([f'<div class="node3d sm {chr(103)+chr(111)+chr(108)+chr(100) if k==3 else chr(32)}" style="font-family:var(--f-display);font-weight:600;font-size:18px">{n}</div>' for k,(n,t,d,h) in enumerate(stairs)],[26,52,78,104],[TEAL,TEAL,TEAL_L,GOLD],'A rising 3D staircase of four steps')}</div>
<div class="grid g4 m-swipe" style="gap:var(--g)">
 {"".join(f'<div class="hd stepcol" data-k="{n}" style="gap:.3cqw"><h3>{t}</h3><p class="small mute">{d}</p></div>' for n,t,d,h in stairs)}
</div>
<div class="row" style="gap:.6cqw">
 <span class="chip gold">Dedicated account manager</span><span class="chip gold">Order pooling for factory prices</span><span class="chip gold">Market access for Indian producers</span><span class="chip gold">No long-term lock-in</span>
</div>""")

# ---------------- 19 COMMITMENTS ----------------
commit = [
 ("doc","Quote first, always","Scope, price, timeline and duties in writing before you pay. Shipping is estimated, then billed at actual cost after landing."),
 ("clock","A fast start","Work begins within 4 hours of payment, because prices and freight windows change quickly."),
 ("eye","Tracking at every milestone","Updates at dispatch, port arrival, customs clearance and delivery."),
 ("lock","Secure payments","Through Cashfree Payments, an RBI-regulated gateway. We never see or store your card or bank details."),
 ("shield","Confidential by default","Your pricing, suppliers and plans stay private. Your data is never sold, under India's DPDP Act."),
 ("mail","Concerns answered fast","Email us with your order details. We reply within one business day."),
]
slide("", "Our commitments", f'''
<div class="hd"><span class="eyebrow">Our commitments</span><h2>Where you stand, in plain words</h2></div>
<div class="grid fill split" style="grid-template-columns:1fr 2fr;gap:2cqw">
  <div class="card" style="background:var(--sea);color:var(--on-sea);border-color:var(--sea);gap:1.1cqw">
    <span class="eyebrow">Our delivery guarantee</span>
    <div class="row" style="flex-wrap:nowrap;gap:.7em"><span style="color:var(--marigold)">{ic("check")}</span><p class="small">If your order arrives, it arrives as described in your quote. Any shortfall in quantity or specification is fixed by us.</p></div>
    <div class="row" style="flex-wrap:nowrap;gap:.7em"><span style="color:var(--marigold)">{ic("check")}</span><p class="small">If it can never be delivered for a reason within our control, you get a full refund.</p></div>
    <div class="row" style="flex-wrap:nowrap;gap:.7em"><span style="color:var(--on-sea-mute)">{ic("clock")}</span><p class="small" style="color:var(--on-sea-mute)">While goods are in transit or clearing customs, refunds are paused and we keep working on your shipment.</p></div>
    <div class="row" style="flex-wrap:nowrap;gap:.7em"><span style="color:var(--on-sea-mute)">{ic("factory")}</span><p class="small" style="color:var(--on-sea-mute)">Supplier cancellation charges, if any, are explained before they apply.</p></div>
  </div>
  <div class="grid g3 m-swipe" style="grid-auto-rows:1fr">
   {"".join(f'<div class="card">{icb(i)}<h3 style="font-size:var(--b)">{t}</h3><p class="small mute">{d}</p></div>' for i,t,d in commit)}
  </div>
</div>
<p class="small mute">Full Terms, Shipping, Refund and Privacy policies are on ameckhouse.in.</p>''')

# ---------------- 20 FAQ ----------------
faq = [
 ("I have never imported. Can I work with you?","Yes. First-time importers and startups are welcome, and we guide you through every step."),
 ("Do I need an IEC?","No. We work under our own IEC and handle 100% of the paperwork. All you need is GST registration."),
 ("What is the smallest order?","Every import or export needs at least 25 units and 20 kg per shipment, and you can mix any products. Ready stock starts at 25 units, corporate orders at 50."),
 ("How do I know the bulk will match my sample?","You approve a sample first. We inspect during production and again before shipping, and fix problems at the factory."),
 ("What does landed cost mean?","Everything to get the product to your door: factory price, freight, insurance, customs duty, IGST and local delivery. Your quote shows it, with shipping as an estimate settled at actual cost after landing."),
 ("Can I order just one shipment?","Yes. There is no long-term commitment. Many customers start with one order and come back."),
 ("Do you only work with China?","No. We source from 35+ countries across Asia, the Middle East and Europe, and export Indian goods worldwide."),
 ("What can you not ship?","Hazardous materials. Everything else, from apparel to machinery and food products, is welcome."),
]
slide("paper", "Questions", f'''
<div class="hd"><span class="eyebrow">Frequently asked questions</span><h2>Questions customers ask us first</h2><p class="small mute">Tap a question to see the answer.</p></div>
<div class="faq fill">{"".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faq)}</div>''')

# ---------------- 21 GET STARTED ----------------
send = [("What","The product, a photo or link, any specifications"),("How many","The number of units you need"),("Budget","Even a rough figure helps"),("When and where","Your deadline and delivery address")]
slide("dark", "Get started", f'''
<div class="grid fill split" style="grid-template-columns:1.05fr .95fr;gap:4cqw;align-items:center">
  <div class="hd" style="gap:1.6cqw">
    <span class="eyebrow">Getting started</span>
    <h2>Start with one message. We come back with a real quote.</h2>
    <div class="grid g2 m-grid2" style="gap:1.4cqw">
      {"".join(f'<div class="hd" style="gap:.3cqw;border-top:2px solid var(--marigold);padding-top:.8cqw"><span class="mono small" style="color:var(--marigold);font-weight:600">0{n+1}</span><h3>{t}</h3><p class="small mute">{d}</p></div>' for n,(t,d) in enumerate(send))}
    </div>
    <p class="mute">No brief is too vague. If you only have an idea, we will help shape it.</p>
    <a class="wa-cta" href="{WA_URL}" target="_blank" rel="noopener">{WA_ICON} Chat with us on WhatsApp</a>
  </div>
  <div class="card" style="gap:1.4cqw;padding:2.2cqw">
    <div class="crate m-hide" aria-hidden="true"><div class="cr"><i class="bk"></i><i class="bt"></i><i class="lt"></i><i class="rt"></i><i class="tp"></i><i class="fr"></i></div><span class="crate-shadow"></span></div>
    <dl class="contact">
      <dt>WhatsApp</dt><dd>+91 83021 92742</dd>
      <dt>Phone</dt><dd>+91 83021 92742</dd>
      <dt>Email</dt><dd>info@ameckhouse.com</dd>
      <dt>Websites</dt><dd>ameckhouse.in <span class="mute" style="font-weight:400">and</span> ameckhouse.com</dd>
      <dt>Catalogue</dt><dd>catalogue.ameckhouse.com</dd>
      <dt>Hours</dt><dd class="small">Monday to Saturday, 10 AM to 7 PM</dd>
    </dl>
    <div class="rule"></div>
    <p class="closer">You bring the vision.<br><span style="color:var(--marigold)">We bring the edge.</span></p>
  </div>
</div>''')

# ---------------- ASSEMBLE ----------------
SLIDES = [x for x in SLIDES if x[1] != "Ready Stock Store"]
N = len(SLIDES)
html = assemble(SLIDES, "How Ameck Works", "Ameck House / Customer guide", "ameckhouse.in", f"Customer guide / {N} pages",
                font_css + CSS, SPRITE, os.environ.get("THREE_SRC", THREE_CDN), whatsapp=True)
(HERE / "how-ameck-works.html").write_text(html)
(HERE / "print.html").write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
    '<style>body{margin:0}</style></head><body>' + html + '</body></html>')
print("slides", N, "bytes", len(html))
