(function(){
  var doc=document;
  var SPA=doc.body.getAttribute('data-mode')==='spa';
  var TITLES={home:'Abhishek Prakash — Digital Marketing Specialist & Meta Ads Expert in Dubai',about:'About — Abhishek Prakash',services:'Services — Abhishek Prakash',clients:'Clients — Abhishek Prakash',kannur:'Digital Marketing Strategist in Kannur, Kerala — Abhishek Prakash',kozhikode:'Digital Marketing Strategist in Kozhikode (Calicut) — Abhishek Prakash',contact:'Contact — Abhishek Prakash'};

  /* image fallback: keep the designed art when a photo can't load */
  function guard(img){
    function drop(){img.remove();}
    if(img.complete&&img.naturalWidth===0){drop();return;}
    img.addEventListener('error',drop);
  }
  doc.querySelectorAll('.ph>img').forEach(guard);

  /* online logos (hosted site only): show the name if the image can't load */
  doc.querySelectorAll('.plate>img').forEach(function(img){
    if(img.src.indexOf('data:')===0)return;
    function fail(){img.remove();}
    img.addEventListener('error',fail);
    if(img.complete&&img.naturalWidth===0)fail();
  });

  /* mobile menu */
  var nav=doc.querySelector('.nav'),mb=doc.querySelector('.menu-btn');
  if(mb){mb.addEventListener('click',function(){var o=nav.classList.toggle('open');mb.setAttribute('aria-expanded',o?'true':'false');});}
  function closeMenu(){if(nav){nav.classList.remove('open');}if(mb){mb.setAttribute('aria-expanded','false');}}

  /* split headings into words so they can animate in */
  function splitWords(el,cls){
    if(el.getAttribute('data-split'))return;
    el.setAttribute('data-split','1');
    el.setAttribute('aria-label',el.textContent.replace(/\s+/g,' ').trim());
    var i=0;
    (function walk(node){
      Array.prototype.slice.call(node.childNodes).forEach(function(n){
        if(n.nodeType===3){
          var frag=doc.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function(part){
            if(!part)return;
            if(/^\s+$/.test(part)){frag.appendChild(doc.createTextNode(part));return;}
            var w=doc.createElement('span');w.className='w';w.setAttribute('aria-hidden','true');w.style.setProperty('--i',i++);w.textContent=part;frag.appendChild(w);
          });
          node.replaceChild(frag,n);
        }else if(n.nodeType===1&&n.tagName!=='BR'&&n.tagName.toLowerCase()!=='svg'){walk(n);}
      });
    })(el);
    el.classList.add(cls);
  }
  doc.querySelectorAll('.q-lead').forEach(function(el){splitWords(el,'split-hl');});

  /* hero name: letters rise in one by one, then a soft glow passes over them now and then */
  (function(){
    var ht=doc.querySelector('.hero-title');
    if(!ht||(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches))return;
    ht.setAttribute('aria-label',ht.textContent.replace(/\s+/g,' ').trim());
    var i=0;
    (function walk(node){
      Array.prototype.slice.call(node.childNodes).forEach(function(n){
        if(n.nodeType===3){
          var frag=doc.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function(part){
            if(!part)return;
            if(/^\s+$/.test(part)){frag.appendChild(doc.createTextNode(part));return;}
            var wd=doc.createElement('span');wd.className='wd';wd.setAttribute('aria-hidden','true');
            Array.from(part).forEach(function(c){var ch=doc.createElement('span');ch.className='ch';ch.style.setProperty('--i',i++);ch.textContent=c;wd.appendChild(ch);});
            frag.appendChild(wd);
          });
          node.replaceChild(frag,n);
        }else if(n.nodeType===1){walk(n);}
      });
    })(ht);
    ht.classList.add('name-anim');
  })();


  /* blur-to-focus reveal: blocks start blurred and sharpen as they enter the screen */
  var reduceMotion=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var RV=['.hero-copy>*','.hero-vis .pill','.portrait','.float-card','.page-hero .left>*','.page-hero .right','.about-hero .left>*','.about-photo .pop','.name-card',
    '.split-head>*','.ai-left>*','.ai-right>*','.story-copy>*','.story-vis','.stat','.tool','.jr','.xcell','.wm','.lead-cell','.next-row','.svc-detail','.also','.step',
    '.faq details','.social','.post-card','.brands-head>*','.marquee','.spot-logo','.spot-copy>*','.philosophy .label','.q-lead','.q-cols p','.q-sign','.c-item','.form .field','.edu-list>.label','.edu-item','.cta>div','.foot-top>*'];
  var GRID='.xgrid,.clients,.stats,.tools,.socials,.q-cols,.edu-items,.steps,.form';
  var io=null;
  function arm(el){el.classList.remove('is-in','done');if(io)io.observe(el);}
  if(!reduceMotion&&'IntersectionObserver' in window){
    io=new IntersectionObserver(function(es){
      es.forEach(function(en){
        if(!en.isIntersecting)return;
        var el=en.target;el.classList.add('is-in');io.unobserve(el);
        setTimeout(function(){el.classList.add('done');},1600);
      });
    },{threshold:.12,rootMargin:'0px 0px -6% 0px'});
    var counts=new Map();
    doc.querySelectorAll(RV.join(',')).forEach(function(el){
      if(el.classList.contains('bz'))return;
      var p=el.parentNode,i=counts.get(p)||0;counts.set(p,i+1);
      var grid=p.matches&&p.matches(GRID);
      var d=(grid?i%4:Math.min(i,6))*0.09+(el.classList.contains('float-card')?0.45:0);
      el.style.setProperty('--d',d.toFixed(2)+'s');
      el.classList.add('bz');
      io.observe(el);
    });
  }
  doc.documentElement.classList.remove('rv-js');

  /* SPA routing on the hash */
  var shown=false;
  function show(){
    var id=(location.hash||'#home').slice(1);
    if(!doc.querySelector('[data-page="'+id+'"]'))id='home';
    doc.querySelectorAll('[data-page]').forEach(function(s){
      var on=s.getAttribute('data-page')===id;
      s.hidden=!on;
      if(on){s.classList.remove('page-enter');void s.offsetWidth;s.classList.add('page-enter');}
    });
    doc.querySelectorAll('.nav a').forEach(function(a){
      if(a.getAttribute('data-nav')===id)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');
    });
    var tEl=doc.querySelector('[data-page="'+id+'"]');
    doc.title=(tEl&&tEl.getAttribute('data-title'))||TITLES[id]||TITLES.home;
    window.scrollTo(0,0);
    var pg=doc.querySelector('[data-page="'+id+'"]');
    if(pg&&io&&shown)pg.querySelectorAll('.bz').forEach(arm);
    shown=true;
    closeMenu();
  }
  if(SPA){window.addEventListener('hashchange',show);show();}
  else{
    var cur=doc.body.getAttribute('data-current');
    doc.querySelectorAll('.nav a').forEach(function(a){if(a.getAttribute('data-nav')===cur)a.setAttribute('aria-current','page');});
  }

  /* service switcher on home */
  var SVC={
    meta:{t:'Facebook & Instagram Ads',tag:'Most requested',d:'Smart ad strategies that don’t just get clicks. They get results. I target the right audience, test, optimise and track every conversion to stretch your budget for maximum impact.',c:['Audience targeting','A/B testing','Budget optimisation','Conversion tracking','Content planning','Ad scripts & reels']},
    seo:{t:'SEO & Content Strategy',tag:'Organic growth',d:'Great content deserves to be found. Keyword research, on-page optimisation and performance tracking help your site climb the rankings and bring in the right kind of traffic.',c:['Keyword research','On-page optimisation','Content planning','Performance tracking','Search-friendly copy','Monthly reporting']},
    wp:{t:'WordPress Website Management',tag:'Websites',d:'Websites that look great and work smoothly. I customise themes, tune speed and keep your site user-friendly, mobile-ready and designed to convert.',c:['Theme customisation','Speed optimisation','Mobile-ready layouts','On-site SEO','Landing pages','Ongoing updates']},
    gads:{t:'Google Ads',tag:'High intent',d:'Ads that put your brand right where people are searching. Keyword research, ad copy, bidding strategy and tracking across Search, Display and YouTube.',c:['Search campaigns','Display campaigns','YouTube campaigns','Keyword research','Ad copywriting','Bidding strategy']}
  };
  var items=doc.querySelectorAll('.svc-item');
  items.forEach(function(b){
    b.addEventListener('click',function(){
      var k=b.getAttribute('data-svc'),s=SVC[k];if(!s)return;
      items.forEach(function(x){x.setAttribute('aria-selected',x===b?'true':'false');});
      var card=doc.querySelector('.feat-card');
      card.querySelector('[data-f="t"]').textContent=s.t;
      card.querySelector('[data-f="tag"]').textContent=s.tag;
      card.querySelector('[data-f="d"]').textContent=s.d;
      var ul=card.querySelector('[data-f="c"]');ul.innerHTML='';
      s.c.forEach(function(x){var li=doc.createElement('li');li.textContent=x;ul.appendChild(li);});
      card.classList.remove('page-enter');void card.offsetWidth;card.classList.add('page-enter');
    });
  });

  /* copy buttons */
  doc.querySelectorAll('[data-copy]').forEach(function(btn){
    btn.addEventListener('click',function(){
      var v=btn.getAttribute('data-copy'),old=btn.textContent;
      function done(){btn.textContent='Copied';setTimeout(function(){btn.textContent=old;},1600);}
      function fallback(){var el=btn.closest('.c-item');var t=el&&el.querySelector('.v');if(t){var r=doc.createRange();r.selectNodeContents(t);var s=window.getSelection();s.removeAllRanges();s.addRange(r);}btn.textContent='Selected';setTimeout(function(){btn.textContent=old;},1600);}
      try{navigator.clipboard.writeText(v).then(done,fallback);}catch(e){fallback();}
    });
  });


  /* analytics events (GA4; does nothing when the tag is not on the page) */
  function track(name,params){try{if(typeof gtag==='function')gtag('event',name,params||{});}catch(e){}}
  doc.addEventListener('click',function(e){
    var a=e.target.closest&&e.target.closest('a[href]');if(!a)return;
    var h=a.getAttribute('href')||'',page=location.pathname;
    if(h.indexOf('wa.me/')>-1||h.indexOf('api.whatsapp.com')>-1)track('whatsapp_click',{page_path:page,link_text:(a.textContent||'').trim().slice(0,40)});
    else if(h.indexOf('tel:')===0)track('phone_click',{page_path:page});
    else if(h.indexOf('mailto:')===0)track('email_click',{page_path:page});
  });
  if(location.pathname.indexOf('/thanks')===0)track('generate_lead',{method:'contact_form'});

  /* contact form */
  var form=doc.getElementById('contact-form');
  if(form){
    form.addEventListener('submit',function(e){
      var ok=true;
      form.querySelectorAll('[required]').forEach(function(inp){
        var f=inp.closest('.field'),err=f.querySelector('.err'),bad=!inp.value.trim()||(inp.type==='email'&&!/^\S+@\S+\.\S+$/.test(inp.value));
        f.classList.toggle('bad',bad);
        err.textContent=bad?(inp.type==='email'&&inp.value.trim()?'Enter a valid email address, like name@company.com.':'This field is required.'):'';
        if(bad&&ok){inp.focus();ok=false;}
      });
      if(!ok){e.preventDefault();return;}
      if(form.hasAttribute('data-netlify'))return; /* Netlify Forms handles the real submission */
      e.preventDefault();
      var fn=form.fname.value.trim(),ln=form.lname.value.trim(),em=form.email.value.trim(),msg=form.message.value.trim();
      var body=msg+'\n\n— '+fn+' '+ln+' ('+em+')';
      var box=doc.getElementById('sent');
      box.hidden=false;
      box.querySelector('pre').textContent=body;
      var a=box.querySelector('a');
      a.href='mailto:abhisheksayyy@gmail.com?subject='+encodeURIComponent('Project enquiry from '+fn+' '+ln)+'&body='+encodeURIComponent(body);
    });
  }

  /* count up the achievement numbers once they scroll into view */
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function countUp(el){
    var end=parseFloat(el.getAttribute('data-count')),dec=+(el.getAttribute('data-dec')||0),t0=null,dur=1100;
    function step(t){if(!t0)t0=t;var k=Math.min(1,(t-t0)/dur),e=1-Math.pow(1-k,3);el.textContent=(end*e).toFixed(dec);if(k<1)requestAnimationFrame(step);else el.textContent=end.toFixed(dec);}
    requestAnimationFrame(step);
  }
  if(!reduce&&'IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.querySelectorAll('[data-count]').forEach(countUp);io.unobserve(en.target);}});},{threshold:.4});
    doc.querySelectorAll('.results').forEach(function(r){io.observe(r);});
  }

  var y=doc.querySelectorAll('[data-year]');y.forEach(function(n){n.textContent=new Date().getFullYear();});
})();
