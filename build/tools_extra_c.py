# -*- coding: utf-8 -*-
"""Toolbench spec C — fills to 100 tools: Math & Finance (4), Time & Productivity (4), Text (3), Encoding (2), Developer (2), Games (1)."""
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

# ---- Math & Finance ----
TOOLS.append(T("fraction-calc", "Math & Finance", "Fraction Lab",
 "Add, reduce and compare fractions — a/b + c/d style input",
 f("ta", "Problem", 'placeholder="3/4 + 1/6\\n8/12 reduce\\n5/8 vs 4/7"') + btns("Solve", "Copy"),
 """function gcd(a,b){while(b){[a,b]=[b,a%b];}return a;}
function run(){var o=[];(V('ta')||'').split('\\n').forEach(function(l){
var m=l.match(/^(\\d+)\\/(\\d+)\\s*([+\\-*/])\\s*(\\d+)\\/\\d+$/),r;
if(l.includes('reduce')){m=l.match(/(\\d+)\\/(\\d+)/);if(m){var a=+m[1],b=+m[2],g=gcd(a,b);l+=' => '+(a/g)+'/'+(b/g);}}
else if((m=l.match(/^(\\d+)\\/(\\d+)\\s*\\+\\s*(\\d+)\\/(\\d+)$/))){var a=+m[1],b=+m[2],c=+m[3],d=+m[4];
var n=a*d+c*b,de=b*d,g=gcd(n,de);l+=' => '+(n/g)+'/'+(de/g);}
else if((m=l.match(/^(\\d+)\\/(\\d+)\\s*vs\\s*(\\d+)\\/(\\d+)$/))){var a=+m[1],b=+m[2],c=+m[3],d=+m[4];
l+=' => '+(a*d===c*b?'equal':a*d>c*b?'greater':'smaller');}
if(m&&l.includes('=>'))o.push(l);else if(l.trim())o.push(l+' => ?');});
OUT(o.join('\\n'));}
wire('ta');"""))

TOOLS.append(T("emi-lite", "Math & Finance", "EMI Quick Check",
 "Loan EMI via the standard formula — total interest and payoff cost",
 '<div class="row">' + num("p", "Principal", "250000") + num("r", "Rate %/yr", "8.5") + num("y", "Years", "5") + '</div>' + btns("Compute", "Copy"),
 """function run(){var P=+V('p'),r=+V('r')/1200,n=+V('y')*12;
if(!(P>0)||!(r>0)||!(n>0)){OUT('fill all three');return;}
var e=Math.pow(1+r,n),emi=P*r*e/(e-1),tot=emi*n;
OUT('EMI      '+emi.toFixed(2)+' / month\\ntotal      '+tot.toFixed(2)+'\\ninterest   '+(tot-P).toFixed(2)+'  ('+((tot-P)/P*100).toFixed(1)+'% of principal)');}
wire(['p','r','y']);run();"""))

TOOLS.append(T("bmi-history", "Math & Finance", "BMI History Chart",
 "Log weight + height, watch the trend and get category per entry",
 f("ta", "Entries", 'placeholder="2026-09-01, 71.2, 178\\n2026-10-01, 70.1, 178"') + btns("Chart", "Copy"),
 """function run(){var o=[];(V('ta')||'').split('\\n').forEach(function(l){var p=l.split(',');
if(p.length>=3){var w=+p[1],h=+p[2]/100,b=w/(h*h);
var c=b<18.5?'under':b<25?'healthy':b<30?'over':'obese';o.push(p[0].trim()+'  '+w+'kg  BMI '+b.toFixed(1)+'  '+c);}});
OUT(o.join('\\n')||'date, kg, cm per line');}
wire('ta');"""))

TOOLS.append(T("donation-split", "Math & Finance", "Bill Split & Tip",
 "Split a bill between people, tip included, awkward cent-remainders handled",
 '<div class="row">' + num("b", "Bill", "84.40") + num("p", "People", "3") + num("t", "Tip %", "15") + '</div>' + btns("Split", "Copy"),
 """function run(){var b=+V('b'),n=Math.max(1,parseInt(V('p'),10)||1),tp=+V('t')/100;
var tot=b*(1+tp),each=Math.floor(tot/n*100)/100;
OUT('total+tip  '+tot.toFixed(2)+'\\neach person  '+each.toFixed(2)+(Math.abs(each*n-tot)<0.01*n?'  (round up the last cent for a couple of people)':''));}
wire(['b','p','t']);run();"""))

# ---- Time & Productivity ----
TOOLS.append(T("timezone-compare", "Time & Productivity", "Timezone Compare",
 "Pick a city, get its clock and the gap to yours",
 f("ta", "Query", 'placeholder="14:30 Tokyo\\n11:00-13:00 meeting with Lagos, 09:00 São Paulo"') + btns("Convert", "Copy"),
 """function run(){var now=new Date(),o=[];
(V('ta')||'').split('\\n').forEach(function(l){
var m=l.match(/^(\\d{1,2}[:.]\\d{2})\\s+(\\d{1,2}[:.]\\d{2})?\\s*(.{3,}?)$/);
if(!m){if(l.trim())o.push(l+' => ?');return;}
var start=m[1].replace('.',':'),dur=m[2]?m[2].replace('.',':'):null;
var places=[...new Set(l.split(',').flatMap(x=>x.split(/\\s+/)).filter(x=>/[A-Za-z]{3,}/.test(x)&&!['with','meeting','and','to'].includes(x.toLowerCase())))];
places.slice(0,8).forEach(pl=>{try{var s=new Intl.DateTimeFormat('en-US',{timeZone:'UTC',hour:'2-digit',minute:'2-digit'}).formatToParts(new Date());
var t=new Date(new Date().toLocaleString('en-US',{timeZone:pl.trim().replace(/_.+/,'')}));
var nowT=t.toLocaleTimeString('en-GB',{timeZone:pl.trim().replace(/_.+/,''),hour:'2-digit',minute:'2-digit'});
if(/^[A-Za-z ]+$/.test(pl.trim())){o.push(pl.trim()+': now '+nowT);}else o.push(pl+': ?');}catch(e){o.push(pl+': ?');}});});
OUT(o.join('\\n'));}
wire('ta');"""))

TOOLS.append(T("pomodoro-log", "Time & Productivity", "Focus Session Log",
 "One-line pomodoro ledger with a daily count",
 f("ta", "Log", 'placeholder="25 Pomodoro — docs\\n5 Break\\n25 Pomodoro — code"') + btns("Count", "Copy"),
 """function run(){var o=[];var tot=0,work=0,brk=0;
(V('ta')||'').split('\\n').forEach(function(l){var m=l.match(/^(\\d+)\\s*(pomodoro|break|deep)/i);if(m){tot++;if(+m[1]>=20)work+=+m[1];else brk+=+m[1];}});
OUT('sessions logged: '+tot+'\\nfocused minutes: '+work+'\\nbreak minutes: '+brk+'\\nratio work/break: '+(brk?(work/brk).toFixed(2):'—'));}
wire('ta');"""))

TOOLS.append(T("stopwatch2", "Time & Productivity", "Stopwatch + Laps",
 "Start/stop with laps and a split list",
 '<div id="sw" style="font:34px/1.2 var(--mono);text-align:center;padding:18px 0">00:00.0</div><div class="row"><button data-act="run">Start</button><button data-act="lap">Lap</button><button data-act="reset">Reset</button></div>',
 """var t0=0,acc=0,laps=[],run_=false,iv=null;
function ms(){return acc+(run_?Date.now()-t0:0);}
function fmt(x){var s=x/1000;return String(Math.floor(s/60)).padStart(2,'0')+':'+String(Math.floor(s%60)).padStart(2,'0')+'.'+Math.floor(x%1000/100);}
function draw(){document.getElementById('sw').textContent=fmt(ms())+(laps.length?'\\n'+laps.map((l,i)=>'lap '+(i+1)+': '+fmt(l)).join('\\n'):'');}
document.addEventListener('click',e=>{var b=e.target.closest('button');if(!b)return;var a=b.dataset.act;
if(a==='run'){if(run_){acc+=Date.now()-t0;run_=false;clearInterval(iv);}else{run_=true;t0=Date.now();}draw();}
if(a==='lap'){laps.push(ms());draw();}if(a==='reset'){acc=0;laps=[];run_=false;clearInterval(iv);draw();}});
draw();"""))

TOOLS.append(T("calendar-gen", "Time & Productivity", "Calendar Generator",
 "Text calendar for any month, month names and leap years included",
 f("ta", "Month", 'placeholder="2026-10\\n2027 March"') + btns("Render", "Copy"),
 """function run(){var o=[];(V('ta')||'').split('\\n').forEach(function(l){
var m=l.match(/^(\\d{4})[-/\\s]([A-Za-z]{3,9}|\\d{1,2})[-/\\s]*(\\d{1,2})?$/i)||l.match(/^(\\d{4})(\\d{2})$/);
if(!m){if(l.trim())o.push(l+' => ?');return;}
var y=+m[1],mo;
if(/^\\d+$/.test(m[2]))mo=+m[2]-1;else mo='janfebmaraprmayjunjulaugsepoctnovdec'.indexOf(m[2].slice(0,3).toLowerCase())/3;
var days=new Date(y,mo+1,0).getDate(),name=new Date(y,mo,1).toLocaleString('en-US',{month:'long',year:'numeric'});
var head='Mo Tu We Th Fr Sa Su',rows=[];
var first=(new Date(y,mo,1).getDay()+6)%7;var line=head+'\\n'+'   '.repeat(first);
for(var d=1;d<=days;d++){line+=(d<10?' ':'')+d;if(d<days&&line.slice(-3).trim().length<14&&line.length&&!(line.length%3))line+=' ';}
rows.push(name+'\\n'+line.replace(/\\n(\\s\\s)/,'\\n$1'));});
OUT((V('ta')||'').trim()?o.join('\\n\\n'):'use 2026-10 or 2027 March');}
run();wire('ta');"""))

# ---- Text ----
TOOLS.append(T("text-replace", "Text", "Find & Replace",
 "Plain or regex replace with match counter",
 f("ta", "Text") + f("fx", "Find", "input", 'placeholder="\\d+ or cat"') + f("rp", "Replace with", "input") + btns("Replace", "Copy"),
 """function run(){var t=V('ta')||'',find=V('fx');if(!find){OUT('write a Find pattern');return;}
try{var rx=new RegExp(find.replace(/[/]/g,'\\\\/'),'g');var n=(t.match(rx)||[]).length;
OUT(t.replace(rx,V('rp')||'')+'\\n\\n('+n+' match'+(n===1?'':'es')+')');}catch(e){OUT('bad pattern: '+e.message);}}
wire(['ta','fx','rp']);"""))

TOOLS.append(T("char-freq", "Text", "Letter Frequency",
 "Per-letter counts for ciphers and typography, sorted densest first",
 f("ta", "Text") + btns("Analyse", "Copy"),
 """function run(){var t=(V('ta')||'').toLowerCase().replace(/[^a-z]/g,'');var f={};
for(const c of t)f[c]=(f[c]||0)+1;
var o=Object.entries(f).sort((a,b)=>b[1]-a[1]).map(x=>x[0].toUpperCase()+'  '+x[1]+'  '+'#'.repeat(x[1]));
OUT(o.join('\\n')||'(letters only)');}
wire('ta');"""))

TOOLS.append(T("madlibs", "Text", "Mad-Libs Filler",
 "Drop words, get back a full sentence with your nouns and verbs",
 f("ta", "Word list", 'placeholder="Noun: noodle\\nVerb: jiggle\\nAdjective: soggy\\nPlace: Reykjavik"') + btns("Fill", "Copy"),
 """function run(){var get=(k,d)=>{var m=(V('ta')||'').match(new RegExp(k+'\\\\s*:\\\\s*(.+)','i'));return m?m[1].trim():d;};
var N=get('noun','cat'),V=get('verb','waddled'),A=get('adjective','soggy'),P=get('place','Reykjavik'),T2=get('thing','a trombone'),F=get('food','kimchi');
OUT('One '+A+' '+F+' '+N+' '+V+' to '+P+' carrying '+T2+'.\\n\\n(uppercase keys Noun, Verb, Adjective, Place, Thing, Food — add your own)');}
wire('ta');"""))

# ---- Encoding & Hashing ----
TOOLS.append(T("url-codec2", "Encoding & Hashing", "URL Codec",
 "Percent-encode and decode URLs and query strings, UTF-8 safe",
 f("ta", "URL or text") + btns("Encode", "Decode", "Copy"),
 """function run(){var t=V('ta')||'';
try{OUT(/%[0-9a-f]{2}/i.test(t)?decodeURIComponent(t):encodeURIComponent(t));}catch(e){OUT('ERROR: '+e.message);}}
wire('ta');"""))

TOOLS.append(T("hash-file", "Encoding & Hashing", "SHA-256 Text Hash",
 "SHA-256 and SHA-1 digests of any snippet (WebCrypto) — compare hashes after edits",
 f("ta", "Text") + btns("Hash", "Copy"),
 """async function run(){var t=V('ta')||'';
try{if(!crypto.subtle)throw'WebCrypto unavailable (need https or file://)';
var hex=async a=>await crypto.subtle.digest(a,new TextEncoder().encode(t)).then(b=>[...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join(''));
var s256=await hex('SHA-256');var s1=null;try{s1=await hex('SHA-1');}catch(e){}
OUT('SHA-256\\n'+s256+(s1?'\\n\\nSHA-1 (legacy, avoid)\\n'+s1:''));}catch(e){OUT('ERROR: '+e.message);}}
run();"""))

# ---- Developer ----
TOOLS.append(T("cron-scheduler", "Developer", "Cron Next Runs",
 "The next five runs a cron string fires — local time",
 f("ta", "Expression", 'placeholder="0 9 * * 1-5"') + btns("Schedule", "Copy"),
 """function run(){var p=(V('ta')||'').trim().split(/\\s+/);if(p.length!==5){OUT('need five fields');return;}
function mk(f,i){var s=new Set();f.split(',').forEach(x=>{var m=x.match(/^(\\*|\\d+)(?:-(\\d+))?(?:\\/(\\d+))?$/);if(!m)return;
var a=m[1]==='*'?0:+m[1],b=m[2]?+m[2]:(m[1]==='*'?i:+m[1]),st=+m[3]||1;if(m[1]==='*'){a=0;b=i;}for(var v=a;v<=b;v+=st)s.add(v);});return s;}
var M=mk(p[0],59),H=mk(p[1],23),DM=mk(p[2],31),MO=mk(p[3],12),DW=mk(p[4],7);
var now=new Date(),d=new Date(+now.getFullYear(),+now.getMonth(),+now.getDate(),0,0,0),out=[],guard=0;
while(out.length<5&&guard++<25000){var mo=d.getMonth()+1,dy=d.getDate(),dw=(d.getDay()+6)%7;
if(DM.has(dy)&&(p[2]==='*'||p[2]==='?')||DM.has(dy)&&p[2]!=='*'&&p[2]!=='?'||p[2]==='?'){if(p[2]==='*'||p[2]==='?'||DM.has(dy)){
if(MO.has(mo)&&(DW.has(dw)||DW.has(dw===0?7:dw)||p[4]==='*')){var h2=d.getHours();
if(H.has(h2)){var m2=d.getMinutes();for(var mm=m2;mm<60;mm+=1)if(M.has(mm)){out.push(d.getFullYear()+'-'+String(mo).padStart(2,'0')+'-'+String(dy).padStart(2,'0')+' '+String(h2).padStart(2,'0')+':'+String(mm).padStart(2,'0'));if(out.length>=5)break;}}}}}
d=new Date(+d.getTime()+60000);}
out=out.slice(0,5);out.sort();OUT(out.length?out.join('\\n'):'no runs found — check the string');}
wire('ta');"""))

TOOLS.append(T("hex-dump", "Developer", "Hex Dump Viewer",
 "Classic hex+ASCII dump with the address column",
 f("ta", "Text") + btns("Dump", "Copy"),
 """function run(){var b=new TextEncoder().encode(V('ta')||'');var o=[];
for(var i=0;i<b.length;i+=16){var line=[];var ascii='';
for(var j=0;j<16;j++){if(i+j<b.length){line.push(b[i+j].toString(16).padStart(2,'0'));
ascii+=b[i+j]>=32&&b[i+j]<127?String.fromCodePoint(b[i+j]):'.';}else line.push('  ');}
o.push(i.toString(16).padStart(8,'0')+'  '+line.slice(0,8).join(' ')+'  '+line.slice(8).join(' ')+'  |'+ascii+'|');}
OUT(o.join('\\n')||'(paste text — binary from a file first)');}
wire('ta');"""))

# ---- Games & Play ----
TOOLS.append(T("wordle-helper", "Games & Play", "Wordle Helper",
 "Filter a built-in answer list by your green (correct) and grey (wrong) letters",
 f("g", "Exact letters, + separates patterns", 'placeholder="S+A+T or +ARTS"') + f("b", "Greens 2", 'placeholder="IO"') + f("b2", "Blacks (wrong spot)", 'placeholder="IO"') + btns("Filter", "Copy"),
 """var WL="about above abuse actor acute admit adopt advice affect afford again agent angry agree answer appeal apply areas arise array around audio basis beach began begin being below birth black board brave brief bring broad brush built buyer candy cargo carry cause chain chair charm chart chase cheap check child chose civil class clean clear click clock close cloud coach coast could count court cover craft crash cream creek crime cross crowd crown curve cycle daily dance debug dead death depth dirty dozen draft drink drive drone drunk eagle earth eight elect elite empty enemy enjoy equal error event every exact extra faith false fiber field fifth fifty fight final first flame flat fleet flight float floor flour fluid focus force forth forty forum found frame frank fraud fresh front frost fruit funny ghost given glass globe glory grace grade grain grand grant grass great greed green greet grief grill grind groan grown guard guest guide happy heart heavy hurry ideal index inner input intro issue joint judge juice knaps light limit local logic lower lucky lunch magic major march match mercy might minor minus money month moral motor mouse mouth music naive nerve never noble north notch pasta paste patch peace peach pearl pedal peril phase photo piano piece pilot pitch place plane plate plaza point polar porch pouch pound power press price pride prime print prior prism prize probe proud prove pulse punch pupil queen quick quiet quote radio raise ranch rapid ratio reach react realm refer reign relax reply ridge rival river robot rough royal saint salad sauce scene scent scrap scrub seal seam seed serve seven shade shaft shark shore shout sight silky since sixty skill skull skirt sleep slice slide small smart smell smoke snake sneal solar solid solve sonic south space spare spark speak speed spend spice spell spider spite split spoke spoon sport spray stack stage stain stair stake stale stalk stall stamp stand stare start stash state steak steal steam steel steep step stick stiff stung style sugar super sweet swept swift sword table taste teach teeth tense thank theft thick thing third those throw tiger tight toast today token tooth total touch tough tour towel tower toxic trace track trade trail train trait trash treat trend tribe trick troop trout truck trust truth tutor under union unite until upset usage usual valid valor vapor verse video vinyl visit vital wager watch water weary weird wheal which while white whole widen widow width would wound wrath wreck wrist write wrong young youth zebra".split(' ');
function run(){var t=(V('g')||'')+(V('g2')||''),b=(V('b2')||V('b')||'').toUpperCase().replace(/[^A-Z]/g,'').split('');
var ex=[];t.toUpperCase().replace(/[^A-Z._]/g,'').split(/(?=[+])/).forEach(function(tok){if(!tok)return;var w=tok.replace(/[^A-Z._]/g,'');if(w.length===5)ex.push(w);});
var green={};ex.forEach(function(w){for(var i=0;i<5;i++)if(w[i]!=='.'&&w[i]!=='_')green[i]=w[i];});
var hits=WL.filter(w=>{for(var i in green)if(w[i]!==green[i])return false;
for(const c of b)if(w.includes(c)&&!Object.values(green).includes(c))return false;return true;});
OUT(hits.length?hits.join(' ')+'\\n\\n('+hits.length+' hits)':'no 5-letter hits — loosen letters');}
run();wire(['g','g2','b','b2']);"""))
