(function(){
 // Keep the rail's open state across pages, but only where it is pinned beside
 // the content. On narrow screens it is a drawer over the page, and every page
 // opening with a drawer across it would be wrong.
 //
 // Stored in a cookie on the parent domain so it carries between olympiads:
 // each one is a separate subdomain, so localStorage -- which is per-origin --
 // kept a separate value for every single one of them.
 var cb=document.getElementById('nav');
 var wide=window.matchMedia('(min-width:1200px)');
 var ms=document.getElementById('mobile-search');
 var mm=document.getElementById('mobile-menu');
 var mq=document.getElementById('railq');
 var ri=document.querySelector('.railinner');
 function save(on){
  var v='nav='+(on?'1':'0')+';path=/;max-age=31536000;SameSite=Lax';
  var h=location.hostname, i=h.indexOf('.');
  // Exactly one cookie. Writing both a host-scoped and a domain-scoped copy
  // lets nav=0 and nav=1 coexist, and document.cookie gives no way to tell
  // which is which -- the reader would match whichever came first.
  // On localhost or a file:// preview there is no parent domain to share with,
  // and a domain= attribute there makes the browser reject the cookie.
  try{document.cookie=i>0?v+';domain=.'+h.slice(i+1):v;}catch(e){}
 }
 function syncMobile(){
  if(cb)cb.setAttribute('aria-expanded',cb.checked?'true':'false');
  var search=!!(cb&&cb.checked&&document.documentElement.classList.contains('mobile-search'));
  var menu=!!(cb&&cb.checked&&!search);
  if(ms){ms.setAttribute('aria-expanded',search?'true':'false');
   ms.setAttribute('aria-label',search?'Close search':'Search');}
  if(mm){mm.setAttribute('aria-expanded',menu?'true':'false');
   mm.setAttribute('aria-label',menu?'Close olympiad menu':'Open olympiad menu');}
 }
 if(cb){
  if(wide.matches)cb.checked=document.documentElement.classList.contains('nav-open');
  cb.addEventListener('change',function(){
   document.documentElement.classList.toggle('nav-open',cb.checked);
   if(!cb.checked)document.documentElement.classList.remove('mobile-search');
   if(wide.matches)save(cb.checked);
   syncMobile();
  });
  // The checkbox is the sidebar's keyboard control and looks like a button,
  // so Enter works on it as well as Space.
  cb.addEventListener('keydown',function(e){
   if(e.key==='Enter'){e.preventDefault();cb.click();}
  });
 }
 function openMobile(kind){
  if(!cb)return;
  if(ri)ri.scrollTop=0;
  if(kind==='menu'&&mq){mq.value='';mq.dispatchEvent(new Event('input'));}
  document.documentElement.classList.toggle('mobile-search',kind==='search');
  cb.checked=true;
  cb.dispatchEvent(new Event('change'));
  if(kind==='search'&&mq)setTimeout(function(){mq.focus();},0);
 }
 if(ms)ms.addEventListener('click',function(){
  if(cb.checked&&document.documentElement.classList.contains('mobile-search')){
   cb.checked=false;cb.dispatchEvent(new Event('change'));
  }else openMobile('search');
 });
 if(mm)mm.addEventListener('click',function(){
  if(cb.checked&&!document.documentElement.classList.contains('mobile-search')){
   cb.checked=false;cb.dispatchEvent(new Event('change'));
  }else openMobile('menu');
 });
 document.addEventListener('keydown',function(e){
  if(e.key==='Escape'&&cb&&cb.checked&&!wide.matches){
   // Focus inside the drawer would be left on something now hidden; hand it
   // back to whichever control opens the drawer at this width.
   var r=document.getElementById('rail'),back=r&&r.contains(document.activeElement);
   cb.checked=false;cb.dispatchEvent(new Event('change'));
   if(back)(mm&&mm.offsetParent?mm:cb).focus();
  }
 });
 // Peek: with a real mouse on a desktop, resting on the closed sidebar's
 // toggle slides the rail in over the page (html.rail-peek, see nav.css
 // "sidebar peek") without pushing it. After a short hover, so crossing the
 // toggle does not flash it; it stays while the pointer is on the toggle, the
 // wordmark or the rail, and goes a moment after it leaves all of them, so a
 // diagonal move into the rail does not lose it. Escape closes it. Clicking the
 // toggle pins it open as usual. The checkbox and the cookie are never
 // touched, and keyboard use is unchanged.
 var hov=window.matchMedia('(hover:hover) and (pointer:fine) and (min-width:992px)');
 var H=document.documentElement,rl=document.getElementById('rail');
 var bar=document.querySelector('.railbar'),tg=bar&&bar.querySelector('.tb-rail');
 var tIn=0,tOut=0;
 function peek(on){clearTimeout(tIn);clearTimeout(tOut);H.classList.toggle('rail-peek',on);}
 function peeking(){return H.classList.contains('rail-peek');}
 if(cb&&rl&&tg){
  tg.addEventListener('mouseenter',function(){
   clearTimeout(tOut);
   if(hov.matches&&!cb.checked&&!peeking())tIn=setTimeout(function(){peek(true);},170);
  });
  tg.addEventListener('mouseleave',function(){clearTimeout(tIn);});
  [bar,rl].forEach(function(el){
   el.addEventListener('mouseenter',function(){clearTimeout(tOut);});
   el.addEventListener('mouseleave',function(){
    if(peeking())tOut=setTimeout(function(){peek(false);},250);
   });
  });
  cb.addEventListener('change',function(){peek(false);});
  document.addEventListener('keydown',function(e){
   if(e.key==='Escape'&&peeking())peek(false);
  });
 }
 syncMobile();
})();

(function(){
  // ---- the way back up ----
  (function(){
    var b=document.createElement('button'); b.type='button'; b.className='totop';
    b.setAttribute('aria-label','Back to top'); b.title='Back to top';
    document.body.appendChild(b);
    var on=false;
    window.addEventListener('scroll',function(){
      var v=window.scrollY>1200; if(v!==on){on=v; b.classList.toggle('show',v);}
    },{passive:true});
    b.addEventListener('click',function(){window.scrollTo({top:0,behavior:
     window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});});
  })();
  var r=document.documentElement;
  var narrow=window.matchMedia('(max-width:991px)');
  // The selected button is not marked here. It used to be, and that left the
  // switch showing neither view selected from first paint until this script ran
  // at the end of the body -- and permanently if the script never ran. The
  // highlight is a CSS rule keyed off the v-cards/v-list class BOOT puts on
  // <html> before paint, so it is correct as early as the layout it describes.
  function set(v){
    if(narrow.matches) v='cards';
    r.classList.remove('v-cards','v-list');
    r.classList.add('v-'+v);
    save('view',v);
  }
  // Narrow screens are card-only, but a desktop list preference is left
  // untouched and restored if the viewport grows again (rotation or resizing).
  function syncView(){
    var m=document.cookie.match(/(?:^|; )view=(cards|list)/);
    var v=narrow.matches?'cards':(m?m[1]:'cards');
    r.classList.remove('v-cards','v-list');
    r.classList.add('v-'+v);
  }
  if(narrow.addEventListener) narrow.addEventListener('change',syncView);
  // Writing the cookie is the same job for both switches, so it is one function.
  function save(k,v){
    var c=k+'='+v+';path=/;max-age=31536000;SameSite=Lax';
    var h=location.hostname, i=h.indexOf('.');
    try{document.cookie=i>0?c+';domain=.'+h.slice(i+1):c;}catch(e){}
  }
  function mode(){
    // What is on screen right now, which is not the same as what is pinned:
    // with no cookie the class is absent and the system decides, so ask the
    // media query rather than assuming dark.
    if(r.classList.contains('light'))return 'light';
    if(r.classList.contains('dark'))return 'dark';
    return window.matchMedia('(prefers-color-scheme: light)').matches?'light':'dark';
  }
  function setMode(v){
    r.classList.remove('light','dark');
    r.classList.add(v);
    save('mode',v);
  }
  // Delegated, so the switch costs one listener rather than one per button.
  document.addEventListener('click',function(e){
    var sa=e.target.closest('.showall');
    if(sa){var bd=sa.closest('.band'), on=bd.classList.toggle('expanded');
      sa.textContent=on?'Show fewer':sa.textContent.replace('Show fewer','');
      if(!on) sa.textContent='Show all '+bd.querySelectorAll('.cols li').length+' problems'; return;}
    var b=e.target.closest('.viewsw button'); if(b) return set(b.dataset.v);
    if(e.target.closest('.modesw')) return setMode(mode()==='light'?'dark':'light');
    var g=e.target.closest('.subsw button');
    if(g){
      var on=g.classList.contains('on');
      r.className=r.className.replace(/\bs-\S+/g,'').replace(/\s+/g,' ').trim();
      // Clicking the chip you are already on clears it, so there is a way back
      // to the whole topic without hunting for another control.
      if(!on) r.classList.add('s-'+g.dataset.s);
      document.querySelectorAll('.subsw button').forEach(function(b){
        b.classList.toggle('on', b===g && !on);});
      return;
    }
    var f=e.target.closest('.topicsw button');
    if(f){
      // Changing topic drops any subtopic: the old one belongs to a topic you
      // are no longer looking at, and leaving it set would hide everything.
      r.className=r.className.replace(/\bs-\S+/g,'').replace(/\s+/g,' ').trim();
      document.querySelectorAll('.subsw button').forEach(function(b){
        b.classList.remove('on');});
      // One topic at a time, so the class is replaced rather than toggled. The
      // empty value is the All chip, which simply leaves no class behind.
      r.className=r.className.replace(/\bt-\S+/g,'').replace(/\s+/g,' ').trim();
      if(f.dataset.t) r.classList.add('t-'+f.dataset.t);
      document.querySelectorAll('.topicsw button').forEach(function(b){
        b.classList.toggle('on', b===f);});
    }});
})();

