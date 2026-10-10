"""
Route Lab: Dijkstra, Prim, Kruskal (หน้าเว็บแอนิเมชัน ฝังใน Streamlit)

ติดตั้ง (ครั้งเดียว) ใน Terminal ของ VS Code:
    pip install streamlit

รัน:
    streamlit run route_lab_app.py
(ถ้าไม่เจอคำสั่ง streamlit ให้ใช้:  python -m streamlit run route_lab_app.py)

ไฟล์นี้ไฟล์เดียวใช้งานได้เลย: หน้าเว็บทั้งหน้าอยู่ในตัวแปร HTML ด้านล่าง
อัลกอริทึมทำงานในหน้าเว็บ (JavaScript) ไม่ได้รันด้วย Python
ข้อมูลเวลาเดินทางเป็นค่าสมมติ เพื่อสาธิตอัลกอริทึมเท่านั้น
"""
import streamlit as st

st.set_page_config(page_title="Route Lab", page_icon="🗺️", layout="wide")
st.markdown(
    "<style>.block-container{padding-top:1rem;padding-bottom:0;max-width:100%}</style>",
    unsafe_allow_html=True,
)

PAGE_HEIGHT = 1150   # ความสูงของกรอบ (พิกเซล) ปรับได้ถ้าอยากให้ยาวหรือสั้นลง

# ---------------------------------------------------------------------------
# หน้าเว็บทั้งหน้า (HTML + CSS + JavaScript)
# ---------------------------------------------------------------------------
HTML = r"""<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Route Lab – Dijkstra, Prim, Kruskal</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600&family=Prompt:wght@500;600&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#E9EEF1; --surface:#FFFFFF; --surface2:#F2F5F7; --ink:#142A33; --muted:#566F7B;
  --rule:#CBD6DC; --edge:#A3B4BD; --route:#0B9A62; --explore:#2D6BDB; --visit:#F2B01E;
  --warn:#CF4527; --on-route:#FFFFFF;
  --c0:#F2B01E; --c1:#5B8DEF; --c2:#27B97C; --c3:#F27A54; --c4:#B07CE0; --c5:#4CC3D1;
  box-sizing:border-box;
  padding-top:env(safe-area-inset-top,0px);
  padding-bottom:env(safe-area-inset-bottom,0px);
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#0E1A20; --surface:#15262E; --surface2:#1B313B; --ink:#E6EEF1; --muted:#93A9B3;
    --rule:#2B434E; --edge:#4C6672; --route:#2ED08C; --explore:#6C9CFF; --visit:#F5C04A;
    --warn:#FF7B5C; --on-route:#05291B;
  }
}
:root[data-theme="dark"]{
  --bg:#0E1A20; --surface:#15262E; --surface2:#1B313B; --ink:#E6EEF1; --muted:#93A9B3;
  --rule:#2B434E; --edge:#4C6672; --route:#2ED08C; --explore:#6C9CFF; --visit:#F5C04A;
  --warn:#FF7B5C; --on-route:#05291B;
}
*,*::before,*::after{box-sizing:border-box}
html{scroll-padding-top:env(safe-area-inset-top,0px)}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font-family:"IBM Plex Sans Thai","Noto Sans Thai","Sarabun",system-ui,sans-serif;
  font-size:15px; line-height:1.6;
}
h1,h2{font-family:"Prompt","IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif; font-weight:600; margin:0; line-height:1.3}
.wrap{max-width:1180px; margin:0 auto; padding:20px 16px 40px}
header{display:flex; flex-wrap:wrap; align-items:baseline; gap:6px 18px; margin-bottom:16px}
header h1{font-size:28px; letter-spacing:.2px}
header p{margin:0; color:var(--muted)}
.grid{display:grid; grid-template-columns:minmax(0,1fr) 350px; gap:16px; align-items:start}
@media (max-width:920px){ .grid{grid-template-columns:minmax(0,1fr)} }

.card{background:var(--surface); border:1.5px solid var(--rule); border-radius:14px}
.toolbar{display:flex; flex-wrap:wrap; gap:8px; align-items:center; padding:10px; margin-bottom:12px}
.toolbar .sp{flex:1}
button,select,input{font:inherit; color:inherit}
button{
  background:var(--surface); border:1.5px solid var(--rule); border-radius:10px;
  padding:6px 12px; cursor:pointer; min-height:38px;
}
button:hover:not(:disabled){border-color:var(--ink)}
button:disabled{opacity:.45; cursor:not-allowed}
button[aria-pressed="true"]{background:var(--ink); color:var(--surface); border-color:var(--ink)}
button.primary{background:var(--route); color:var(--on-route); border-color:var(--route); font-weight:600}
button.primary:hover:not(:disabled){border-color:var(--ink)}
:focus-visible{outline:3px solid var(--explore); outline-offset:2px}
.group{display:flex; gap:6px; flex-wrap:wrap}

.canvas{position:relative; aspect-ratio:800/520; overflow:hidden; border-radius:14px}
.canvas svg{display:block; width:100%; height:100%; touch-action:none; user-select:none; -webkit-user-select:none}
.canvas[data-tool="move"] [data-node]{cursor:grab}
.canvas[data-tool="add"] svg{cursor:crosshair}
.canvas[data-tool="link"] [data-node],
.canvas[data-tool="weight"] [data-edge],
.canvas[data-tool="del"] [data-node],
.canvas[data-tool="del"] [data-edge]{cursor:pointer}
.dot{fill:var(--rule)}
.edge{stroke:var(--edge); stroke-width:3; stroke-linecap:round; fill:none}
.edge.tree{stroke:var(--explore); stroke-width:5}
.edge.path{stroke:var(--route); stroke-width:8}
.edge.focus{stroke:var(--visit); stroke-width:7}
.edge.reject{stroke:var(--warn); stroke-width:7}
.hit{stroke:transparent; stroke-width:18; fill:none}
.wbox{fill:var(--surface); stroke:var(--rule); stroke-width:1.2}
.wtxt{fill:var(--muted); font-size:12px; font-weight:500; text-anchor:middle; dominant-baseline:central}
.wbox.on{stroke:var(--route)} .wtxt.on{fill:var(--ink); font-weight:600}
.node{fill:var(--surface); stroke:var(--ink); stroke-width:4}
.node.visited{fill:var(--visit)}
.node.frontier{stroke-dasharray:4 3}
.node.current{fill:var(--explore)}
.node.onpath{fill:var(--route)}
.node.pending{stroke:var(--explore); stroke-width:6}
.ring{fill:none; stroke:var(--route); stroke-width:3}
.nlabel{fill:var(--ink); font-size:13px; font-weight:500; text-anchor:middle; paint-order:stroke; stroke:var(--surface); stroke-width:4; stroke-linejoin:round}
.badge{fill:var(--ink)} .badge-t{fill:var(--surface); font-size:11px; font-weight:600; text-anchor:middle; dominant-baseline:central}
.flag{font-size:12px; font-weight:600; fill:var(--route); paint-order:stroke; stroke:var(--surface); stroke-width:4}
.flag.end{fill:var(--warn)}

.pop{
  position:absolute; transform:translate(-50%,-130%); background:var(--surface); border:1.5px solid var(--ink);
  border-radius:10px; padding:8px; display:flex; gap:8px; align-items:center; z-index:5;
}
.pop[hidden]{display:none}
.pop input{width:76px; border:1.5px solid var(--rule); border-radius:8px; padding:5px 8px; background:var(--surface2)}
.pop label{display:flex; gap:6px; align-items:center; font-size:13px; color:var(--muted)}
.hint{margin:10px 2px 0; color:var(--muted); font-size:14px}
.stats{display:flex; flex-wrap:wrap; gap:6px 18px; margin:6px 2px 0; font-size:13px; color:var(--muted)}
.stats b{color:var(--ink); font-weight:600}

aside .card{padding:14px; margin-bottom:12px}
.tabs{display:grid; grid-template-columns:repeat(3,1fr); gap:6px; margin-bottom:12px}
.tabs button{text-align:left; line-height:1.3; padding:8px 8px}
.tabs small{display:block; color:inherit; opacity:.7; font-size:11px}
h2{font-size:18px; margin-bottom:4px}
.desc{margin:0 0 8px; color:var(--muted)}
.cx{font-size:13px; color:var(--muted); margin:0}
.cx b{color:var(--ink); font-weight:600}
.row{display:flex; gap:10px; margin:12px 0}
.row label{flex:1; display:flex; flex-direction:column; gap:3px; font-size:13px; color:var(--muted)}
select{background:var(--surface2); border:1.5px solid var(--rule); border-radius:10px; padding:6px 8px; min-height:38px; width:100%}
.ctrl{display:grid; grid-template-columns:1.3fr 1fr 1fr 1fr; gap:6px}
.ctrl button{padding:6px 4px}
.speed{display:flex; align-items:center; gap:10px; margin-top:10px; font-size:13px; color:var(--muted)}
.speed input{flex:1; accent-color:var(--route)}
.prog{font-size:13px; color:var(--muted); margin:0 0 2px}
.msg{margin:0; min-height:3.2em}
.result{margin-top:10px; padding:10px 12px; border-radius:10px; background:var(--surface2); border-left:5px solid var(--route)}
.result[hidden]{display:none}
.result b{font-weight:600}
.log{margin:0; padding:0 0 0 22px; max-height:190px; overflow:auto; font-size:13px; color:var(--muted)}
.log li{padding:2px 0}
.log li.now{color:var(--ink); font-weight:600}
.empty{color:var(--muted); font-size:13px; margin:0}
@media (prefers-reduced-motion: no-preference){
  .edge,.node{transition:stroke .15s, fill .15s, stroke-width .15s}
}
@keyframes draw{from{stroke-dasharray:1;stroke-dashoffset:1}to{stroke-dasharray:1;stroke-dashoffset:0}}
@keyframes pulse{0%{transform:scale(1.55)}100%{transform:scale(1)}}
@media (prefers-reduced-motion: no-preference){
  .edge.focus,.edge.reject,.edge.path{animation:draw .55s ease-out}
  .node.current{animation:pulse .5s ease-out; transform-box:fill-box; transform-origin:center}
}
.noanim .edge,.noanim .node{animation:none !important}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>Route Lab</h1>
    <p>ทดลองหาเส้นทางที่ดีที่สุดด้วยทฤษฎีกราฟ: ลากจุด เชื่อมเส้น แล้วรันอัลกอริทึมทีละขั้น</p>
  </header>

  <div class="grid">
    <main>
      <div class="card toolbar" role="toolbar" aria-label="เครื่องมือแก้ไขกราฟ">
        <div class="group" id="tools">
          <button data-tool="move" aria-pressed="true">ลากจุด</button>
          <button data-tool="add" aria-pressed="false">เพิ่มจุด</button>
          <button data-tool="link" aria-pressed="false">เชื่อมเส้น</button>
          <button data-tool="weight" aria-pressed="false">แก้เวลา</button>
          <button data-tool="del" aria-pressed="false">ลบ</button>
        </div>
        <span class="sp"></span>
        <div class="group">
          <button id="btnBkk">แผนที่กรุงเทพ</button>
          <button id="btnRand">สุ่มกราฟ</button>
          <button id="btnClear">ล้างทั้งหมด</button>
        </div>
      </div>

      <div class="card canvas" id="canvas" data-tool="move">
        <svg id="svg" viewBox="0 0 800 520" role="img" aria-label="กราฟแสดงจุดและเส้นทางเชื่อมระหว่างจุด">
          <defs>
            <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><circle class="dot" cx="20" cy="20" r="1.3"/></pattern>
          </defs>
          <rect width="800" height="520" fill="url(#grid)"/>
          <g id="layer"></g>
        </svg>
        <div class="pop" id="pop" hidden>
          <label>เวลา (นาที) <input id="popIn" type="number" min="1" max="999" inputmode="numeric"></label>
          <button class="primary" id="popOk">ตกลง</button>
        </div>
      </div>
      <p class="hint" id="hint"></p>
      <div class="stats">
        <span>จุด (V) <b id="sV">0</b></span>
        <span>เส้นเชื่อม (E) <b id="sE">0</b></span>
        <span>น้ำหนักเส้น = เวลาเดินทางเป็นนาที (ตัวเลขสมมติ)</span>
      </div>
    </main>

    <aside>
      <div class="card">
        <div class="tabs" id="algoTabs">
          <button data-algo="dijkstra" aria-pressed="true">Dijkstra<small>เส้นทางสั้นสุด</small></button>
          <button data-algo="prim" aria-pressed="false">Prim<small>MST โตจากจุดเริ่ม</small></button>
          <button data-algo="kruskal" aria-pressed="false">Kruskal<small>MST เรียงเส้น</small></button>
        </div>
        <h2 id="aTitle"></h2>
        <p class="desc" id="aDesc"></p>
        <p class="cx" id="aCx"></p>

        <div class="row" id="rowSel">
          <label id="startWrap">จุดเริ่มต้น<select id="selStart"></select></label>
          <label id="endWrap">จุดปลายทาง<select id="selEnd"></select></label>
        </div>

        <div class="ctrl">
          <button class="primary" id="btnPlay">เล่น</button>
          <button id="btnNext">ถัดไป</button>
          <button id="btnBack">ย้อน</button>
          <button id="btnReset">รีเซ็ต</button>
        </div>
        <div class="speed"><span>ช้า</span><input type="range" id="speed" min="150" max="1400" step="50" value="700" aria-label="ความเร็วในการเล่น"><span>เร็ว</span></div>
      </div>

      <div class="card">
        <p class="prog" id="prog"></p>
        <p class="msg" id="msg" aria-live="polite"></p>
        <div class="result" id="result" hidden></div>
      </div>

      <div class="card">
        <h2 style="font-size:15px;margin-bottom:6px">บันทึกการทำงาน</h2>
        <ol class="log" id="log"></ol>
        <p class="empty" id="logEmpty">ยังไม่มีขั้นตอน</p>
      </div>
    </aside>
  </div>
</div>

<script>
(() => {
  const W = 800, H = 520;
  const $ = id => document.getElementById(id);
  const svg = $('svg'), layer = $('layer'), canvas = $('canvas');

  let nodes = [], edges = [], nextId = 0;
  let tool = 'move', pending = null, drag = null, weightEdge = null;
  let algo = 'dijkstra', steps = [], idx = -1, timer = null, statusMsg = '';
  let startId = null, endId = null;

  const key = (a, b) => a < b ? a + '-' + b : b + '-' + a;
  const N = id => nodes.find(n => n.id === id);
  const nm = id => (N(id) ? N(id).name : '?');
  const letter = id => id < 26 ? String.fromCharCode(65 + id) : 'N' + id;
  const wOf = (a, b) => { const e = edges.find(e => key(e.a, e.b) === key(a, b)); return e ? e.w : 0; };

  const ALGOS = {
    dijkstra: {
      title: 'Dijkstra: เส้นทางที่ใช้เวลาน้อยที่สุด',
      desc: 'ยืนยันจุดที่ใกล้จุดเริ่มต้นที่สุดทีละจุด แล้วปรับระยะของเพื่อนบ้านถ้าเจอทางลัด ใช้กับเส้นที่มีน้ำหนักไม่ติดลบ เหมือนหลักการที่แอปนำทางใช้',
      cx: 'เวลา: <b>O(V²)</b> แบบง่ายในโค้ดนี้ หรือ <b>O((V+E) log V)</b> เมื่อใช้ heap',
      needStart: true, needEnd: true
    },
    prim: {
      title: 'Prim: ต้นไม้ครอบคลุมน้อยที่สุด (MST)',
      desc: 'ต่อทุกจุดให้ถึงกันด้วยเส้นรวมถูกที่สุด โดยโตเป็นต้นไม้จากจุดเริ่มต้น เลือกเส้นที่ถูกที่สุดที่ยื่นออกจากส่วนที่ต่อแล้ว เหมาะกับการวางสายไฟ ท่อ หรือเครือข่าย',
      cx: 'เวลา: <b>O(E log V)</b> เมื่อใช้ heap (โค้ดนี้ใช้การสแกนเส้นแบบง่าย)',
      needStart: true, needEnd: false
    },
    kruskal: {
      title: 'Kruskal: ต้นไม้ครอบคลุมน้อยที่สุด (MST)',
      desc: 'เรียงเส้นจากถูกไปแพง แล้วพิจารณาทีละเส้น: เลือกถ้าเชื่อมสองกลุ่มที่ยังแยกกัน ข้ามถ้าทำให้เกิดวงจร (สีของจุดคือกลุ่มที่เชื่อมกันแล้ว เส้นแดงคือเส้นที่ถูกข้าม)',
      cx: 'เวลา: <b>O(E log E)</b> จากการเรียงเส้น ใช้ Union-Find ตรวจวงจร',
      needStart: false, needEnd: false
    }
  };
  const HINTS = {
    move: 'ลากจุดเพื่อย้ายตำแหน่ง',
    add: 'แตะที่ว่างบนแผนที่เพื่อวางจุดใหม่',
    link: 'แตะจุดแรก แล้วแตะจุดที่สองเพื่อสร้างเส้นเชื่อม',
    weight: 'แตะที่เส้นเพื่อแก้เวลาเดินทาง (นาที)',
    del: 'แตะจุดหรือเส้นเพื่อลบ'
  };

  /* ---------- graph editing ---------- */
  function addNode(x, y, name) {
    const id = nextId++;
    nodes.push({ id, name: name || ('จุด ' + letter(id)), x: Math.round(x), y: Math.round(y) });
    return id;
  }
  function addEdge(a, b, w) {
    if (a === b || edges.some(e => key(e.a, e.b) === key(a, b))) return false;
    edges.push({ a, b, w });
    return true;
  }
  function defaultW(a, b) {
    const p = N(a), q = N(b);
    return Math.max(2, Math.round(Math.hypot(p.x - q.x, p.y - q.y) / 11));
  }
  function removeNode(id) {
    nodes = nodes.filter(n => n.id !== id);
    edges = edges.filter(e => e.a !== id && e.b !== id);
  }
  function changed() {
    stop(); steps = []; idx = -1; statusMsg = ''; pending = null; hidePop();
    syncSelects(); fullUpdate();
  }

  function loadBangkok() {
    nodes = []; edges = []; nextId = 0;
    const P = [
      ['จตุจักร', 440, 60], ['อารีย์', 250, 100], ['อนุสาวรีย์', 160, 210], ['ราชเทวี', 300, 250],
      ['สยาม', 400, 300], ['ประตูน้ำ', 500, 220], ['อโศก', 600, 320], ['พร้อมพงษ์', 690, 400],
      ['สีลม', 340, 430], ['สะพานตากสิน', 220, 470], ['ลาดพร้าว', 620, 110], ['รัชดา', 700, 210]
    ];
    P.forEach(p => addNode(p[1], p[2], p[0]));
    [[0,1,8],[0,10,10],[0,5,16],[1,2,7],[1,3,12],[2,3,9],[3,4,6],[3,5,9],[4,5,8],[4,6,11],
     [5,6,10],[4,8,12],[8,9,9],[6,7,7],[10,11,9],[11,6,12],[2,9,20],[8,7,22]]
      .forEach(e => addEdge(e[0], e[1], e[2]));
    startId = 2; endId = 7;
    changed();
  }
  function loadRandom() {
    nodes = []; edges = []; nextId = 0;
    let tries = 0;
    while (nodes.length < 9 && tries < 3000) {
      tries++;
      const x = 60 + Math.random() * 680, y = 50 + Math.random() * 410;
      if (nodes.every(m => Math.hypot(m.x - x, m.y - y) > 120)) addNode(x, y);
    }
    const d = (a, b) => Math.hypot(a.x - b.x, a.y - b.y);
    const inT = [nodes[0].id];
    while (inT.length < nodes.length) {
      let best = null;
      for (const a of inT) for (const b of nodes) {
        if (inT.includes(b.id)) continue;
        const dd = d(N(a), b);
        if (!best || dd < best.d) best = { a, b: b.id, d: dd };
      }
      addEdge(best.a, best.b, defaultW(best.a, best.b)); inT.push(best.b);
    }
    for (const n of nodes) {
      nodes.filter(m => m.id !== n.id).sort((p, q) => d(n, p) - d(n, q)).slice(0, 2)
        .forEach(m => addEdge(n.id, m.id, defaultW(n.id, m.id)));
    }
    startId = nodes[0].id; endId = nodes[nodes.length - 1].id;
    changed();
  }
  function clearAll() { nodes = []; edges = []; nextId = 0; startId = endId = null; changed(); }

  /* ---------- algorithms (each returns an array of step snapshots) ---------- */
  function adjacency() {
    const adj = {}; nodes.forEach(n => adj[n.id] = []);
    edges.forEach(e => { adj[e.a].push({ to: e.b, w: e.w }); adj[e.b].push({ to: e.a, w: e.w }); });
    return adj;
  }
  const treeFromPrev = prev => Object.keys(prev).map(v => key(+v, prev[v]));
  function pathTo(prev, t) { const p = [t]; while (prev[p[0]] !== undefined) p.unshift(prev[p[0]]); return p; }
  const edgesOfPath = p => p.slice(1).map((v, i) => key(p[i], v));
  const sumPath = p => p.slice(1).reduce((s, v, i) => s + wOf(p[i], v), 0);
  const names = p => p.map(nm).join(' → ');

  function runDijkstra(s, t) {
    const adj = adjacency(), dist = {}, prev = {}, done = new Set(), out = [];
    nodes.forEach(n => dist[n.id] = Infinity); dist[s] = 0;
    const lab = () => Object.fromEntries(nodes.map(n => [n.id, dist[n.id] === Infinity ? '∞' : String(dist[n.id])]));
    const snap = (msg, x = {}) => out.push(Object.assign({ msg, visited: [...done], labels: lab(), treeEdges: treeFromPrev(prev) }, x));
    snap('เริ่มที่ ' + nm(s) + ' ตั้งระยะเป็น 0 ส่วนจุดอื่นเป็น ∞ (ยังไปไม่ถึง)', { current: s });
    for (;;) {
      let u = null, best = Infinity;
      for (const n of nodes) if (!done.has(n.id) && dist[n.id] < best) { best = dist[n.id]; u = n.id; }
      if (u === null) break;
      done.add(u);
      snap('เลือก ' + nm(u) + ' เพราะใกล้ที่สุดในกลุ่มที่ยังไม่ยืนยัน (' + best + ' นาที) แล้วล็อกระยะนี้', { current: u });
      if (u === t) break;
      for (const { to, w } of adj[u]) {
        if (done.has(to)) continue;
        const nd = dist[u] + w;
        if (nd < dist[to]) {
          dist[to] = nd; prev[to] = u;
          snap('ผ่าน ' + nm(u) + ' ไป ' + nm(to) + ' ได้ ' + nd + ' นาที ดีกว่าเดิม จึงอัปเดต', { current: u, focus: key(u, to) });
        } else {
          snap(nm(to) + ' มีระยะ ' + dist[to] + ' อยู่แล้ว ดีกว่า ' + nd + ' จึงไม่เปลี่ยน', { current: u, focus: key(u, to) });
        }
      }
    }
    if (dist[t] === Infinity) {
      snap('ไปไม่ถึง ' + nm(t) + ' เพราะไม่มีเส้นเชื่อมต่อกัน', { result: 'ไม่พบเส้นทางจาก <b>' + nm(s) + '</b> ไป <b>' + nm(t) + '</b>' });
    } else {
      const p = pathTo(prev, t);
      snap('ได้เส้นทางที่เร็วที่สุดแล้ว', {
        pathNodes: p, pathEdges: edgesOfPath(p), treeEdges: [],
        result: 'เส้นทาง: <b>' + names(p) + '</b><br>รวม <b>' + dist[t] + ' นาที</b> ผ่าน ' + (p.length - 1) + ' เส้น'
      });
    }
    return out;
  }

  function runPrim(s) {
    const inT = new Set([s]), tree = [], out = []; let total = 0;
    const snap = (msg, x = {}) => out.push(Object.assign({ msg, visited: [...inT], treeEdges: [...tree] }, x));
    snap('เริ่มต้นต้นไม้ที่ ' + nm(s), { current: s });
    for (;;) {
      let best = null;
      for (const e of edges) if (inT.has(e.a) !== inT.has(e.b) && (!best || e.w < best.w)) best = e;
      if (!best) break;
      const nv = inT.has(best.a) ? best.b : best.a, from = nv === best.a ? best.b : best.a;
      inT.add(nv); tree.push(key(best.a, best.b)); total += best.w;
      snap('เส้นที่ถูกที่สุดที่ออกจากต้นไม้คือ ' + nm(from) + '–' + nm(nv) + ' (' + best.w + ') จึงเพิ่ม ' + nm(nv) + ' ต้นทุนรวม ' + total,
        { current: nv, focus: key(best.a, best.b) });
    }
    const all = inT.size === nodes.length;
    snap(all ? 'ต่อครบทุกจุดแล้ว' : 'กราฟนี้ไม่เชื่อมกันทั้งหมด จึงได้ต้นไม้เฉพาะส่วนที่ต่อถึง', {
      pathEdges: [...tree], treeEdges: [],
      result: 'ใช้ <b>' + tree.length + ' เส้น</b> ต้นทุนรวม <b>' + total + ' นาที</b>' + (all ? (() => {
        const kt = kruskalCore();
        return '<br>Kruskal ได้ต้นทุนรวม <b>' + kt.total + ' นาที</b> ' + (kt.total === total ? 'เท่ากัน (MST มีต้นทุนต่ำสุดได้ค่าเดียว)' : 'ต่างกัน: ตรวจสอบกราฟ');
      })() : '<br>มีจุดที่ต่อไม่ถึง ' + (nodes.length - inT.size) + ' จุด')
    });
    return out;
  }

  function primCore(s) {
    const inT = new Set([s]); let total = 0;
    for (;;) {
      let best = null;
      for (const e of edges) if (inT.has(e.a) !== inT.has(e.b) && (!best || e.w < best.w)) best = e;
      if (!best) break;
      inT.add(inT.has(best.a) ? best.b : best.a); total += best.w;
    }
    return { total, count: inT.size };
  }
  function kruskalCore() {
    const par = {}; nodes.forEach(n => par[n.id] = n.id);
    const find = x => { while (par[x] !== x) { par[x] = par[par[x]]; x = par[x]; } return x; };
    let total = 0, count = 0;
    for (const e of [...edges].sort((p, q) => p.w - q.w)) {
      const ra = find(e.a), rb = find(e.b);
      if (ra !== rb) { par[ra] = rb; total += e.w; count++; }
    }
    return { total, count };
  }

  function runKruskal() {
    const out = [], tree = []; let total = 0;
    const sorted = [...edges].sort((p, q) => p.w - q.w || p.a - q.a || p.b - q.b);
    const par = {}; nodes.forEach(n => par[n.id] = n.id);
    const find = x => { while (par[x] !== x) { par[x] = par[par[x]]; x = par[x]; } return x; };
    const compMap = () => {
      const roots = {}, m = {};
      nodes.forEach(n => { const r = find(n.id); if (!(r in roots)) roots[r] = Object.keys(roots).length; m[n.id] = roots[r]; });
      return m;
    };
    const snap = (msg, x = {}) => out.push(Object.assign({ msg, treeEdges: [...tree], comp: compMap() }, x));
    snap('เรียงเส้นจากถูกไปแพงทั้งหมด ' + sorted.length + ' เส้น เริ่มต้นทุกจุดเป็นกลุ่มของตัวเอง ('
      + sorted.slice(0, 5).map(e => e.w).join(', ') + (sorted.length > 5 ? ', …' : '') + ')');
    let stoppedEarly = false;
    for (let i = 0; i < sorted.length; i++) {
      const e = sorted[i], k = key(e.a, e.b), ra = find(e.a), rb = find(e.b);
      if (ra !== rb) {
        par[ra] = rb; tree.push(k); total += e.w;
        snap('เลือกเส้น ' + nm(e.a) + '–' + nm(e.b) + ' (' + e.w + ') เพราะเชื่อมสองกลุ่มที่ยังแยกกัน ต้นทุนรวม ' + total, { focus: k });
        if (tree.length === nodes.length - 1) { stoppedEarly = i < sorted.length - 1; break; }
      } else {
        snap('ข้ามเส้น ' + nm(e.a) + '–' + nm(e.b) + ' (' + e.w + ') เพราะสองจุดนี้อยู่กลุ่มเดียวกันแล้ว จะเกิดวงจร', { focus: k, reject: true });
      }
    }
    const connected = tree.length === nodes.length - 1;
    const pr = nodes.length ? primCore(nodes[0].id) : { total: 0 };
    let note = '';
    if (connected) note = '<br>Prim ได้ต้นทุนรวม <b>' + pr.total + ' นาที</b> ' + (pr.total === total ? 'เท่ากัน (MST มีต้นทุนต่ำสุดได้ค่าเดียว)' : 'ต่างกัน: ตรวจสอบกราฟ');
    else note = '<br>กราฟไม่เชื่อมกัน จึงได้ "ป่า" คือหนึ่งต้นไม้ต่อหนึ่งส่วนที่เชื่อมกัน';
    snap(connected ? (stoppedEarly ? 'ต่อครบทุกจุดแล้ว เส้นที่เหลือจะเกิดวงจรทั้งหมดจึงไม่ต้องดูต่อ' : 'ต่อครบทุกจุดแล้ว')
                   : 'พิจารณาครบทุกเส้นแล้ว แต่กราฟไม่เชื่อมกันทั้งหมด', {
      pathEdges: [...tree], treeEdges: [],
      result: 'ใช้ <b>' + tree.length + ' เส้น</b> ต้นทุนรวม <b>' + total + ' นาที</b>' + note
    });
    return out;
  }

  /* ---------- playback ---------- */
  function compute() {
    steps = []; idx = -1; statusMsg = '';
    const A = ALGOS[algo];
    if (!nodes.length) { statusMsg = 'ยังไม่มีจุดบนแผนที่ ลองกด "แผนที่กรุงเทพ" หรือเพิ่มจุดเอง'; return false; }
    if (A.needStart && (startId === null || !N(startId))) { statusMsg = 'เลือกจุดเริ่มต้นก่อน'; return false; }
    if (algo === 'kruskal' && !edges.length) { statusMsg = 'ยังไม่มีเส้นเชื่อม ลองเพิ่มเส้นก่อน'; return false; }
    if (A.needEnd && (endId === null || !N(endId) || endId === startId)) { statusMsg = 'เลือกจุดปลายทางที่ไม่ใช่จุดเดียวกับจุดเริ่มต้น'; return false; }
    steps = algo === 'dijkstra' ? runDijkstra(startId, endId)
          : algo === 'prim' ? runPrim(startId) : runKruskal();
    return true;
  }
  function next() {
    if (!steps.length && !compute()) { fullUpdate(); return false; }
    if (idx < steps.length - 1) idx++;
    fullUpdate();
    if (idx >= steps.length - 1) stop();
    return idx < steps.length - 1;
  }
  function back() { stop(); if (idx >= 0) idx--; fullUpdate(); }
  function reset() { stop(); steps = []; idx = -1; statusMsg = ''; fullUpdate(); }
  function stop() { if (timer) { clearInterval(timer); timer = null; } $('btnPlay').textContent = 'เล่น'; }
  function play() {
    if (timer) { stop(); return; }
    if (!steps.length || idx >= steps.length - 1) { steps = []; idx = -1; if (!compute()) { fullUpdate(); return; } }
    $('btnPlay').textContent = 'หยุด';
    const tick = () => { if (!next()) stop(); };
    timer = setInterval(tick, 1550 - +$('speed').value);
    tick();
  }
  $('speed').addEventListener('input', () => {
    if (timer) { clearInterval(timer); timer = setInterval(() => { if (!next()) stop(); }, 1550 - +$('speed').value); }
  });

  /* ---------- rendering ---------- */
  function render() {
    svg.classList.toggle('noanim', !!drag);
    const A = ALGOS[algo];
    const st = idx >= 0 ? steps[idx] : null;
    const compSize = {};
    if (st && st.comp) Object.values(st.comp).forEach(c => compSize[c] = (compSize[c] || 0) + 1);
    const tree = new Set(st && st.treeEdges || []), path = new Set(st && st.pathEdges || []);
    const visited = new Set(st && st.visited || []), front = new Set(st && st.frontier || []);
    const onPath = new Set(st && st.pathNodes || []);
    const labels = st && st.labels || {};
    let h = '';
    const cls = e => { const k = key(e.a, e.b); return st && st.focus === k ? (st.reject ? 'edge reject' : 'edge focus') : path.has(k) ? 'edge path' : tree.has(k) ? 'edge tree' : 'edge'; };
    const rank = e => { const c = cls(e); return (c.includes('focus') || c.includes('reject')) ? 3 : c.includes('path') ? 2 : c.includes('tree') ? 1 : 0; };
    [...edges].sort((p, q) => rank(p) - rank(q)).forEach(e => {
      const a = N(e.a), b = N(e.b);
      h += '<line pathLength="1" class="' + cls(e) + '" x1="' + a.x + '" y1="' + a.y + '" x2="' + b.x + '" y2="' + b.y + '"/>';
    });
    edges.forEach((e, i) => {
      const a = N(e.a), b = N(e.b);
      h += '<line class="hit" data-edge="' + i + '" x1="' + a.x + '" y1="' + a.y + '" x2="' + b.x + '" y2="' + b.y + '"/>';
    });
    edges.forEach(e => {
      const a = N(e.a), b = N(e.b), mx = (a.x + b.x) / 2, my = (a.y + b.y) / 2, s = String(e.w), w = 12 + s.length * 8;
      const on = path.has(key(e.a, e.b));
      h += '<g pointer-events="none"><rect class="wbox' + (on ? ' on' : '') + '" x="' + (mx - w / 2) + '" y="' + (my - 10) + '" width="' + w + '" height="20" rx="6"/><text class="wtxt' + (on ? ' on' : '') + '" x="' + mx + '" y="' + my + '">' + s + '</text></g>';
    });
    nodes.forEach(n => {
      let c = 'node';
      if (visited.has(n.id)) c += ' visited';
      if (front.has(n.id)) c += ' frontier';
      if (st && st.current === n.id) c += ' current';
      if (onPath.has(n.id)) c += ' onpath';
      if (pending === n.id) c += ' pending';
      h += '<g data-node="' + n.id + '">';
      if ((A.needStart && n.id === startId) || (A.needEnd && n.id === endId)) h += '<circle class="ring" cx="' + n.x + '" cy="' + n.y + '" r="20"/>';
      h += '<circle class="hit" style="stroke-width:0;fill:transparent" cx="' + n.x + '" cy="' + n.y + '" r="26"/>';
      const cc = st && st.comp ? st.comp[n.id] : undefined;
      const fillStyle = (cc !== undefined && compSize[cc] > 1) ? ' style="fill:var(--c' + (cc % 6) + ')"' : '';
      h += '<circle class="' + c + '"' + fillStyle + ' cx="' + n.x + '" cy="' + n.y + '" r="13"/>';
      h += '<text class="nlabel" x="' + n.x + '" y="' + (n.y + 32) + '">' + n.name + '</text>';
      h += '</g>';
    });
    nodes.forEach(n => {
      const L = labels[n.id];
      if (L !== undefined) {
        const w = 12 + String(L).length * 7;
        h += '<g pointer-events="none"><rect class="badge" x="' + (n.x - w / 2) + '" y="' + (n.y - 38) + '" width="' + w + '" height="18" rx="9"/><text class="badge-t" x="' + n.x + '" y="' + (n.y - 29) + '">' + L + '</text></g>';
      }
      if (A.needStart && n.id === startId) h += '<text class="flag" pointer-events="none" x="' + (n.x + 20) + '" y="' + (n.y - 14) + '">เริ่ม</text>';
      if (A.needEnd && n.id === endId && n.id !== startId) h += '<text class="flag end" pointer-events="none" x="' + (n.x + 20) + '" y="' + (n.y - 14) + '">ถึง</text>';
    });
    layer.innerHTML = h;
  }

  function updateStatus() {
    const st = idx >= 0 ? steps[idx] : null;
    $('prog').textContent = steps.length ? 'ขั้นที่ ' + (idx + 1) + ' จาก ' + steps.length : (statusMsg ? 'ยังเริ่มไม่ได้' : 'พร้อมเริ่ม');
    $('msg').textContent = st ? st.msg : (statusMsg || 'กด "เล่น" เพื่อดูอัลกอริทึมทำงานอัตโนมัติ หรือ "ถัดไป" เพื่อไปทีละขั้น');
    const r = $('result');
    if (st && st.result) { r.hidden = false; r.innerHTML = st.result; } else { r.hidden = true; }
    const log = $('log');
    log.innerHTML = idx >= 0 ? steps.slice(0, idx + 1).map((s, i) => '<li class="' + (i === idx ? 'now' : '') + '">' + s.msg + '</li>').join('') : '';
    $('logEmpty').hidden = idx >= 0;
    log.scrollTop = log.scrollHeight;
    $('btnBack').disabled = idx < 0;
    $('btnNext').disabled = steps.length > 0 && idx >= steps.length - 1;
    $('sV').textContent = nodes.length; $('sE').textContent = edges.length;
  }
  function fullUpdate() {
    const A = ALGOS[algo];
    $('aTitle').textContent = A.title; $('aDesc').textContent = A.desc; $('aCx').innerHTML = A.cx;
    $('startWrap').style.display = A.needStart ? '' : 'none';
    $('endWrap').style.display = A.needEnd ? '' : 'none';
    $('rowSel').style.display = (A.needStart || A.needEnd) ? '' : 'none';
    document.querySelectorAll('#algoTabs button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.algo === algo)));
    document.querySelectorAll('#tools button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.tool === tool)));
    canvas.dataset.tool = tool; $('hint').textContent = HINTS[tool];
    render(); updateStatus();
  }
  function syncSelects() {
    if (startId !== null && !N(startId)) startId = null;
    if (endId !== null && !N(endId)) endId = null;
    if (startId === null && nodes.length) startId = nodes[0].id;
    if (endId === null && nodes.length > 1) endId = nodes[nodes.length - 1].id;
    const opts = sel => nodes.map(n => '<option value="' + n.id + '"' + (n.id === sel ? ' selected' : '') + '>' + n.name + '</option>').join('');
    $('selStart').innerHTML = opts(startId); $('selEnd').innerHTML = opts(endId);
  }

  /* ---------- pointer interaction ---------- */
  function pt(e) {
    const p = svg.createSVGPoint(); p.x = e.clientX; p.y = e.clientY;
    const r = p.matrixTransform(svg.getScreenCTM().inverse());
    return { x: Math.max(24, Math.min(W - 24, r.x)), y: Math.max(24, Math.min(H - 34, r.y)) };
  }
  function hidePop() { $('pop').hidden = true; weightEdge = null; }
  function showPop(i) {
    const e = edges[i], a = N(e.a), b = N(e.b);
    weightEdge = i;
    const pop = $('pop');
    pop.style.left = ((a.x + b.x) / 2 / W * 100) + '%';
    pop.style.top = ((a.y + b.y) / 2 / H * 100) + '%';
    pop.hidden = false; $('popIn').value = e.w; $('popIn').focus(); $('popIn').select();
  }
  function applyPop() {
    if (weightEdge === null) return;
    const v = Math.round(+$('popIn').value);
    if (v >= 1 && v <= 999) { edges[weightEdge].w = v; hidePop(); changed(); } else { $('popIn').focus(); }
  }
  $('popOk').addEventListener('click', applyPop);
  $('popIn').addEventListener('keydown', e => { if (e.key === 'Enter') applyPop(); if (e.key === 'Escape') hidePop(); });

  svg.addEventListener('pointerdown', e => {
    const nEl = e.target.closest('[data-node]'), eEl = e.target.closest('[data-edge]');
    const p = pt(e);
    if (tool !== 'weight') hidePop();
    if (tool === 'move') {
      if (nEl) { drag = { id: +nEl.dataset.node }; svg.setPointerCapture(e.pointerId); }
    } else if (tool === 'add') {
      if (!nEl && !eEl) { addNode(p.x, p.y); changed(); }
    } else if (tool === 'link') {
      if (nEl) {
        const id = +nEl.dataset.node;
        if (pending === null) { pending = id; fullUpdate(); }
        else if (pending !== id) {
          const ok = addEdge(pending, id, defaultW(pending, id));
          const idxNew = edges.length - 1; pending = null; changed();
          if (ok) showPop(idxNew);
        } else { pending = null; fullUpdate(); }
      } else { pending = null; fullUpdate(); }
    } else if (tool === 'weight') {
      if (eEl) showPop(+eEl.dataset.edge); else hidePop();
    } else if (tool === 'del') {
      if (nEl) { removeNode(+nEl.dataset.node); changed(); }
      else if (eEl) { edges.splice(+eEl.dataset.edge, 1); changed(); }
    }
  });
  svg.addEventListener('pointermove', e => {
    if (!drag) return;
    const p = pt(e), n = N(drag.id);
    n.x = Math.round(p.x); n.y = Math.round(p.y); drag.moved = true;
    render();
  });
  const endDrag = () => { if (drag && drag.moved) { stop(); steps = []; idx = -1; statusMsg = ''; fullUpdate(); } drag = null; };
  svg.addEventListener('pointerup', endDrag);
  svg.addEventListener('pointercancel', endDrag);

  /* ---------- wiring ---------- */
  document.querySelectorAll('#tools button').forEach(b => b.addEventListener('click', () => { tool = b.dataset.tool; pending = null; hidePop(); fullUpdate(); }));
  document.querySelectorAll('#algoTabs button').forEach(b => b.addEventListener('click', () => { algo = b.dataset.algo; reset(); }));
  $('selStart').addEventListener('change', e => { startId = +e.target.value; reset(); });
  $('selEnd').addEventListener('change', e => { endId = +e.target.value; reset(); });
  $('btnPlay').addEventListener('click', play);
  $('btnNext').addEventListener('click', () => { stop(); next(); });
  $('btnBack').addEventListener('click', back);
  $('btnReset').addEventListener('click', reset);
  $('btnBkk').addEventListener('click', loadBangkok);
  $('btnRand').addEventListener('click', loadRandom);
  $('btnClear').addEventListener('click', clearAll);

  loadBangkok();
})();
</script>
</body>
</html>
"""


def show_page(html, height):
    """Streamlit รุ่นใหม่ใช้ st.iframe ส่วนรุ่นเก่าใช้ components.html"""
    if hasattr(st, "iframe"):
        st.iframe(html, width="stretch", height=height)
    else:
        import streamlit.components.v1 as components
        components.html(html, height=height, scrolling=True)


show_page(HTML, PAGE_HEIGHT)