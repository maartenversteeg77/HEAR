// Uitschuifpaneel "Alle producten" op productpagina's (alleen desktop). Besluit 30 okt 2026.
(function(){
  var t=document.querySelector('.ps-tab'),p=document.getElementById('ps'),sc=document.querySelector('.ps-scherm');
  if(!t||!p||!sc)return;
  var d=p.querySelector('.ps-dicht'),mq=matchMedia('(min-width:1101px)'),rust=matchMedia('(prefers-reduced-motion: reduce)');
  function open(f){p.hidden=false;sc.hidden=false;requestAnimationFrame(function(){requestAnimationFrame(function(){p.classList.add('open');sc.classList.add('open')})});t.setAttribute('aria-expanded','true');if(f)d.focus()}
  function dicht(f){p.classList.remove('open');sc.classList.remove('open');t.setAttribute('aria-expanded','false');setTimeout(function(){if(!p.classList.contains('open')){p.hidden=true;sc.hidden=true}},rust.matches?0:320);if(f)t.focus()}
  t.addEventListener('click',function(){open(true)});
  d.addEventListener('click',function(){dicht(true)});
  sc.addEventListener('click',function(){dicht(false)});
  document.addEventListener('keydown',function(ev){if(ev.key==='Escape'&&p.classList.contains('open'))dicht(true)});
  mq.addEventListener&&mq.addEventListener('change',function(){if(!mq.matches)dicht(false)});
  // eenmalig voorproefje per bezoek; niet bij 'minder beweging'
  try{
    if(mq.matches&&!rust.matches&&!sessionStorage.getItem('ps-gezien')){
      sessionStorage.setItem('ps-gezien','1');
      setTimeout(function(){open(false);setTimeout(function(){if(!p.matches(':hover'))dicht(false);else p.addEventListener('mouseleave',function(){dicht(false)},{once:true})},2200)},1000);
    }
  }catch(x){}
})();
