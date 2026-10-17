(function(){
  var cfg=window.JOG, P=cfg.items, N=P.length, i=0, hoek=0;
  var wijzer=document.getElementById('wijzer'), titel=document.getElementById('titel'), scherm=document.getElementById('scherm'), tekst=document.getElementById('tekst'), jog=document.getElementById('jog'), labels=document.getElementById('labels');
  var kuil=document.getElementById('kuiltjes'); if(kuil){ for(var k=0;k<22;k++){ var d=document.createElement('i'); var a=360/22*k; d.style.transform='rotate('+a+'deg) translateY('+(window.innerWidth<600?'-640%':'-560%')+')'; kuil.appendChild(d); } }
  var off=180/N; // labels tussen de kwartieren, zoals SLIP/VINYL/SYNC/MASTER
  if(labels) P.forEach(function(p){ var sp=document.createElement('span'); sp.textContent=p.kort||p.titel; labels.appendChild(sp); });
  function plaats(){ if(!labels) return; var r=labels.clientWidth/2-11; labels.querySelectorAll('span').forEach(function(sp,k){ var a=360/N*k+off, flip=(a>90&&a<270)?180:0; sp.style.transform='translate(-50%,-50%) rotate('+a+'deg) translateY('+(-r)+'px) rotate('+flip+'deg)'; }); }
  plaats(); window.addEventListener('resize',plaats);
  function esc(t){return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function toon(){
    var p=P[i]; titel.textContent=p.kort||p.titel;
    if(p.beeld){ scherm.style.backgroundImage='url('+p.beeld+')'; scherm.classList.add('foto'); } else { scherm.style.backgroundImage=''; scherm.classList.remove('foto'); }
    wijzer.style.transform='rotate('+(hoek+off)+'deg)';
    if(labels) labels.querySelectorAll('span').forEach(function(sp,k){sp.classList.toggle('aan',k===i)});
    if(P[i].slug&&history.replaceState) history.replaceState(null,'','#'+P[i].slug);
    tekst.classList.remove('wissel'); void tekst.offsetWidth; tekst.classList.add('wissel');
    var h='<ul class="dots" aria-label="Onderdelen">'+P.map(function(q,k){return '<li><button type="button" data-k="'+k+'"'+(k===i?' class="aan" aria-current="true"':'')+' aria-label="'+esc(q.titel)+'"></button></li>'}).join('')+'</ul>';
    if(cfg.midden){ h+='<h2>'+esc(p.titel)+'</h2>'+(p.statement?'<p class="sub">'+esc(p.statement)+'</p>':'')+'<p>'+esc(p.intro)+'</p>'; }
    else { h+='<p class="label">'+esc(p.titel)+'</p><h2>'+esc(p.statement)+'</h2><p>'+esc(p.intro)+'</p>'; }
    if(p.principes&&p.principes.length) h+='<ul class="principes">'+p.principes.map(function(t){return '<li>'+esc(t)+'</li>'}).join('')+'</ul>';
    if(p.waar&&p.waar.length) h+='<div class="waar"><h3>Waar merk je dit aan?</h3><ul>'+p.waar.map(function(t){return '<li>'+esc(t)+'</li>'}).join('')+'</ul></div>';
    if(p.knop) h+='<p class="knoprij"><a class="wa sc" href="'+esc(p.href)+'">'+esc(p.knop)+'<i aria-hidden="true">→</i></a></p>';
    else if(p.href) h+='<p class="inline-link"><a href="'+esc(p.href)+'">Lees het hele principe →</a></p>';
    tekst.innerHTML=h;
  }
  function naar(k){ var d=((k-i)%N+N)%N; if(d===0) return; hoek+=360/N*d; i=k; toon(); }
  jog.addEventListener('click',function(){ naar((i+1)%N); });
  tekst.addEventListener('click',function(ev){ var b=ev.target.closest('button[data-k]'); if(b) naar(+b.dataset.k); });
  var x0=null;
  function start(ev){ x0=(ev.touches?ev.touches[0]:ev).clientX; }
  function eind(ev){ if(x0===null) return; var x1=(ev.changedTouches?ev.changedTouches[0]:ev).clientX, dx=x1-x0; x0=null; if(Math.abs(dx)>40){ naar(dx<0?(i+1)%N:(i-1+N)%N); } }
  [jog,tekst].forEach(function(el){ el.addEventListener('touchstart',start,{passive:true}); el.addEventListener('touchend',eind); });
  var h=location.hash.slice(1); P.forEach(function(p,k){ if(p.slug===h){ i=k; hoek=360/N*k; } });
  toon();
})();
