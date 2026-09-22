# The nine guides the Learn index has been advertising.
#
# Every one was a card linking to "#". The index is open to search, so it was a
# page inviting Google to index nine promises the site could not keep.
#
# House rules, because this is health-adjacent copy on a site that sells
# consumables and nothing else:
#
#   - Consumables only. Never imply we supply a medicine, a peptide or a
#     hormone, in any form.
#   - Technique is described in terms of the equipment: gauge, length, angle.
#     Never a dose, never a site for a named drug, never a frequency.
#   - The directions that came with the medicine, and the prescriber, come
#     first and are said to come first.
#   - No therapeutic outcome claims.
#   - Australian spelling, Australian rules, no em dashes.
#
# Each guide: slug, title (the h1), meta (the reading time shown on the index),
# blurb (the card body), desc (the search snippet), answer (the one line that
# answers the question the title asks, shown first and quoted by assistants),
# body (sections), faq, related.

A_NOTE = ('General information about the equipment, not medical advice. The '
          'directions that came with your medicine and the person who '
          'prescribed it come first, every time.')

GUIDES = [

{
 'slug': 'needle-numbers-explained',
 'title': 'What the numbers on a needle mean',
 'meta': 'Guide · 6 min',
 'blurb': 'Gauge, length, units on the barrel, and why the scale runs backwards.',
 'desc': ('Gauge, length and the unit scale on a syringe barrel, explained. Why '
          '31G is finer than 27G, what the millimetres measure, and which number '
          'matters for what.'),
 'answer': ('Gauge is the thickness of the needle and the scale runs backwards, so '
            'a higher number is a finer needle. The millimetres are the length. The '
            'units on the barrel measure the liquid, not the needle.'),
 'body': [
  ('Gauge is thickness, and bigger means finer', [
   'Gauge, written as a number followed by G, describes how thick the needle is. '
   'It runs backwards from what most people expect: 31G is finer than 29G, which '
   'is finer than 27G, which is finer than 23G. The number is roughly how many '
   'needles of that size would fit across a fixed width, so more of them means '
   'each one is thinner.',
   'The practical trade is comfort against speed. A finer needle is noticeably '
   'more comfortable going in and takes longer to draw through, because you are '
   'pulling the same volume of liquid through a smaller hole. A thicker needle '
   'fills faster and is easier to feel. Nothing else changes.',
   'Hubs are colour coded to ISO 6009, which is why a box of 23G needles has the '
   'same blue hub whoever made them. The colour is a convenience for reading a '
   'tray at a glance, not a rating.',
  ]),
  ('Length is measured in millimetres or inches', [
   'The second number is how long the needle is, given in millimetres for short '
   'needles and sometimes in inches for longer ones. A 4mm pen needle and a '
   '38mm intramuscular needle are doing completely different jobs.',
   'Length decides which layer of tissue the tip reaches. That is a question for '
   'whoever prescribed the medicine, because it depends on the medicine and on '
   'you, not on a rule of thumb from a website.',
  ]),
  ('The units on the barrel measure liquid, not the needle', [
   'A U-100 insulin syringe is graduated in units rather than millilitres. U-100 '
   'means the scale assumes a concentration of one hundred units per millilitre, '
   'so one hundred units fills exactly 1mL and a single unit mark is one '
   'hundredth of a millilitre.',
   'This is why insulin syringes exist as a separate thing. At that volume a '
   'millilitre scale is unreadable and a unit scale is not. It also means a '
   'U-100 syringe and a U-40 syringe are not interchangeable: the same mark '
   'means a different amount of liquid. U-40 is mostly a veterinary '
   'concentration in Australia. Read the vial before you choose the syringe.',
   'Luer-lock syringes are graduated in millilitres instead, because they are '
   'used for larger volumes where a unit scale would be meaningless.',
  ]),
 ],
 'faq': [
  ('Is a higher gauge number a bigger needle?',
   'No, the opposite. A higher number is a finer needle. 31G is finer than 27G.'),
  ('Does a finer needle hurt less?',
   'Generally yes, and it is the main reason to choose one. It also draws more '
   'slowly, which is the trade you are making.'),
  ('What does the G stand for?',
   'Gauge. It comes from wire gauge, where the number counts how many wires fit '
   'across a fixed width, which is why the scale runs backwards.'),
  ('Can I use a U-100 syringe for a U-40 product?',
   'No. The graduations assume a different concentration, so the same mark means '
   'a different amount of liquid. Match the syringe to what the vial says.'),
 ],
 'related': ['gauge-comparison', 'reading-a-syringe', 'subcutaneous-technique'],
},

{
 'slug': 'gauge-comparison',
 'title': '29G, 30G or 31G: which should I buy?',
 'meta': 'Guide · 5 min',
 'blurb': 'The trade between comfort and how long you spend drawing up.',
 'desc': ('The practical difference between 29G, 30G and 31G needles: comfort, '
          'how long drawing up takes, and when the thicker one is the better '
          'choice anyway.'),
 'answer': ('All three work. 31G is the most comfortable and the slowest to draw '
            'through, 29G is the quickest to fill and the easiest to feel, and 30G '
            'sits between them. If the liquid is thick or oily, go thicker.'),
 'body': [
  ('What actually changes between them', [
   'Very little, and that is worth saying plainly. All three are fine needles in '
   'the same family, and the difference between them is a fraction of a '
   'millimetre of outer diameter. Nobody is going to get a different result from '
   'their medicine because they chose 30G over 31G.',
   'What does change is comfort and draw time. A 31G needle is the most '
   'comfortable of the three and the slowest to pull liquid through. A 29G fills '
   'noticeably faster and you will feel it more. Whether that trade is worth it '
   'depends on how much you are drawing and how often.',
  ]),
  ('When to go thicker on purpose', [
   'Viscosity is the main reason. A thin watery solution moves through a 31G '
   'without complaint. An oil moves very slowly, sometimes slowly enough that '
   'you give up and squeeze, which is how a plunger gets forced and a dose gets '
   'lost.',
   'The usual answer for anything viscous is to draw up with a wider needle and '
   'swap to a finer one to inject. A drawing-up needle is blunt and wide, which '
   'fills a barrel in seconds rather than a minute, and it cannot be injected '
   'with by accident. It is a second needle per dose and it is worth it.',
   'The other reason is dexterity. Very fine needles bend if they meet '
   'resistance and are fiddly to handle. If you find that frustrating, a 29G is '
   'not a worse choice, it is a different one.',
  ]),
  ('Length matters more than gauge', [
   'If you are trying to decide between these three, you are optimising the '
   'thing that matters least. Length decides which layer of tissue the tip '
   'reaches, and that is a genuine clinical question rather than a comfort '
   'preference.',
   'Australian and international guidance has moved towards shorter needles for '
   'injections under the skin over the last decade, which is why 4mm pen needles '
   'are now standard. Which length suits you is a question for your prescriber.',
  ]),
 ],
 'faq': [
  ('Is 31G always the best choice?',
   'No. It is the most comfortable and the slowest to draw through. If you are '
   'pulling anything viscous, a wider needle to draw up will save you more '
   'frustration than the finer needle saves you discomfort.'),
  ('Will a finer needle change how the medicine works?',
   'No. The needle delivers the liquid; it does not change it.'),
  ('Can I reuse a needle to save money?',
   'No. They are single use. A used needle is blunter, which hurts more, and '
   'reusing one is how an infection starts. Buying in bulk is the way to make '
   'this cheap.'),
 ],
 'related': ['needle-numbers-explained', 'subcutaneous-technique', 'sharps-disposal-australia'],
},

{
 'slug': 'reading-a-syringe',
 'title': 'Reading a syringe',
 'meta': 'Guide · 4 min',
 'blurb': 'Units, millilitres, and making sure the two are not confused.',
 'desc': ('How to read the scale on an insulin syringe and a luer-lock syringe, '
          'what U-100 means, and why units and millilitres are not '
          'interchangeable.'),
 'answer': ('Insulin syringes are marked in units and luer-lock syringes in '
            'millilitres. On a U-100 syringe, 100 units is 1mL, so one unit mark is '
            '0.01mL. Read the vial first and match the syringe to it.'),
 'body': [
  ('Find out which scale you are holding', [
   'Look at the barrel. If the numbers run 10, 20, 30 up to 50 or 100 and the '
   'word units appears, it is an insulin syringe. If they run 0.2, 0.4, 0.6 and '
   'so on, or 1, 2, 3, it is graduated in millilitres.',
   'The two are not interchangeable and there is no conversion you can do in '
   'your head reliably, because it depends on the concentration of what is in '
   'the vial. Match the syringe to what the label says.',
  ]),
  ('What U-100 means', [
   'U-100 describes the concentration the scale assumes: one hundred units per '
   'millilitre. On a 1mL U-100 syringe, the 100 mark and the 1mL mark are the '
   'same place on the barrel, and a single unit is one hundredth of a '
   'millilitre.',
   'U-40 syringes exist for products at forty units per millilitre, which in '
   'Australia is mostly veterinary. Using one scale for the other concentration '
   'gives you the wrong amount of liquid. This is the single most important '
   'thing on this page.',
  ]),
  ('Reading the line, not the tip', [
   'The measurement is taken at the flat top of the rubber stopper inside the '
   'barrel, not at the pointed tip of it. On a small dose that difference is a '
   'meaningful share of what you drew.',
   'Hold the syringe at eye level rather than looking down at it. Reading a '
   'scale from an angle shifts where the line appears to sit, which matters more '
   'the smaller the dose is.',
   'Half unit syringes exist if you need finer resolution than a whole unit. '
   'Whether you need one is a question for your prescriber, not a preference.',
  ]),
 ],
 'faq': [
  ('How many units are in a millilitre?',
   'On a U-100 scale, one hundred. On a U-40 scale, forty. The scale has to '
   'match the concentration of what is in the vial.'),
  ('Why do insulin syringes have a fixed needle?',
   'It removes the dead space where a luer fitting would be. On a small dose '
   'that space holds a meaningful share of what you drew up.'),
  ('Where exactly do I read the measurement?',
   'At the flat top of the rubber stopper, at eye level.'),
 ],
 'related': ['needle-numbers-explained', 'reconstitution-basics', 'gauge-comparison'],
},

{
 'slug': 'first-injection',
 'title': 'Your first injection, step by step',
 'meta': 'Guide · 8 min',
 'blurb': 'Before, drawing up, injecting, and what to do afterwards.',
 'desc': ('What to have ready before a first self-injection and how the '
          'equipment works. General information about the consumables, not '
          'instruction for any medicine.'),
 'answer': ('Have your medicine, the right syringe or pen needle, alcohol swabs '
            'and a sharps container on a clean surface before you start. The '
            'technique itself, including where and how much, comes from whoever '
            'prescribed it.'),
 'body': [
  ('What this page is and is not', [
   'This describes the equipment and the order things happen in. It does not '
   'tell you where to inject, how much, or how often, because those depend '
   'entirely on the medicine and on you, and they come from the person who '
   'prescribed it and from the leaflet in the box.',
   'If you have been handed a script and nobody walked you through the '
   'practical side, that is worth a phone call to the prescribing clinic or a '
   'pharmacist. Most will talk you through it, and many will do it in person '
   'the first time. It is a normal thing to ask for.',
  ]),
  ('Before you start', [
   'Clear a surface and wash your hands properly. Lay out what you need so you '
   'are not hunting for something mid way: the medicine, the syringe or pen '
   'needle, an alcohol swab, something clean to hold over the site afterwards, '
   'and the sharps container open and within reach.',
   'Check the medicine. Look at the expiry, look at the liquid, and read the '
   'label to confirm it is what you think it is and at the concentration you '
   'think it is. If it looks cloudy when it should be clear, or has anything '
   'floating in it, do not use it.',
   'Let it come to room temperature if it has been refrigerated and the '
   'directions say to. Cold liquid stings more going in. How long that takes is '
   'on the leaflet.',
  ]),
  ('Drawing up, if you are using a syringe', [
   'Swab the rubber stopper on the vial and let it dry. The alcohol does its '
   'work as it evaporates, so wiping it off straight away defeats the purpose.',
   'Draw air into the syringe to match the volume you are taking out, push it '
   'into the vial, then invert and draw. The air replaces the liquid you remove '
   'and stops a vacuum forming, which is what makes a vial fight you.',
   'Tap the barrel to bring bubbles to the top and push them back into the '
   'vial. A small bubble in a subcutaneous injection is not the emergency the '
   'internet suggests, but it does mean you have less liquid than the scale '
   'says, which is the real reason to clear it.',
   'If the liquid is thick, draw up with a wider blunt needle and swap to a '
   'finer one to inject. Never inject with a drawing-up needle.',
  ]),
  ('Afterwards', [
   'The needle goes straight into the sharps container, immediately, without '
   'recapping it. Recapping is when most needlestick injuries happen. This is '
   'the one part of the process where the advice is the same for everyone.',
   'A spot of blood is common and not a problem. Hold something clean over it '
   'rather than rubbing. If a site is hot, swollen, increasingly painful over '
   'the following days, or you feel unwell, that is a call to your prescriber '
   'rather than a thing to wait out.',
   'Write down what you did and when, at least for the first few. It is much '
   'easier to have a useful conversation with your prescriber when you can '
   'answer questions about what actually happened.',
  ]),
 ],
 'faq': [
  ('Do I need to swab my skin first?',
   'Advice varies and depends on the setting and the medicine. Follow what your '
   'prescriber told you. If you do swab, let it dry before the needle goes in.'),
  ('What if I see a small air bubble?',
   'For an injection under the skin it is not dangerous, but it means you have '
   'less liquid than the scale shows. Tap it to the top and push it back into '
   'the vial before you measure.'),
  ('Is it normal to bleed a little?',
   'Yes. Hold something clean over the spot rather than rubbing it.'),
  ('Can I put the cap back on the needle before binning it?',
   'No. Recapping is when most needlestick injuries happen. Straight into the '
   'sharps container.'),
 ],
 'related': ['subcutaneous-technique', 'sharps-disposal-australia', 'reading-a-syringe'],
},

{
 'slug': 'subcutaneous-technique',
 'title': 'Injecting under the skin',
 'meta': 'Guide · 6 min',
 'blurb': 'Angle, pinching the skin, and why short needles changed the advice.',
 'desc': ('What subcutaneous means, why guidance moved to shorter needles, and '
          'what the angle and the skin pinch are for. Equipment information, not '
          'advice.'),
 'answer': ('Subcutaneous means into the fat layer under the skin rather than into '
            'muscle. Modern short needles usually go straight in at ninety degrees '
            'without a pinch, which is why guidance changed. Your prescriber sets '
            'the site and the length.'),
 'body': [
  ('What the layer is', [
   'Under the skin and above the muscle there is a layer of fat. A subcutaneous '
   'injection puts the medicine there, where it is absorbed more slowly and more '
   'steadily than it would be from muscle.',
   'How thick that layer is varies enormously between people and between sites '
   'on the same person. That is the whole reason needle length is a clinical '
   'decision rather than a preference.',
  ]),
  ('Why the advice about angles changed', [
   'The old instruction to pinch a fold of skin and go in at forty five degrees '
   'came from an era of longer needles. With a 12mm or 13mm needle, going '
   'straight in risked reaching muscle on a lean person, so you lifted the fat '
   'away from the muscle first and came in shallow.',
   'Short needles removed the problem. A 4mm pen needle is shorter than the '
   'distance to muscle at the usual sites on almost everyone, so it goes '
   'straight in at ninety degrees and the pinch becomes unnecessary. This is why '
   'diabetes guidance in Australia and internationally moved to the shortest '
   'available needle.',
   'If you are using a longer needle, the older technique may still apply. '
   'Which applies to you depends on the needle you have and on your build, and '
   'it is a question for your prescriber rather than a rule you can take off a '
   'page.',
  ]),
  ('Rotating sites', [
   'Injecting into the same spot repeatedly changes the tissue there. It can '
   'become lumpy or hardened, and tissue in that state absorbs unpredictably, '
   'which makes the medicine itself less consistent.',
   'The fix is to move. Work systematically rather than randomly, so you can '
   'actually remember where you have been, and give each area time before you '
   'come back to it. Which areas are available to you is part of what your '
   'prescriber should have set out.',
   'Feel the area before you inject. If it is lumpy, hard, bruised or sore, use '
   'somewhere else and mention it at your next appointment.',
  ]),
 ],
 'faq': [
  ('Do I still need to pinch the skin?',
   'With a short needle, usually not. With a longer one it may still apply. It '
   'depends on the needle and on you, so follow what your prescriber told you.'),
  ('What angle should I use?',
   'Short needles generally go straight in at ninety degrees. Longer needles may '
   'call for a shallower angle. The needle you have determines the answer.'),
  ('Why does the same dose feel different in different spots?',
   'Because the fat layer is not the same thickness everywhere, and tissue that '
   'has been injected repeatedly absorbs differently. That is what rotating is '
   'for.'),
 ],
 'related': ['intramuscular-technique', 'gauge-comparison', 'first-injection'],
},

{
 'slug': 'intramuscular-technique',
 'title': 'Injecting into muscle',
 'meta': 'Guide · 7 min',
 'blurb': 'Drawing up with one needle and injecting with another.',
 'desc': ('Why intramuscular injections use two needles, what the gauges and '
          'lengths are for, and why the drawing-up needle never goes into '
          'anyone.'),
 'answer': ('An intramuscular injection goes through the fat into the muscle, so it '
            'needs a longer needle than a subcutaneous one. Draw up with a wide '
            'blunt needle and swap to a sharp one to inject. The site, the length '
            'and the dose come from your prescriber.'),
 'body': [
  ('Why there are two needles', [
   'Intramuscular injections are usually oils or thicker solutions, and they go '
   'into a vial with a rubber stopper. Both of those argue for a different '
   'needle at each stage.',
   'Drawing up through a fine needle is slow, and doing it repeatedly through a '
   'rubber stopper blunts the tip and cores small pieces of rubber into the '
   'vial. A drawing-up needle is wide and usually blunt, so it fills the barrel '
   'quickly and cannot be injected with by accident. Some are sharp fill '
   'needles for going through a stopper, which is a different thing again.',
   'You then swap to a sharp needle of the right gauge and length to inject. '
   'One vial, two needles, both into the sharps container afterwards.',
  ]),
  ('What the length is doing', [
   'A subcutaneous needle is short on purpose so it stops in the fat. An '
   'intramuscular needle has to pass through that fat and reach the muscle '
   'underneath, so it is longer. Common lengths run from about 25mm to 38mm.',
   'How much fat the needle has to cross varies between people and between '
   'sites, which is exactly why the length is chosen for you rather than picked '
   'off a shelf. Too short and the medicine lands in fat, where an oil in '
   'particular absorbs badly and can sit as a painful lump. Too long is its own '
   'problem.',
   'This is not a judgement you should make from a website, and we are not '
   'going to pretend otherwise. Your prescriber picks it.',
  ]),
  ('Practical notes on the equipment', [
   'Luer-lock rather than luer-slip for anything viscous. A slip tip is a push '
   'fit, and pushing a thick oil generates enough pressure to separate the '
   'needle from the barrel. A lock screws on and cannot.',
   'Warming an oil in your hands for a minute makes it noticeably easier to '
   'push. Do not heat it any other way.',
   'Draw slowly. Pulling hard on a small syringe against a thick liquid is how '
   'you get a barrel full of bubbles that then take longer to clear than the '
   'slow draw would have taken.',
  ]),
 ],
 'faq': [
  ('Can I inject with the drawing-up needle?',
   'No. Blunt fill needles are not sharp enough and the wide bore is '
   'unnecessarily traumatic. They also go blunter still after a stopper.'),
  ('Why luer-lock and not luer-slip?',
   'A slip tip can separate under pressure, and a thick oil generates plenty of '
   'it. A lock screws on.'),
  ('How do I know what length I need?',
   'From your prescriber. It depends on the site and on your build, and it is '
   'not something to estimate.'),
  ('Why is my oil so slow to draw?',
   'Viscosity and a narrow needle. Draw up with a wider blunt needle, and warm '
   'the vial in your hands for a minute first.'),
 ],
 'related': ['subcutaneous-technique', 'gauge-comparison', 'sharps-disposal-australia'],
},

{
 'slug': 'reconstitution-basics',
 'title': 'Mixing a powder with sterile water',
 'meta': 'Guide · 8 min',
 'blurb': 'How much to add, how to avoid contaminating the bottle, how long it keeps.',
 'desc': ('What bacteriostatic water is, why the volume you add sets the '
          'concentration, and how to keep a multi-use vial clean. We supply the '
          'diluent, never the compound.'),
 'answer': ('Reconstituting means adding sterile liquid to a powder to dissolve it. '
            'The volume you add decides the concentration, so it decides what every '
            'mark on the syringe is worth afterwards. Use the volume your '
            'prescriber specified.'),
 'body': [
  ('What we do and do not supply', [
   'We sell bacteriostatic water, sterile water for injection, vial adapters, '
   'drawing-up needles, syringes and swabs. We do not sell peptides, hormones or '
   'any prescription medicine, in any form, and we are not going to tell you '
   'what to put in the vial or how much of it to use.',
   'This page is about the equipment and the arithmetic. Everything specific to '
   'a compound comes from whoever is managing your treatment.',
  ]),
  ('Bacteriostatic water and sterile water are different', [
   'Sterile water for injection is exactly that and nothing else. Once you '
   'pierce the stopper it is a single use product, because there is nothing in '
   'it to stop bacteria growing.',
   'Bacteriostatic water contains benzyl alcohol, usually around nine tenths of '
   'a per cent, which inhibits bacterial growth and allows a vial to be entered '
   'more than once over a period of days. That is what makes a multi-dose vial '
   'practical.',
   'Benzyl alcohol is not suitable for everyone, and which diluent is right is '
   'part of the prescribing decision rather than a preference.',
  ]),
  ('The volume you add sets the concentration', [
   'This is the part people get wrong. The powder is a fixed amount. The liquid '
   'you add is what changes, and it determines how much powder ends up in each '
   'unit on the syringe.',
   'Put simply: add twice as much water and every mark on the barrel is worth '
   'half as much. Nothing about the powder changed. Which is why the volume has '
   'to be the one you were told to use, and why writing it on the vial matters.',
   'Our reconstitution calculator does the arithmetic if you have the strength '
   'and the volume. It does not tell you what either of them should be.',
  ]),
  ('Keeping the vial clean', [
   'Swab the stopper before every entry and let it dry. Every time, not just the '
   'first.',
   'Add the water slowly, down the inside wall of the vial rather than straight '
   'onto the powder. Then swirl or roll it gently until it dissolves. Do not '
   'shake it. Many of these compounds are fragile and shaking is what foams and '
   'damages them.',
   'A vial adapter seats once in the stopper and gives you a clean luer port to '
   'work through, which means you are not pushing a needle through the same '
   'piece of rubber over and over. On a vial you will enter many times it pays '
   'for itself in coring alone.',
   'Label it. Date, what is in it, and the volume you added. In a month you will '
   'not remember, and guessing is not an option.',
  ]),
 ],
 'faq': [
  ('How much water should I add?',
   'The volume your prescriber specified. It sets the concentration, so it '
   'changes what every mark on the syringe means.'),
  ('Can I use tap water or saline?',
   'No to tap water, ever. Sodium chloride for injection is a diluent for some '
   'products and not others. Use what the directions specify.'),
  ('How long does it keep once mixed?',
   'That depends on the compound and the diluent, and it is on the directions '
   'that came with it. Bacteriostatic water allows repeated entry over a period; '
   'sterile water does not.'),
  ('Why should I not shake it?',
   'Many of these compounds are fragile. Shaking foams the solution and can '
   'damage them. Swirl or roll gently instead.'),
 ],
 'related': ['reading-a-syringe', 'storing-supplies', 'needle-numbers-explained'],
},

{
 'slug': 'sharps-disposal-australia',
 'title': 'Sharps disposal, state by state',
 'meta': 'Guide · 7 min',
 'blurb': 'Where a full container actually goes, what every state agrees on, and how to find the answer for your address.',
 'desc': ('Where to take a full sharps container in Australia. What every state '
          'agrees on, what differs, and how to find the current answer for your '
          'own address.'),
 'answer': ('Used needles go straight into an Australian Standard sharps container, '
            'never into household rubbish, recycling or the green bin. A full one '
            'goes back to a participating pharmacy, a council collection point, a '
            'public disposal bin, or a public hospital or community health centre, '
            'depending on where you live. Your council and your state health '
            'department are the authority on which of those applies to your address.'),
 'body': [
  ('The part that is the same everywhere', [
   'Nothing sharp goes in a household bin. Not the rubbish bin, not the recycling, '
   'not the green waste. A needle in a kerbside bin becomes a needlestick injury for '
   'whoever handles it next, and that is a waste worker, a sorting line operator, or '
   'a member of your own household. Every state and territory says the same thing '
   'about this and none of them makes an exception for a needle that was only used '
   'once.',
   'The container has to be a real one. In Australia that means it meets AS 4031 or '
   'AS/NZS 4261: rigid yellow plastic, a lid that locks shut permanently, a '
   'biohazard mark, and a fill line. The standard exists because the container is '
   'the only thing between a used needle and the next pair of hands, and a container '
   'that can be reopened or crushed is not doing that job.',
   'Fill it to the line and no further, which is usually about three quarters. '
   'Overfilling is the most common reason a collection point refuses a container, '
   'and pressing down on a full one to make room is how people injure themselves.',
   'Do not recap a needle before it goes in, and do not try to bend, break or cut '
   'one. Recapping is where a large share of needlestick injuries happen, because it '
   'puts a moving hand directly in front of a sharp point.',
  ]),
  ('Where a full container goes', [
   'There are four routes in Australia, and which ones exist near you depends on '
   'your council and your state rather than on anything national.',
   'Participating pharmacies. Many pharmacies accept full containers, and many sell '
   'empty ones. Participation is voluntary and not universal, so ring before you '
   'make the trip rather than arriving with a full container and no plan.',
   'Council collection points and exchange schemes. A lot of councils run a swap: '
   'bring the full one in, take an empty one away, often at no charge. Councils that '
   'do this usually run it from a customer service centre or a transfer station.',
   'Public disposal bins. Some councils install permanent sharps bins in public '
   'toilets and other locations. These are intended for loose sharps rather than for '
   'emptying a household container into.',
   'Public hospitals and community health centres. In several states these accept '
   'community sharps directly, which is often the most reliable option when the '
   'other three are unclear.',
  ]),
  ('What differs by state', [
   'New South Wales runs a community sharps programme through NSW Health, and '
   'disposal points include public hospitals, community health centres, '
   'participating pharmacies and public disposal bins.',
   'Queensland works similarly, with public hospitals, participating pharmacies and '
   'some medical centres accepting community sharps.',
   'Victoria devolves it almost entirely to councils, and arrangements differ '
   'between neighbouring councils in the same city. Melbourne alone has more than '
   'thirty, so the answer for one suburb is not the answer for the next.',
   'Western Australia also varies by local government, and the state advises '
   'residents to check with their council or their healthcare provider.',
   'South Australia, Tasmania, the ACT and the Northern Territory each publish their '
   'own guidance, and in each case the local council remains the practical starting '
   'point.',
   'The honest summary is that there is no single national answer, and anyone who '
   'gives you one has not checked. What is national is the rule about household '
   'bins and the container standard.',
  ]),
  ('Finding the current answer for your address', [
   'Specific addresses and opening hours change, and a guide that lists them goes '
   'stale quietly, which is worse than not listing them at all when the thing you '
   'are carrying is a container of used needles. Two methods stay reliable.',
   'Search your council name together with "sharps" or "needle disposal". Almost '
   'every Australian council publishes this in an A to Z waste guide, and that page '
   'is maintained by the people who actually run the service.',
   'Ask the pharmacy that dispenses for you. They will know whether they accept '
   'containers themselves and, if not, usually where the nearest point is. '
   'Diabetes Australia also publishes a national resource on safe sharps disposal '
   'that is kept current.',
   'We supply containers that meet the standard. We are not a collection service and '
   'we do not take full containers back, so the routes above are the ones that '
   'apply.',
  ]),
  ('Travelling with sharps', [
   'A sharps container can travel in hand luggage on Australian domestic flights, '
   'and airlines expect to see it alongside the equipment it belongs to. Keep it in '
   'the same bag as the rest of your supplies rather than packed separately.',
   'Going overseas, check the destination rather than assuming. Disposal '
   'arrangements that are routine here do not exist everywhere, and some countries '
   'treat used sharps as regulated waste with rules about carrying them.',
  ]),
 ],
 'faq': [
  ('Can I put a sharps container in the wheelie bin?',
   'No, in every state and territory. A sealed container still ends up on a sorting '
   'line or in a truck where someone handles it, and a needle that comes loose there '
   'is a needlestick injury for a person doing their job.'),
  ('Can I use a hard plastic bottle instead?',
   'No. A drink bottle is not rigid enough, cannot be sealed permanently, carries no '
   'biohazard marking, and will not be accepted at a collection point. It also looks '
   'like a drink bottle, which is the specific reason it is dangerous in a household '
   'with children.'),
  ('Do pharmacies take full containers?',
   'Many do and many do not, because participation is voluntary rather than required. '
   'Ring first. A pharmacy that does not accept them can usually tell you which '
   'nearby one does.'),
  ('Is sharps disposal free?',
   'Collection is usually free where a council or health service provides it. The '
   'empty container is often not, though a number of councils run an exchange where '
   'you swap a full one for an empty one at no charge.'),
  ('What do I do if I am stuck by a used needle?',
   'Wash the area with soap and running water, do not squeeze it, cover it, and seek '
   'medical advice promptly rather than waiting to see what happens. In Australia '
   'that means a GP, an emergency department, or healthdirect on 1800 022 222 for '
   'advice on where to go.'),
 ],
 'related': ['storing-supplies', 'first-injection', 'artg-explained'],
},
{
 'slug': 'artg-explained',
 'title': 'What ARTG listing actually means',
 'meta': 'Guide · 4 min',
 'blurb': 'The difference between listed, registered and neither.',
 'desc': ('What the ARTG is, the difference between a listed and a registered '
          'product, and why plenty of legitimate consumables are on neither.'),
 'answer': ('The ARTG is the Therapeutic Goods Administration’s register of '
            'products approved for supply in Australia. Listed means assessed '
            'against a lower risk pathway, registered means individually evaluated, '
            'and some low risk goods need neither.'),
 'body': [
  ('What the register is', [
   'The Australian Register of Therapeutic Goods is maintained by the '
   'Therapeutic Goods Administration. Therapeutic goods supplied in Australia '
   'generally have to be included on it, and the entry is held by a sponsor, '
   'which is the Australian entity responsible for the product.',
   'The register is public. If a product claims an ARTG number you can look it '
   'up and see what was actually approved, which is more useful than the claim '
   'itself.',
  ]),
  ('Listed, registered, and included', [
   'Registered goods have been individually evaluated by the TGA for quality, '
   'safety and, where it applies, effectiveness. This is the higher scrutiny '
   'pathway and it is where higher risk products sit.',
   'Listed goods go through a lower risk pathway. The sponsor certifies that the '
   'product meets the applicable requirements and uses only permitted '
   'ingredients and permitted claims. The TGA audits rather than evaluating '
   'every one before supply.',
   'Medical devices are classified by risk, from Class I up, and the '
   'requirements scale with the class. A syringe and an implant are not treated '
   'the same way and should not be.',
  ]),
  ('Why some things are on neither', [
   'Not everything in a treatment room is a therapeutic good. Paper towel, couch '
   'roll and facial tissues are not, and looking for an ARTG number on a box of '
   'tissues will not find one.',
   'That is why we show approval status per product, from a real value for that '
   'specific product, rather than printing a blanket claim across a catalogue. A '
   'site that puts the same regulatory line on cotton wool and on a syringe is '
   'telling you nothing about either.',
   'Where a product in our range has an entry, the number belongs on its page. '
   'Where it does not, nothing should appear, and nothing does.',
  ]),
 ],
 'faq': [
  ('Is registered better than listed?',
   'It is a different pathway for different risk, not a quality ranking. '
   'Registered products are individually evaluated; listed ones go through a '
   'lower risk route with auditing.'),
  ('Can I look up an ARTG number myself?',
   'Yes. The register is public and searchable on the TGA website, and it will '
   'tell you what was actually approved and who sponsors it.'),
  ('Does everything you sell have an ARTG entry?',
   'No, and it should not. Paper towel and tissues are not therapeutic goods. '
   'We show the status per product where it applies and show nothing where it '
   'does not.'),
 ],
 'related': ['storing-supplies', 'sharps-disposal-australia', 'needle-numbers-explained'],
},

{
 'slug': 'storing-supplies',
 'title': 'Storing supplies correctly',
 'meta': 'Guide · 3 min',
 'blurb': 'Temperature, light, and how to read a batch and expiry.',
 'desc': ('How to store consumables so they are still sterile when you need '
          'them: temperature, light, humidity, and what batch numbers and expiry '
          'dates are for.'),
 'answer': ('Keep consumables in their packaging, somewhere cool, dry and out of '
            'direct sunlight, and use the oldest stock first. The expiry date on a '
            'sterile item is the date its sterility is guaranteed to, not a '
            'best-before.'),
 'body': [
  ('Sterile packaging is the product', [
   'A sterile syringe is only sterile while its wrapper is intact. A pouch that '
   'has been opened, torn, crushed or got damp is no longer a sterile item, '
   'whatever the date on it says.',
   'Which means the packaging is not something to get rid of to save space. '
   'Leave things in their boxes and blisters until the moment you use them, and '
   'check the pouch before you open it.',
  ]),
  ('Cool, dry, dark', [
   'Room temperature, out of direct sunlight, away from heat and away from '
   'damp. A linen cupboard is usually fine. A car boot in an Australian summer '
   'is not, and neither is a windowsill or the cupboard above the kettle.',
   'Adhesives are the most temperature sensitive things in a normal supply '
   'cupboard. Tape and plasters that have been hot go gummy or stop sticking '
   'altogether, and there is no way back from that.',
   'Anything that says refrigerate belongs in a fridge at the stated '
   'temperature, not in the freezer and not in the door where the temperature '
   'swings every time it opens. Most consumables do not need refrigeration; the '
   'medicine often does.',
  ]),
  ('Batch numbers and expiry dates', [
   'The batch or lot number identifies the production run. It exists so that if '
   'a problem is found, the affected run can be traced and recalled precisely '
   'rather than pulling everything. It is the reason keeping the box is useful.',
   'The expiry date on a sterile single use item is the date the manufacturer '
   'guarantees sterility and performance to. It is not a best-before and it is '
   'not conservative padding. Past it, the guarantee is gone.',
   'Use the oldest first. Put new stock behind old stock rather than on top of '
   'it, and check dates when something arrives rather than when you reach for '
   'it in a hurry.',
  ]),
 ],
 'faq': [
  ('Can I use something just past its expiry date?',
   'The manufacturer no longer guarantees it is sterile. For a single use '
   'sterile item, that is the whole point of the item.'),
  ('Does anything here need refrigerating?',
   'Most consumables do not. Check the packaging, and follow it where it says '
   'otherwise. The medicine is a separate question and usually a stricter one.'),
  ('What is the batch number for?',
   'Tracing a production run if a fault is found, so a recall can be precise. '
   'It is a good reason to keep the box until the contents are used.'),
  ('Where should I not store supplies?',
   'A car, a bathroom, a windowsill, or anywhere above a heat source. Heat and '
   'damp are what ruin adhesives and packaging.'),
 ],
 'related': ['artg-explained', 'reconstitution-basics', 'sharps-disposal-australia'],
},

]

BY_SLUG = {g['slug']: g for g in GUIDES}
