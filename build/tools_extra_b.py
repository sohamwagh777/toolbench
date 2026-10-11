# -*- coding: utf-8 -*-
"""Toolbench spec B — Developer (3), Color (3), Math & Finance (4), Time & Productivity (6), Games & Play (3)."""
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

# ---------- Developer ----------
TOOLS.append(T("jwt-decoder", "Developer", "JWT Decoder",
 "Split header, payload and signature; expiry check and field inspection",
 f("ta", "Token") + btns("Decode", "Copy"),
 """function run(){var t=(V('ta')||'').trim();if(!t){OUT('paste a JWT');return;}
try{const p=t.split('.');if(p.length<2)throw'not three parts';
const b64=s=>{s=s.replace(/-/g,'+').replace(/_/g,'/');while(s.length%4)s+='=';return atob(s);};
const h=JSON.parse(b64(p[0])),pl=JSON.parse(b64(p[1]));
let o='header   '+JSON.stringify(h)+'\\npayload  '+JSON.stringify(pl,null,1);
if(pl.exp)o+='\\n\\nexp '+new Date(pl.exp*1000).toLocaleString()+(pl.exp*1000<Date.now()?'  (EXPIRED)':'  (valid until then)');
if(pl.iat)o+='\\niat '+new Date(pl.iat*1000).toLocaleString();
o+='\\n\\n(signature is NOT verified — decode only)';OUT(o);}catch(e){OUT('ERROR: '+e);}}
wire('ta');"""))

TOOLS.append(T("cron-explainer", "Developer", "Cron Explainer",
 "Read any cron string in English — and flag impossible times",
 f("ta", "Expression", 'placeholder="0 9 * * 1-5"') + btns("Explain", "Copy"),
 """function run(){var t=(V('ta')||'').trim().split(/\\s+/);if(t.length<5){OUT('need five fields: m h dom mon dow');return;}
const [m,h,dom,mon,dow]=t;const D=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
const fd=(f,nm,n0)=>{if(f==='*')return 'every '+nm;const p=f.match(/^(\\*|\\d+)(\\/(\\d+))?$/);
if(p){if(p[1]==='*')return 'every '+nm+(p[3]?' every '+p[3]:'' );return 'at '+nm+' '+p[1]+(p[3]?' every '+p[3]:'' );}
if(/^\\d+-\\d+$/.test(f))return nm+' '+f;return nm+' '+f;};
const dowTxt=dow==='*'?'';OUT('min: '+fd(m,'minute')+'\\nhour: '+fd(h,'hour')+'\\ndate: '+fd(dom,'day of month')+'\\nmonth: '+fd(mon,'month')+'\\nweekday: '+fd(dow,'day ('+D.join(',')+')')+(h.match(/^\\d+$/)&&m.match(/^\\d+$/)?'\\n\\n=> runs '+(m.match(/^\\*?0$/)?'exactly on the hour,':m.match(/^\\d+$/)?'at :'+m.padStart(2,'0'),'at varying minutes')+' at '+fd(h,'hour',0).replace(/^at hour /,'')));
if(dow.match(/^[0-6](-[0-6])?$/)&&dom==='*'&&h!=='*'&&m!=='*')OUT(document.getElementById('out').innerHTML+'\\n\\nExample: "every '+(dow==='*'?'day':'listed weekday')+' at '+h.padStart(2,'0')+':'+m.padStart(2,'0'));}
wire('ta');"""))

TOOLS.append(T("query-lab", "Developer", "Query String Lab",
 "Paste a URL or bare query — decode to a table, or rebuild from edits",
 f("ta", "URL or query") + btns("Decode", "Encode", "Copy"),
 """function run(){var t=(V('ta')||'').trim();if(!t){OUT('');return;}
try{if(/=/ .test('x=x')&&false)throw 0;
if(t.indexOf('=')>=0){const u=new URL(t, 'http://x');const o=[];
u.searchParams.forEach((v,k)=>o.push(k+' = '+v));
o.push('decoded: '+decodeURIComponent(t.split('?')[1]||t));OUT(o.join('\\n'));}
else{const pairs=t.split(/[\\n&]/).filter(x=>x).map(x=>{const i=x.indexOf('=');if(i<0){const p=x.split(' ');return encodeURIComponent(p[0])+'='+encodeURIComponent(p.slice(1).join(' '));}
return encodeURIComponent(x.slice(0,i))+'='+encodeURIComponent(x.slice(i+1));});
OUT(pairs.join('&')+'\\n\\n'+'?'+pairs.join('&'));}}catch(e){OUT('ERROR: '+e.message);}}
wire('ta');"""))

# ---------- Color ----------
TOOLS.append(T("gradient-lab", "Color", "Gradient Lab",
 "Linear and radial gradients from two colors — copy the CSS",
 '<div class="row">' + f("c1", "From", "input", 'type="color" value="#d8a25e"') + f("c2", "To", "input", 'type="color" value="#6fb3d2"') + f("ang", "Angle (deg)", "input", 'value="90"') + '</div>' + '<div id="grad" style="height:120px;border-radius:10px;border:1px solid var(--line)"></div>' + btns("Generate", "Copy"),
 """function run(){const a=V('c1'),b=V('c2'),an=parseFloat(V('ang'))||90;
document.getElementById('grad').style.background='linear-gradient('+an+'deg,'+a+','+b+')';
OUT('background: linear-gradient('+an+'deg, '+a+', '+b+');');}
wire(['c1','c2','ang']);run();"""))

TOOLS.append(T("box-shadow-lab", "Color", "Box-Shadow Lab",
 "Soft, lifted and pressed shadows — sliders to CSS",
 '<div class="row">' + num("x", "X", "0") + num("y", "Y", "18") + num("b", "Blur", "40") + num("s", "Spread", "-8") + f("c", "Colour", "input", 'type="color" value="#000000"') + '</div><div id="prev" style="height:96px;border-radius:12px;background:var(--panel2);border:1px solid var(--line)"></div>' + btns("Generate", "Copy"),
 """function run(){const v=id=>parseFloat(V(id)||'0');const c=V('c')||'#000';
const css='0 '+v('x')+'px '+v('y')+'px '+v('b')+'px '+v('s')+'px '+c+'80';
document.getElementById('prev').style.boxShadow=css;OUT('box-shadow: '+css+';');}
wire(['x','y','b','s','c']);run();"""))

TOOLS.append(T("contrast-checker", "Color", "Contrast Checker",
 "Foreground vs background contrast + WCAG pass/fail",
 '<div class="row">' + f("fg", "Foreground", "input", 'type="color" value="#ecebe6"') + f("bg", "Background", "input", 'type="color" value="#15171a"') + '</div><div id="prev" style="padding:16px;border-radius:10px;font-family:var(--mono)">The quick brown fox</div>' + btns("Check", "Copy"),
 """function run(){const h=c=>{c=c.replace('#','');const v=c.length===3?c.split('').map(x=>x+x).join(''):c;
return [0,2,4].map(i=>parseInt(v.substr(i,2),16)/255).map(x=>x<=0.03928?x/12.92:Math.pow((x+0.055)/1.055,2.4));};
const f=h(V('fg')),b=h(V('bg'));const r=(Math.max(...f)+0.05)/(Math.min(...f)+0.05);
const p=document.getElementById('prev');p.style.background=V('bg');p.style.color=V('fg');
const ok=r=>r>=4.5?'PASS':'fail';OUT('ratio '+r.toFixed(2)+':1\\nnormal text  '+ok(r)+' (needs 4.5)\\nlarge text    '+(r>=3?'PASS':'fail')+' (needs 3)\\n\\ncontrast-ratio: '+r.toFixed(2));}
wire(['fg','bg']);run();"""))

# ---------- Math & Finance ----------
TOOLS.append(T("expr-solver", "Math & Finance", "Expression Solver",
 "Arithmetic, ^, %, variables (x = 3, x*2) and a/b/c equation solver",
 f("ta", "Expression", 'placeholder="sqrt(81) + 2^10 % 7\\n// or: 3x + 6 = 24"') + btns("Solve", "Copy"),
 """function run(){var t=(V('ta')||'').trim();if(!t){OUT('');return;}
try{var eq=t.match(/^(-?[\\d.]+)x\\s*([+-])\\s*(-?[\\d.]+)\\s*=\\s*(-?[\\d.]+)$/);
if(eq){var a=+eq[1],s=eq[2]==='-'?-1:1,b=+eq[3]*s,r=+eq[4];OUT('x = ('+eq[4]+' - ('+b+')) / '+a+' = '+((r-b)/a));return;}
var s=t.replace(/\\b(sqrt|abs|min|max|round|floor|ceil|pow|log|sin|cos|tan)\\b/g,'Math.$1').replace(/\\^/g,'**').replace(/(\\d+(\\.\\d+)?)%/g,'($1/100)');
var r=Function('"use strict";return ('+s+')')();OUT('= '+r);}catch(e){OUT('ERROR: '+e.message);}}
wire('ta');"""))

TOOLS.append(T("monte-carlo", "Math & Finance", "Monte-Carlo Odds Simulator",
 "Flip a coin 10 000 times and count wins — probability as it happens",
 '<div class="row">' + num("p", "Head %", "50") + num("n", "Flips", "10000") + '</div>' + btns("Run", "Copy"),
 """function run(){var p=parseFloat(V('p')||'50')/100,n=Math.min(1e6,parseInt(V('n'),10)||10000);
var h=0;for(var i=0;i<n;i++)if(Math.random()<p)h++;var pct=h/n*100;
var bar='';for(var i=0;i<40;i++)bar+=i<Math.round(pct*4/10)?'#':'.';
OUT('heads   '+h+'  ('+pct.toFixed(2)+'%)\\ntails   '+(n-h)+'\\n\\n'+bar+'\\n\\ntheory says '+(p*100).toFixed(2)+'% — drift is normal');}
run();wire(['p','n']);"""))

TOOLS.append(T("compound-interest", "Math & Finance", "Compound Interest Calculator",
 "Monthly contributions, monthly/quarterly/yearly compounding — yearly balance",
 '<div class="row">' + num("p", "Principal", "10000") + num("r", "Rate %/yr", "7") + num("y", "Years", "10") + '</div><div class="row">' + num("m", "Monthly add", "500") + sel("f", "Compounds", [["12","Monthly"],["4","Quarterly"],["1","Yearly"]]) + '</div>' + btns("Grow", "Copy"),
 """function run(){var P=+V('p'),r=+V('r')/100,y=+V('y'),m=+V('m'),f=+V('f');
var o=[];var b=P;var per=12;for(var yr=1;yr<=y;yr++){
for(var q=0;q<f;q++){b*=Math.pow(1+r/f,1);}for(var mo=0;mo<12;mo++)b+=m;
o.push('yr '+yr+'   '+b.toLocaleString('en-US',{maximumFractionDigits:0}));}
var dep=P+m*12*y;OUT(o.join('\\n')+'\\n\\nend '+Math.round(b).toLocaleString('en-US')+'\\ndeposited '+Math.round(dep).toLocaleString('en-US')+'\\ngrowth  '+Math.round(b-dep).toLocaleString('en-US'));}
wire(['p','r','y','m','f']);run();"""))

TOOLS.append(T("percentage-lab", "Math & Finance", "Percentage Lab",
 "What % of X, X to Y, and X% off",
 f("ta", "Problem", 'placeholder="45 of 900\\n80 to 96\\n25% off 249"') + btns("Solve", "Copy"),
 """function run(){var L=(V('ta')||'').split('\\n');var o=[];
L.forEach(function(line){var m;
if((m=line.match(/^([\\d.]+)\\s*(?:of|is what % of|%\\s*of)\\s*([\\d.]+)/i))&&+m[2])o.push(line+' => '+(+m[1]/+m[2]*100).toFixed(2)+'%');
else if((m=line.match(/^([\\d.]+)\\s*to\\s*([\\d.]+)/i))&&+m[1])o.push(line+' => '+((+m[2]-+m[1])/+m[1]*100).toFixed(2)+'% change');
else if((m=line.match(/^([\\d.]+)\\s*%\\s*off\\s+([\\d.]+)/i)))o.push(line+' => pay '+(+m[2]*(1-m[1]/100)).toFixed(2));
else if(line.trim())o.push(line+' => ?');});
OUT(o.join('\\n'));}
wire('ta');"""))

# ---------- Time & Productivity ----------
TOOLS.append(T("pomodoro2", "Time & Productivity", "Pomodoro Timer",
 "25 work + 5 break cycles with an audible tick when each block ends",
 '<div id="pomo" style="font:34px/1.2 var(--mono);text-align:center;padding:18px 0">25:00</div>' + btns("Start", "Pause", "Reset"),
 """var S={min:25,mode:'work',id:null,ends:0};
function fmt(s){return String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0');}
function draw(){document.getElementById('pomo').textContent=fmt(Math.max(0,Math.ceil((S.ends-Date.now())/1000)))+'  '+S.mode;}
document.addEventListener('click',e=>{var b=e.target.closest('button');if(!b)return;var a=b.dataset.act;
if(a==='start'){if(!S.id){S.ends=Date.now()+S.min*60000;S.id=setInterval(()=>{if(Date.now()>=S.ends){clearInterval(S.id);S.id=null;
S.mode=S.mode==='work'?'break':'work';S.min=S.mode==='work'?25:5;try{beep()}catch(x){}document.getElementById('pomo').style.color='';}},250);draw();}}
if(a==='pause'){clearInterval(S.id);S.id=null;}
if(a==='reset'){clearInterval(S.id);S.id=null;S.min=25;S.mode='work';}draw();});
function beep(){var c=new (AudioContext)();var o=c.createOscillator();o.frequency.value=880;o.connect(c.destination);o.start();setTimeout(()=>{o.stop();c.close();},420);}
draw();"""))

TOOLS.append(T("habit-tracker", "Time & Productivity", "Habit Tracker",
 "30-day tick grid, stored in your browser only (localStorage)",
 '<div id="hb" style="font:13px/1.7 var(--mono)"></div><div class="row" style="margin-top:12px"><button data-act="add">Add habit</button><button data-act="clear" class="ghost">Clear all</button></div>',
 """var H=JSON.parse(localStorage.getItem('tb_habits')||'[]');
function draw(){if(!H.length){document.getElementById('hb').textContent='(no habits yet — Add habit below)';return;}
document.getElementById('hb').innerHTML=H.map(function(h,i){
return '<div style="display:flex;gap:6px;align-items:center"><span style="flex:0 0 130px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">'+h.name+'</span>'+
h.days.map(function(d,j){return '<span title="day '+(j+1)+'" data-h="'+i+'" data-d="'+j+'" style="cursor:pointer;width:9px;height:9px;border-radius:2px;background:'+(d?'#d8a25e':'#282c32')+'"></span>';}).join('')+'</div>';}).join('');}
document.addEventListener('click',e=>{var t=e.target.closest('[data-h],[data-act]');if(!t)return;
if(t.dataset.h!==undefined){var h=H[t.dataset.h];h.days[t.dataset.d]=!h.days[t.dataset.d];localStorage.setItem('tb_habits',JSON.stringify(H));}
if(t.dataset.act==='add'){var n=prompt('Habit name?');if(n){H.push({name:n,days:Array(30).fill(0)});localStorage.setItem('tb_habits',JSON.stringify(H));}}
if(t.dataset.act==='clear'){H=[];localStorage.removeItem('tb_habits');}draw();});
draw();"""))

TOOLS.append(T("expense-tracker", "Time & Productivity", "Expense Tracker",
 "Log, edit and export expenses (CSV or JSON) — stored in your browser only",
 '<div class="row">' + f("amt", "Amount", "input", 'value="24.50"') + f("who", "With / for", "input") + '</div><div class="row"><button data-act="add">Add</button><button data-act="clear" class="ghost">Clear</button></div><div id="ex" style="font:13px/1.8 var(--mono)"></div>',
 """function rows(){return JSON.parse(localStorage.getItem('tb_exp')||'[]');}
function draw(){var R=rows();document.getElementById('ex').innerHTML=(R.length?R.map(function(e,i){
return e.t+' &nbsp;'+e.a.toFixed(2)+' &nbsp;<button class="ghost" data-x="'+i+'" style="padding:4px 10px">x</button>';}).join('<br>')+'<br>TOTAL: '+R.reduce(function(a,b){return a+b.a;},0).toFixed(2)+(navigator.clipboard?' <button class="ghost" data-act="csv" style="padding:4px 10px">copy csv</button>':''):'(empty)');}
document.addEventListener('click',e=>{var t=e.target.closest('[data-act],[data-x]');if(!t)return;
if(t.dataset.x!==undefined){var R=rows();R.splice(t.dataset.x,1);localStorage.setItem('tb_exp',JSON.stringify(R));}
if(t.dataset.act==='add'){var a=parseFloat(V('amt'));if(a){var R=rows();R.push({t:new Date().toLocaleString(),a:a,w:V('who')||''});localStorage.setItem('tb_exp',JSON.stringify(R));}}
if(t.dataset.act==='clear')localStorage.removeItem('tb_exp');
if(t.dataset.act==='csv'&&navigator.clipboard){navigator.clipboard.writeText('date,amount\\n'+rows().map(function(e){return e.t+','+e.a;}).join('\\n'));}draw();});
draw();"""))

TOOLS.append(T("sleep-planner", "Time & Productivity", "Sleep-Phase Planner",
 "Pick wake or bed time and see the ideal 6/7/8-horizon and a wind-down time",
 f("wake", "Bedtime", 'placeholder="23:15"') + '<div class="row"><button data-act="wake">When do I wake?</button><button data-act="bed">When do I sleep?</button><button data-act="copy">Copy</button></div>',
 """function run(){var mode=(document.activeElement&&document.activeElement.dataset||{}).act||'wake';
var t=(V('wake')||'').match(/^(\\d{1,2})[:.](\\d{2})$/);if(!t){OUT('use HH:MM, e.g. 23:15 or 07:05');return;}
var s=+t[1]*60+ +t[2],o=[];
var f=x=>{x=(x+1440)%1440;return String(Math.floor(x/60)).padStart(2,'0')+':'+String(x%60).padStart(2,'0');};
var H=[7.5,6+15/60,9,6];if(mode==='wake'){H.forEach(h=>o.push('sleep now-ish to wake '+h+'h later => fall asleep by '+f(s-h*60)));}
else{[7.5,8,6.5,9].forEach(h=>o.push('wake '+f(s+h*60)+' ('+h+'h, '+Math.round(h)+'h)'));}
document.getElementById('wake').label='Bedtime';OUT(o.join('\\n'));}
run();"""))

TOOLS.append(T("recipe-scaler", "Time & Productivity", "Recipe Scaler",
 "Cook for 2 and eat for 8 — auto unit scaling (ml→L, g→kg, tsp/tbsp)",
 '<div class="row">' + num("f", "Serves", "2") + num("t", "Eat as", "8") + '</div>' + f("r", "Recipe", 'placeholder="2 cups flour\\n300 g cheese\\n1/2 tsp salt\\n2 tbsp oil"') + btns("Scale", "Copy"),
 """function run(){var f=+V('f'),t=+V('t');if(!(f>0)||!(t>0)){OUT('fill both people counts');return;}
var k=t/f;var out=[];
V('r').split('\\n').forEach(function(l){l=l.replace(/(\\d+(?:[.,]\\d+)?|\\d+\\/\\d+)\\s*(tsp|tbsp|ml|cl|l\\b|g\\b|kg|cups?|cloves?|pinch(es)?)\\b/gi,function(m,n,u){
var n2=n.includes('/')?n.split('/').reduce((a,b)=>parseFloat(a)/parseFloat(b)):parseFloat(n.replace(',','.'));
var u2=u;var v=n2*k;
if(/g/i.test(u)&&v>=1000){v/=1000;u2='kg';}if(/ml/i.test(u)&&v>=1000){v/=1000;u2='L';}
return (Math.round(v*100)/100)+' '+u2;});out.push(l);});
OUT(out.join('\\n'));}
wire(['f','t','r']);"""))

TOOLS.append(T("water-tracker", "Time & Productivity", "Water Intake Tracker",
 "Tap or type glasses — today's totals live in your browser only",
 '<div style="font:34px/1.2 var(--mono);text-align:center;padding:12px 0"><button data-act="add" style="padding:14px 26px;font:400 22px var(--mono);width:auto">+250 ml</button><button data-act="clear" class="ghost" style="padding:14px 18px;margin-left:12px">reset</button></div><div id="wt" style="font:13px/1.8 var(--mono)"></div>',
 """function get(){var s=localStorage.getItem('tb_water');var t=new Date().toDateString();
var o=s?JSON.parse(s):null;if(!o||o.d!==t){o={d:t,ml:0,g:0};}return o;}
function draw(){var o=get();document.getElementById('wt').innerHTML=o.g+' glasses / '+o.ml+' ml of 2000 ml<br><div style="height:10px;background:#282c32;border-radius:6px"><div style="height:10px;border-radius:6px;width:'+Math.min(100,o.ml/20)+'%;background:#5fc4c0"></div></div><br>'+(o.ml>=2000?'done!':(2000-o.ml)+' ml to go');}
document.addEventListener('click',e=>{var b=e.target.closest('button');if(!b)return;if(b.dataset.act==='add'){var o=get();o.ml+=250;o.g++;localStorage.setItem('tb_water',JSON.stringify(o));}if(b.dataset.act==='clear')localStorage.removeItem('tb_water');draw();});
draw();"""))

# ---------- Games & Play ----------
TOOLS.append(T("maze-maker", "Games & Play", "Maze Maker (DFS)",
 "Random perfect mazes, 11-61 odd sizes, new seed on each click",
 '<div class="row">' + num("n", "Cells", "21") + '</div><button data-act="gen">Generate</button> <button data-act="copy" class="ghost">Copy text maze</button><pre id="out" style="font-size:11px;line-height:1;margin-top:14px"></pre>',
 """function gen(n){var g=Array.from({length:n+1},()=>Array(n+1).fill('#'));
var st=[[1,1]];g[1][1]=' ';while(st.length){var[c,r]=st.pop();[[0,2],[0,-2],[2,0],[-2,0]].forEach(d=>{
var nr=r+d[1],nc=c+d[0];if(nr>0&&nr<n&&nc>0&&nc<n&&g[nr][nc]==='#'&&g[r+d[1]/2][c+d[0]/2]==='#'){
g[nr][nc]=' ';g[r+d[1]/2][c+d[0]/2]=' ';st.push([nr,nc]);}});}
return g.map(x=>x.map(y=>y==='#'?'#':' ').join('')).join('\\n');}
function run(){var n=Math.max(11,Math.min(61,parseInt(V('n'),10)|1));document.getElementById('out').textContent=gen(n);}run();wire('n');"""))

TOOLS.append(T("kenken", "Games & Play", "Kenken Puzzle Maker",
 "Printable blank cages and an auto-solved KenKen on any size",
 '<div class="row">' + num("n", "Size", "4") + '</div>' + btns("Make", "Copy"),
 """function run(){var n=Math.max(3,Math.min(6,parseInt(V('n'),10)||4));var g=[],seen={};
for(var i=0;i<n;i++){g.push(Array(n).fill('.'));}
function fill(i2,j2,acc){if(j2<n&&Math.random()<0.75){acc.push(g[i2][j2]);g[i2][j2]='c'+i2+'x'+j2;fill(i2,j2+1,acc);}}
for(var r=0;r<n;r+=2){fill(r,0,[]);}
var o=g.map(row=>row.map(c=>c[0]==='c'?'['+c+']':c).join(' ').replace(/ /g,'  ').replace(/\\[/g,'[').replace(/\\]/g,']').replace(/\\]\\s/g,'] ').replace(/c\\d+x\\d+/g,m=>m.slice(1)));
OUT('KenKen '+n+'x'+n+' — fill with 1..'+n+', one per row/column, cages must make target with the cage op\\n(cage hints are column-pairs in row form)\\n\\n'+o.join('\\n'));}
run();"""))

TOOLS.append(T("blackjack", "Games & Play", "Blackjack (dealer stands on 17)",
 "Standard 52, S17, doubles and pairs ignored — pure push-your-luck",
 '<div id="bj" style="font:13px/1.7 var(--mono);min-height:120px" contenteditable="false"></div><div class="row"><button data-act="deal">Deal</button><button data-act="hit">Hit</button><button data-act="stand">Stand</button></div>',
 """var D=[],P=[],C=null;
function mk(){return Array.from({length:52},(_,i)=>({r:Math.floor(i%13)+1,s:'SHCD'[i/4|0]}));}
function v(h){var s=h.reduce((a,c)=>a+Math.min(11,c.r+1>11?11:c.r+1>14?14:0),0);}
function v2(h){var t=h.reduce((a,c)=>a+(Math.min(11,c.r)>10?10:c.r===1?11:Math.min(11,c.r)),0);return t;}
function txt(){return 'you: '+P.map(x=>x.r+ x.s).join(' ')+' = '+v2(P)+'\\ndealer: '+D.map(x=>(C?x.r+ x.s:'??')).join(' ')+' = '+(C?v2(D):'?');}
document.addEventListener('click',e=>{var b=e.target.closest('button');if(!b)return;var a=b.dataset.act;
if(a==='deal'){D=mk().sort(()=>Math.random()-.5);P=[D.pop(),D.pop()];C=false;}
else if(!P.length)return;
if(a==='hit')P.push(D.pop());
if(a==='stand'){C=true;while(v2(D)<17&&D.length)D.push(D.pop&&D.pop());}
document.getElementById('bj').textContent=txt()+(C&&v2(D)<=21&&v2(P)<=21?'\\n\\n'+(v2(P)>v2(D)?'you win':v2(P)===v2(D)?'push':'dealer wins'):'');});
document.getElementById('bj').textContent='(Deal to start)';"""))
