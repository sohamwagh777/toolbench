# Shared design shell for Toolbench: premium dark "workbench" system.
# Pages: landing = Explore surface (catalog), tool pages = Operate surface (compact workbenches).

PAGE = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__ · Toolbench</title>
<style>
:root{--bg:#0e0f11;--panel:#15171a;--panel2:#1b1e22;--line:#282c32;--ink:#ecebe6;--mut:#8f949b;
--acc:__ACC__;--mono:ui-monospace,'Cascadia Mono','JetBrains Mono','SF Mono',Consolas,monospace;
--sans:ui-sans-serif,-apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;
--serif:Georgia,'Iowan Old Style','Times New Roman',serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.55 var(--sans)}
a{color:inherit}header.tb{display:flex;align-items:center;gap:16px;max-width:780px;margin:0 auto;padding:22px 20px 14px}
header.tb .back{font:600 11px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;text-decoration:none;color:var(--mut);border:1px solid var(--line);padding:9px 12px;border-radius:8px;white-space:nowrap;transition:color .15s,border-color .15s}
header.tb .back:hover{color:var(--ink);border-color:var(--mut)}
header.tb .mid{flex:1;min-width:0}header.tb .cat{font:600 10px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--acc)}
header.tb h1{font:400 21px/1.25 var(--serif);margin:4px 0 3px}
header.tb .desc{margin:0;font-size:12.5px;color:var(--mut)}
header.tb .tag{font:600 10px/1 var(--mono);letter-spacing:.14em;color:var(--mut);text-decoration:none}
main{max-width:780px;margin:0 auto;padding:6px 20px 56px}
section.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px}
.row{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:12px}
.fld{display:flex;flex-direction:column;gap:5px;min-width:0}.fld.grow{flex:1 1 220px}
label{font:600 10.5px/1.2 var(--mono);letter-spacing:.09em;text-transform:uppercase;color:var(--mut)}
input,select,textarea{background:var(--panel2);border:1px solid var(--line);color:var(--ink);border-radius:8px;padding:9px 11px;font:13px/1.4 var(--mono);width:100%}
input:focus,select:focus,textarea:focus{outline:none;border-color:var(--acc);box-shadow:0 0 0 3px color-mix(in srgb,var(--acc) 18%,transparent)}
textarea{min-height:130px;resize:vertical}
button{background:var(--acc);color:#101214;font:700 11.5px/1 var(--sans);letter-spacing:.07em;text-transform:uppercase;padding:11px 15px;border-radius:8px;border:0;cursor:pointer;transition:filter .15s}
button:hover{filter:brightness(1.12)}button.ghost{background:var(--panel2);color:var(--ink);border:1px solid var(--line)}
#out{white-space:pre-wrap;word-break:break-word;background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:14px 16px;font:13px/1.65 var(--mono);min-height:52px;margin-top:14px}
#out:empty::before{content:'—';color:var(--mut)}
.hint{font-size:12px;color:var(--mut);margin:0 0 12px}
.hint b{color:var(--ink);font-weight:600}
.priv{font-size:11px;color:var(--mut);opacity:.8;margin:14px 0 0}
@media (max-width:640px){header.tb{padding:16px 14px 10px}main{padding:4px 14px 40px}.row{flex-direction:column}}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
</style></head><body>
<header class="tb"><a class="back" href="../index.html" title="Back to all tools (Esc)">&#8592; All tools</a>
<div class="mid"><div class="cat">__CAT__</div><h1>__TITLE__</h1><p class="desc">__DESC__</p></div>
<a class="tag" href="../index.html">TOOLBENCH</a></header>
<main>__BODY__<p class="priv">Private &amp; local: everything stays in this page — no network calls, no tracking, your input never leaves this tab.</p></main>
<script>
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const V=id=>{const e=document.getElementById(id);return e?e.value.trim():'';};
const OUT=h=>{const o=document.getElementById('out');if(o)o.innerHTML=h;};
const fmt=(n,d=6)=>{if(n===null||n===undefined||!isFinite(n))return '\\u2014';return (+n).toLocaleString('en-US',{maximumFractionDigits:d});};
const wire=ids=>(Array.isArray(ids)?ids:[ids]).forEach(i=>{const e=document.getElementById(i);if(e)e.addEventListener('input',()=>window.run&&window.run());});
document.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;
const act=(b.dataset.act||'').toLowerCase();
if(act==='copy'){if(navigator.clipboard&&navigator.clipboard.writeText){const t=document.getElementById('out').innerText;navigator.clipboard.writeText(t).then(()=>{const o=b.textContent;b.textContent='Copied ✓';setTimeout(()=>b.textContent=o,900)})}return}
if(window.run)run();});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!(e.target.closest&&e.target.closest('input,textarea,select'))){location.href='../index.html';}});
__SCRIPT__
</script>
</body></html>
"""

LANDING = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Toolbench — 100 daily-use tools</title>
<style>
:root{--bg:#0e0f11;--panel:#15171a;--panel2:#1b1e22;--line:#282c32;--ink:#ecebe6;--mut:#8f949b;--acc:#d8a25e;
--mono:ui-monospace,'Cascadia Mono','JetBrains Mono','SF Mono',Consolas,monospace;
--sans:ui-sans-serif,-apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;
--serif:Georgia,'Iowan Old Style','Times New Roman',serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.55 var(--sans)}
header.top{position:sticky;top:0;z-index:5;background:rgba(14,15,17,.92);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.top-in{max-width:1060px;margin:0 auto;padding:14px 22px;display:flex;gap:18px;align-items:center;flex-wrap:wrap}
.brand{font:400 19px/1.2 var(--serif);letter-spacing:.01em}.brand b{font-weight:400;color:var(--acc)}
.count{font:600 10px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--mut);border:1px solid var(--line);padding:6px 9px;border-radius:99px}
.search{flex:1 1 260px;display:flex;align-items:center;gap:10px;background:var(--panel2);border:1px solid var(--line);border-radius:9px;padding:8px 13px}
.search input{flex:1;background:transparent;border:0;color:var(--ink);font:13.5px var(--mono);outline:none}
.search kbd{font:10px var(--mono);color:var(--mut);border:1px solid var(--line);border-radius:4px;padding:2px 6px}
.chips{max-width:1060px;margin:0 auto;padding:12px 22px;display:flex;gap:8px;flex-wrap:wrap}
.chip{font:600 10.5px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;text-decoration:none;color:var(--mut);background:var(--panel2);border:1px solid var(--line);padding:8px 12px;border-radius:99px;transition:color .15s,border-color .15s}
.chip:hover,.chip.on{color:var(--ink);border-color:var(--mut)}
main{max-width:1060px;margin:0 auto;padding:18px 22px 72px}
section.cat{margin:26px 0 8px;scroll-margin-top:130px}
.cat h2{font:400 20px/1.3 var(--serif);border-bottom:1px solid var(--line);padding-bottom:10px;margin:0 0 16px}
.cat h2 small{float:right;font:600 10px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--mut);padding-top:8px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:12px}
a.tool{display:block;text-decoration:none;background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 16px;transition:border-color .15s,transform .15s}
a.tool:hover{border-color:var(--mut);transform:translateY(-1px)}
a.tool b{display:block;font:600 13.5px/1.3 var(--sans);color:var(--ink)}
a.tool span{display:block;font:12px/1.45 var(--mono);color:var(--mut);margin-top:5px}
a.tool i{display:inline-block;width:7px;height:7px;border-radius:99px;background:var(--catacc,#d8a25e);margin-right:7px;vertical-align:1px}
.empty{padding:60px 0;text-align:center;color:var(--mut);font:13px var(--mono)}
footer{border-top:1px solid var(--line);margin-top:44px;padding:18px 22px;text-align:center;font:11.5px var(--mono);color:var(--mut);letter-spacing:.06em}
@media (max-width:640px){.top-in{padding:12px 14px}.chips{padding:10px 14px}main{padding:14px 14px 56px}}
</style></head><body>
<header class="top"><div class="top-in">
<div class="brand">Tool<b>bench</b></div><div class="count">__NCOUNT__ tools · __NCATS__ categories</div>
<div class="search"><input id="q" type="search" placeholder="Filter tools — type to search, press Esc to clear" autocomplete="off"><kbd>/</kbd></div>
</div>
<nav class="chips">__CHIPS__</nav></header>
<main>__SECTIONS__<div class="empty" id="nores" hidden>No tools match that filter.</div></main>
<footer>100 client-side tools · no network calls · no tracking · data never leaves the page · built Oct 2026</footer>
<script>
const q=document.getElementById('q'),chips=[...document.querySelectorAll('.chip')],cards=[...document.querySelectorAll('a.tool')],secs=[...document.querySelectorAll('section.cat')],nores=document.getElementById('nores');
function apply(){const t=q.value.trim().toLowerCase();const active=chips.find(c=>c.classList.contains('on'));
let shown=0;cards.forEach(a=>{const sec=a.closest('section.cat');const m=(!t||a.textContent.toLowerCase().includes(t))&&(!active||sec&&sec.dataset.cat===active.dataset.cat);a.hidden=!m;if(m)shown++;});
secs.forEach(s=>{s.hidden=[...s.querySelectorAll('a.tool')].every(a=>a.hidden);});nores.hidden=shown!==0;}
chips.forEach(c=>c.addEventListener('click',e=>{e.preventDefault();const was=c.classList.contains('on');chips.forEach(x=>x.classList.remove('on'));if(!was)c.classList.add('on');apply();}));
q.addEventListener('input',apply);
document.addEventListener('keydown',e=>{if(e.key==='Escape'){q.value='';apply();}if(e.key==='/'&&document.activeElement!==q){e.preventDefault();q.focus();q.select();}});
</script>
</body></html>
"""

def render_page(tool, accent):
    body, script = tool["body"], tool.get("script", "")
    # guarantee #out for scripts that write into it (fixes the dead-JS class of bugs)
    if 'id="out"' not in body and ("OUT(" in script or "getElementById('out')" in script):
        body += '<div id="out"></div>'
    if tool.get("howto"):
        body += '<p class="hint"><b>How to use.</b> ' + tool["howto"] + '</p>'
    html = (PAGE.replace("__ACC__", accent).replace("__CAT__", tool["cat"]).replace("__TITLE__", tool["title"])
            .replace("__DESC__", tool["desc"]).replace("__BODY__", body).replace("__SCRIPT__", script))
    return html

def render_landing(tools, accents, build_note):
    cats, order = {}, []
    for t in tools:
        if t["cat"] not in cats:
            cats[t["cat"]] = []; order.append(t["cat"])
        cats[t["cat"]].append(t)
    chips = "".join(f'<a class="chip" href="#c{i}" data-cat="{c}">{c}</a>' for i, c in enumerate(order))
    secs = ""
    for i, c in enumerate(order):
        acc = accents.get(c, "#d8a25e")
        rows = "".join(f'<a class="tool" href="tools/{t["id"]}.html"><b>{t["title"]}</b><span>{t["desc"]}</span></a>' for t in cats[c])
        secs += f'<section class="cat" id="c{i}" data-cat="{c}" style="--catacc:{acc}"><h2>{c}<small>{len(cats[c])} tools</small></h2><div class="grid">{rows}</div></section>'
    return LANDING.replace("__NCOUNT__", str(len(tools))).replace("__NCATS__", str(len(order))).replace("__CHIPS__", chips).replace("__SECTIONS__", secs).replace("__BUILDTIME__", build_note)
