# Placeholder catalogue. Prices, codes and batch data are invented so the browsing
# experience is complete end to end. Nothing here is a real product record.
B = "https://d8j0ntlcm91z4.cloudfront.net/user_302vtY04kC9nbtUjJJAhLoDVMFw/"
# Images that were repaired locally and re-uploaded sit on the other bucket.
U = "https://d2ol7oe51mr4n9.cloudfront.net/user_302vtY04kC9nbtUjJJAhLoDVMFw/"
I = {
 'syringe_box': B+'hf_20260912_014655_c87ec5d7-96f6-4729-b6ef-fc062184ab3f.png',
 'syringes':    B+'hf_20260912_023904_ac99bf9d-40bb-4cb3-b197-e10d78b28291.png',
 'barrel':      B+'hf_20260912_031429_c3ac1819-2bb8-4e0b-af1e-dbd72e0116fd.png',
 'carton':      B+'hf_20260912_023904_70721a4d-07ea-42bc-b730-aba9835e34b7.png',
 'blister':     B+'hf_20260912_023904_ee6d90dc-da5a-4635-81c5-6707caee41a3.png',
 'tray':        B+'hf_20260912_023904_19f69ed5-241c-4963-8176-8700fc6688c2.png',
 'gloves':      B+'hf_20260912_014655_ce0a72ce-81b1-4e0f-9b65-5b02b25a2093.png',
 'vial_swabs':  B+'hf_20260912_014655_90258385-316a-41e3-ad9d-cb1d75f7eda4.png',
 'dressings':   B+'hf_20260912_014655_fc63b5f4-f8cb-41c5-9e1d-bb51f3eb6a8a.png',
 'diagnostic':  B+'hf_20260912_014655_b20c505c-894a-4948-a4ec-b6811facc908.png',
 'sharps':      B+'hf_20260912_014655_ff570e50-4d34-4cd4-882b-4e40b83438e1.png',
 'needle_macro':B+'hf_20260912_031429_9653357d-54b9-47f5-bdac-f1686c716860.png',
 'lengths':     B+'hf_20260912_031429_c3ac1819-2bb8-4e0b-af1e-dbd72e0116fd.png',
 # The launch range. One photograph per product rather than a shared family set,
 # because these are the first real SKUs and a picture of something else is not
 # a picture of the thing you are buying.
 'cotton_wool': B+'hf_20260915_111902_1adc5949-ff18-47c2-a576-2cfb89e269e1.png',
 'hand_towels': B+'hf_20260915_111901_c5c01f5a-5e9d-4cd1-81fa-de32f17fa06f.png',
 'tissues':     B+'hf_20260915_111902_f3e1fc31-f656-45cf-b97d-4e59d6ade4a9.png',
 'crepe':       B+'hf_20260915_111902_73529e6d-85a5-4ad0-b520-6895ba5d18d8.png',
 'sutures':     B+'hf_20260915_111902_0a56cd8c-12a4-4c97-a2b2-e3822156c612.png',
 'depressors':  B+'hf_20260915_111920_7a628413-5282-4fd0-9ef1-a6cdc1feec3d.png',
 'continence':  B+'hf_20260915_111920_76f6efeb-d410-4d6d-a284-d9bc4471f625.png',
 'kinesio':     B+'hf_20260915_112232_e93ce35d-9a21-4d6b-bed9-d925f476a1a9.png',
 'stockings':   B+'hf_20260915_112231_8109e286-e963-4222-a9c4-eb6082edb19f.png',
 'plasters':    B+'hf_20260915_112445_a17e73ef-2587-4d63-b396-e5482f228145.png',
 'scar_gel':    B+'hf_20260915_112445_df1c68f9-58ba-4ea0-91e5-d922bb72275c.png',
 # Repaired after the OCR gate found generated lettering. See brand/PHOTOGRAPHY.md.
 'hand_wash':   U+'cd48a92f-24bd-4e14-91e7-c8539ca1b0c2.png',
 'rigid_tape':  U+'c5ace70a-b068-4174-89a0-6967a0428a36.png',
 'urine_strips':U+'0c77e718-d1f9-4641-99a2-412f2643e68d.png',
 'eab':         U+'e5cd5eeb-ff9a-4071-ad51-a5105a08bfbf.png',
 'specula':     U+'21cf8591-5e0e-4502-b291-4ffe19155c2f.png',
}
SHOTS = {  # four views per product family, reused across the catalogue
 'syringe': [('syringe_box','The box, closed'),('syringes','Three out of the box'),('barrel','Lengths side by side'),('carton','The carton opened')],
 'needle':  [('carton','The box, closed'),('needle_macro','Macro of the bevel'),('lengths','Lengths side by side'),('blister','Blister wrapped, in the tray')],
 'glove':   [('gloves','The dispenser box'),('tray','A pair, laid flat'),('carton','The carton'),('blister','Cuff detail')],
 'prep':    [('vial_swabs','Foil sachets beside a vial'),('carton','The carton'),('tray','A sachet opened'),('blister','Stacked in the tray')],
 'wound':   [('dressings','Sterile pouches and gauze'),('tray','A pouch opened'),('carton','The carton'),('blister','Layered in the box')],
 'diag':    [('diagnostic','Strips and a lancet'),('tray','The vial of strips'),('carton','The carton'),('blister','Single use, sealed')],
 'clinic':  [('sharps','The container, lid open'),('carton','The carton'),('tray','Bracket and key'),('blister','Aperture detail')],
 # The launch range. A single shot each: one honest photograph beats four where
 # three of them are something else in the same box.
 'cotton':     [('cotton_wool','Cotton wool, out of the bag')],
 'plasters':   [('plasters','Unwrapped, fabric and plastic')],
 'bandage':    [('crepe','Rolled, out of the pack')],
 'scar':       [('scar_gel','The nozzle, cap beside it')],
 'suture':     [('sutures','Foil packs laid out')],
 'urine':      [('urine_strips','The tube')],
 'specula':    [('specula','Tips, largest to smallest')],
 'depressor':  [('depressors','A fan of them')],
 'continence': [('continence','Two pads, laid flat')],
 'handwash':   [('hand_wash','The pump bottle and the refill')],
 'towels':     [('hand_towels','Interleaved, stacked')],
 'tissues':    [('tissues','The flat box')],
 'rigid':      [('rigid_tape','Three rolls')],
 'eab':        [('eab','Two rolls')],
 'kinesio':    [('kinesio','Three rolls, from above')],
 'stockings':  [('stockings','Folded flat')],
}

# Per-product regulatory and origin facts, keyed by slug.
#
# Deliberately empty. An ARTG entry and a country of origin are claims about
# specific goods, and until a supplier has given us one for a specific product
# there is nothing true to print. shop.py renders these rows only where a value
# exists, so an unfilled product simply does not make the claim rather than
# making a generic one.
#
#   REGULATORY = {'nitrile-examination-gloves':
#                   [('ARTG', 'ARTG 123456'), ('Country of origin', 'Malaysia')]}
REGULATORY = {}


def sku(cat, p, vi, pi):
    """Stable code for one product in one variant and one pack size.

    The cart carries it and the Shopify export emits it, so a line someone added
    before the catalogue was real still identifies the right variant afterwards.
    The whole slug, not a truncation: blood-glucose-meter and
    blood-glucose-test-strips collide at any sensible prefix length.
    """
    return 'GPS-%s-%s-%02d%02d' % (cat['slug'][:3].upper(), p['slug'].upper(),
                                   vi + 1, pi + 1)


def P(name, slug, tag, spec, blurb, family, variants, packs, extra=()):
    return dict(name=name, slug=slug, tag=tag, spec=spec, blurb=blurb,
                family=family, variants=variants, packs=packs, extra=list(extra))

CATEGORIES = [
{
 'slug':'syringes-needles', 'name':'Syringes & needles', 'count':28, 'img':I['syringe_box'],
 'alt':'A box of insulin syringes with three laid in front',
 'intro':'Everything that goes between the vial and the skin. Insulin syringes with the needle fixed for small doses read in units, luer-lock barrels for anything you draw and swap, and separate needles in the gauges and lengths people actually use rather than the full ISO range. A U-100 insulin syringe comes in 1mL, 0.5mL and 0.3mL, and the smaller the barrel the further apart the markings sit, which is the only reason to choose one over another for a small volume. The needle is fixed, so there is no dead space between barrel and hub and nothing is left behind. A luer-lock syringe is the opposite arrangement: the needle screws on and off, so you can draw with one and inject with another, and the screw fitting will not separate under pressure the way a slip fitting can. Gauge is thickness and the scale runs backwards, so 31G is finer than 29G, and [the difference between 29G, 30G and 31G](/learn/gauge-comparison) is comfort against how long you spend drawing up. Length decides whether you land under the skin or in muscle. Hub colours follow ISO 6009, which is why a 23G hub is the same blue on every box in the country. Drawing-up needles are blunt on purpose. They are wide enough to pull a thick liquid out of a vial in seconds and they cannot be injected with by accident. Pen needles fit any standard injector pen, whichever brand. The units printed on a barrel measure the liquid rather than the needle, which is worth knowing before you [read a syringe](/learn/reading-a-syringe) in a hurry. If you are not certain which pair you want, the Gauge Finder asks three plain questions and tells you.',
 'filters':[('all','Everything'),('insulin','Insulin syringes'),('luer','Luer-lock'),('needles','Needles'),('access','Vial access')],
 'products':[
  P('U-100 insulin syringes','u-100-insulin-syringes','insulin','Fixed needle, graduated in units','A fixed needle and a unit scale, which is what makes a small dose readable. The finer gauges are noticeably more comfortable and slightly slower to draw.','syringe',
    [('27G × 13mm','Reference spec'),('29G × 13mm','Fills fastest'),('30G × 8mm','The middle'),('31G × 6mm','Least sensation')],
    [('Box of 100',4776),('Box of 200',8990),('Carton of 500',20450)],
    [('Barrel','1.0mL and 0.5mL'),('Graduation','1 unit'),('Needle','Fixed, pre-attached'),('Dead space','Low'),('Material','DEHP free, PVC free'),('Sterilisation','Ethylene oxide')]),
  P('Luer-lock syringes','luer-lock-syringes','luer','Three part, screw fitting','A screw fitting that cannot separate under pressure, which matters the moment you push anything viscous. Three part construction for a smooth plunger.','syringe',
    [('1mL','Fine graduations'),('3mL','The common one'),('5mL','Larger volumes')],
    [('Box of 100',3240),('Box of 200',6100)],
    [('Construction','Three part, siliconised'),('Fitting','Luer-lock'),('Sterilisation','Ethylene oxide'),('Single use','Yes')]),
  P('Hypodermic needles','hypodermic-needles','needles','ISO colour coded hub','Separate needles for drawing and injecting, colour coded to the ISO standard so the gauge is readable across a bench at a glance.','needle',
    [('23G × 1in','Intramuscular'),('23G × 1.5in','Deeper IM'),('25G × 1in','Finer IM'),('27G × 1/2in','Subcutaneous')],
    [('Box of 100',1290),('Box of 500',5450)],
    [('Hub','ISO 6009 colour coded'),('Bevel','Triple ground'),('Range','18G to 25G'),('Sterilisation','Ethylene oxide')]),
  P('Drawing-up needles','drawing-up-needles','needles','Blunt fill, wide bore','Blunt, so it cannot be injected with by accident, and wide enough to pull a thick oil out of a vial in seconds rather than a minute.','needle',
    [('18G blunt fill','Standard'),('21G sharp fill','Through a stopper')],
    [('Box of 100',1420),('Box of 500',6200)],
    [('Gauge','18G'),('Tip','Blunt fill or sharp fill'),('Use','Drawing and reconstitution only'),('Sterilisation','Ethylene oxide')]),
  P('Vial access devices','vial-access-devices','access','Needle free, vented','Seats once in the stopper and gives you a clean luer port to work through, so you stop pushing a needle through the same spot and coring rubber into the vial.','prep',
    [('20mm','Standard vial'),('13mm','Small vial')],
    [('Box of 50',2650),('Box of 100',4900)],
    [('Neck sizes','13mm and 20mm'),('Filter','0.2 micron vented'),('Port','Luer-lock, needle free'),('Sterility','Sterile, single use')]),
  P('Pen needles','pen-needles','needles','Fits every standard injector pen','The shortest and finest on the Australian market. A 4mm needle very rarely reaches muscle whatever your build, which is why guidance has moved to it.','needle',
    [('32G × 4mm','Shortest'),('31G × 5mm','Slightly longer'),('31G × 8mm','If advised')],
    [('Box of 100',1890),('Box of 200',3490)],
    [('Thread','Universal'),('Use','Single use')]),
 ]},
{
 'slug':'gloves-ppe', 'name':'Gloves & PPE', 'count':31, 'img':I['gloves'],
 'alt':'A box of nitrile gloves with two gloves emerging',
 'intro':'Barrier protection for a treatment room or a kitchen bench. Nitrile rather than latex as the default, because latex sensitivity is common enough that most Australian practices moved years ago, and a glove that gives somebody a reaction is worse than no glove at all. Latex is still here for the people who prefer the feel of it and know they are fine with it. Everything is powder free. Powder was banned in surgical settings for good reason and it has no place in an examination glove either: it carries latex protein into the air and it contaminates whatever you are working on. Nitrile examination gloves come in three sizes rather than a box of mediums, because a glove that is too big catches on everything and one that is too small splits at the web of the thumb. Black nitrile and blue nitrile are the same glove in a different colour: blue reads as clinical and shows a tear against skin, black hides staining and is what most mobile practitioners buy. Masks are rated to the Australian standard rather than described loosely, so a Level 2 mask is a Level 2 mask. Gowns and aprons on a roll for the jobs where something is going to splash. Buy a single box or a carton, and the price per unit is on the page either way, which is not true of most of the people we are competing with.',
 'filters':[('all','Everything'),('gloves','Gloves'),('masks','Masks'),('gowns','Gowns & aprons'),('hygiene','Hand hygiene')],
 'products':[
  P('Nitrile examination gloves','nitrile-examination-gloves','gloves','Powder free, textured fingertips','The default for a reason. No latex proteins, better puncture resistance than vinyl, and a textured fingertip that still works when wet.','glove',
    [('Small',''),('Medium',''),('Large',''),('Extra large','')],
    [('Box of 100',1990),('Carton of 10 boxes',17900)],
    [('Material','Nitrile'),('Powder','Free')]),
  P('Latex examination gloves','latex-examination-gloves','gloves','Powder free, high tactility','More tactile than nitrile and still preferred for some fine work. Not for anyone with a latex sensitivity, and label the room accordingly.','glove',
    [('Small',''),('Medium',''),('Large','')],
    [('Box of 100',1650),('Carton of 10 boxes',14800)],
    [('Material','Natural rubber latex'),('Powder','Free')]),
  P('Surgical masks, Level 2','surgical-masks-level-2','masks','Three layer, fluid resistant','Level 2 to the Australian standard, which is the everyday clinical choice. Level 3 where splash is likely.','prep',
    [('Level 1','Low fluid'),('Level 2','Standard'),('Level 3','High fluid')],
    [('Box of 50',1290),('Carton of 40 boxes',44900)],
    [('Standard','AS 4381'),('Layers','Three')]),
  P('Isolation gowns','isolation-gowns','gowns','Fluid resistant, thumb loop','Full coverage with a thumb loop so the cuff stays where you put it. Disposable, because laundering a barrier defeats it.','prep',
    [('Regular',''),('Large','')],
    [('Pack of 10',3450),('Carton of 50',15900)],
    [('Closure','Neck and waist ties'),('Use','Single use')]),
  P('Aprons on a roll','aprons-on-a-roll','gowns','Perforated, wall dispensable','Pull, tear, wear. The cheapest barrier in the room and the one most often missing when it is needed.','prep',
    [('Standard',''),('Heavy duty','')],
    [('Roll of 200',2290),('Carton of 6 rolls',12400)],
    [('Material','LDPE'),('Format','Perforated roll')]),
  P('Alcohol hand rub','alcohol-hand-rub','hygiene','70% ethanol, with emollient','Seventy percent is the number that matters. The emollient is why staff will actually use it forty times a day.','prep',
    [('500mL pump','Bench'),('5L refill','Bulk')],
    [('Each',1290),('Carton of 6',6900)],
    [('Alcohol','70% v/v'),('Format','Gel')]),
 ]},
{
 'slug':'diluents-swabs', 'name':'Diluents & swabs', 'count':19, 'img':I['vial_swabs'],
 'alt':'A glass vial, a carton and foil swab sachets',
 'intro':'Skin prep and the water you mix with. Alcohol swabs are the single highest turnover line in most rooms and the easiest to under order, so they come in two hundreds rather than hundreds. They are 70 per cent isopropyl, which is the concentration that actually works: pure alcohol evaporates before it has done anything, and the water in a 70 per cent solution is what lets it stay wet long enough to matter. Bacteriostatic water and sterile water are not the same thing and the difference matters. Bacteriostatic water is preserved with benzyl alcohol, which is what lets a vial keep once it has been broached. Sterile water has no preservative, so it is single use and the rest of the vial is waste. If you are mixing something you will come back to, the preserved one is the one you want, and [mixing a powder with sterile water](/learn/reconstitution-basics) covers how much to add and why the volume changes the concentration. Chlorhexidine where alcohol alone is not enough, and povidone iodine where chlorhexidine is not tolerated. Sodium chloride sachets for irrigation. You will want [syringes and needles](/shop/syringes-needles) to go with it, and [what the numbers on a needle mean](/learn/needle-numbers-explained) if the gauges are not yet second nature. We supply the diluent and the equipment, never the compound.',
 'filters':[('all','Everything'),('swabs','Swabs'),('water','Water & diluents'),('antiseptic','Antiseptics')],
 'products':[
  P('Alcohol swabs','alcohol-swabs','swabs','70% isopropyl, foil sachet','Two per injection, one for the stopper and one for the skin. Buy the two hundred, it is cheaper per swab and you will not run out mid month.','prep',
    [('70% isopropyl','Standard'),('With chlorhexidine','Stronger')],
    [('Box of 200',890),('Carton of 20 boxes',15900)],
    [('Alcohol','70% isopropyl'),('Pad','Two ply non-woven'),('Size','65 × 30mm'),('Wrap','Individual foil sachet')]),
  P('Bacteriostatic water','bacteriostatic-water','water','Benzyl alcohol preserved','Preserved, so the vial keeps for weeks refrigerated once broached. Sterile water has no preservative and is single use the moment you open it.','prep',
    [('10mL',''),('30mL','')],
    [('Each',1450),('Pack of 5',6800)],
    [('Preservative','0.9% benzyl alcohol'),('Vial','Multi-dose glass'),('Stopper','Butyl rubber, aluminium crimp'),('Sizes','10mL and 30mL')]),
  P('Sterile water for injection','sterile-water-for-injection','water','No preservative, single use','Unpreserved. Use the whole ampoule or discard it, because there is nothing in it holding back growth.','prep',
    [('10mL ampoule','The standard'),('20mL ampoule','Larger volume')],
    [('Box of 50',3900),('Box of 100',7200)],
    [('Preservative','None'),('Format','Plastic ampoule, twist open'),('Grade','Water for injection BP'),('Use','Single use')]),
  P('Chlorhexidine skin prep','chlorhexidine-skin-prep','antiseptic','2% in 70% alcohol','The combination used before anything invasive. Let it dry, which is the step everyone skips and the step that does the work.','prep',
    [('Swabsticks','Small site'),('Applicator wand','Larger field'),('500mL bottle','Bulk')],
    [('Box of 25',4900),('Each',1690)],
    [('Chlorhexidine','0.5% to 2% w/v'),('Alcohol','70% v/v'),('Format','Swabstick or single use applicator')]),
  P('Povidone iodine swabsticks','povidone-iodine-swabsticks','antiseptic','10% solution, triple stick','Where chlorhexidine is contraindicated or unavailable. Stains, which is occasionally useful for seeing what you have covered.','prep',
    [('Triple stick',''),('Single stick','')],
    [('Box of 50',2450),('Box of 200',8200)],
    [('Iodine','10% w/v'),('Format','Swabstick')]),
  P('Sodium chloride sachets','sodium-chloride-sachets','water','0.9%, 30mL single use','Single use, so what you clean with is never the variable. A big bottle is contaminated the minute it is opened.','prep',
    [('30mL',''),('20mL','')],
    [('Box of 50',1890),('Carton of 10 boxes',16500)],
    [('Concentration','0.9% w/v'),('Use','Single use')]),
 ]},
{
 'slug':'wound-care', 'name':'Wound care', 'count':34, 'img':I['dressings'],
 'alt':'Surgical tape, gauze squares and sterile pouches',
 'intro':'What a treatment room reaches for, in quantities that make sense for one person or for a clinic. The upgrade over a chemist plaster is the contact layer. A non adherent dressing lifts off without taking the new tissue with it, which is the whole game in a wound that is actually healing, and it is the difference between a dressing change that takes a minute and one that undoes a week. Routine cleaning is saline rather than antiseptic, because antiseptics are cytotoxic to the cells doing the work. Antiseptic has its place, and that place is not a clean granulating wound you are simply redressing. Sterile gauze swabs for cleaning and packing, island dressings where you want the pad and the adhesive in one piece, and conforming bandages to hold a dressing on a limb that moves. Fixation tape that holds without removing skin when it comes away, which matters more the older or thinner the skin is. A workplace first aid kit for the rooms that have to have one. [Storing supplies correctly](/learn/storing-supplies) matters more here than most people expect: a sterile dressing is only sterile while its pouch is intact and in date, and a box kept in a hot car is not the box you think it is.',
 'filters':[('all','Everything'),('dressings','Dressings'),('gauze','Gauze'),('tape','Tapes & bandages'),('firstaid','First aid')],
 'products':[
  P('Non-adherent dressings','non-adherent-dressings','dressings','Low adherent contact layer','Lifts off without pulling the wound bed apart. The single biggest difference between a clinic dressing and a chemist one.','wound',
    [('5 × 5cm',''),('7.5 × 10cm',''),('10 × 20cm','')],
    [('Box of 50',2650),('Box of 100',4900)],
    [('Layer','Low adherent'),('Sterility','Individually sealed')]),
  P('Sterile gauze swabs','sterile-gauze-swabs','gauze','8 ply, individually sealed','For cleaning and for padding under a dressing. Individually sealed, so opening one does not commit the rest.','wound',
    [('5 × 5cm',''),('7.5 × 7.5cm',''),('10 × 10cm','')],
    [('Box of 100',1450),('Carton of 10 boxes',12900)],
    [('Ply','8'),('Sterility','EN 556')]),
  P('Fixation tape','fixation-tape','tape','Hypoallergenic, tears by hand','Holds a dressing without taking skin off on removal, and tears cleanly across so you are not hunting for scissors.','wound',
    [('2.5cm',''),('5cm',''),('7.5cm','')],
    [('Roll',690),('Box of 12 rolls',7200)],
    [('Backing','Non woven'),('Adhesive','Hypoallergenic')]),
  P('Conforming bandages','conforming-bandages','tape','Stretch, self adherent','Follows a limb rather than fighting it. Self adherent, so it holds without clips.','wound',
    [('5cm',''),('7.5cm',''),('10cm','')],
    [('Pack of 12',2190),('Carton of 6 packs',11400)],
    [('Stretch','Conforming'),('Fastening','Self adherent')]),
  P('Island dressings','island-dressings','dressings','Absorbent pad, adhesive border','Pad and border in one, for a wound that needs covering rather than packing. Waterproof options for showering.','wound',
    [('6 × 7cm',''),('10 × 8cm',''),('10 × 15cm','')],
    [('Box of 50',3290),('Box of 100',6100)],
    [('Border','Adhesive'),('Pad','Absorbent, low adherent')]),
  P('First aid kit, workplace','first-aid-kit-workplace','firstaid','Wall mounted, restockable','Compliant contents in a case you can actually restock line by line rather than replacing whole.','wound',
    [('1 to 25 people',''),('26 to 100 people','')],
    [('Each',8900),('Refill pack',3400)],
    [('Mounting','Wall bracket'),('Contents','Itemised list included')]),
 ]},
{
 'slug':'diagnostics', 'name':'Diagnostics', 'count':26, 'img':I['diagnostic'],
 'alt':'Test strips, safety lancets and a monitoring device',
 'intro':'The consult room and the kitchen bench, which increasingly want the same things. Safety lancets retract after firing so they cannot be used twice by accident, which is the whole point of them. They come in depths, and the right depth is the shallowest one that gives you enough blood, because going deeper than you need is just a sorer finger. Blood glucose test strips are matched to a meter and are not interchangeable between brands, so check the meter before the strips. Strips are also the line most often thrown away unused, because a pot opened and left is on a much shorter clock than the printed expiry. Urinalysis strips, thermometer probe covers and speculum covers in the sizes that fit what you already own. ECG electrodes and ultrasound gel for the rooms that need them. Everything here has a batch and an expiry printed on the carton, and both are shown on the product page before you buy rather than discovered when the box arrives. [Storing supplies correctly](/learn/storing-supplies) is what keeps those dates meaningful, and anything that has pierced skin goes to [sharps disposal](/learn/sharps-disposal-australia) rather than a bin.',
 'filters':[('all','Everything'),('lancets','Lancets'),('strips','Test strips'),('covers','Covers & consumables'),('ecg','ECG & ultrasound')],
 'products':[
  P('Safety lancets','safety-lancets','lancets','Single use, retracting','Fires once and retracts. It cannot be reused by accident, which is exactly what you want in a shared or domestic setting.','diag',
    [('28G, 1.8mm','Standard'),('30G, 1.5mm','Finer'),('21G, 2.2mm','Larger sample')],
    [('Box of 100',2290),('Box of 200',4200)],
    [('Mechanism','Retracting'),('Use','Single use')]),
  P('Blood glucose test strips','blood-glucose-test-strips','strips','Vial of 50, batch coded','Batch coded on the vial, which is the number your meter wants. Check compatibility before you order a carton.','diag',
    [('Vial of 50',''),('Vial of 100','')],
    [('Box of 2 vials',3900),('Carton of 10',17900)],
    [('Sample','0.5 microlitre'),('Storage','Room temperature')]),
  P('Thermometer probe covers','thermometer-probe-covers','covers','Universal, single use','Fits the common oral and tympanic probes. Cheap, and the thing that stops a thermometer being a vector.','diag',
    [('Universal oral',''),('Tympanic','')],
    [('Box of 100',890),('Carton of 20 boxes',15400)],
    [('Fit','Universal'),('Use','Single use')]),
  P('Vaginal speculum, disposable','vaginal-speculum-disposable','covers','Sterile, with light channel','Single use, with a channel for a light source. Sized small through large.','diag',
    [('Small',''),('Medium',''),('Large','')],
    [('Box of 25',4900),('Carton of 100',17900)],
    [('Sterility','Individually wrapped'),('Light','Channel compatible')]),
  P('ECG electrodes','ecg-electrodes','ecg','Wet gel, foam backed','Foam backed with a wet gel that has not dried out in the packet, which is the usual complaint with cheap electrodes.','diag',
    [('Adult',''),('Paediatric','')],
    [('Bag of 50',1890),('Carton of 600',19900)],
    [('Gel','Wet'),('Backing','Foam')]),
  P('Ultrasound gel','ultrasound-gel','ecg','Non staining, hypoallergenic','Does not stain the probe or the linen, which is the difference between a gel you buy once and one you buy again.','ecg' if False else 'diag',
    [('250mL bottle',''),('5L refill','')],
    [('Each',890),('Carton of 6',4600)],
    [('Type','Non sterile'),('pH','Neutral')]),
 ]},
{
 'slug':'clinic-disposal', 'name':'Clinic & disposal', 'count':17, 'img':I['sharps'],
 'alt':'A sharps container beside a roll of couch covering',
 'intro':'The lines that run out mid clinic and the ones a regulator asks about. Sharps containers to the Australian standard in the sizes that suit a bench, a wall bracket or a home bathroom cupboard. Used needles cannot go in kerbside waste anywhere in the country, and [the rules for a full container differ by state](/learn/sharps-disposal-australia). The standard is what makes a container a container: rigid walls, a lid that locks shut permanently, a biohazard mark and a fill line. A drink bottle has none of those and will not be accepted anywhere that takes sharps. Size it to how fast you fill it rather than to the shelf you want it on. A container that takes a year to fill has been open for a year. Wall mounts for the rooms where a bench container is a hazard in itself, and a bracket that takes the same body so you are not buying two systems. Couch roll, blueys and clinical waste bags in cartons rather than singles, because these are the wrong place to be lean. Surface wipes rated for clinical use rather than the supermarket equivalent. [What the numbers on a needle mean](/learn/needle-numbers-explained) if you are working out what is going into the container in the first place.',
 'filters':[('all','Everything'),('sharps','Sharps containers'),('couch','Couch roll & blueys'),('waste','Clinical waste')],
 'products':[
  P('Sharps container, bench','sharps-container-bench','sharps','AS 4031, one hand aperture','Sized for a bench or a bathroom cupboard. A one hand aperture, because the other hand is holding something sharp.','clinic',
    [('0.5L','Bag or cupboard'),('1.4L','Home or bench'),('2L','Busier bench')],
    [('Each',1250),('Carton of 12',12900)],
    [('Standard','AS 4031'),('Material','Puncture resistant polypropylene'),('Colour','Yellow'),('Closure','Temporary and final, with finger guard')]),
  P('Sharps container, wall mount','sharps-container-wall-mount','sharps','Bracketed, keyed final closure','One per treatment room, bracketed at the point of use. Carrying a sharp between rooms is how staff get injured.','clinic',
    [('5L',''),('10L',''),('20L','')],
    [('Each',2450),('Carton of 6',12900)],
    [('Standard','AS 4031'),('Mount','Bracket included')]),
  P('Couch roll','couch-roll','couch','Perforated, two ply','The line every practice manager says runs out first. Six rolls to a carton, and you will use them.','clinic',
    [('50cm',''),('60cm','')],
    [('Carton of 6',4250),('Pallet of 48',31900)],
    [('Ply','Two'),('Perforation','Sheet')]),
  P('Blueys, underpads','blueys-underpads','couch','Absorbent, waterproof backing','Protects the couch and the floor under it. Cheaper than the laundry and much cheaper than the upholstery.','clinic',
    [('60 × 90cm',''),('60 × 60cm','')],
    [('Box of 50',3890),('Carton of 4 boxes',13900)],
    [('Backing','Waterproof'),('Core','Fluff pulp')]),
  P('Clinical waste bags','clinical-waste-bags','waste','Yellow, printed to standard','Printed to the standard so the contractor takes them without an argument. Yellow for clinical, not general.','clinic',
    [('27L',''),('72L','')],
    [('Roll of 50',1890),('Carton of 10 rolls',16400)],
    [('Colour','Yellow, clinical'),('Print','To standard')]),
  P('Surface wipes, clinical','surface-wipes-clinical','waste','Alcohol free, tub of 200','Alcohol free, so they can go on the surfaces alcohol degrades. Contact time is on the tub and it is longer than people think.','clinic',
    [('Alcohol free','Most surfaces'),('70% alcohol','Fast dry')],
    [('Tub of 200',1590),('Carton of 6 tubs',8400)],
    [('Contact time','Printed on tub'),('Format','Canister')]),
 ]},
]


# --- the launch range -------------------------------------------------------
# Merged at the end so the categories above keep their original copy. See
# catalogue_extra.py for where these came from.
from catalogue_extra import EXTRA_PRODUCTS, EXTRA_CATEGORIES, EXTRA_FILTERS

_by = {c['slug']: c for c in CATEGORIES}
for _slug, _prods in EXTRA_PRODUCTS.items():
    _by[_slug]['products'].extend(_prods)
for _slug, _fs in EXTRA_FILTERS.items():
    _by[_slug]['filters'].extend(_fs)
for _c in EXTRA_CATEGORIES:
    _c['img'] = I[_c.pop('imgkey')]
    CATEGORIES.append(_c)
# The count a category advertises in the nav and on the shop index. It used to be
# a forward looking number against a placeholder catalogue. These are real
# products now, so it is the number of pages that exist.
for _c in CATEGORIES:
    _c['count'] = len(_c['products'])
TOTAL = sum(len(_c['products']) for _c in CATEGORIES)
