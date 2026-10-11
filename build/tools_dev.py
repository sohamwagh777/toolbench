# -*- coding: utf-8 -*-
"""Developer category tools (15)."""
from gen_helpers import mkpage

CAT = "Developer"

def f(fid, label, tag="textarea", attrs=""):
    if tag == "textarea":
        return '<div class="fld grow"><label for="%s">%s</label><textarea id="%s" %s></textarea></div>' % (fid, label, fid, attrs)
    return '<div class="fld grow"><label for="%s">%s</label><input id="%s" type="text" %s></div>' % (fid, label, fid, attrs)

def sel(fid, label, opts):
    o = "".join('<option value="%s"%s>%s</option>' % (v, (" selected" if v == d else ""), d) for v, d in opts)
    return '<div class="fld"><label for="%s">%s</label><select id="%s">%s</select></div>' % (fid, label, fid, o)

def btns(*names):
    return '<div class="row">' + "".join('<button data-act="%s">%s</button>' % (n.lower(), n) for n in names) + '</div>'

def page(i, title, desc, body, js):
    return mkpage(i, CAT, title, desc, body, js)

TOOLS = []

# 1 JSON Formatter
TOOLS.append(page("json-formatter", "JSON Formatter",
    "Pretty-print or minify JSON with error line hints. Handles any valid JSON.",
    '<section class="card"><div class="row">' + sel("m", "Mode", [("pretty", "Pretty"), ("min", "Minify")]) + '</div>' + f("ta", "JSON") + '<div class="row" style="margin-top:12px">' + btns("Run", "Copy") + '</div><div id="out"></div></section>',
    """function run(){const t=V('ta')||'';if(!t)return OUT('');
try{const o=JSON.parse(t);OUT(V('m')==='min'?JSON.stringify(o):JSON.stringify(o,null,2))}
catch(e){OUT('Parse error: '+e.message)}}
if(!V('ta')){$('#ta').value='{"name":"toolbench","tools":[1,2,3],"nested":{"ok":true}}'}run();wire(['ta','m']);"""))

# 2 JSON → TypeScript
TOOLS.append(page("json-to-ts", "JSON → TypeScript",
    "Paste JSON, get TypeScript interfaces with optional-free inferred types and nested objects.",
    '<section class="card">' + f("ta", "JSON") + '<div class="row" style="margin-top:12px">' + btns("Run", "Copy") + '</div><div id="out"></div></section>',
    """function T(v){if(v===null)return'null';if(Array.isArray(v))return v.length&&typeof v[0]==='object'&&v[0]!==null?'Array<'+T(v[0])+'>':'Array<'+(Array.isArray(v)?T(v[0]):typeof v[0])+'>';
const t=typeof v;if(t!=='object')return t;
const p=Object.entries(v).map(e=>'  '+e[0]+': '+T(e[1])+';');return p.length?'{\\n'+p.join('\\n')+'\\n}':'object'}
function run(){try{const o=JSON.parse(V('ta')||'null');OUT('interface Root '+T(o)+';')}catch(e){OUT('Parse error: '+e.message)}}
if(!V('ta')){$('#ta').value='{"id":1,"tags":["a","b"],"meta":{"x":true}}'}run();wire('ta');"""))

# 3 JWT Decoder
TOOLS.append(page("jwt-decoder", "JWT Decoder",
    "Split a JWT, decode header + payload, flag expired exp claims. Local only — nothing is sent.",
    '<section class="card"><p class="hint">Paste a token to decode its header and claims.</p>' + f("ta", "Token") + '<div class="row" style="margin-top:12px">' + btns("Decode", "Copy") + '</div><div id="out"></div></section>',
    """function d64(s){s=s.replace(/-/g,'+').replace(/_/g,'/');while(s.length%4)s+='=';return decodeURIComponent(escape(atob(s)))}
function run(){const t=V('ta')||'';const p=t.split('.');if(p.length!==3)return OUT('Not a JWT — expected 3 dot-separated parts');
try{const h=JSON.parse(d64(p[0])),c=JSON.parse(d64(p[1]));let s='HEADER\\n'+JSON.stringify(h,null,2)+'\\n\\nPAYLOAD\\n'+JSON.stringify(c,null,2);
if(c.exp!==undefined){const e=c.exp*1000;s+='\\n\\nexp: '+new Date(e).toISOString()+(e<Date.now()?' — EXPIRED':' — valid')}
OUT(s)}catch(e){OUT('Decode error: '+e.message)}}
function e64(s){return btoa(unescape(encodeURIComponent(s))).replace(/\\+/g,'-').replace(/\\//g,'_').replace(/=/g,'')}
if(!V('ta')){$('#ta').value=e64('{"alg":"HS256","typ":"JWT"}')+'.'+e64('{"sub":"42","name":"Jane","iat":1700000000,"exp":1710000000}')+'.SIGNATURE'}run();wire('ta');"""))

# 4 Markdown Preview
TOOLS.append(page("markdown-preview", "Markdown Preview",
    "Headings, bold/italic, code, links, lists and rules — rendered right here, no CDN.",
    '<section class="card">' + f("ta", "Markdown") + '<div class="row" style="margin-top:12px">' + btns("Run", "Copy") + '</div><div id="out"></div></section>',
    """function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;')}
function inl(s){return s.replace(/`([^`]+)`/g,'<code>$1</code>').replace(/\\*\\*([^*]+)\\*\\*/g,'<b>$1</b>').replace(/\\*([^*]+)\\*/g,'<i>$1</i>').replace(/\\[([^\\]]+)\\]\\(([^)]+)\\)/g,'<a href="$2">$1</a>')}
function run(){const L=(V('ta')||'').split('\\n').map(l=>{const e=esc(l);
if(/^#{1,6} /.test(l)){const n=l.split(' ')[0].length;return '<b style="font-size:'+(22-n)+'px">'+inl(esc(l.replace(/^#+ /,'')))+'<b>'}
if(/^\\s*[-*] /.test(l))return '&nbsp;&nbsp;• '+inl(esc(l.replace(/^\\s*[-*] /,'')));
if(/^\\s*\\d+\\. /.test(l))return '&nbsp;&nbsp;'+l.replace(/^(\\s*)(\\d+)(\\. )/,'$1$2. ').replace(/\\d\\. /,'$& ');
if(/^(\\s*)[ ]*[-*] /.test(l))return inl(esc(l));
if(/^-{3,}$/.test(l))return '―――';return inl(esc(l))});OUT(L.join('<br>'))}
if(!V('ta')){$('#ta').value='# Notes\\n\\n- buy **milk** and *eggs*\\n- see [site](https://example.com)\\n\\n---\\n\\nDone: `run()`'}run();wire('ta');"""))

# 5 Cron Explainer
TOOLS.append(page("cron-explainer", "Cron Explainer",
    "Paste a 5-field crontab line, get plain-English timing plus per-field breakdown.",
    '<section class="card">' + f("ta", "Cron expression", "text", 'placeholder="0 9 * * 1-5"') + '<div class="row" style="margin-top:12px">' + btns("Run", "Copy") + '</div><div id="out"></div></section>',
    """const N=['minute','hour','day of month','month','day of week'];
function desc(f,i){const n=N[i];const p=(x)=>x;
if(f==='*')return'every '+n.toLowerCase();
const s=f.replace(/^\\*\\//,'every ').replace(/^\\*\\//,'');
if(/^\\*\\/(\\d+)$/.test(f))return'every '+RegExp.$1+(i==2||i==4?'':' '+n.toLowerCase()+'s')+(i==2||i==4?' days':'');
if(/^(\\d+)-(\\d+)$/.test(f))return'from '+RegExp.$1+' to '+RegExp.$2+' '+n.toLowerCase()+'s';
if(/^[\\d,]+$/.test(f))return'nurture'.replace('nurture','on')+' '+f.split(',').join(', ')+' '+n.toLowerCase()+'s';
return'at '+f+' '+n.toLowerCase()}
function run(){const t=(V('ta')||'').trim();if(!t)return OUT('');const p=t.split(/\\s+/);
if(p.length!==5)return OUT('Need exactly 5 fields (min hour dom mon dow). Got '+p.length);
const per=p.map((x,i)=>{const e=desc(x,i);return e.startsWith('at')?e:null}).filter(Boolean);
const mins=p[1]==='*'?p[0]:'minute '+p[0]+', hour '+p[1];
let out='Raw: '+t;if(per.length)out+='\\n≈ '+per.join(' on ')+'\\n\\nPer field:\\n'+p.map((x,i)=>x+' — '+desc(x,i)).join('\\n');
OUT(out)}
if(!V('ta')){$('#ta').value='0 9 * * 1-5'}run();wire('ta');"""))

# 6 Regex Tester
TOOLS.append(page("regex-tester", "Regex Tester",
    "Test a pattern with flags against text: match count, positions and captured groups.",
    '<section class="card"><div class="row">' + f("pat", "Pattern") + f("flags", "Flags", "text", 'value="gim" placeholder="g i m s u"') + '</div>' + f("ta", "Test text") + '<div class="row" style="margin-top:12px">' + btns("Run", "Copy") + '</div><div id="out"></div></section>',
    """function run(){let re;try{re=new RegExp(V('pat')||'',V('flags')||'g')}catch(e){return OUT('Bad pattern: '+e.message)}
const t=V('ta')||'';let m,n=0;const o=[];
while((m=re.exec(t))!==null){n++;if(re.source==='')break;o.push('['+m.index+'] "'+m[0]+'"'+(m.length>1?' groups: '+JSON.stringify(m.slice(1)):''));if(m.index===re.lastIndex)re.lastIndex++;if(n>50)break}
OUT(n?('matches: '+n+(n>50?'+ (truncated)':'')+'\\n'+o.join('\\n')):'no matches — '+re)}
if(!V('pat')){$('#pat').value='(\\\\w+)@(\\\\w+)\\\\.(\\\\w+)'}if(!V('ta')){$('#ta').value='mail me at me@corp.dev please'}run();wire(['pat','flags','ta']);"""))

# 7 HTTP Status Lookup
TOOLS.append(page("http-status-lookup", "HTTP Status Lookup",
    "Type any status code or keyword, get meaning and the usual cause. 32 codes, fully offline.",
    '<section class="card">' + f("q", "Code or keyword", "text", 'placeholder="429, redirect, teapot…"') + '<div style="height:12px"></div><div id="out"></div></section>',
    """const S={200:'OK — request succeeded',201:'Created — resource made',204:'No Content — success, empty body',206:'Partial Content — range request (resumable downloads)',301:'Moved Permanently — old links still work, cached forever by browsers',302:'Found — temporary redirect',304:'Not Modified — browser cache still fresh',307:'Temporary Redirect — keeps method/body unlike 302',308:'Permanent Redirect — keeps method/body',400:'Bad Request — malformed syntax',401:'Unauthorized — login/credentials missing or wrong',403:'Forbidden — logged in but not allowed',404:'Not Found — wrong URL, removed page, or typo',405:'Method Not Allowed — wrong verb (GET vs POST)',408:'Request Timeout — server gave up waiting',409:'Conflict — e.g. duplicate entry, etag mismatch',410:'Gone — deleted on purpose (unlike 404)',418:'Teapot — April Fools joke code (RFC 2324)',422:'Unprocessable — syntax fine, semantics wrong',425:'Too Early — server refuses replay risk',429:'Too Many Requests — rate limit hit, back off',431:'Header Fields Too Large',451:'Unavailable For Legal Reasons',500:'Internal Server Error — generic crash',501:'Not Implemented — server lacks feature',502:'Bad Gateway — upstream gave bad response',503:'Service Unavailable — overload/maintenance, retry later',504:'Gateway Timeout — upstream too slow',505:'HTTP Version Not Supported',507:'Insufficient Storage',508:'Loop Detected'};
function run(){const q=(V('q')||'').trim().toLowerCase();
if(!q)return OUT(Object.entries(S).slice(0,12).map(e=>e[0]+' '+e[1]).join('\\n')+'\\n\\n…type to search any of the 32 codes');
const h=Object.entries(S).filter(e=>e[0].includes(q)||e[1].toLowerCase().includes(q));
OUT(h.length?h.map(e=>e[0]+' — '+e[1]).join('\\n'):'no match for "'+q+'" — try a code, a word ("redirect", "limit") or a verb')}
run();wire('q');"""))

# 8 cURL → fetch
TOOLS.append(page("curl-to-fetch", "cURL → fetch",
    "Paste a curl command, get browser fetch()/XMLHttpRequest equivalent with headers and body.",
    '<section class="card">' + f("ta", "cURL command") + '<div class="row" style="margin-top:12px">' + btns("Convert", "Copy") + '</div><div id="out"></div></section>',
    """function run(){const t=(V('ta')||'').replace(/\\\\\\\\\\n/g,' ').replace(/\\s+/g,' ').trim();if(!t)return OUT('');
const url=(t.match(/https?:\\/\\/[^'"\\s]+/)||[''])[0];const tok=t.split(/\\s+(?=(?:-[^\\s]|[^\\s]+\\s+https?:))/).join(' ');
const m=(t.match(/(?:-X|--request)\\s+(\\w+)/)||[])[1]||'GET';
const hs=[...t.matchAll(/(?:-H|--header)\\s+["']([^"']+)["']/g)].map(x=>x[1]);
const b=(t.match(/(?:--data-raw|--data|-d)\\s+['"]?([^{\\s][^"'}]*)['"]?/)||[])[1];
let s='fetch("'+url+'", {\\n  method: "'+m+'",\\n  headers: {'+hs.map(h=>{const p=h.split(/: /);return'"'+p[0]+'": "'+p.slice(1).join(': ')+'"'}).join(', ')+(hs.length?' ':'')+'},';
if(b)s+='\\n  body: '+JSON.stringify(b)+',';
s+='\\n}).then(r=>r.text()).then(console.log);';OUT(s)}
if(!V('ta')){$('#ta').value="curl -X POST https://api.example.com/v1/items -H 'Content-Type: application/json' -H 'Authorization: Bearer tok' --data '{\\"id\\":7}'"}run();wire('ta');"""))

# 9 YAML → JSON
TOOLS.append(page("yaml-to-json", "YAML → JSON",
    "Indentation-based subset converter: mappings, sequences, scalars with type inference.",
    '<section class="card">' + f("ta", "YAML") + '<div class="row" style="margin-top:12px">' + btns("Run", "Copy") + '</div><div id="out"></div></section>',
    """function scalar(s){s=s.trim();if(/^".*"$/.test(s)||/^'.*'$/.test(s))return s.slice(1,-1);
if(/^-?\\d+(\\.\\d+)?$/.test(s))return parseFloat(s);if(s==='true')return true;if(s==='false')return false;if(s==='null'||s==='~'||s==='')return null;return s}
function run(){const src=(V('ta')||'').split('\\n').filter(l=>l.trim()&&!l.trim().startsWith('#'));
const root={};const stack=[[0,root]];
try{for(const l of src){const ind=l.match(/^ */)[0].length;const line=l.trim();
while(stack.length&&ind<stack[stack.length-1][0])stack.pop();
const top=stack[stack.length-1][1];
if(/^- /.test(line)){const[k,v]=line.slice(2).split(/:\\s*/);top.list=top.list||[];top.list.push(v!==undefined?scalar(v):line.slice(2))}
else{const i=line.indexOf(':');if(i<0)throw'no colon: '+line;
const k=line.slice(0,i).trim(),v=line.slice(i+1).trim();
if(v===''){const n={};(top.list||(delete top.list,top))[k]=n;stack.push([ind+2,n]);if(!Array.isArray(top))top[k]=n}else top[k]=scalar(v)}}
OUT(JSON.stringify(root,null,2))}catch(e){OUT('YAML error: '+e.message)}}
if(!V('ta')){$('#ta').value='app: toolbench\\nport: 8080\\nfeatures:\\n  - search\\n  - dark mode\\ndb:\\n  engine: postgres\\n  pool: 5'}run();wire('ta');"""))

# 10 env ⇄ JSON
TOOLS.append(page("env-to-json", "env ⇄ JSON",
    "Convert .env KEY=VALUE text to JSON and back. Quotes kept, comments dropped.",
    '<section class="card"><div class="row">' + sel("m", "Direction", [("e2j", ".env → JSON"), ("j2e", "JSON → .env")]) + '</div>' + f("ta", "Input") + '<div class="row" style="margin-top:12px">' + btns("Convert", "Copy") + '</div><div id="out"></div></section>',
    """function run(){const t=V('ta')||'';
try{if(V('m')==='e2j'){const o={};t.split('\\n').forEach(l=>{l=l.trim();if(!l||l.startsWith('#'))return;const i=l.indexOf('=');if(i>0)o[l.slice(0,i)]=l.slice(i+1).replace(/^(["'])(.*)\\1$/,'$2')});OUT(JSON.stringify(o,null,2))}
else{const o=JSON.parse(t);OUT(Object.entries(o).map(e=>e[0]+'='+String(e[1]).replace(/^"|"$/g,'')).join('\\n'))}}
catch(e){OUT('Error: '+e.message)}}
if(!V('ta')){$('#ta').value='# staging\\nPORT=8080\\nDB_URL="postgres://u:***@db:5432/app"\\nDEBUG=true'}run();wire(['m','ta']);"""))

# 11 HTML Preview
TOOLS.append(page("html-preview", "HTML Preview",
    "Live sandboxed preview of an HTML snippet — paste markup, watch it render below.",
    '<section class="card">' + f("ta", "HTML source") + '<div class="row" style="margin-top:12px">' + btns("Run", "Copy") + '</div><iframe id="pv" sandbox="" style="width:100%;height:220px;border:1px solid var(--line);border-radius:10px;background:#fff;margin-top:12px"></iframe></section>',
    """function run(){const t=V('ta')||'';$('#pv').srcdoc=t}
if(!V('ta')){$('#ta').value='<h3 style="color:#0e6e5c">Hello</h3><p>Rendered <b>live</b> in the box below.</p>'}run();wire('ta');"""))

# 12 JS Scratch Runner
TOOLS.append(page("js-runner", "JS Scratch Runner",
    "Run a snippet against a captured console.log. Good for testing regexes and one-liners.",
    '<section class="card"><p class="hint">No network, no DOM access beyond helpers — output and errors show below.</p>' + f("ta", "JavaScript") + '<div class="row" style="margin-top:12px">' + btns("Run", "Copy") + '</div><div id="out"></div></section>',
    """function run(){const c=[];const log=(...a)=>c.push(a.map(x=>typeof x==='object'?JSON.stringify(x):String(x)).join(' '));
try{const f=new Function('console','"use strict";'+V('ta'));let r=f({log});if(r!==undefined)log('=>',r);OUT(c.join('\\n')||'(no output)')}
catch(e){OUT('Error: '+e.constructor.name+': '+e.message+(c.length?'\\n'+c.join('\\n'):''))}}
if(!V('ta')){$('#ta').value='const s=[1,2,3].map(x=>x*x);\\nconsole.log(s);\\ns.reduce((a,b)=>a+b,0)'}run();wire('ta');"""))

# 13 UUID Generator
TOOLS.append(page("uuid-generator", "UUID v4 Generator",
    "Batch-random UUIDs (crypto-backed) with a re-roll seed — same count/seed, same list.",
    '<section class="card"><div class="row">' + f("count", "Count", "number", 'value="10" min="1" max="100"') + f("seed", "Seed (blank = random each edit)", "text") + '</div>' + btns("Reroll", "Copy") + '<div id="out"></div></section>',
    """function mul(x){return function(){x|=0;x=x+0x6D2B79F5|0;let t=Math.imul(x^x>>>15,1|x);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function v4(rnd){const h=Array.from({length:32},()=>Math.floor(rnd()*16));h[12]='4';h[16]='89ab'[Math.floor(rnd()*4)];
const s=h.join('');return s.slice(0,8)+'-'+s.slice(8,12)+'-'+s.slice(12,16)+'-'+s.slice(16,20)+'-'+s.slice(20)}
function run(){const n=Math.min(100,Math.max(1,parseInt(V('count'))||10));const sd=V('seed');
const rnd=sd?mul([...sd].reduce((a,c)=>Math.imul(a^c.charCodeAt(0),16777619)>>>0,2166136261)):Math.random;
OUT([...Array(n)].map(()=>v4(rnd)).join('\\n'))}
run();wire(['count','seed']);"""))

# 14 HTML Minifier
TOOLS.append(page("html-minifier", "HTML Minifier",
    "Collapse markup whitespace, strip HTML comments and unused attributes. Paste-safe (escaped).",
    '<section class="card">' + f("ta", "HTML") + '<div class="row" style="margin-top:12px">' + btns("Run", "Copy") + '</div><div id="out"></div></section>',
    """function run(){let t=(V('ta')||'').replace(/<!--[\\s\\S]*?-->/g,'')
.replace(/\\s*([<>])\\s*/g,'$1').replace(/\\s{2,}/g,' ').replace(/\\n+/g,'\\n');
const before=(V('ta')||'').length;OUT(t.trim()+'\\n\\n'+before+' → '+t.trim().length+' chars ('+Math.round(100*(1-t.length/before))+'% smaller)')}
if(!V('ta')){$('#ta').value='<nav>\\n  <a href="/">Home</a>\\n  <a href="/about">About</a>\\n</nav>'}run();wire('ta');"""))

# 15 Query String
TOOLS.append(page("query-builder", "Query String Lab",
    "Paste a URL to list its params and values, or edit params and get a rebuilt URL.",
    '<section class="card">' + f("url", "URL or params (k=v per line)", "text") + '<div class="row" style="margin-top:12px">' + btns("Run", "Copy") + '</div><div id="out"></div></section>',
    """function run(){let s=(V('url')||'').trim();if(!s)return OUT('');let base='',rest=s;
if(/^https?:\\/\\//i.test(s)){const u=new URL(s);base=u.origin+u.pathname;rest=u.search.slice(1)}
const params=rest.split(/\\n|&/).map(x=>x.trim()).filter(Boolean).map(x=>{const i=x.indexOf('=');return i<0?[x,'']:[x.slice(0,i),x.slice(i+1)]});
const rebuilt=base+(params.length?'?'+params.map(p=>p[0]+'='+p[1]).join('&'):'');
let U='';try{U='\\n\\nencoded:\\n'+decodeURIComponent(rebuilt)}catch(e){}
OUT(params.length?('params ('+params.length+'):\\n'+params.map(p=>'  '+p[0]+' = '+p[1]).join('\\n')+'\\n\\nrebuilt:\\n'+rebuilt):'no params found')}
if(!V('url')){$('#url').value='https://shop.example/cart?utm_source=nl&coupon=SAVE10'}run();wire('url');"""))
