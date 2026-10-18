const presets={
 en:{review:'Video review',versions:'Video versions',hint:'Choose a version or scroll to the next film.',swipe:'Scroll or swipe to compare',soundOff:'Enable sound',soundOn:'Mute sound',prev:'↑ Previous',next:'Next ↓',download:'Download MP4 ↓',language:'Video language',format:'Video format',copy:'Copy link',copied:'Current film link copied',copyFail:'Copy the browser address',error:'Unable to load the video list.',play:'Play'},
 zh:{review:'影片審閱',versions:'影片版本',hint:'選一款，或者上下滑動睇下一條。',swipe:'上下滑動，逐條比較',soundOff:'開啟聲音',soundOn:'關閉聲音',prev:'↑ 上一條',next:'下一條 ↓',download:'下載 MP4 ↓',language:'影片語言',format:'影片格式',copy:'複製連結',copied:'已複製目前影片連結',copyFail:'請複製瀏覽器網址',error:'影片列表未能載入。',play:'播放'}
};
const $=id=>document.getElementById(id);
const query=new URLSearchParams(location.search);
let config,locale,format,rows=[],active=0,observer,sound=false;
let requested=location.hash.slice(1);
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
const text=()=>config?.messages?.[locale]||presets[locale?.startsWith('zh')?'zh':'en'];
function url(){const u=new URL(location.href);u.searchParams.set('lang',locale);u.searchParams.set('format',format);u.hash=rows[active]?.id||requested;history.replaceState(null,'',u);}
function release(video){video.pause();if(video.hasAttribute('src')){video.removeAttribute('src');video.load();}}
function activate(index,play=true){
 if(index<0||index>=rows.length)return;
 active=index;requested=rows[index].id;
 [...$('feed').querySelectorAll('video')].forEach((video,i)=>{
  if(Math.abs(i-active)<=1){
   if(!video.hasAttribute('src')){video.src=rows[i].src;video.preload=i===active?'metadata':'none';video.load();}
   video.muted=i===active?!sound:true;
   if(i!==active)video.pause();else if(play)video.play().catch(()=>{});
  }else release(video);
 });
 $('counter').textContent=String(index+1).padStart(2,'0')+' / '+String(rows.length).padStart(2,'0');
 $('prev').disabled=index===0;$('next').disabled=index===rows.length-1;
 document.querySelectorAll('.version').forEach((a,i)=>{a.classList.toggle('active',i===active);if(i===active)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current');});
 $('status').textContent=requested;url();
}
function go(index){if(index>=0&&index<rows.length)$('feed').children[index].scrollIntoView({behavior:reduced?'instant':'smooth',block:'start'});}
function localize(){
 const t=text();document.documentElement.lang=locale;document.title=config.product+' · '+t.review;$('brand').textContent=config.product;
 $('locale').value=locale;$('format').value=format;$('locale').setAttribute('aria-label',t.language);$('format').setAttribute('aria-label',t.format);
 $('heading').textContent=t.versions;$('hint').textContent=t.hint;$('swipe').textContent=t.swipe;$('prev').textContent=t.prev;$('next').textContent=t.next;$('copy').textContent=t.copy;
 $('sound').textContent=sound?t.soundOn:t.soundOff;$('sound').setAttribute('aria-pressed',String(sound));$('versions').setAttribute('aria-label',t.versions);$('feed').setAttribute('aria-label',t.versions);
}
function render(){
 observer?.disconnect();$('feed').querySelectorAll('video').forEach(release);
 rows=config.rows.filter(r=>r.locale===locale&&r.format===format);
 active=Math.max(0,rows.findIndex(r=>r.id===requested));
 localize();$('versions').replaceChildren();$('feed').replaceChildren();
 const spec=config.formats.find(f=>f.id===format);
 rows.forEach((row,i)=>{
  const a=document.createElement('a');a.className='version';a.href='#'+row.id;
  const thumb=document.createElement('img');thumb.src=row.poster;thumb.alt='';thumb.loading='lazy';
  const title=document.createElement('span');title.textContent=row.id+' · '+row.name;a.append(thumb,title);a.onclick=e=>{e.preventDefault();go(i);};$('versions').append(a);
  const card=document.createElement('article');card.className='clip';card.dataset.index=String(i);card.setAttribute('aria-label',row.id+' · '+row.name);
  const player=document.createElement('div');player.className='player';player.style.setProperty('--ratio',String(spec.width/spec.height));
  const video=document.createElement('video');video.controls=true;video.playsInline=true;video.loop=true;video.preload='none';video.muted=true;video.poster=row.poster;video.setAttribute('aria-label',text().play+' '+row.name);
  video.addEventListener('play',()=>{if(i!==active)activate(i,false);$('feed').querySelectorAll('video').forEach(v=>{if(v!==video)v.pause();});});
  player.append(video);
  const info=document.createElement('div');info.className='clip-info';const copy=document.createElement('div');const h=document.createElement('h1');h.textContent=row.id+' · '+row.name;const p=document.createElement('p');p.textContent=config.locales.find(l=>l.id===locale).label+' · '+spec.width+' × '+spec.height+' · '+spec.duration_seconds+'s';copy.append(h,p);
  const download=document.createElement('a');download.className='download';download.href=row.src;download.download=row.src.split('/').pop();download.textContent=text().download;info.append(copy,download);card.append(player,info);$('feed').append(card);
 });
 const initial=active;
 requestAnimationFrame(()=>{
  $('feed').scrollTop=initial*$('feed').clientHeight;
  observer=new IntersectionObserver(entries=>{
   const candidates=entries.filter(e=>e.isIntersecting&&e.intersectionRatio>.6).sort((a,b)=>b.intersectionRatio-a.intersectionRatio);
   if(candidates[0]){const n=Number(candidates[0].target.dataset.index);if(n!==active)activate(n);}
  },{root:$('feed'),threshold:[.6,.8]});
  [...$('feed').children].forEach(card=>observer.observe(card));activate(initial);
 });
}
$('prev').onclick=()=>go(active-1);$('next').onclick=()=>go(active+1);
$('locale').onchange=()=>{requested=rows[active]?.id;locale=$('locale').value;render();};
$('format').onchange=()=>{requested=rows[active]?.id;format=$('format').value;render();};
$('sound').onclick=()=>{sound=!sound;localize();const video=$('feed').children[active]?.querySelector('video');if(video){video.muted=!sound;video.play().catch(()=>{});}};
$('copy').onclick=async()=>{try{await navigator.clipboard.writeText(location.href);$('status').textContent=text().copied;}catch{$('status').textContent=text().copyFail;}};
$('brand').onclick=e=>{e.preventDefault();go(0);};
document.addEventListener('keydown',e=>{if(e.target.closest('video,select,input,textarea,button,a'))return;if(['ArrowDown','ArrowUp'].includes(e.key)){e.preventDefault();go(active+(e.key==='ArrowDown'?1:-1));}});
window.addEventListener('hashchange',()=>{const n=rows.findIndex(r=>r.id===location.hash.slice(1));if(n>=0&&n!==active)go(n);});
document.addEventListener('visibilitychange',()=>{const v=$('feed').children[active]?.querySelector('video');if(document.hidden)v?.pause();else v?.play().catch(()=>{});});
try{
 const response=await fetch('videos.json');if(!response.ok)throw Error('Manifest unavailable');config=await response.json();
 if(!config.rows?.length||!config.locales?.length||!config.formats?.length)throw Error('Empty manifest');
 for(const name of ['paper','ink','accent'])if(config.brand?.[name])document.documentElement.style.setProperty('--'+name,config.brand[name]);
 locale=config.locales.some(l=>l.id===query.get('lang'))?query.get('lang'):config.locales[0].id;
 format=config.formats.some(f=>f.id===query.get('format'))?query.get('format'):config.formats[0].id;
 for(const l of config.locales){const o=document.createElement('option');o.value=l.id;o.textContent=l.label;$('locale').append(o);}
 for(const f of config.formats){const o=document.createElement('option');o.value=f.id;o.textContent=f.label||f.id;$('format').append(o);}
 render();
}catch{$('status').textContent=text().error;}
