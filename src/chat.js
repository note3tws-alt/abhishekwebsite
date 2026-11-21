/* Chat assistant: answers common questions and passes visitor messages to Abhishek */
(function(){
  var doc=document;
  var WA='971588615423';
  var EMAIL='abhisheksayyy@gmail.com';
  var SPA=doc.body.getAttribute('data-mode')==='spa';
  function waIcon(){var i=doc.querySelector('.wa-ico');return i?'<img class="wa-ico" src="'+i.getAttribute('src')+'" alt="" width="16" height="16">':'';}
  function waLink(text){return 'https://wa.me/'+WA+'?text='+encodeURIComponent(text);}

  var A={
    greet:"Hi! I’m AP Assistant 👋 I can tell you about his services and results, or pass your message straight to him. What would you like to know?",
    services:"Abhishek offers:\n• Meta Ads & performance marketing\n• Social media marketing & content strategy\n• Video scripts & content production\n• Influencer marketing\n• Lead generation\n• Google Ads, SEO & WordPress websites",
    results:"Across the brands he manages, Abhishek’s Meta Ads average a 10–15X return on ad spend. He also built @TheWorldStories into a 3.2M-follower travel page on Twitter.",
    meta:"Meta Ads are Abhishek’s core skill. He plans Facebook and Instagram campaigns around leads and sales, tests creatives, and tracks every enquiry, averaging 10–15X ROAS across the brands he manages.",
    seo:"Yes, Abhishek handles SEO, local SEO and Google Ads, and builds fast WordPress websites so businesses get found when customers search.",
    price:"Pricing depends on what you need and your ad budget, so Abhishek shares a custom quote after a short chat. Want me to pass your details to him?",
    where:"Abhishek is based in Dubai and works with brands across the UAE and India, including Kannur, Kozhikode and the rest of Kerala. Most work happens over WhatsApp, calls and video meetings.",
    who:"Abhishek Prakash is a Dubai-based Digital Marketing Specialist with 7+ years of experience across India and the UAE. Most recently, he was Head of Marketing at Zee Real Estate in Dubai (August – October 2026).",
    content:"Yes. Abhishek writes video scripts, plans content calendars, coordinates shoots, manages video editors and runs influencer collaborations.",
    time:"Abhishek replies within 24 hours, 7 days a week.",
    fallback:"I’m not sure about that one. Would you like me to pass your question to Abhishek?"
  };
  var CHIPS_MAIN=[['Services','services'],['Results','results'],['Pricing','price'],['Contact Abhishek','lead']];

  function intent(t){
    t=t.toLowerCase();
    if(/\b(hi|hello|hey|salam|namaste)\b/.test(t))return 'greet';
    if(/(price|pricing|cost|charge|fee|budget|quote|rate|how much)/.test(t))return 'price';
    if(/(contact|talk|call|hire|whatsapp|email|reach|speak|meet|book|start|work with)/.test(t))return 'lead';
    if(/(roas|result|achiev|case|proof|follower|growth)/.test(t))return 'results';
    if(/(meta|facebook|instagram|fb ads|insta|ads)/.test(t))return 'meta';
    if(/(seo|google|rank|website|wordpress|search)/.test(t))return 'seo';
    if(/(video|reel|content|script|editor|influencer|shoot)/.test(t))return 'content';
    if(/(where|located|location|dubai|uae|kannur|kozhikode|calicut|kerala|india|remote)/.test(t))return 'where';
    if(/(who|about|experience|background|abhishek)/.test(t))return 'who';
    if(/(reply|response|how long|when|time)/.test(t))return 'time';
    if(/(service|offer|do you|help|provide)/.test(t))return 'services';
    return 'fallback';
  }

  /* ---- build the widget ---- */
  var root=doc.createElement('div');root.className='chat';
  root.innerHTML=
    '<button class="chat-launch" type="button" aria-expanded="false" aria-controls="chat-panel" aria-label="Open AP Assistant chat">'+
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5h16v11H9l-5 4z"/><circle cx="9" cy="10.5" r="1"/><circle cx="12" cy="10.5" r="1"/><circle cx="15" cy="10.5" r="1"/></svg>'+
      '<span class="chat-launch-label">Ask AP Assistant</span></button>'+
    '<section class="chat-panel" id="chat-panel" role="dialog" aria-label="Chat with AP Assistant" hidden>'+
      '<header class="chat-head"><span class="chat-av"></span><div><b>AP Assistant</b><span>Replies within 24 hours</span></div>'+
      '<button class="chat-x" type="button" aria-label="Close chat">×</button></header>'+
      '<div class="chat-log" aria-live="polite"></div>'+
      '<div class="chat-chips"></div>'+
      '<form class="chat-form"><label class="sr" for="chat-input">Type your message</label>'+
      '<input id="chat-input" autocomplete="off" placeholder="Type your message…" maxlength="500">'+
      '<button type="submit" aria-label="Send">'+
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12l16-8-6 16-2.5-6.5z"/></svg></button></form>'+
    '</section>';
  doc.body.appendChild(root);
  var launch=root.querySelector('.chat-launch'),panel=root.querySelector('.chat-panel'),log=root.querySelector('.chat-log'),
      chips=root.querySelector('.chat-chips'),form=root.querySelector('.chat-form'),input=root.querySelector('#chat-input');
  var face=doc.querySelector('.me-pic img');
  if(face){var im=doc.createElement('img');im.src=face.src;im.alt='';root.querySelector('.chat-av').appendChild(im);}

  var lead=null; /* {step, name, need, contact} */
  var started=false;

  function add(text,who,html){
    var m=doc.createElement('div');m.className='msg '+(who||'bot');
    if(html)m.innerHTML=html;else m.textContent=text;
    log.appendChild(m);log.scrollTop=log.scrollHeight;return m;
  }
  function typing(cb,ms){
    var t=add('','bot typing','<span></span><span></span><span></span>');
    setTimeout(function(){t.remove();cb();},ms||650);
  }
  function setChips(list){
    chips.innerHTML='';
    (list||[]).forEach(function(c){
      var b=doc.createElement('button');b.type='button';b.className='chip-q';b.textContent=c[0];
      b.addEventListener('click',function(){handle(c[0],c[1]);});chips.appendChild(b);
    });
  }
  function bot(key){typing(function(){add(A[key]);
    if(key==='price'||key==='fallback')setChips([['Yes, pass my details','lead'],['See services','services']]);
    else setChips(CHIPS_MAIN);});}

  function startLead(){
    lead={step:'name'};
    typing(function(){add('Great, I’ll pass this to Abhishek. What’s your name?');setChips([]);input.placeholder='Your name';input.focus();});
  }
  function leadStep(text){
    if(lead.step==='name'){lead.name=text;lead.step='need';
      typing(function(){add('Thanks, '+text.split(' ')[0]+'! What do you need help with? A line or two about your business and goals is perfect.');input.placeholder='What you need help with';});}
    else if(lead.step==='need'){lead.need=text;lead.step='contact';
      typing(function(){add('And the best email or WhatsApp number to reach you?');input.placeholder='Email or phone number';});}
    else if(lead.step==='contact'){
      var ok=/\S+@\S+\.\S+/.test(text)||/[\d\s+()-]{7,}/.test(text);
      if(!ok){typing(function(){add('That doesn’t look like an email or phone number. Could you check it? For example name@company.com or +971 50 123 4567.');});return;}
      lead.contact=text;lead.step='done';input.placeholder='Type your message…';
      finish();
    }
  }
  function summary(){return 'Hi Abhishek, I’m '+lead.name+'. '+lead.need+' You can reach me at '+lead.contact+'.';}
  function offerDirect(intro){
    add('',  'bot', intro+'<div class="msg-actions"><a class="msg-btn wa" href="'+waLink(summary())+'" target="_blank" rel="noopener">'+waIcon()+'Send on WhatsApp</a>'+
      '<a class="msg-btn" href="mailto:'+EMAIL+'?subject='+encodeURIComponent('Enquiry from '+lead.name)+'&body='+encodeURIComponent(summary())+'">Send by email</a></div>'+
      '<span class="msg-note">WhatsApp: +971 58 861 5423 · Email: '+EMAIL+'</span>');
    setChips(CHIPS_MAIN);
  }
  function finish(){
    if(SPA){typing(function(){offerDirect('Thanks! Tap below to send your message to Abhishek directly.');});return;}
    var body=new URLSearchParams({'form-name':'chatbot',name:lead.name,contact:lead.contact,message:lead.need,page:location.pathname});
    var t=add('','bot typing','<span></span><span></span><span></span>');
    fetch('/',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:body.toString()})
      .then(function(r){t.remove();if(!r.ok)throw new Error(r.status);
        try{if(typeof gtag==='function')gtag('event','generate_lead',{method:'chat_assistant'});}catch(e){}
        add('Thanks, '+lead.name.split(' ')[0]+'! Your message has been sent to Abhishek. He replies within 24 hours.');
        offerDirect('Want a faster reply? You can also message him directly:');})
      .catch(function(){t.remove();offerDirect('I couldn’t send that automatically. Please tap below to send it to Abhishek directly:');});
  }

  function handle(text,forced){
    add(text,'me');
    if(lead&&lead.step!=='done'&&!forced){leadStep(text);return;}
    var k=forced||intent(text);
    if(k==='lead'){startLead();return;}
    bot(k);
  }

  function open(auto){
    hideTeaser();
    panel.hidden=false;launch.setAttribute('aria-expanded','true');root.classList.add('is-open');
    if(!started){started=true;typing(function(){add(A.greet);setChips(CHIPS_MAIN);},500);}
    if(!auto)setTimeout(function(){input.focus();},60);
  }
  function close(){markSeen&&markSeen();panel.hidden=true;launch.setAttribute('aria-expanded','false');root.classList.remove('is-open');launch.focus();}
  launch.addEventListener('click',function(){panel.hidden?open():close();});

  /* pop up once per visit, 10 seconds after the page loads */
  var teaser=doc.createElement('div');teaser.className='chat-teaser';teaser.hidden=true;
  teaser.innerHTML='<button type="button" class="ct-open"><b>AP Assistant</b><span>Hi! Want to grow your business online? Ask me anything.</span></button><button type="button" class="ct-x" aria-label="Dismiss">×</button>';
  root.insertBefore(teaser,launch);
  function hideTeaser(){teaser.hidden=true;}
  teaser.querySelector('.ct-open').addEventListener('click',function(){open();});
  teaser.querySelector('.ct-x').addEventListener('click',hideTeaser);
  function seen(){try{return sessionStorage.getItem('ap-chat-pop')==='1';}catch(e){return false;}}
  function markSeen(){try{sessionStorage.setItem('ap-chat-pop','1');}catch(e){}}
  /* short two-note chime, generated in the browser (no audio file needed) */
  var AC=window.AudioContext||window.webkitAudioContext,actx=null;
  function unlock(){
    if(!AC)return;
    try{if(!actx)actx=new AC();if(actx.state==='suspended')actx.resume();}catch(e){}
  }
  ['pointerdown','keydown','touchstart'].forEach(function(ev){doc.addEventListener(ev,unlock,{once:true,passive:true});});
  function chime(){
    if(!actx||actx.state!=='running')return; /* browsers block sound until the visitor interacts */
    var t=actx.currentTime;
    [[784,0],[1175,0.13]].forEach(function(n){
      var o=actx.createOscillator(),g=actx.createGain();
      o.type='sine';o.frequency.value=n[0];
      g.gain.setValueAtTime(0.0001,t+n[1]);
      g.gain.exponentialRampToValueAtTime(0.18,t+n[1]+0.02);
      g.gain.exponentialRampToValueAtTime(0.0001,t+n[1]+0.55);
      o.connect(g);g.connect(actx.destination);o.start(t+n[1]);o.stop(t+n[1]+0.6);
    });
  }
  setTimeout(function(){
    if(started||seen()||!panel.hidden)return;
    markSeen();
    open(true);
    root.classList.add('popped');
    chime();
    setTimeout(function(){root.classList.remove('popped');},2400);
  },10000);
  root.querySelector('.chat-x').addEventListener('click',close);
  doc.addEventListener('keydown',function(e){if(e.key==='Escape'&&!panel.hidden)close();});
  form.addEventListener('submit',function(e){e.preventDefault();var v=input.value.trim();if(!v)return;input.value='';handle(v);});
  doc.querySelectorAll('[data-open-chat]').forEach(function(b){b.addEventListener('click',function(e){e.preventDefault();open();});});
})();
