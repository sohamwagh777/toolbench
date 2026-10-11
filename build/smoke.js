// Functional smoke: run each page's inline <script> under a minimal DOM stub; report throws.
const fs = require("fs");
const dir = process.argv[2];
const files = fs.readdirSync(dir).filter(f => f.endsWith(".html"));

function makeEl(id) {
  const el = {
    id, value: id === "ta" || id === "r" ? "sample text 123" : "", checked: false,
    style: {}, textContent: "", innerHTML: "", label: "", dataset: {},
    addEventListener() {}, appendChild() {}, removeChild() {}, setAttribute() {},
    insertBefore() {}, classList: { add() {}, remove() {}, contains() { return false; } },
    closest() { return null; }, focus() {}, select() {}, getBoundingClientRect() { return { x: 0, y: 0, width: 300, height: 200, top: 0, left: 0 }; },
    children: [], querySelector() { return makeEl("sub"); }, querySelectorAll() { return []; },
    getContext() { return ctx2d; }, width: 300, height: 300, textLength: 10,
  };
  return el;
}
const ctx2d = new Proxy({}, { get: (t, k) => { if (k === "canvas") return makeEl("cv"); return typeof k === "string" ? (() => { }) : undefined; }, set: () => true });

function makeDoc() {
  const doc = {
    getElementById: id => makeEl(id),
    createElement: tag => makeEl("new-" + tag),
    querySelector: s => makeEl("q" + s),
    querySelectorAll: s => [makeEl("qa" + s)],
    addEventListener() {}, removeEventListener() {},
    documentElement: makeEl("html"), body: makeEl("body"), head: makeEl("head"),
    activeElement: makeEl("active"), fonts: { ready: Promise.resolve() },
    hidden: false, visibilityState: "visible", title: "t",
    createDocumentFragment: () => makeEl("frag"),
  };
  return doc;
}

let fails = [];
for (const f of files) {
  const html = fs.readFileSync(dir + "/" + f, "utf8");
  const scripts = [...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(m => m[1]).join("\n;\n");
  if (!scripts.trim()) continue;
  const doc = makeDoc();
  const win = {
    document: doc, addEventListener() {}, dispatchEvent() {},
    requestAnimationFrame: cb => { cb(performance.now()); return 1; },
    cancelAnimationFrame() {}, setInterval: () => 1, clearInterval() {},
    setTimeout: (cb) => { try { cb && cb(); } catch (e) { } return 2; }, clearTimeout() {},
    innerWidth: 800, innerHeight: 900, devicePixelRatio: 1,
    AudioContext: function () { return { destination: {}, createOscillator: () => ({ connect() {}, start() {}, stop() {}, frequency: {} }), close() {} }; },
    ResizeObserver: function () { return { observe() {}, unobserve() {} }; },
    matchMedia: () => ({ matches: false, addEventListener() {} }),
    scrollTo() {}, getComputedStyle: () => ({ getPropertyValue: () => "" }),
    localStorage: { getItem: () => null, setItem() {}, removeItem() {} },
    sessionStorage: { getItem: () => null, setItem() {}, removeItem() {} },
    navigator: { clipboard: { writeText: () => Promise.resolve() } },
    crypto: { subtle: { digest: () => Promise.resolve(new ArrayBuffer(32)) }, getRandomValues: a => a },
    Image: function () { return { set src(v) { }, onload: null }; },
    Audio: function () { return { play: () => Promise.resolve(), pause() {} }; },
    fetch: () => Promise.reject(new Error("no-net")),
    performance: { now: () => 1234 },
  };
  try {
    const fn = new Function("window", "document", "navigator", "localStorage", "sessionStorage", "crypto", "fetch", "performance", "requestAnimationFrame", "cancelAnimationFrame", "setInterval", "clearInterval", "setTimeout", "AudioContext", "ResizeObserver", "matchMedia", "scrollTo", "getComputedStyle", "Image", "Audio", "self",
      '"use strict";' + scripts);
    fn(win, doc, win.navigator, win.localStorage, win.sessionStorage, win.crypto, win.fetch, win.performance,
      win.requestAnimationFrame, win.cancelAnimationFrame, win.setInterval, win.clearInterval, win.setTimeout,
      win.AudioContext, win.ResizeObserver, win.matchMedia, win.scrollTo, win.getComputedStyle, win.Image, win.Audio, win);
  } catch (e) {
    fails.push(f + " -> " + e.message.slice(0, 110));
  }
}
console.log(fails.length ? "RUNTIME-FAIL " + fails.length + ":\n" + fails.join("\n") : "PASS: " + files.length + " pages: inline script executed, no top-level throw");
