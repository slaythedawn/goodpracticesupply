# The launch range, from the priority sourcing shortlist.
#
# Tab 1 of that shortlist is the Target 10, the complete self-injection kit, and
# every one of those ten already had a page. What was missing was most of tab 2.
# This module adds the twenty SKUs that had nowhere to land and the two
# categories they needed, and it is merged into CATEGORIES at the end of
# catalogue.py so none of the existing product copy is disturbed.
#
# Specs here are transcribed from the shortlist. Prices, codes and batch data are
# still invented: no factory has quoted yet.

from catalogue import P

# slug of the category to extend -> products to append
EXTRA_PRODUCTS = {

'syringes-needles': [
 P('Luer-slip syringes','luer-slip-syringes','luer','Slip tip, three part, sterile',
   'The same barrel as a luer-lock without the thread, for when the needle pushes on rather than screws on. Cheaper per unit and quicker to change, but it will not hold against pressure, so anything you are pushing hard belongs on a lock.',
   'syringe',
   [('1mL','Small doses'),('3mL','The common one'),('5mL','Draw and transfer'),('10mL','Irrigation and fill')],
   [('Box of 100',3180),('Carton of 500',14200),('Carton of 1000',26900)],
   extra=[('Tip','Luer slip'),('Construction','Three part, siliconised'),('Sterilisation','Ethylene oxide'),('Single use','Yes')]),
],

'diluents-swabs': [
 P('Cotton wool balls','cotton-wool-balls','cotton','100% cotton, non-sterile, bulk',
   'Plain cotton wool, in a bag rather than a jar, for pressure after a needle and for prep where a swab is more than you need. Bulk is the only sensible way to buy these.',
   'prep',
   [('Balls, medium','The usual'),('Balls, large','More absorbent'),('Tipped applicators','For detail work')],
   [('Bag of 500',890),('Bag of 1000',1540),('Carton of 5000',6900)],
   extra=[('Material','100% bleached cotton'),('Sterility','Non-sterile'),('Use','Prep and pressure')]),
],

'wound-care': [
 P('Adhesive plasters','adhesive-plasters','plasters','Plastic and fabric, assorted, box of 100',
   'The box you actually run out of. Assorted sizes in both plastic and fabric, because the plastic ones stay put in water and the fabric ones flex over a knuckle. Latex free adhesive.',
   'wound',
   [('Plastic, assorted','Water resistant'),('Fabric, assorted','Flexes and breathes'),('Blue detectable','Food handling areas')],
   [('Box of 100',1290),('Box of 250',2840),('Carton of 1000',9900)],
   extra=[('Adhesive','Latex free acrylic'),('Pad','Low adherent'),('Sterility','Individually wrapped, sterile')]),

 P('Crepe bandages','crepe-bandages','bandages','Cotton crepe, 5 to 15cm',
   'Light support and holding a dressing down. Cotton crepe stretches in one direction and relaxes as it warms, which is why it needs checking rather than pulling tight once.',
   'wound',
   [('5cm','Fingers and wrists'),('7.5cm','Forearm and ankle'),('10cm','Knee and calf'),('15cm','Thigh and torso')],
   [('Each',340),('Box of 12',3660),('Carton of 72',19800)],
   extra=[('Material','Cotton crepe'),('Stretch','Single direction'),('Sterility','Non-sterile')]),

 P('Cohesive bandage','cohesive-bandage','bandages','Self adherent, 5cm x 4.5m, latex free',
   'Sticks to itself and to nothing else, so it holds without tape and comes off without taking hair with it. The one to reach for over a dressing on an awkward shape.',
   'wound',
   [('2.5cm','Fingers'),('5cm','The common one'),('7.5cm','Limbs')],
   [('Box of 12',2280),('Box of 24',4180),('Carton of 96',15600)],
   extra=[('Material','Latex free cohesive'),('Length','4.5m stretched'),('Fixation','Self adherent, no tape')]),

 P('Hydrocolloid and foam dressings','hydrocolloid-foam-dressings','dressings','Sterile, 10 x 10cm',
   'The dressings that manage moisture rather than just cover. Hydrocolloid for shallow wounds with light exudate, foam where there is more to absorb and the area needs cushioning.',
   'wound',
   [('Hydrocolloid, 10 x 10cm','Shallow, light exudate'),('Foam, 10 x 10cm','More absorbent'),('Foam adhesive border','Stays without tape')],
   [('Box of 5',2450),('Box of 10',4590),('Carton of 50',20900)],
   extra=[('Sterility','Sterile, individually pouched'),('Size','10 x 10cm'),('Wear time','Up to 7 days, per instructions')]),

 P('Silicone scar gel','silicone-scar-gel','dressings','Medical silicone, 15g tube',
   'Medical grade silicone in a tube, for closed and fully healed skin. It is not a dressing and it is not for open wounds. Follow the directions from whoever is managing the scar.',
   'wound',
   [('15g tube','The standard'),('30g tube','Larger areas')],
   [('Each',2990),('Box of 6',16400),('Box of 12',30800)],
   extra=[('Active','Medical grade silicone'),('Format','Self drying gel'),('Use','Closed, healed skin only')]),

 P('Sutures','sutures','procedure','Sterile, 3-0 and 4-0 on a cutting needle',
   'Non-absorbable nylon and absorbable, both on a reverse cutting needle, in the two sizes a treatment room gets through. Supplied sterile, single use, with the needle swaged on.',
   'wound',
   [('Nylon 3-0','Non-absorbable'),('Nylon 4-0','Non-absorbable, finer'),('Absorbable 3-0','No removal'),('Absorbable 4-0','No removal, finer')],
   [('Box of 12',4290),('Box of 24',7980),('Carton of 72',22400)],
   extra=[('Needle','Reverse cutting, swaged'),('Sterility','Sterile, single use'),('Thread length','75cm')]),
],

'diagnostics': [
 P('Urinalysis strips','urinalysis-strips','strips','10 parameter, tube of 100',
   'Ten pads on a strip, read against the chart on the tube. Keep the lid closed and the desiccant in, because these go off fast once air gets at them.',
   'diag',
   [('10 parameter','The standard panel'),('4 parameter','Screening only')],
   [('Tube of 100',2190),('Box of 5 tubes',9900),('Carton of 20 tubes',36800)],
   extra=[('Parameters','10'),('Read','Visual, against the tube chart'),('Storage','Sealed, with desiccant')]),

 P('Otoscope ear specula','otoscope-ear-specula','covers','Disposable tips, 2.5mm and 4mm',
   'Disposable tips in the two sizes that cover adults and children. Check they seat on your otoscope head before you order a carton, because the fittings are not universal.',
   'diag',
   [('2.5mm','Paediatric'),('4mm','Adult'),('Mixed bag','Both sizes')],
   [('Bag of 100',1690),('Box of 500',7400),('Carton of 1000',13800)],
   extra=[('Sizes','2.5mm and 4mm'),('Sterility','Non-sterile, single use'),('Fitting','Check against your otoscope head')]),

 P('Blood glucose meter','blood-glucose-meter','meters','Meter, lancing device and case',
   'The meter that matches the strips. Meters and strips are a closed pair, so a meter from one maker will not read another maker’s strip, whatever the box says.',
   'diag',
   [('Meter only','You have strips'),('Starter kit','Meter, device, 10 strips')],
   [('Each',3490),('Box of 5',15900),('Carton of 20',58000)],
   extra=[('Sample','Capillary blood'),('Strips','Matched strips only'),('Memory','Last 500 readings')]),

 P('Tongue depressors','tongue-depressors','practice','Wooden, adult, non-sterile',
   'Plain birch, smooth edges, adult length. Bought by the hundred because they are single use and there is no reason to buy them any other way.',
   'diag',
   [('Adult','150mm'),('Paediatric','140mm')],
   [('Box of 100',690),('Carton of 1000',5400),('Carton of 5000',24500)],
   extra=[('Material','Birch, smooth edged'),('Sterility','Non-sterile'),('Length','150mm adult')]),
],

'clinic-disposal': [
 P('Incontinence pads and pants','incontinence-pads','continence','Shaped pads and pull-ups, by absorbency',
   'Shaped pads for use inside close fitting underwear and pull-up pants where a pad will not stay put. Absorbency matters more than size, and the two do not track together.',
   'clinic',
   [('Pad, moderate','Day use'),('Pad, maximum','Night use'),('Pull-up, medium','Mobile'),('Pull-up, large','Mobile')],
   [('Pack of 14',1890),('Carton of 4 packs',6900),('Carton of 8 packs',12900)],
   extra=[('Absorbency','Rated per line'),('Format','Shaped pad or pull-up'),('Sizing','By hip measurement')]),
],

}

# Two categories the shortlist needed that the site did not have.
EXTRA_CATEGORIES = [
{
 'slug':'hygiene-cleaning', 'name':'Hygiene & cleaning', 'count':14,
 'imgkey':'gloves',
 'alt':'A dispenser box of gloves beside a folded pack',
 'intro':'The consumables a room gets through without anyone ordering them, until the day nobody can. Hand wash and hand towels at the basin, tissues on the desk, cotton wool for pressure after a needle. None of it is interesting and all of it stops the room working when it runs out, which is exactly what a standing order is for.',
 'filters':[('all','Everything'),('hands','At the basin'),('paper','Paper'),('cotton','Cotton')],
 'products':[
  P('Liquid hand wash','hand-soap','hands','pH neutral, 500mL pump and 5L refill',
    'A pH neutral wash for hands that are washed twenty times a day, plus the 5L refill, because buying pumps over and over is the expensive way to do it.',
    'glove',
    [('pH neutral','Everyday washing'),('Antibacterial','Where it is required')],
    [('500mL pump',790),('5L refill',3290),('Carton of 2 x 5L',6200)],
    extra=[('Format','Pump bottle and bulk refill'),('pH','Neutral, skin matched'),('Fragrance','None')]),

  P('Interleaved hand towels','hand-towels','paper','Slimfold interleaved, carton',
    'Interleaved rather than roll, so one comes out and the next one waits. Slimfold fits the standard dispenser, which is most of them.',
    'glove',
    [('Slimfold','Standard dispenser'),('Ultraslim','Compact dispenser')],
    [('Carton of 2400',4290),('Carton of 4000',6890)],
    extra=[('Fold','Interleaved, slimfold'),('Ply','1 ply'),('Dispenser','Standard slimfold')]),

  P('Facial tissues','facial-tissues','paper','2 ply, box',
    'Two ply, flat box, on the desk and in the treatment room. Bought by the carton because a single box lasts about a fortnight.',
    'glove',
    [('Standard box','100 sheets'),('Cube box','Fits a trolley')],
    [('Box of 100',190),('Carton of 24 boxes',3890),('Carton of 48 boxes',7200)],
    extra=[('Ply','2 ply'),('Sheets','100 per box'),('Format','Flat or cube box')]),

  P('Cotton wool rolls','cotton-wool-rolls','cotton','100% cotton, zig-zag roll',
    'A zig-zag roll you tear from rather than pre-formed balls, for when the piece you want is a different size every time.',
    'prep',
    [('375g roll','The standard'),('500g roll','Larger')],
    [('Each',1090),('Box of 6',5900),('Carton of 12',10900)],
    extra=[('Material','100% bleached cotton'),('Format','Zig-zag roll'),('Sterility','Non-sterile')]),
 ],
},
{
 'slug':'taping-supports', 'name':'Taping & supports', 'count':11,
 'imgkey':'dressings',
 'alt':'Rolls of strapping tape beside an elastic bandage',
 'intro':'Rigid where you want a joint to stop, elastic where you want it to move and still be held. The two get bought together and used together: rigid zinc oxide for the anchor, elastic adhesive over the top so it survives a session. Kinesiology tape is a different job again and is here because clinics ask for it in the same order.',
 'filters':[('all','Everything'),('rigid','Rigid'),('elastic','Elastic'),('compression','Compression')],
 'products':[
  P('Rigid strapping tape','rigid-strapping-tape','rigid','Zinc oxide, 38mm x 13.7m',
    'The rigid zinc oxide roll that does the anchoring. It does not stretch, which is the whole point, and it tears straight across by hand.',
    'wound',
    [('25mm','Fingers and thumbs'),('38mm','The common one'),('50mm','Larger joints')],
    [('Each',690),('Box of 8',4990),('Carton of 48',27900)],
    extra=[('Adhesive','Zinc oxide'),('Stretch','Rigid, none'),('Length','13.7m')]),

  P('Elastic adhesive bandage','elastic-adhesive-bandage','elastic','EAB, 75mm x 4.5m stretched',
    'Elastic adhesive over the top of a rigid anchor, so the strapping moves with the limb instead of peeling off it. Cuts with scissors rather than tearing.',
    'wound',
    [('50mm','Ankle and wrist'),('75mm','The common one')],
    [('Each',1090),('Box of 6',5900),('Carton of 36',32400)],
    extra=[('Adhesive','Zinc oxide'),('Stretch','Elastic, lengthwise'),('Length','4.5m stretched')]),

  P('Kinesiology tape','kinesiology-tape','elastic','Cotton elastic, 5cm x 5m',
    'Cotton elastic with a wave pattern adhesive, in a roll you cut to shape. A different job to strapping: it stays on for days and it does not restrict a joint.',
    'wound',
    [('Beige','The default'),('Black','Most asked for'),('Blue','Colour coded'),('Pre-cut strips','No scissors')],
    [('Roll',1490),('Box of 6 rolls',7900),('Bulk roll, 31.5m',6900)],
    extra=[('Material','Cotton elastic'),('Adhesive','Acrylic, wave pattern'),('Wear time','Up to 5 days')]),

  P('Compression stockings','compression-stockings','compression','Class 1 knee high',
    'Class 1 knee high, sized on ankle and calf measurement rather than shoe size. Sizing is the whole job here: a stocking that is too big does nothing and one that is too small will not be worn.',
    'wound',
    [('Small','By measurement'),('Medium','By measurement'),('Large','By measurement'),('Extra large','By measurement')],
    [('Pair',2490),('Box of 5 pairs',10900),('Carton of 20 pairs',39900)],
    extra=[('Class','Class 1, 14 to 17mmHg'),('Length','Knee high'),('Sizing','Ankle and calf measurement')]),
 ],
},
]

# Filter chips the new products need on categories that already existed.
EXTRA_FILTERS = {
 'diluents-swabs': [('cotton','Cotton wool')],
 'wound-care':     [('bandages','Bandages'),('plasters','Plasters'),('procedure','Procedure')],
 'diagnostics':    [('meters','Meters'),('practice','Practice items')],
 'clinic-disposal':[('continence','Continence')],
}
