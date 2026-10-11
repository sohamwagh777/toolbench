# -*- coding: utf-8 -*-
"""Text category tools (15)."""
from gen_helpers import mkpage

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
    t = mkpage(i, "Text", title, desc, body, js)
    t["copy"] = True
    return t

TOOLS = []

# 1 Word / character counter
TOOLS.append(page("word-counter", "Word & Character Counter",
    "Live counts: characters, words, sentences, paragraphs, lines, reading time.",
    '<section class="card"><p class="hint">Counts update as you type.</p>' + f("ta", "Text") + '<div id="out"></div></section>',
    """function run(){const t=V('ta')||'';
const w=(t.match(/\\S+/g)||[]).length;
const s=(t.match(/[^.!?\n]+[.!?]+(?=\\s|$)/g)||[]).length;
const p=(t.match(/[^\\n]+/g)||[]).filter(x=>x.trim()).length;
const rt=Math.max(1,Math.round(w/200*10)/10);
OUT([['Characters (no spaces)',(t.match(/[^\\s]/g)||[]).length],['Characters (all)',t.length],['Words',w],['Sentences',s],['Paragraphs',p],['Reading time',rt+' min']].map(r=>r[0].padEnd(20,' ')+' '+r[1]).join('\\n'))}
if(!V('ta')){$('#ta').value="Paste or type text here. Counts update live as you type — words, sentences, paragraphs and reading time."}
run();wire('ta');"""))

# 2 Lorem generator
WORDS = "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua enim ad minim veniam quis nostrud exercitation ullamco laboris nisi aliquip ex ea commodo consequat duis aute irure in reprehenderit voluptate velit esse cillum eu fugiat nulla pariatur excepteur sint occaecat cupidatat non proident sunt culpa qui officia deserunt mollit anim id est laborum".split()
TOOLS.append(page("lorem-generator", "Lorem Ipsum Generator",
    "Classical Latin filler with correct-ish grammar. Choose sentences or words.",
    '<section class="card"><div class="row">' + sel("mode", "Mode", [("sent", "Sentences"), ("word", "Words")]) + f("count", "Count", "number", 'value="4" min="1" max="200"') + '</div><div class="row">' + btns("Generate", "Copy") + '</div><div id="out"></div></section>',
    "const W=" + repr(WORDS).replace("'", '"') + """;
function rnd(a){return Math.floor(Math.random()*a)}
function sentence(){const n=6+rnd(10);const w=[];for(let i=0;i<n;i++)w.push(W[rnd(W.length)]);const s=w.join(' ');return s[0].toUpperCase()+s.slice(1)+'.'}
function run(){const m=V('mode'),c=Math.max(1,Math.min(200,parseInt(V('count'))||4));const out=[];
if(m==='sent'){for(let i=0;i<c;i++)out.push(sentence())}else{const w=[];for(let i=0;i<c;i++)w.push(W[rnd(W.length)]);out.push(w.join(' '))}
OUT(out.join('\\n\\n'))}
run();wire(['mode','count']);"""))

# 3 Diff
TOOLS.append(page("text-diff", "Text Diff",
    "Line-by-line diff of two texts with + / - markers (LCS match).",
    '<section class="card"><div class="row">' + f("a", "Text A") + f("b", "Text B") + '</div>' + btns("Diff", "Copy") + '<div id="out"></div></section>',
    """function run(){const A=(V('a')||'').split('\\n'),B=(V('b')||'').split('\\n');
const n=A.length,m=B.length;let prev=Array(m+1).fill(0);
for(let i=1;i<=n;i++){const cur=Array(m+1).fill(0);
 for(let j=1;j<=m;j++){cur[j]=(A[i-1]===B[j-1])?prev[j-1]+1:Math.max(prev[j],cur[j-1])}
 prev=cur}
const ops=[];let i=n,j=m;
while(i>0&&j>0){if(A[i-1]===B[j-1]){ops.push(['  ',A[i-1]]);i--;j--}else if(prev[i][j-1]!==undefined&&prev[i][j-1]>=prev[i-1][j]){ops.push(['+ ',B[j-1]]);j--}else{ops.push(['- ',A[i-1]]);i--}}
while(i>0){ops.push(['- ',A[i-1]]);i--}while(j>0){ops.push(['+ ',B[j-1]]);j--}
ops.reverse();const same=ops.filter(o=>o[0]==='  ').length;
OUT('match '+Math.round(100*same/ops.length)+'%\\n'+ops.map(o=>o[0]+o[1]).join('\\n'))}
if(!V('a')){$('#a').value="alpha\\nbeta\\ngamma"}if(!V('b')){$('#b').value="alpha\\nbeta major\\ngamma"}run();wire(['a','b']);"""))

# 4 Name generator (nickname anagram)
TOOLS.append(page("name-generator", "Team Name Generator",
    "Deterministic team/nickname generator seeded from your words — same seed, same name.",
    '<section class="row card"><div class="fld grow">' + f("seed", "Seed word") + '</div><button data-act="run">Generate</button></section><section class="card"><div id="out"></div></section>',
    """const P="Iron Velvet Solar Cobalt Neon Lunar Ember Arctic Pixel Mystic Crimson Quantum".split(" ");
const S="Fox Forge Foundry Labs Works Syndicate Protocol Collective Atelier Station Network Guild".split(" ");
function h(s){let h=2166136261;for(const c of s.toLowerCase()){h^=c.charCodeAt(0);h=Math.imul(h,16777619)>>>0}return h>>>0}
function run(){const s=V('seed')||'seed';let x=h(s);const pick=a=>{x=(Math.imul(x,1664525)+1013904223)>>>0;return a[x%a.length]};
const l=[...new Array(5)].map((_,k)=>pick(P)+' '+pick(S)).map((n,k)=>(k+1)+'. '+n);OUT(l.join('\\n'))}
run();wire('seed');"""))

# 5 Regex replace
TOOLS.append(page("regex-replace", "Regex Replace",
    "Find/replace with regex flags, $1 captures, live match count and per-line hits.",
    '<section class="card"><div class="row">' + f("pat", "Pattern") + f("flags", "Flags", "text", 'value="gm" placeholder="g i m s"') + '</div><div class="row">' + f("rep", "Replacement (use $1)") + '</div>' + f("ta", "Text") + '<div class="row" style="margin-top:12px">' + btns("Replace", "Copy") + '</div><div id="out"></div></section>',
    """if(!V('pat')){$('#pat').value="(\\w+) (\\w+)"}if(!V('rep')){$('#rep').value="$2 $1"}if(!V('ta')){$('#ta').value="hello world\\nfoo bar"}
function run(){try{const re=new RegExp(V('pat')||'',V('flags')||'gm');OUT(V('ta').replace(re,V('rep')))}catch(e){OUT('RegExp error: '+e.message)}}
run();wire(['pat','flags','rep','ta']);"""))

# 6 Slug generator
TOOLS.append(page("slug-generator", "Slug Generator",
    "URL-safe slugs: transliterates accents, strips emoji, keeps any language readable.",
    '<section class="card">' + f("ta", "Text") + '<div class="row" style="margin-top:12px">' + sel("sep", "Separator", [("-", "hyphen -"), ("_", "underscore _"), ("", "none")]) + btns("Generate", "Copy") + '</div><div id="out"></div></section>',
    """const M={"á":"a","à":"a","â":"a","ä":"a","ã":"a","å":"a","é":"e","è":"e","ê":"e","ë":"e","í":"i","ì":"i","î":"i","ï":"i","ó":"o","ò":"o","ô":"o","ö":"o","õ":"o","ů":"u","ú":"u","ü":"u","ñ":"n","ç":"c","ý":"y","þ":"th","ø":"o","đ":"d","ł":"l"};
function run(){const s=V('ta')||'';const sep=V('sep');let s2='';
for(const c of s.toLowerCase()){s2+=(M[c]||c)}
s2=s2.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').replace(/[^a-z0-9]+/g,sep||'-').replace(/^-+|-+$/g,'');
OUT(s2)}
if(!V('ta')){$('#ta').value="Crème Brûlée — Straße!"}run();wire(['ta','sep']);"""))

# 7 Line tools
TOOLS.append(page("line-tools", "Line Tools",
    "Sort, reverse, dedupe, trim, number, remove blanks — per line.",
    '<section class="card"><div class="row">' + sel("act", "Operation", [["dedupe","Dedupe"],["sort","Sort A→Z"],["sortn","Sort numeric"],["reverse","Reverse"],["trim","Trim edges"],["number","Add numbers"],["denumber","Strip numbers"],["blank","Remove blanks"],["freq","Word frequency"]]) + '</div>' + f("ta", "Lines") + '<div class="row" style="margin-top:12px">' + btns("Run", "Copy") + '</div><div id="out"></div></section>',
    """function run(){let L=(V('ta')||'').split('\\n');const a=V('act');let o=[];
if(a==='dedupe')o=[...new Set(L)];
else if(a==='sort')o=[...L].sort();
else if(a==='sortn')o=[...L].sort((x,y)=>(parseFloat(x)||0)-(parseFloat(y)||0));
else if(a==='reverse')o=[...L].reverse();
else if(a==='trim')o=L.map(x=>x.trim());
else if(a==='number')o=L.map((x,i)=>(i+1)+'. '+x);
else if(a==='denumber')o=L.map(x=>x.replace(/^\\s*\\d+[.)\\s]+/,''));
else if(a==='blank')o=L.filter(x=>x.trim());
else if(a==='freq'){const m={};(V('ta').toLowerCase().match(/[a-zà-ÿ0-9']+/g)||[]).forEach(w=>m[w]=(m[w]||0)+1);
o=Object.entries(m).sort((x,y)=>y[1]-x[1]).slice(0,50).map(e=>e[1]+'\\t'+e[0])}
OUT(o.join('\\n'))}
if(!V('ta')){$('#ta').value="banana\\napple\\nbanana\\n\\n cherry "}run();wire(['ta','act']);"""))

# 8 Case converter
TOOLS.append(page("case-converter", "Case Converter",
    "UPPER, lower, Title, Sentence, camelCase, PascalCase, snake_case, kebab, aLtErNaTiNg.",
    '<section class="card"><div class="row">' + sel("m", "Case", [["upper","UPPER"],["lower","lower"],["title","Title Case"],["sentence","Sentence case"],["camel","camelCase"],["pascal","PascalCase"],["snake","snake_case"],["kebab","kebab-case"],["alt","aLtErNaTiNg"]]) + '</div>' + f("ta", "Text") + '<div class="row" style="margin-top:12px">' + btns("Convert", "Copy") + '</div><div id="out"></div></section>',
    """const isL=c=>/[a-zà-ÿ]/.test(c);
function run(){const t=V('ta')||'';const m=V('m');const W=t.match(/[^\\s_-]+|[\\s_-]+/g)||[];let o='';
if(m==='upper')o=t.toUpperCase();
else if(m==='lower')o=t.toLowerCase();
else if(m==='title')o=t.replace(/([^\\s]+)/g,x=>x[0].toUpperCase()+x.slice(1).toLowerCase());
else if(m==='sentence')o=(t[0]||'').toUpperCase()+t.slice(1).toLowerCase();
else if(m==='alt')o=[...t].map((c,i)=>i%2?c.toUpperCase():c.toLowerCase()).join('');
else{const w=t.replace(/([a-z])([A-Z])/g,'$1 $2').split(/[\\s_-]+/).filter(Boolean).map(x=>x[0].toUpperCase()+x.slice(1).toLowerCase());
if(m==='camel')o=w.map(x=>x[0].toLowerCase()+x.slice(1)).join('');
else if(m==='pascal')o=w.join('');else if(m==='snake')o=w.join('_').toLowerCase();else if(m==='kebab')o=w.join('-').toLowerCase()}
OUT(o||'\\u2014')}
if(!V('ta')){$('#ta').value="hello World from ToolBench"}run();wire(['m','ta']);"""))

# 9 Palindrome checker
TOOLS.append(page("palindrome-checker", "Palindrome Checker",
    "Checks words, phrases and numbers, ignoring punctuation and spacing.",
    '<section class="card">' + f("ta", "Text") + '<div class="row" style="margin-top:12px">' + btns("Check", "Copy") + '</div><div id="out"></div></section>',
    """function run(){const t=(V('ta')||'').toLowerCase().replace(/[^a-zà-ÿ0-9]+/gi,'');
const rev=[...t].reverse().join('');
const words=(V('ta')||'').trim().split(/\\s+/).filter(w=>{const c=w.toLowerCase().replace(/[^a-z0-9]/g,'');const r=[...c].reverse().join('');return c.length>2&&c===r});
OUT((t.length&&t===rev?'YES — palindrome\\n':'NO — not a palindrome\\n')+(words.length?'palindromic words: '+words.join(', '):''))}
if(!V('ta')){$('ta')&&0;$('#ta').value="Never odd or even"}run();wire('ta');"""))

# 10 Typo check
TOOLS.append(page("typo-checker", "Typo Scanner",
    "Flags doubled words, doubled punctuation, and common misspelling pairs (their/there, its/it's…).",
    '<section class="card">' + f("ta", "Text") + '<div class="row" style="margin-top:12px">' + btns("Scan", "Copy") + '</div><div id="out"></div></section>',
    """const P=[["\\btheir\\b","their — 'they' own; 'there' = place; 'they're' = they are"],["\\bthen\\b(?!\\s*\\?|\\s*\\.)","check 'then' vs 'than'"],["\\bfeet\\b","feet (unit) vs feat (feat/deed)"],["\\bquiet\\b","quiet vs quite"],["\\bnowa days\\b",null]];
const FIX={";,":",",",;":";",",,":",","..":"."," ,":",",' :':':'," !":"!"," ?":"?"};
function run(){const t=V('ta')||'';const f=[];
(t.match(/\\b(\\w+)\\s+\\1\\b/gi)||[]).forEach(x=>{const w=x.split(/\\s+/)[0];if(!/^(that|had|the)$/i.test(w))f.push('doubled word: "'+x+'"')});
Object.keys(FIX).forEach(k=>{if(t.includes(k))f.push('spacing/punct: "'+k+'" → "'+FIX[k]+'"')});
P.forEach(p=>{const m=t.match(new RegExp(p[1],'gi'));if(m)f.push(p[1].replace(/\\(?!.*\\)/g,'')+' — check: '+p[2])});
OUT(f.length?('flagged '+f.length+' issue(s):\\n'+f.map(x=>'· '+x).join('\\n')):'looks clean — no common typos found')}
if(!V('ta')){$('#ta').value="This is is about their house; the cat, and it's food is near the feet of quiet Mr. Ender."}run();wire('ta');"""))

# 11 Random word generator
TOOLS.append(page("random-words", "Random Word Generator",
    "English word pool with number/emoji garnish options — good for usernames and passphrases.",
    '<section class="card"><div class="row">' + f("count", "Count", "number", 'value="6" min="1" max="100"') + sel("gar", "Garnish", [["", "none"], ("num","with digits"), ("sep","hyphenated")]) + '</div>' + btns("Generate", "Copy") + '<div id="out"></div></section>',
    """const W="amber anchor atlas basil birch breeze cinder cobalt coral cypress ember fable falcon fjord garnet glacier harbor hazel ironviolet juniper kestrel lapis lotus lumen maple mesa nimbus onyx opal orchid pebble phoenix quartz raven ridge saffron sapphire thicket timber topper umbrella velvet vertex willow zenith zephyr".split(" ");
function run(){const c=Math.min(100,parseInt(V('count'))||6),g=V('gar');const out=[];
for(let i=0;i<c;i++){let w=W[Math.floor(Math.random()*W.length)]+'-'+W[Math.floor(Math.random()*W.length)];if(g==='num')w+=Math.floor(Math.random()*90+10);out.push(w)}
OUT(out.join('\\n'))}
run();wire(['count','gar']);"""))

# 12 Markdown preview → (see dev) ; here: Letter counter — keep? swap to Text: Text Reverser (word/char/line)
TOOLS.append(page("text-reverser", "Text Reverser",
    "Reverse characters, words or lines; also strips repeated whitespace.",
    '<section class="card"><div class="row">' + sel("m", "Reverse", [["char","Characters"],["word","Words"],["line","Lines"]]) + '</div>' + f("ta", "Text") + '<div class="row" style="margin-top:12px">' + btns("Run", "Copy") + '</div><div id="out"></div></section>',
    """function run(){const t=V('ta')||'';const m=V('m');
if(m==='char')OUT([...t].reverse().join(''));
else if(m==='word')OUT(t.split(/\\s+/).reverse().join(' '));
else OUT(t.split('\\n').reverse().join('\\n'))}
if(!V('ta')){$('#ta').value="Hello, world!"}run();wire(['m','ta']);"""))

# 13 Unicode inspector
TOOLS.append(page("unicode-inspector", "Unicode Inspector",
    "Per-codepoint U+… inspection with names for common blocks, emoji clusters kept whole.",
    '<section class="card">' + f("ta", "Text") + '<div class="row" style="margin-top:12px">' + btns("Inspect", "Copy") + '</div><div id="out"></div></section>',
    """const B=[[0x0000,0x007F,'Basic Latin'],[0x0080,0x036F,'Latin Ext / IPA'],[0x0370,0x03FF,'Greek'],[0x0400,0x04FF,'Cyrillic'],[0x0590,0x05FF,'Hebrew'],[0x0600,0x06FF,'Arabic'],[0x0900,0x097F,'Devanagari'],[0x1000,0x109F,'Myanmar'],[0x1100,0x11FF,'Hangul Jamo'],[0x1780,0x17FF,'Khmer'],[0x1E00,0x1EFF,'Latin Ext Add'],[0x2000,0x206F,'General Punct'],[0x2190,0x21FF,'Arrows'],[0x2500,0x257F,'Box Drawing'],[0x2600,0x26FF,'Misc Symbols'],[0x3040,0x309F,'Hiragana'],[0x30A0,0x30FF,'Katakana'],[0x3400,0x4DBF,'CJK Ext A'],[0x4E00,0x9FFF,'CJK'],[0xAC00,0xD7AF,'Hangul Syll.'],[0xF900,0xFAFF,'CJK Compat'],[0xFE00,0xFE0F,'Variation Sel.'],[0x1F300,0x1FAFF,'Emoji & Symbols'],[0x20000,0x2FA1F,'CJK Ext B+']];
function block(cp){for(const b of B)if(cp>=b[0]&&cp<=b[1])return b[2];return cp>0xFFFF?'Supplementary':'Unknown'}
function run(){const t=[...(V('ta')||'')];const o=[];
for(const c of t){const cps=[...c].map(ch=>'U+'+ch.codePointAt(0).toString(16).toUpperCase().padStart(4,'0'));
o.push(c+'\\tU+'+cps.join('+')+'\\t'+block(c.codePointAt(0)))}
OUT('char\\tcode\\tblock\\n'+o.join('\\n')+'\\n\\n'+t.length+' grapheme clusters')}
if(!V('ta')){$('#ta').value="café → ç '👨‍👩‍👧'"}run();wire('ta');"""))

# 14 Letter frequency? skip -> Text Spinner? Do: Text Obfuscator (ROT13-free) -> better: "Case-insensitive line finder (grep)"
TOOLS.append(page("grep", "Line Finder (grep)",
    "Search lines with regex or literal, case-insensitive option, shows line numbers.",
    '<section class="card"><div class="row">' + f("pat", "Pattern") + sel("m", "Mode", [["lit","Literal"],["re","Regex"]]) + '<div class="fld"><label for="cs">Case</label><select id="cs"><option value="1" selected>Ignore case</option><option value="0">Match case</option></select></div></div>' + f("ta", "Text") + '<div class="row" style="margin-top:12px">' + btns("Find", "Copy") + '</div><div id="out"></div></section>',
    """function run(){const p=V('pat')||'';if(!p)return OUT('');let re;
try{re=(V('m')==='re')?new RegExp(p,V('cs')?'im':'im'.replace('i','')):(V('cs')?new RegExp(p.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&'),'i'):new RegExp(p.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&')))}
catch(e){return OUT('bad regex: '+e.message)}
const hits=[];V('ta').split('\\n').forEach((l,i)=>{if(re.test(l))hits.push((i+1)+': '+l)});
OUT(hits.length?hits.join('\\n'):'no matches')}
if(!V('pat')){$('#pat').value='error'}if(!V('ta')){$('#ta').value="line one\\nAn Error here\\nall good"}run();wire(['pat','ta','cs','m']);"""))

# 15 Text Repetitor — placeholder replaced by "Word Scramble (anagram solver)"
TOOLS.append(page("text-shuffle", "Text Scrambler",
    "Deterministic char/word shuffle (seedable) — for quick codes and teasers.",
    '<section class="card"><div class="row">' + f("m", "Mode", "text", 'value="char" placeholder="char / word / line"') + f("seed", "Seed", "text", 'value="42"') + '</div>' + f("ta", "Text") + '<div class="row" style="margin-top:12px">' + btns("Scramble", "Unscramble", "Copy") + '</div><div id="out"></div></section>',
    """function h(s){let h=2166136261;for(const c of s){h^=c.charCodeAt(0);h=Math.imul(h,16777619)>>>0}return h>>>0}
function shuf(a,seed){let x=h(seed);const b=[...a];for(let i=b.length-1;i>0;i--){x=(Math.imul(x,1664525)+1013904223)>>>0;const j=x%(i+1);[b[i],b[j]]=[b[j],b[i]]}return b}
function run(){const t=V('ta')||'';const m=V('m')||'char';const seed=V('seed')||'0';
if(m==='char')OUT(shuf([...t],seed).join(''));
else if(m==='word')OUT(shuf(t.split(/\\s+/),seed).join(' '));
else OUT(shuf(t.split('\\n'),seed).join('\\n'))}
if(!V('ta')){$('#ta').value="meet me at eight sharp"}run();wire(['m','seed','ta']);"""))
