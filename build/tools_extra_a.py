# -*- coding: utf-8 -*-
"""Toolbench spec A — Text (7) + Encoding & Hashing (7). Each tool renders via shell."""
from gen_helpers import mkpage

def f(fid, label, tag="textarea", attrs=""):
    if tag == "textarea":
        return '<div class="fld grow"><label for="%s">%s</label><textarea id="%s" %s></textarea></div>' % (fid, label, fid, attrs)
    return '<div class="fld grow"><label for="%s">%s</label><input id="%s" type="text" %s></div>' % (fid, label, fid, attrs)

def num(fid, label, val=""):
    return '<div class="fld"><label for="%s">%s</label><input id="%s" type="number" step="any" value="%s"></div>' % (fid, label, fid, val)

def sel(fid, label, opts):
    o = "".join('<option value="%s"%s>%s</option>' % (v, (" selected" if i == 0 else ""), d) for i, (v, d) in enumerate(opts))
    return '<div class="fld"><label for="%s">%s</label><select id="%s">%s</select></div>' % (fid, label, fid, o)

def btns(*names):
    return '<div class="row">' + "".join('<button data-act="%s">%s</button>' % (n.lower(), n) for n in names) + '</div>'

def T(i, cat, title, desc, body, js):
    return mkpage(i, cat, title, desc, body, js)

TOOLS = []

# ---------- Text ----------
TOOLS.append(T("case-converter", "Text", "Case Converter",
 "camelCase to snake_case and back — code-style renaming for snippets and file names",
 f("ta", "Input") + btns("Convert", "Copy"),
 """function run(){const t=V('ta')||'';const w=t.match(/[A-Za-z0-9_']+/g)||[];
const camel=w.length?w[0].toLowerCase()+w.slice(1).map(x=>x[0].toUpperCase()+x.slice(1)).join(''):'';
const snake=w.map(x=>x.toLowerCase()).join('_');const kebab=w.map(x=>x.toLowerCase()).join('-');
const title=w.map(x=>x[0].toUpperCase()+x.slice(1)).join(' ');
OUT(['camelCase   '+camel,'snake_case  '+snake,'kebab-case  '+kebab,'Title Case  '+title,'UPPER       '+t.toUpperCase(),'lower       '+t.toLowerCase()].join('\\n'));}
wire('ta');run();"""))

TOOLS.append(T("line-tools", "Text", "Line Tools",
 "Trim, sort, unique, reverse and dedupe lines — combine or split",
 f("ta", "Lines") + '<div class="row"><label class="fld"><input type="checkbox" id="srt" style="width:auto"> sort</label><label class="fld"><input type="checkbox" id="uni" style="width:auto"> unique</label><label class="fld"><input type="checkbox" id="rvr" style="width:auto"> reverse</label></div>' + btns("Run", "Copy"),
 """function run(){var L=V('ta').split('\\n').map(x=>x.trim());if(document.getElementById('uni').checked)L=[...new Set(L)];
if(document.getElementById('srt').checked)L.sort();if(document.getElementById('rvr').checked)L.reverse();
OUT(L.join('\\n'));}
wire(['ta','srt','uni','rvr']);run();"""))

TOOLS.append(T("text-reverser", "Text", "Text Reverser",
 "Flip characters, words or whole lines — mirror, encrypt-ish, puzzle",
 f("ta", "Input") + btns("Reverse", "Copy"),
 """function run(){const t=V('ta')||'';
OUT('chars: '+t.split('').reverse().join('')+'\\n\\nwords: '+t.split(/\\s+/).reverse().join(' ')+'\\n\\nlines: '+t.split('\\n').reverse().join('\\n'));}
wire('ta');"""))

TOOLS.append(T("unicode-inspector", "Text", "Unicode Inspector",
 "Every symbol with its U+hex point, HTML entity and decimal code",
 f("ta", "Text") + btns("Inspect", "Copy"),
 """function run(){const t=V('ta')||'';const o=[];const seen={};
for(const ch of t){if(seen[ch])continue;seen[ch]=1;const c=ch.codePointAt(0);
o.push(ch+'  U+'+c.toString(16).toUpperCase().padStart(4,'0')+'  &#'+c+';  '+c);}
OUT(o.join('\\n')||'—');}
wire('ta');"""))

WORDS = "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua enim ad minim veniam quis nostrud exercitation ullamco laboris nisi aliquip ex ea commodo consequat duis aute irure in reprehenderit voluptate velit esse cillum eu fugiat nulla pariatur excepteur sint occaecat cupidatat non proident sunt culpa qui officia deserunt mollit anim id est laborum".split()
TOOLS.append(T("lorem-generator", "Text", "Lorem Ipsum Generator",
 "Classical Latin filler in tidy sentences — pick count",
 '<div class="row">' + num("n", "Sentences", "3") + '</div>' + btns("Generate", "Copy"),
 """function run(){var W="%s";var w=W.split(' ');var n=Math.min(20,parseInt(V('n')||'3',10)||3);var o=[];
for(var s=0;s<n;s++){var len=8+Math.floor(Math.random()*9);var p=[];
for(var i=0;i<len;i++){p.push(w[Math.floor(Math.random()*w.length)]);}
var s2=p.join(' ');s2=s2[0].toUpperCase()+s2.slice(1)+'.';o.push(s2);}OUT(o.join('\\n\\n'));}
run();wire('n');""" % " ".join(WORDS)))

TOOLS.append(T("palindrome-checker", "Text", "Palindrome Checker",
 "Tests a word or sentence forwards and backwards — plus mirror result",
 f("ta", "Candidate") + btns("Check", "Copy"),
 """function run(){const t=(V('ta')||'').toLowerCase();const c=t.replace(/[^a-z0-9]/g,'');const r=c.split('').reverse().join('');
OUT((c.length<2?'(type at least two letters)\\n\\n':'')+'cleaned: '+c+'\\nreversed: '+r+'\\n\\n'+(c===r?'✔ palindrome':'✖ not a palindrome'));}
wire('ta');"""))

WLIST = "amber anchor basil bison cinder coral cove cypress ember fable falcon fern flint geyser glade granite harbor heron indigo ivory jasper juniper kettle lagoon larch mango maple mesa meteor nectar nimbus opal orchid pebble pilot prairie quill quiver ravine reef sable saffron sapling summit tamarind teal thicket tundra umbra umber violet walnut willow xanadu yarrow zenith zephyr"
TOOLS.append(T("random-words", "Text", "Random Word List",
 "75 seed words for passphrases, usernames and naming",
 '<div class="row">' + num("n", "How many", "6") + '</div>' + btns("Draw", "Copy"),
 """function run(){var W="%s".split(' ');var n=Math.min(50,parseInt(V('n')||'6',10)||6);var p=[];
for(var i=0;i<n;i++){p.push(W[Math.floor(Math.random()*W.length)]);}OUT(p.join(' '));}
run();wire('n');""" % " ".join(WLIST.split())))

# ---------- Encoding & Hashing ----------
TOOLS.append(T("hex-text-codec", "Encoding & Hashing", "Hex ⇄ Text",
 "Latin-1/UTF-8 round trip in both directions — decode/encode on one box",
 f("ta", "Hex or text") + btns("Decode", "Encode", "Copy"),
 """function run(){var t=V('ta')||'';if(!t){OUT('');return;}
try{if(/^[0-9A-Fa-f\\s]+$/.test(t)&&t.replace(/\\s+/g,'').length%2===0&&t.replace(/\\s+/g,'').length>=4){
var hx=t.replace(/\\s+/g,'');var b=new Uint8Array(hx.length/2);
for(var i=0;i<b.length;i++)b[i]=parseInt(hx.substr(i*2,2),16);OUT(new TextDecoder().decode(b));}
else{OUT([...new TextEncoder().encode(t)].map(x=>x.toString(16).toUpperCase()).join(' '));}}
catch(e){OUT('ERROR: '+e.message);}}
wire('ta');"""))

TOOLS.append(T("bin-text-codec", "Encoding & Hashing", "Binary ⇄ Text",
 "8-bit bytes both ways — type text to see bits, or bits to get text back",
 f("ta", "Binary or text") + btns("Decode", "Encode", "Copy"),
 """function run(){var t=V('ta')||'';if(!t){OUT('');return;}
try{if(/^[01 ]+$/.test(t.trim())&&t.replace(/\\s+/g,'').length>=4){
OUT(t.trim().split(/\\s+/).filter(x=>x.length===8).map(x=>String.fromCodePoint(parseInt(x,2))).join('')||'give 8-bit groups');}
else{OUT([...new TextEncoder().encode(t)].map(x=>x.toString(2).padStart(8,'0')).join(' '));}}
catch(e){OUT('ERROR: '+e.message);}}
wire('ta');"""))

TOOLS.append(T("rot13-caesar", "Encoding & Hashing", "ROT13 + Caesar",
 "ROT13 for a wink, Caesar with any shift for a wink at the Romans",
 f("ta", "Text") + '<div class="row">' + num("sh", "Shift (ROT13 = 13)", "13") + '</div>' + btns("Encrypt", "Decrypt", "Copy"),
 """var mode='enc';
function shift(t,s){return t.replace(/[a-z]/gi,function(c){var base=(c>='A'&&c<='Z')?65:97;
return String.fromCodePoint((((c.toUpperCase().charCodeAt(0)-65)-0+ (mode==='dec'?(26-(s%26)):(s%26)))+ (base===97?0:0))%26 + (base===65?65:97));});}
function run(){var t=V('ta')||'';var s=((parseInt(V('sh'),10)||13)%26+26)%26;
OUT(shift(t,s)+(s===13&&mode!=='dec'?'\\n\\n(that was ROT13 — applying it again undoes it)':''));}
document.addEventListener('click',e=>{if(e.target.closest('[data-act=encrypt]'))mode='enc';if(e.target.closest('[data-act=decrypt]'))mode='dec';});"""))

TOOLS.append(T("vigenere", "Encoding & Hashing", "Vigenère Cipher",
 "Polyalphabetic tabula recta with a keyword — decode inverts it automatically",
 f("ta", "Text") + '<div class="row">' + f("kw", "Keyword", "input", 'value="lemon"') + '</div>' + btns("Encrypt", "Decrypt", "Copy"),
 """var mode='enc';
document.addEventListener('click',e=>{if(e.target.closest('[data-act=encrypt]'))mode='enc';if(e.target.closest('[data-act=decrypt]'))mode='dec';});
function run(){var t=V('ta')||'';var k=(V('kw')||'lemon').toUpperCase().replace(/[^A-Z]/g,'');
if(!k){OUT('need a letter keyword');return;}var j=0,o='';
for(const c of t){if(/[a-z]/i.test(c)){const s=k.charCodeAt(j++%k.length)-65;var B=c.toUpperCase().charCodeAt(0)-65;
var e=(mode==='dec'?(B-s+26)%26:(B+s)%26)+65;o+=String.fromCodePoint(e+(c===c.toLowerCase()?32:0));}else o+=c;}
OUT(o);}
wire(['ta','kw']);"""))

TOOLS.append(T("checksum", "Encoding & Hashing", "Checksum (CRC32 / FNV-1a)",
 "Non-cryptographic checksums — quick integrity and dictionary lookup keys",
 f("ta", "Text") + btns("Hash", "Copy"),
 """function run(){var t=V('ta')||'';
var T=[];for(var i=0;i<256;i++){var c=i;for(var k=0;k<8;k++)c=(c&1)?(0xEDB88320^(c>>>1)):(c>>>1);T[i]=c>>>0;}
var crc=0xFFFFFFFF;for(const ch of new TextEncoder().encode(t)){crc=(T[(crc^ch)&0xFF]^(crc>>>8))>>>0;}crc=(crc^0xFFFFFFFF)>>>0;
var fnv=0x811C9DC5>>>0;for(const ch of new TextEncoder().encode(t)){fnv=Math.imul(fnv^ch,0x01000193)>>>0;}
OUT('CRC32   '+crc.toString(16).toUpperCase().padStart(8,'0')+'\\nFNV-1a  '+fnv.toString(16).toUpperCase().padStart(8,'0'));}
wire('ta');run();"""))

TOOLS.append(T("entropy-checker", "Encoding & Hashing", "Entropy & Repeat Scanner",
 "Shannon bits/char and run-length scan — how compressible and how guessable",
 f("ta", "Text") + btns("Scan", "Copy"),
 """function run(){var t=V('ta')||'';if(!t){OUT('');return;}var f={};for(const c of t)f[c]=(f[c]||0)+1;
var H=0,n=t.length;for(const k in f){var p=f[k]/n;H+=-p*Math.log2(p);}
var runs=1;for(var i=1;i<t.length;i++)if(t[i]!==t[i-1])runs++;
OUT('entropy  '+H.toFixed(3)+' bits/char\\nunique   '+Object.keys(f).length+' / '+n+'\\nruns     '+runs+(n>0&&H<2.5?'  (very repetitive)':''));}
wire('ta');"""))

TOOLS.append(T("unicode-escaper", "Encoding & Hashing", "Unicode Escaper",
 "Escape and unescape \\uXXXX, HTML entities and URL percent encoding",
 f("ta", "Text or escape") + btns("Escape", "Unescape", "Copy"),
 """function run(){var t=V('ta')||'';
if(/&#(x[0-9a-f]+|[0-9]+);|\\\\u[0-9a-f]{4}/i.test(t)){try{OUT(
 t.replace(/&#x([0-9a-f]+);/gi,(m,h)=>String.fromCodePoint(parseInt(h,16)))
 .replace(/&#([0-9]+);/g,(m,d)=>String.fromCodePoint(+d))
 .replace(/\\\\u([0-9a-f]{4})/gi,(m,h)=>String.fromCodePoint(parseInt(h,16))));return;}catch(e){}}
OUT(t.split('').map(c=>{var c0=c.charCodeAt(0);return (c0<128&&/[\\w \\n]/.test(c))?c:'&#'+c0+';';}).join(''));}
wire('ta');"""))
