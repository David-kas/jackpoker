(function(){
const qs=(s,c=document)=>c.querySelector(s);const qsa=(s,c=document)=>Array.from(c.querySelectorAll(s));
const slug=(document.body.dataset.page||'index');
let lang=localStorage.getItem('lang')==='en'?'en':'ru';
let dict=null;
async function load(langCode){const res=await fetch('/lang/'+langCode+'.json');return res.json();}
function setMeta(page){if(!dict||!dict.meta||!dict.meta[page])return;const m=dict.meta[page];document.title=m.title;const d=qs('meta[name="description"]');if(d)d.content=m.description;const ogt=qs('meta[property="og:title"]');if(ogt)ogt.content=m.title;const ogd=qs('meta[property="og:description"]');if(ogd)ogd.content=m.description;const twt=qs('meta[name="twitter:title"]');if(twt)twt.content=m.title;const twd=qs('meta[name="twitter:description"]');if(twd)twd.content=m.description;}
function resolve(path){return path.split('.').reduce((a,k)=>a&&a[k],dict);} 
function apply(){if(!dict)return;document.documentElement.lang=lang;qsa('[data-lang]').forEach(el=>el.classList.toggle('active',el.dataset.lang===lang));
qsa('[data-i18n]').forEach(el=>{const v=resolve(el.dataset.i18n);if(typeof v==='string')el.textContent=v;});
qsa('[data-i18n-html]').forEach(el=>{const v=resolve(el.dataset.i18nHtml);if(typeof v==='string')el.innerHTML=v;});
qsa('[data-cta-idx]').forEach(el=>{const i=Number(el.dataset.ctaIdx)||0;el.textContent=(dict.cta&&dict.cta[i])||el.textContent;});
qsa('.lang-btn').forEach(b=>b.classList.toggle('active',b.dataset.setLang===lang));
setMeta(slug);
}
qsa('.lang-btn').forEach(btn=>btn.addEventListener('click',async()=>{const nxt=btn.dataset.setLang;if(nxt===lang)return;lang=nxt;localStorage.setItem('lang',lang);dict=await load(lang);apply();}));
qsa('.faq-q').forEach(btn=>btn.addEventListener('click',()=>btn.closest('.faq-item').classList.toggle('open')));
const burger=qs('.burger');const wrap=qs('.nav-wrap');if(burger&&wrap)burger.addEventListener('click',()=>wrap.classList.toggle('open'));
load(lang).then(d=>{dict=d;apply();});
})();
