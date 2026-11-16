# Service pages (/services/...) and case studies (/case-studies/...) for abhishekreally.com.
# build.py renders each entry into a page, adds it to the sitemap and writes its structured data.
# Content rules: no invented numbers, clients, results or credentials. Case studies separate
# Abhishek's own work from team work, and say plainly when figures are not published.

ROAS_NOTE = ('The 10–15X figure is an average return on ad spend on Meta Ads across the brands I manage. '
             'It is an average, not a promise: results depend on the product, offer, budget and market. '
             'Lead-generation campaigns are judged on cost per qualified lead, not ROAS.')

# ---------------------------------------------------------------- services
SERVICE_PAGES = [
{
 'id': 'svc-performance', 'slug': 'services/performance-marketing', 'crumb': 'Performance Marketing',
 'name': 'Performance Marketing',
 'seo_title': 'Performance Marketing Specialist in Dubai | Abhishek Prakash',
 'desc': 'Performance marketing in Dubai and Kerala: paid campaigns planned, tracked and optimised around sales and qualified leads, not likes. By Abhishek Prakash.',
 'pill': 'Service · Performance marketing',
 'h1': 'Performance marketing <span class="ghost">measured in sales and leads.</span>',
 'lead': 'I plan, run and optimise paid campaigns around one question: what did this bring the business? Every campaign starts with a clear goal, proper tracking and a budget that moves to what works.',
 'incl_h': 'What’s included <span class="ghost">in performance marketing.</span>',
 'incl_p': 'From the first plan to the weekly optimisation, handled by one person.',
 'incl': [
   ('target', 'Goal and funnel planning', 'One clear goal per campaign: sales, leads or messages, mapped to how your customers buy.'),
   ('chart', 'Tracking set-up checks', 'Conversion and ROAS tracking checked before money is spent, so results can be trusted.'),
   ('megaphone', 'Meta Ads campaigns', 'Facebook and Instagram campaigns planned, launched and scaled.'),
   ('pen', 'Creative testing', 'Several ad concepts and scripts tested at once, so the winners get the budget.'),
   ('sliders', 'Ongoing optimisation', 'Audiences, creatives and budgets adjusted as the data comes in.'),
   ('cal', 'Clear reporting', 'Reports in the terms you care about: enquiries, bookings and sales.'),
 ],
 'for': ['Brands selling online or through WhatsApp that want ads to pay for themselves', 'Service businesses that need a steady flow of enquiries', 'Teams already running ads who want an expert to take over or audit them'],
 'steps': [('Audit and plan', 'I look at what you’ve run before, your offer and your numbers, then write the plan.'),
           ('Launch and test', 'Campaigns go live with several creatives and audiences to learn fast.'),
           ('Optimise and report', 'Budget moves to what works, and you get a clear report on results.')],
 'proof': ['cs-unicorn-bakes', 'cs-fairmont'],
 'roas': True,
 'related': ['svc-meta-ads', 'svc-lead-generation', 'svc-consulting'],
 'faq': [
   ('What is performance marketing?', 'Advertising that is planned and judged by measurable results, such as sales, leads or messages, rather than reach or likes. Every campaign has tracking, a target and regular optimisation.'),
   ('Which platforms do you use?', 'Mainly Meta Ads (Facebook and Instagram), where most of my experience is. I also run Google Ads where search intent makes sense for the business.'),
   ('How do you measure success?', 'For e-commerce and retail, return on ad spend (ROAS) and sales. For lead generation, cost per qualified lead and how many leads turn into customers.'),
   ('What budget do I need?', 'It depends on your market, your offer and your goal. After a first conversation I recommend a starting budget and explain what it can realistically achieve.'),
   ('How soon will I see results?', 'Campaigns usually need a few weeks of testing before results settle. I share what’s working from the first week, and I never promise guaranteed results.'),
 ],
},
{
 'id': 'svc-meta-ads', 'slug': 'services/meta-ads', 'crumb': 'Meta Ads',
 'name': 'Meta Ads (Facebook & Instagram Ads)',
 'seo_title': 'Meta Ads Expert in Dubai: Facebook & Instagram Ads',
 'desc': 'Meta Ads management in Dubai and Kerala: Facebook and Instagram ads for sales, leads and WhatsApp enquiries, with creatives, targeting and honest reporting.',
 'pill': 'Service · Meta Ads',
 'h1': 'Meta Ads expert in Dubai <span class="ghost">for Facebook and Instagram.</span>',
 'lead': 'Meta Ads are where most of my results come from. I plan the campaigns, write the ad concepts and scripts, set up the targeting, and optimise every week for sales, leads or WhatsApp enquiries.',
 'incl_h': 'Meta Ads management, <span class="ghost">end to end.</span>',
 'incl_p': 'Facebook ads and Instagram ads run as one system from Meta Ads Manager.',
 'incl': [
   ('search', 'Account review', 'A look at past campaigns, tracking and creatives before anything new is launched.'),
   ('users', 'Audience targeting', 'Audiences built around who actually buys, by location, interest and behaviour.'),
   ('pen', 'Ad concepts and scripts', 'Creative concepts and video scripts written for Reels, Stories and Feed.'),
   ('megaphone', 'Campaign set-up', 'Sales, lead-form and click-to-WhatsApp campaigns structured for the goal.'),
   ('sliders', 'Weekly optimisation', 'Creatives, audiences and budgets adjusted based on results.'),
   ('chart', 'ROAS and lead reporting', 'Reports on return on ad spend, cost per lead and what to do next.'),
 ],
 'for': ['E-commerce and retail brands in the UAE and India', 'Real estate, consultancy and service businesses that need enquiries', 'Local Kerala businesses that want customers nearby'],
 'steps': [('Review', 'I review your account, offer and audience, and agree on one clear goal.'),
           ('Create and launch', 'I write the concepts and scripts and launch campaigns with several creatives.'),
           ('Scale what works', 'Winning ads and audiences get more budget, and the rest are cut.')],
 'proof': ['cs-unicorn-bakes', 'cs-fairmont', 'cs-zee-real-estate'],
 'roas': True,
 'related': ['svc-performance', 'svc-lead-generation', 'svc-content'],
 'faq': [
   ('Are Facebook ads and Instagram ads managed separately?', 'No. Both run from Meta Ads Manager, so I plan them together and let the results decide how much goes to each placement.'),
   ('Do you make the ad creatives?', 'I develop the creative concepts and write the video scripts. Filming and editing are done by your team, a videographer or editors I coordinate, depending on the project.'),
   ('What ROAS can I expect?', 'Across the brands I manage, Meta Ads average a 10–15X return on ad spend. That is an average, not a promise; your result depends on your product, offer, budget and market.'),
   ('Can you take over an existing ad account?', 'Yes. I start with a review of what has run so far, keep what works and fix tracking or structure problems before scaling.'),
   ('Do you run Meta Ads for real estate in Dubai?', 'Yes. I ran real estate marketing and property promotion campaigns as Head of Marketing at Zee Real Estate in Dubai.'),
 ],
},
{
 'id': 'svc-lead-generation', 'slug': 'services/lead-generation', 'crumb': 'Lead Generation',
 'name': 'Lead Generation',
 'seo_title': 'Lead Generation Specialist in Dubai | Abhishek Prakash',
 'desc': 'Lead generation for real estate, consultancy and service businesses in Dubai and Kerala: campaigns tuned for lead quality, not just a cheap cost per lead.',
 'pill': 'Service · Lead generation',
 'h1': 'Lead generation <span class="ghost">built for quality, not just volume.</span>',
 'lead': 'Cheap leads that never answer the phone cost more than they save. I build lead-generation campaigns for consultancies, real estate and service businesses that bring people who are ready to talk.',
 'incl_h': 'How I generate <span class="ghost">better leads.</span>',
 'incl_p': 'The ad is only half of it. The form, the follow-up and the feedback loop matter as much.',
 'incl': [
   ('funnel', 'Lead-generation strategy', 'The right offer, audience and channel for the kind of client you want.'),
   ('pen', 'Ad concepts and creatives', 'Messages that speak to serious buyers and filter out the rest.'),
   ('check', 'Qualifying questions', 'Lead forms and WhatsApp flows that ask the questions your sales team needs.'),
   ('building', 'Real estate campaigns', 'Property promotion and project launch campaigns for Dubai developers and agents.'),
   ('sliders', 'Lead quality optimisation', 'Campaigns adjusted using feedback on which leads turned into customers.'),
   ('chart', 'Cost per qualified lead', 'Reporting on qualified leads and conversions, not just form fills.'),
 ],
 'for': ['Immigration, business setup and other consultancies', 'Real estate developers, brokers and agents in Dubai', 'Clinics, institutes and service businesses in Kerala'],
 'steps': [('Define a good lead', 'We agree on what a qualified lead looks like for your sales team.'),
           ('Build the campaign', 'Ads, forms and WhatsApp flows are set up to attract and qualify.'),
           ('Close the loop', 'Your feedback on lead quality shapes every round of optimisation.')],
 'proof': ['cs-fairmont', 'cs-zee-real-estate'],
 'roas': False,
 'related': ['svc-meta-ads', 'svc-performance', 'svc-consulting'],
 'faq': [
   ('What makes a lead “qualified”?', 'A lead that matches the client you want, has a real need and budget, and answers when your team follows up. We define it together before launch.'),
   ('Lead forms or WhatsApp: which is better?', 'Both can work. Lead forms collect details at scale; click-to-WhatsApp starts a conversation straight away. I usually test both and keep what brings better customers.'),
   ('Which industries have you generated leads for?', 'Immigration and business setup consultancy at Fairmont Project Management Services, and real estate at Zee Real Estate, both in Dubai.'),
   ('How do you measure lead generation?', 'By cost per qualified lead and how many leads become customers. Raw cost per lead alone can be misleading.'),
   ('Do you handle the follow-up calls?', 'No. Your sales team owns the follow-up. I make sure leads reach them quickly with the details they need, and use their feedback to improve the campaigns.'),
 ],
},
{
 'id': 'svc-social-media', 'slug': 'services/social-media-marketing', 'crumb': 'Social Media Marketing',
 'name': 'Social Media Marketing',
 'seo_title': 'Social Media Marketing in Dubai & Kerala | Abhishek Prakash',
 'desc': 'Social media marketing from someone who grew a page to 3.2M+ followers: strategy, content calendars, Reels, influencer collaborations and organic growth.',
 'pill': 'Service · Social media marketing',
 'h1': 'Social media marketing <span class="ghost">from someone who built an audience of millions.</span>',
 'lead': 'I grew @TheWorldStories to 3.2M+ followers before I ever ran an ad. Today I use what that taught me to manage brands’ social media: strategy, content, community and influencer collaborations.',
 'incl_h': 'Social media management <span class="ghost">that builds a following.</span>',
 'incl_p': 'Organic content and influencer work that makes your paid ads work harder.',
 'incl': [
   ('share', 'Social media strategy', 'What to post, where and why, built around your audience and goals.'),
   ('cal', 'Content calendars', 'Monthly calendars so your page stays active and consistent.'),
   ('video', 'Reels and short-form video', 'Concepts and scripts made for the way people scroll today.'),
   ('users', 'Influencer collaborations', 'Finding, onboarding and working with creators who fit your brand.'),
   ('star', 'Brand positioning', 'A clear, recognisable voice across Instagram and Facebook.'),
   ('chart', 'Engagement and growth tracking', 'Monthly look at what grew your audience and what to change.'),
 ],
 'for': ['Local brands in Kerala that want a stronger Instagram presence', 'Dubai businesses that need a consistent, professional page', 'Brands planning influencer collaborations'],
 'steps': [('Strategy', 'We agree on your audience, voice and the content pillars to post around.'),
           ('Create', 'I plan the calendar, write the scripts and coordinate shoots or creators.'),
           ('Grow', 'We track what works and do more of it each month.')],
 'proof': ['cs-theworldstories', 'cs-unicorn-bakes'],
 'roas': False,
 'related': ['svc-content', 'svc-meta-ads', 'svc-consulting'],
 'faq': [
   ('What did growing a 3.2M-follower page teach you?', 'How algorithms reward consistency, what makes people stop and share, and why audience comes before selling. The Internet Archive recorded @TheWorldStories at 3.21M followers in July 2017.'),
   ('Do you handle influencer marketing?', 'Yes. I identify suitable creators, handle onboarding and manage the collaboration, as I did for Unicorn Bakes in Payyanur.'),
   ('Which platforms do you manage?', 'Mainly Instagram and Facebook, where my clients’ customers are most active.'),
   ('Do you also run paid ads on social media?', 'Yes. Organic content and Meta Ads work best together, and I manage both.'),
 ],
},
{
 'id': 'svc-content', 'slug': 'services/content-strategy', 'crumb': 'Content Strategy',
 'name': 'Content Strategy & Video Scripts',
 'seo_title': 'Content Strategy & Video Scripts in Dubai | Abhishek Prakash',
 'desc': 'Content strategy, video scripts, content calendars and production oversight for brands in Dubai and Kerala, from the first idea to the final edit.',
 'pill': 'Service · Content strategy',
 'h1': 'Content strategy and video scripts <span class="ghost">from concept to final cut.</span>',
 'lead': 'Good ads and good pages start with good content. I build content strategies for different industries, write the video scripts, plan the calendars and manage editors so production stays on track.',
 'incl_h': 'Content, <span class="ghost">planned and produced.</span>',
 'incl_p': 'One person responsible for the idea, the script and the finished piece.',
 'incl': [
   ('cal', 'Content strategy', 'Content pillars and formats chosen for your industry and audience.'),
   ('pen', 'Video scripts', 'Scripts for Reels, ads and brand videos, written to hold attention.'),
   ('star', 'Creative concepts', 'Campaign ideas that give every piece of content a reason to exist.'),
   ('video', 'Shoot coordination', 'Shot lists, schedules and on-the-day direction.'),
   ('team', 'Editor management', 'Briefing and coordinating video editors through to the final cut.'),
   ('grid', 'Content calendars', 'Monthly plans that keep every channel consistent.'),
 ],
 'for': ['Brands with a production team that needs direction', 'Real estate and property marketing teams', 'Businesses starting short-form video for the first time'],
 'steps': [('Plan', 'Strategy, pillars and a calendar agreed for the month.'),
           ('Script and shoot', 'Scripts written, shoots coordinated, editors briefed.'),
           ('Publish and learn', 'Content goes live, and results shape the next month’s plan.')],
 'proof': ['cs-zee-real-estate', 'cs-theworldstories'],
 'roas': False,
 'related': ['svc-social-media', 'svc-meta-ads', 'svc-performance'],
 'faq': [
   ('Do you film and edit the videos yourself?', 'I write the scripts, plan the shoots and manage the editors. At Zee Real Estate this was done with the Modus D3 creative team; for other clients it can be your team or freelancers I coordinate.'),
   ('Can you write scripts for ads as well as organic content?', 'Yes. Ad scripts are written for the first few seconds and a clear call to action; organic scripts focus on value and shareability.'),
   ('Which industries have you created content for?', 'Real estate, consultancy, cakes and pastries, beauty and salons, and travel, across the UAE and India.'),
   ('How far ahead do you plan content?', 'Usually a month at a time, with room for timely posts and campaign launches.'),
 ],
},
{
 'id': 'svc-consulting', 'slug': 'services/digital-marketing-consulting', 'crumb': 'Consulting',
 'name': 'Digital Marketing Consulting',
 'seo_title': 'Digital Marketing Consultant in Dubai | Abhishek Prakash',
 'desc': 'Digital marketing consulting in Dubai and Kerala: ad account and social media audits, growth strategy and guidance for in-house teams, from a hands-on marketer.',
 'pill': 'Service · Consulting',
 'h1': 'Digital marketing consultant <span class="ghost">for brands that want a clear plan.</span>',
 'lead': 'Not every business needs a full-time marketer. Sometimes you need someone experienced to look at what you’re doing, tell you honestly what is and isn’t working, and give your team a plan.',
 'incl_h': 'Consulting <span class="ghost">that ends in a plan you can use.</span>',
 'incl_p': 'Practical advice from someone who still runs campaigns every week.',
 'incl': [
   ('search', 'Ad account audit', 'A review of your Meta Ads set-up, tracking, creatives and spend.'),
   ('share', 'Social media audit', 'What your pages say about you and how to improve them.'),
   ('target', 'Growth strategy', 'Which channels to focus on, in what order and with what budget.'),
   ('team', 'Team guidance', 'Direction for in-house marketers, creative teams and video editors.'),
   ('funnel', 'Funnel review', 'From ad to enquiry to sale: where people drop off and why.'),
   ('cal', 'Action plan', 'A written plan with priorities your team can act on.'),
 ],
 'for': ['Founders who want a second opinion before spending more on ads', 'In-house teams that need senior direction', 'Businesses choosing between doing it themselves and hiring help'],
 'steps': [('Listen', 'We talk through your business, goals, numbers and current marketing.'),
           ('Review', 'I review your accounts, pages and funnel.'),
           ('Recommend', 'You get clear recommendations and a prioritised plan.')],
 'proof': ['cs-zee-real-estate', 'cs-fairmont'],
 'roas': False,
 'related': ['svc-performance', 'svc-meta-ads', 'svc-lead-generation'],
 'faq': [
   ('What’s the difference between consulting and management?', 'With consulting, I review and advise and your team does the work. With management, I run the campaigns and content myself.'),
   ('Can you work with my existing agency or team?', 'Yes. I can review their work, set priorities and guide them, as I did coordinating creative teams and editors at Zee Real Estate and Modus D3.'),
   ('Is consulting available for businesses in Kerala?', 'Yes. I work with businesses in Dubai and anywhere in Kerala, over calls, video meetings and WhatsApp.'),
   ('What do I need to share before we start?', 'Access to your ad account and pages if possible, your goals, and any numbers you track today, such as enquiries and sales.'),
 ],
},
]

# ---------------------------------------------------------------- case studies
CASE_STUDIES = [
{
 'id': 'cs-theworldstories', 'slug': 'case-studies/theworldstories', 'crumb': '@TheWorldStories',
 'name': '@TheWorldStories', 'years': '2011 – 2018', 'where': 'Twitter · worldwide audience', 'role': 'Creator and sole manager',
 'channels': 'Twitter, organic content', 'logo': None,
 'seo_title': 'Case Study: Growing @TheWorldStories to 3.2M Followers',
 'desc': 'How Abhishek Prakash built @TheWorldStories, a travel page on Twitter, from scratch to 3.21M followers, with the archived proof and the lessons for brands.',
 'excerpt': 'A travel page on Twitter, started from scratch in 2011 and grown to 3.21M followers by 2017.',
 'h1': '@TheWorldStories: <span class="ghost">from zero to 3.2M followers on Twitter.</span>',
 'lead': 'Before I worked in marketing, I built a travel page on Twitter from scratch. It grew to over 3.2 million followers and taught me how audiences really grow.',
 'body': '''
<h2>The context</h2>
<p>In 2011 I created @TheWorldStories, a travel page on Twitter built around beautiful destinations and photography. There was no brand, budget or team behind it. It was a personal project.</p>
<h2>My role</h2>
<p>I created the page and managed it myself: choosing the content, posting, and learning what made people follow and share. This is my own work, not a team result.</p>
<h2>What I did</h2>
<ul>
<li>Built the page from scratch around one clear theme: travel destinations and photography</li>
<li>Posted consistently and learned how the platform’s algorithm rewarded engagement</li>
<li>Studied which posts people stopped for, shared and followed the page because of</li>
<li>Grew the audience organically, without paid advertising</li>
</ul>
<h2>The result</h2>
<p>The page grew to over <strong>3.2 million followers</strong>. The Internet Archive captured the profile, displayed as “Travel Scenes”, on 26 July 2017 with <strong>3.21M followers, 60.3K tweets and 13.7K following</strong>. You can <a href="https://web.archive.org/web/20170726141138/twitter.com/theworldstories" target="_blank" rel="noopener">view the archived profile on the Wayback Machine</a>.</p>
<p>In 2016 it was the most-followed travel page in its category. The account was suspended in Twitter’s 2018 purge, so the archive is the record that remains.</p>
<h2>What it taught me, and what it means for brands</h2>
<ul>
<li><strong>Audience before selling.</strong> People follow a page for what it gives them. Brands that lead with value earn the right to sell.</li>
<li><strong>Consistency compounds.</strong> Growth came from showing up every day with the same clear theme.</li>
<li><strong>Know what resonates.</strong> Watching what people share is the fastest way to learn what they want.</li>
</ul>
<p>These lessons shape how I plan <a href="@svc-social-media">social media marketing</a> and <a href="@svc-content">content strategy</a> for brands today.</p>
''',
},
{
 'id': 'cs-unicorn-bakes', 'slug': 'case-studies/unicorn-bakes', 'crumb': 'Unicorn Bakes',
 'name': 'Unicorn Bakes', 'years': '2020 – 2024', 'where': 'Payyanur, Kannur, Kerala', 'role': 'Digital marketing and social media lead',
 'channels': 'Meta Ads, Instagram, Facebook, influencers', 'logo': 'unicorn-bakes',
 'seo_title': 'Case Study: Unicorn Bakes, Payyanur | Abhishek Prakash',
 'desc': 'How Abhishek Prakash ran Meta Ads, social media and influencer marketing for Unicorn Bakes, a customised cake shop in Payyanur, Kerala, from 2020 to 2024.',
 'excerpt': 'Meta Ads, content and influencer marketing for a customised cake and pastry shop in Payyanur.',
 'h1': 'Unicorn Bakes: <span class="ghost">growing a Payyanur cake shop online.</span>',
 'lead': 'From 2020 to 2024 I handled the complete digital marketing and social media growth for Unicorn Bakes, a customised cake and pastry business in Payyanur, Kannur.',
 'body': '''
<h2>The context</h2>
<p>Unicorn Bakes is a customised cake and pastry business in Payyanur, in Kannur district. Customised cakes are a visual, local and occasion-driven product, so most customers discover a shop on Instagram and order over a message or a call.</p>
<h2>My role</h2>
<p>I was responsible for the brand’s complete digital marketing: Meta advertising, social media content strategy and influencer marketing. The baking, the product and the customer service were the business owners’ work.</p>
<h2>What I did</h2>
<ul>
<li>Planned and executed Meta advertising campaigns on Facebook and Instagram</li>
<li>Managed the complete social media content strategy</li>
<li>Developed creative concepts and advertising campaigns</li>
<li>Planned content calendars and coordinated shoots</li>
<li>Identified, onboarded and collaborated with influencers</li>
<li>Managed the brand’s overall online presence</li>
<li>Drove customer acquisition and sales through paid advertising</li>
</ul>
<h2>The outcome</h2>
<p>Over four years the marketing helped establish Unicorn Bakes as one of the leading customised cake shops in its town, and contributed significantly to business growth and increased sales.</p>
<p><strong>A note on numbers:</strong> sales figures belong to the business and are not published here, so the outcome is described in words rather than with a statistic.</p>
<h2>What other local businesses can take from it</h2>
<ul>
<li>For local, visual products, Instagram content and Meta Ads work best together.</li>
<li>Local influencers put a small brand in front of the right people quickly.</li>
<li>A steady content calendar keeps the brand in mind between occasions.</li>
</ul>
<p>Running a business in Kannur or elsewhere in Kerala? See <a href="@kannur">digital marketing in Kannur</a> or <a href="@kerala">my work across Kerala</a>.</p>
''',
},
{
 'id': 'cs-fairmont', 'slug': 'case-studies/fairmont', 'crumb': 'Fairmont',
 'name': 'Fairmont Project Management Services', 'years': '2025 – 2026', 'where': 'Dubai, UAE', 'role': 'Digital marketing, lead generation and performance advertising',
 'channels': 'Meta Ads, lead generation', 'logo': None,
 'seo_title': 'Case Study: Lead Generation for a Dubai Consultancy',
 'desc': 'How Abhishek Prakash ran Meta Ads lead generation for Fairmont Project Management Services, an immigration and business setup consultancy in Dubai.',
 'excerpt': 'Meta Ads lead generation for an immigration and business setup consultancy in Dubai.',
 'h1': 'Fairmont: <span class="ghost">lead generation for a Dubai consultancy.</span>',
 'lead': 'From 2025 to 2026 I ran digital marketing, lead generation and performance advertising for Fairmont Project Management Services, an immigration and business setup consultancy in Dubai.',
 'body': '''
<h2>The context</h2>
<p>Fairmont Project Management Services is a Dubai consultancy for immigration and business setup. In this kind of business, what matters is reaching people with a real plan and getting them to talk to the team.</p>
<h2>My role</h2>
<p>I planned and ran the Meta Ads campaigns and the lead-generation strategy, and created the advertising concepts. Handling enquiries, consultations and closing clients was the consultancy team’s work.</p>
<h2>What I did</h2>
<ul>
<li>Planned and executed Meta Ads campaigns</li>
<li>Developed lead-generation strategies for immigration and business setup services</li>
<li>Created advertising concepts and marketing creatives</li>
<li>Optimised campaigns to improve lead quality and conversions</li>
<li>Analysed campaign performance and improved return on ad spend</li>
</ul>
<h2>The outcome</h2>
<p>Lead quality, conversions and return on ad spend improved for the consultancy’s immigration and business setup services.</p>
<p><strong>A note on numbers:</strong> the consultancy’s lead and revenue figures belong to the business, so no specific statistic is published for this project.</p>
<h2>Lessons for service businesses</h2>
<ul>
<li>Define a qualified lead with the sales team before launch.</li>
<li>Use the ad and the form to filter, not just to attract.</li>
<li>Judge campaigns on cost per qualified lead, not raw cost per lead.</li>
</ul>
<p>More on how I approach this: <a href="@svc-lead-generation">lead generation</a>.</p>
''',
},
{
 'id': 'cs-zee-real-estate', 'slug': 'case-studies/zee-real-estate', 'crumb': 'Zee Real Estate & Modus D3',
 'name': 'Zee Real Estate & Modus D3', 'years': 'Aug – Oct 2026', 'where': 'Dubai, UAE', 'role': 'Head of Marketing',
 'channels': 'Content, video, Meta Ads, real estate campaigns', 'logo': 'zee-real-estate',
 'seo_title': 'Case Study: Zee Real Estate & Modus D3, Dubai',
 'desc': 'Abhishek Prakash’s work as Head of Marketing at Zee Real Estate and its in-house design agency Modus D3 in Dubai: content, video and real estate campaigns.',
 'excerpt': 'Head of Marketing for a Dubai real estate company and its in-house design agency.',
 'h1': 'Zee Real Estate &amp; Modus D3: <span class="ghost">leading marketing for multiple brands.</span>',
 'lead': 'From August to October 2026 I was Head of Marketing at Zee Real Estate in Dubai and its in-house design agency, Modus D3, managing marketing and content across several businesses.',
 'body': '''
<h2>The context</h2>
<p>Zee Real Estate is a Dubai real estate company. Modus D3 (Modus D3 Advertising Agency L.L.C) is its in-house design agency for advertising, branding, videography and digital publication. Together they needed marketing that could run across several brands at once.</p>
<h2>My role</h2>
<p>As Head of Marketing I set the content and marketing direction and led the creative work. Production was a <strong>team effort</strong>: the Modus D3 team and video editors produced the work, and I planned, scripted, coordinated and oversaw it.</p>
<h2>What I did</h2>
<ul>
<li>Managed digital marketing for multiple businesses</li>
<li>Developed content strategies for different industries</li>
<li>Wrote video scripts and developed creative concepts</li>
<li>Planned social media content calendars</li>
<li>Managed and coordinated video editors and oversaw content production</li>
<li>Built strategies for brand awareness, engagement and lead generation</li>
<li>Ran real estate marketing and property promotion campaigns</li>
</ul>
<h2>The outcome</h2>
<p>The role was about running marketing at scale: several brands, one creative team and a steady flow of content and campaigns. It built my experience in managing multiple brands at once, leading creative teams and executing strategy across different industries.</p>
<p><strong>A note on numbers:</strong> this was a short, team-based role, and no campaign figures are published here. Results belong to the companies and the team as a whole.</p>
<h2>What it means for your brand</h2>
<ul>
<li>I can direct a creative team as well as run campaigns myself.</li>
<li>I understand Dubai real estate marketing and property launches.</li>
<li>I can keep content consistent across several brands or projects.</li>
</ul>
<p>See how this feeds into my <a href="@svc-content">content strategy</a> and <a href="@svc-lead-generation">lead generation</a> work.</p>
''',
},
]
