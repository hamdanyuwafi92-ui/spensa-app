const qs = (sel, parent = document) => parent.querySelector(sel);
const qsa = (sel, parent = document) => Array.from(parent.querySelectorAll(sel));