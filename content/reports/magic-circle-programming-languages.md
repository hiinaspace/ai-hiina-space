---
id: magic-circle-programming-languages
title: Magic circle programming languages
version: 1
published: 2026-10-27
updated: 2026-10-27
author: Hiina
produced-by: "Claude deep-research run with citation checking"
model: claude-opus-5-5
sources-through: 2026-10-26
status: current
takeaway: "A drawn magic circle can be an executable program if meaning lives in rings, angles and containment; prototype Widdershins, a counter-clockwise stack language where neatness lowers mana cost, first."
topics: [programming-languages, gesture-recognition, vr]
---

Can a programming language have a magic circle as its source code, drawn freehand in VR or photographed from ink on paper, and then executed? This report surveys the prior art (esoteric languages, Minecraft magic mods, gesture-casting games, fiction and medieval combinatorics), reviews what diagram recognisers and vision-language models can and cannot do in 2026, and proposes five circle languages, each with its own model of computation and its own answer to what "drawn well" should mean.

The motivating project is a VR spellcasting prototype that already recognises button-gated strokes and glyphs and computes per-stroke quality metrics; several recommendations below are framed as extensions of a prototype like that.

## 1. Summary

A programming language whose source is a magic circle is buildable, and the hard parts are smaller than they look: rings, angles, containment and vertex counts are cheap to recognise from strokes or a photo, while the things recognisers still get wrong (arbitrary line topology, tiny glyph detail) can be designed out of the notation. The closest prior art splits the problem in two. **Mystical** (Denis Moskowitz, 2025) draws PostScript as magic circles but has "no interpreter that will ingest a Mystical image" ([Mystical README](https://suberic.net/~dmm/projects/mystical/README.html)). The **2026 Witch Hat Atelier fan recognisers**, led by wha-spell-simulator, go the other way: they turn a freehand ring and sigil into a GlyphAST and a SpellIR and run it, with neatness setting duration, but they support one ring and one sigil and record nested rings as unsupported ([wha-spell-simulator](https://github.com/ytnrvdf/wha-spell-simulator)). Hex Casting and Psi prove players will program diegetically, Noita proves a spell list can be an interpreter, and VIPR (1990s) is the one serious language built from nested rings. What nobody has built is a compositional circle language you can draw freehand, or photograph, and execute, with drawing quality wired into the semantics in a principled way. The five designs below fill that gap with five different computational models. **Prototype Widdershins first**: it is a stack language read counter-clockwise around a ring, where neatness lowers mana cost and mana doubles as gas, and it reuses almost all of an existing VR stroke-and-glyph recogniser. The one-evening experiment is to fit a ring to the first closed stroke, place four $Q glyphs around it, and measure whether angular order is a reliable program order.

## 2. Every existing system solves one half of the problem

The prior art falls into families that each own a piece of the idea: notation without recognition, recognition without composition, diegetic programming without freehand input, and fiction with grammar but no machine. The table summarises the systems that matter most, sorted by how visual structure carries meaning.

| System | Input | What the visual structure means | Role of drawing quality | Source quality |
|---|---|---|---|---|
| Mystical (2025) | Generated from PostScript text | Rings = executable/data arrays, read CCW from 3:00; sigils = operators | None; output only | Primary README |
| wha-spell-simulator and kin (2026) | Freehand strokes on a canvas | One ring (open = prepared, closed = active), one element sigil, modifier signs by angle | Neatness sets duration (0.65 to 8.5 s); sigil size sets scale | Primary repo docs |
| VIPR (1990s) | Structured editor | Nested rings = sequence; sibling rings = alternatives; arrows = substitution | None | Secondary only |
| Rotary (2014) | ASCII text | Each closed ring of characters is a unit of control | None | Esolang wiki (secondary) |
| Piet (2001) | Bitmap | Hue/lightness change between colour blocks = opcode; block area = number | None; discrete cells | Esolang wiki (secondary) |
| Wierd (1997) | Text grid | Turn angle of a line = opcode | None | Esolang wiki (secondary) |
| Hex Casting (Minecraft) | Mouse snapped to hex lattice | Exact turn sequence = opcode key; slate track in spell circles = control flow | None; input is discretised | Primary source code |
| Psi (Minecraft) | 9x9 grid editor | Adjacency on parameter sides = data binding (dataflow DAG) | None | Primary source code |
| Noita wands | Slot list | Spell order = instruction stream with draw/call semantics | None | Fan wiki (secondary) |
| Magicka | Key presses | Element multiset with precedence and cancellation; Magicks are ordered sequences | None | Wikipedia, fan wiki (secondary) |
| SF6 motion inputs | Stick | Direction sequence within frame windows, with priority rules | Leniency windows | News report of community testing (secondary) |
| Arx Fatalis | Mouse gestures | Runes as morphemes (create/negate, improve/reduce) | Pass/fail | Wikipedia, retrospective (secondary) |
| War of Wizards (VR) | Controller drawing | Shape selects spell | Larger and more accurate = stronger | Store page (secondary) |
| Rithmatics (fiction) | Chalk | Line type = role; bindpoints = attachment geometry | Evenness, curvature, straightness = strength | Fan wiki (secondary) |
| Llull's Fourth Figure | Rotating paper discs | Disc rotation = letter combination | None | Stanford Encyclopedia |

### Mystical, VIPR and the ring notations

Mystical is the most direct ancestor. Its main ring "starts at the rightmost (3:00) point and flow continues widdershins", rings are read from the outside in, executable arrays `{}` are circles with a star and the alchemical "work complete" marker, non-executable arrays `[]` drop the star and use a triangle marker, dictionaries are double-bordered polygons, `/name` is drawn in a triangle, and most of the author's examples build variable sigils by "letter collision" after Spare's chaos magick ([Mystical README](https://suberic.net/~dmm/projects/mystical/README.html)). It is a pretty-printer: a human transcribes the drawing back to PostScript, and the author questions whether a ring per brace scales past operator-heavy languages like Forth. One fork, `cogerk/mystical_ps`, describes itself as "a python interpreter for mystical", but its README still carries the "no interpreter" line and what it interprets is unverified ([cogerk fork](https://github.com/cogerk/mystical_ps)). When Mystical circulated, MetaFilter commenters independently asked for exactly the two missing pieces, a ring-based input method and image recognition back to code ([MetaFilter](https://www.metafilter.com/208819/Mystical) (secondary)).

**VIPR** (Citrin, Doherty and Zorn) is the one academically published language built on nested rings. The accessible descriptions agree that programs are "nested series of concentric rings", that "each step in a computation involves merging two rings in the presence of a state object", that an arrow means substitution (when execution reaches a ring with an outgoing arrow, that ring is replaced by the arrow's target, which gives loops, calls and returns from one mechanism), and that every function has a mandatory continuation parameter drawn as a small tangent circle ([Berkeley survey CSD-04-1368](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2004/Archive/CSD-04-1368.pdf) (secondary); [Bremen lecture slides](https://www.informatik.uni-bremen.de/agbkb/lehre/ss04/VS/Material/vipr.sxi.pdf) (secondary); [Berger thesis](https://www.en.pms.ifi.lmu.de/publications/diplomarbeiten/Sacha.Berger/THESIS/HTML-view/part2.html) (secondary)). Sibling rings at one level are alternatives with no order among them. None of the original papers (VL'94, JVLC 1997 and 1998) could be retrieved, so the guard notation and data representation are unknown. **VIPR is the only rewriting-based ring language found, and Covenant below borrows its spirit.**

Other ring notations are thinner. Rotary arranges Brainfuck-like characters in closed ASCII rings, the instruction pointer runs clockwise from an `x`, and ring-pointer instructions choose which ring runs next ([Esolangs: Rotary](https://esolangs.org/wiki/Rotary) (secondary)). Circular Gallifreyan (Loren Sherman, 2011) writes English transliteration as word circles read counter-clockwise from the bottom, with sentences as enclosing circles and numbers as concentric rings where each line adds 1 and each circle adds 5 ([Sherman's guide](https://shermansplanet.com/gallifreyan/guide.pdf)); dozens of text-to-image generators exist but no image-to-text recogniser was found, probably because the same word can be legally drawn many ways. The Japanese Magical Circle Engine is a text language that emits circle drawings, not a recogniser ([Scrapbox villagepump](https://scrapbox.io/villagepump/%E9%AD%94%E6%B3%95%E9%99%A3%E8%A8%80%E8%AA%9E) (secondary)). Procedural magic-circle generators on GitHub (danielstern/MagicCircles, areinhold17/MagicCirclePreview) are decorative and do not encode data ([MagicCircles](https://github.com/danielstern/MagicCircles)). Circular machine-readable codes show the encoding side is solved for short keys: ShotCode reads bits by angle and distance from a bullseye and stores a 40-bit lookup number ([Wikipedia: ShotCode](https://en.wikipedia.org/wiki/ShotCode) (secondary)), and a third-party reverse-engineering of Spotify Codes reports 23 bars at 3 bits per data bar decoding to 45 bits (37 for a media key, 8 checksum), while noting only that a *patent* suggests a convolutional code and that it cannot explain the 60-to-45-bit step ([levelup blog](https://levelup.gitconnected.com/spotify-codes-and-how-they-work-664f4e4b8489) (secondary)).

### Graphical esolangs encode meaning in discrete geometry

The 2D esolangs supply design axes rather than a template, and all of them read exact cells, not noisy drawings. **Piet** keys its 17 commands on the *change* in hue and lightness between colour blocks, so a global colour shift preserves meaning, and pushes numbers as the codel count of the previous block, so size is a number ([Esolangs: Piet](https://esolangs.org/wiki/Piet) (secondary; the 2001 date is a wiki category tag)). **Wierd** (Pressey, Olmstead and Colagioia, 1997) is the closest in spirit to a drawn sigil: lines of non-whitespace where the turn angle selects the instruction ([Esolangs: Wierd](https://esolangs.org/wiki/Wierd) (secondary)). **Hexagony** (Martin Ender, 2015 per wiki tag) uses a hexagonal source with instruction pointers at the corners and corner exits that branch on the sign of memory ([Esolangs: Hexagony](https://esolangs.org/wiki/Hexagony) (secondary)). **Aheui** packs opcode, direction and operand into the three slots of a Hangul syllable, a working model of a composite rune ([Esolangs: Aheui](https://esolangs.org/wiki/Aheui) (secondary)). Funge-98's default of reflecting the instruction pointer on an unknown instruction is an elegant fail-safe for a misdrawn glyph ([Funge-98 spec](https://github.com/catseye/Funge-98/blob/master/doc/funge98.markdown)). Beyond esolangs, Bret Victor's Alligator Eggs shows a rewrite calculus played as a game with colour as binding ([Alligator Eggs](https://worrydream.com/AlligatorEggs)), and Tromp's lambda diagrams draw lambda terms as lines ([Tromp](https://tromp.github.io/cl/diagrams.html)).

### Hex Casting and Psi bracket diegetic programming

**Hex Casting** is a real stack machine dressed as magic, and its source code shows how little of its visual form carries meaning. A pattern is a start direction plus a list of relative turns on a hex lattice; the lookup key is the turn list alone, compared by exact hash, so rotation is free but stroke order and handedness are identity ([HexPattern.kt](https://raw.githubusercontent.com/gamma-delta/HexMod/main/Common/src/main/java/at/petrak/hexcasting/api/casting/math/HexPattern.kt); [PatternRegistryManifest.java](https://raw.githubusercontent.com/gamma-delta/HexMod/main/Common/src/main/java/at/petrak/hexcasting/common/casting/PatternRegistryManifest.java)). Drawn paths cannot reuse a lattice edge or backtrack. A deprecated (since 0.11.4) overload has a flag for checking alternate stroke orders that simply throws "NYI"; the live mechanism is the exact key plus per-world "Great Spells", whose accepted drawing is an Euler-path re-drawing scrambled from the world seed so the shape is public but the stroke order is secret ([ScrungledPatternsSave.java](https://raw.githubusercontent.com/gamma-delta/HexMod/main/Common/src/main/java/at/petrak/hexcasting/server/ScrungledPatternsSave.java)). Length loosely tracks power: Greater Teleport is a 31-turn signature, Flay Mind 29, Ignite 8 ([HexActions.java](https://raw.githubusercontent.com/gamma-delta/HexMod/main/Common/src/main/java/at/petrak/hexcasting/common/lib/hex/HexActions.java)). Only two families parse shape algorithmically: Numerical Reflection, a shift-and-add accumulator where forward adds 1, left adds 5, right adds 10, sharp left doubles and sharp right halves (the book admits "Irritatingly, there is no easy way to draw numbers"), and Bookkeeper's Gambit, where flat segments keep a stack item and dips drop it ([SpecialHandlerNumberLiteral.kt](https://raw.githubusercontent.com/gamma-delta/HexMod/main/Common/src/main/java/at/petrak/hexcasting/common/casting/actions/math/SpecialHandlerNumberLiteral.kt)).

What Hex gets right is the theatre around execution. Mishaps are typed exceptions with colours and thematic penalties: Invalid Pattern is yellow and pushes Garbage, Not Enough Iotas pads with Garbage, Mathematical Error costs vigor, and the Garbage iota lets a broken spell limp on with poisoned data ([lang file](https://raw.githubusercontent.com/gamma-delta/HexMod/main/Common/src/main/resources/assets/hexcasting/lang/en_us.flatten.json5)). Costs come out of amethyst "media", and you can overcast from your own health. In 0.11.x the source shows a default op budget of 100,000, a default spell-circle length of 1024, and a mishap when the stack is too large to serialise, all server-configurable ([HexConfig.java](https://raw.githubusercontent.com/gamma-delta/HexMod/main/Common/src/main/java/at/petrak/hexcasting/api/mod/HexConfig.java); [CastingVM.kt](https://raw.githubusercontent.com/gamma-delta/HexMod/main/Common/src/main/java/at/petrak/hexcasting/api/casting/eval/vm/CastingVM.kt)); the often-quoted 1024-iota stack and 512 meta-eval limits come from a 2023 FAQ for 0.10.x ([forum FAQ](https://forum.petra-k.at/viewtopic.php?p=130) (secondary)). The current release is 0.11.4 for Minecraft 1.20.1, from late August 2026 ([CHANGELOG](https://raw.githubusercontent.com/gamma-delta/HexMod/main/CHANGELOG.md)). The community treats it as a language: a Conway's Game of Life spell circle that "uses no addon functionality", though its author recommends an addon or a permanently powered directrix to stop it freezing ([forum](https://forum.petra-k.at/viewtopic.php?p=401) (secondary)); a compiler *design* with closures, a Z combinator and call/cc via Iris' Gambit ([s5bug gist](https://gist.github.com/s5bug/5f453c9c159fb77bad9dff1a8954fb3b) (secondary)); HexParse, which compiles text to pattern iotas ([ModDex](https://moddex.gg/mod/hexparse) (secondary)); and HexDebug, a Debug Adapter Protocol server for stepping through hexes in VS Code ([Modrinth: HexDebug](https://modrinth.com/mod/hexdebug), the mod's own page). The VS Code extension's author refused to support importing hexes without drawing them ([forum](https://forum.petra-k.at/viewtopic.php?p=52) (secondary)), while HexParse does exactly that. **That split shows drawing being treated as an I/O bottleneck for big programs and as the point of the game for small ones**, a tension any circle language inherits.

**Psi** (Vazkii), which Hex cites as its inspiration, is the opposite case: layout carries the binding. Pieces on a 9x9 grid read their parameters from specific adjacent sides, connectors redirect, and the compiler walks back from side-effecting "tricks" to build a dependency-ordered action list, rejecting cycles with INFINITE_LOOP ([SpellCompiler.java](https://raw.githubusercontent.com/VazkiiMods/Psi/master/Xplat/src/main/java/vazkii/psi/common/spell/SpellCompiler.java)). Each piece evaluates at most once per cast (four Debug tricks print the same random number), tricks run row by row from the top and left to right within a row (the in-game book's summary page words this the other way round), and spell cost is computed at compile time from number constants ([Psi lang file](https://raw.githubusercontent.com/VazkiiMods/Psi/master/Xplat/src/main/resources/assets/psi/lang/en_us.json)). Psi's layout is semantic, but it looks like a circuit board. The other magic mods are recipe matching. Ars Nouveau's grammar is one Form first, Effects in order, and Augments modifying the glyph to their left ([ars.guide](https://ars.guide/book/getting_started/introduction_to_glyphs/)), with a third-party guide giving 10 glyphs per spell and summed mana costs ([minecraft-guides](https://www.minecraft-guides.com/mod/ars-nouveau/wiki/spell-builder/) (secondary)); Occultism rituals match a chalk layout exactly and report the specific error ([siriusmc guide](https://wiki.siriusmc.net/books/modpack-guides-and-tutorials/page/occultism-rituals-atm10) (secondary)).

### Noita, Magicka and fighting games supply evaluation models

**Noita's wand is a depth-first card interpreter.** The fan wiki's Expert Guide frames it as deck, hand and discard piles, where modifiers draw one card, multicasts draw several, each spell draws its children before its siblings, and spells never modify each other: they all mutate a shared "shot state", while each trigger opens a child shot state for its payload ([Expert Guide: Draw](https://noita.wiki.gg/wiki/Expert_Guide:_Draw) (secondary)). Greek-letter spells are calls with a recursion limit of 2 ("Tau, Tau, Spark Bolt" yields three Spark Bolts because the second Tau cannot call Tau) ([Calling and Recursion](https://noita.wiki.gg/wiki/Expert_Guide:_Calling_and_Recursion) (secondary)). Divide By spells copy the next spell and are explicitly *not* recursive, so that limit does not bound them; the wiki's 800-copy figure comes from Tau copying a 10x10x4x2 Divide chain, and it mentions an "iteration limit" whose value nobody here read ([Divide By](https://noita.wiki.gg/wiki/Divide_By) (secondary)). Trigger loops can run away and crash the game ([Trigger Loop](https://noita.wiki.gg/wiki/Trigger_Loop) (secondary)), and the community built a Wand Simulator that draws the evaluation tree because nobody can hold it in their head ([Wand Simulator](https://noita.wiki.gg/wiki/Tool:_Noita_Wand_Simulator) (secondary)). Those two facts, bounded resources and visible evaluation, recur in every design below.

**Magicka is a multiset grammar.** Up to five of eight base elements (plus steam and ice) are queued, element order does not change an ordinary spell, a precedence hierarchy (shields, projectiles, beams, steam, lightning, sprays) picks the spell type, and there is no mana bar ([Wikipedia: Magicka](https://en.wikipedia.org/wiki/Magicka) (secondary)). Opposing pairs (water and lightning, lightning and earth, life and arcane, cold and fire) cancel ([Magicka wiki: Elements](https://magicka.fandom.com/wiki/Elements) (secondary)). Magicks are the ordered exceptions, fixed sequences like Haste and Teleport, and only Portal accepts two orderings ([Magicka wiki: Magicks](https://magicka.fandom.com/wiki/Magicks_(Magicka_1)) (secondary)). The Arrowhead postmortem says elements were meant to "give meaning to each spell, and vary its efficiency" instead of draining a mana bar ([Game Developer](https://gamedeveloper.com/business/postmortem-arrowhead-game-studios-i-magicka-i-) (secondary)). Athanor below keeps the multiset and the oppositions but invents its own reaction table.

Fighting games are the precedent for accepting imprecise input deterministically. A hobbyist implementation write-up stores directions in a buffer, inserts neutral, flips for facing, and matches *backwards* from the button press with a per-step frame window and a strict or fuzzy flag ([critpoints.net](https://critpoints.net/2025/02/05/how-to-code-fighting-game-motion-inputs/) (secondary)). Community testing of Street Fighter 6 by Loic "WydD" Petit, reported by EventHubs, found an 11-frame quarter-circle buffer, half-circle windows widened from 8 to 12 frames and 360s from 25 to 32 compared with SF5, input polled three times per frame, and priority rules (Overdrive specials over everything, 360 over quarter-circle) that cause unintended moves when inputs share prefixes ([EventHubs](https://www.eventhubs.com/news/2023/jun/17/sf6-input-trouble-breakdown) (secondary; not Capcom data)). **Ambiguity resolution, not tolerance, becomes the dominant failure once many inputs share prefixes**, which argues for glyph sets with distinct primitives.

### Drawing-as-casting games mostly gate on shape and scale on size

Gesture-casting games mostly recognise a shape and then pass or fail it. Arx Fatalis runes "must be correctly drawn in order to successfully cast a spell" ([Wikipedia: Arx Fatalis](https://en.wikipedia.org/wiki/Arx_Fatalis) (secondary)); a retrospective describes them as morphemes, where a left-to-right line means "create" and its flip "negate", bottom-up means "improve" and its inversion "reduce", across about 20 runes and nearly 50 spells ([Super Jump](https://superjumpmagazine.com/arx-fatalis-magic-was-ahead-of-its-time-and-technology) (secondary)). That is the closest shipped example of compositional shape semantics. Okami's Celestial Brush drew recurring reviewer complaints about recognition ([Wikipedia: Okami](https://en.wikipedia.org/wiki/%C5%8Ckami) (secondary)), and Castlevania: Dawn of Sorrow's Magic Seals, a pattern of connected points on a circle copied within a time limit, drew complaints about stylus ergonomics and pacing ([Wikipedia: Dawn of Sorrow](https://en.wikipedia.org/wiki/Castlevania:_Dawn_of_Sorrow) (secondary)). The Magus Circle released on 24 September 2026 with the line "Even the most crudely drawn sigils still hold magic within" and options to slow or freeze time while drawing ([Steam](https://store.steampowered.com/app/2796640/The_Magus_Circle/) (store page, secondary)); nothing was verified about how accuracy affects spells.

A few games do scale effect by quality. **War of Wizards** (Arcane Miracle Entertainment, VR, released 21 September 2022) says on its store page, rechecked for this report: "The bigger and more accurate you draw them, the stronger they are!" and "their power is fully determined by how you draw them" ([Steam: War of Wizards](https://store.steampowered.com/app/2009460/War_of_Wizards/) (store page, secondary; it states the developer's claim, not measured behaviour, and does not describe the scorer)). Lost Magic (DS, 2006) rewards accurate drawing with more powerful spells according to Wikipedia ([Wikipedia: Lost Magic](https://en.wikipedia.org/wiki/Lost_Magic) (secondary)), or with critical hits according to a review ([Game Revolution](https://www.gamerevolution.com/review/37102-lostmagic-review) (secondary)); the sources disagree on mechanism. An itch.io prototype, Skill & Spell, grades precision into damage multipliers of x1, x1.25 and x1.5 ([devlog](https://totallynotdevs.itch.io/skill-and-spell/devlog/1676576/first-playable-prototype-drawing-runes-and-dueling-the-dummy)), and a mobile game scaled damage with circle size ([4Gamer](https://www.4gamer.net/games/335/G033541/) (secondary)). Against this sits Edward McNeill's IRONSTRIKE write-up: rune tracing in fast VR combat missed lines "by fractions of an inch", frustration did not drop with experience, and loosening it made flailing optimal, so the game switched to crossing line segments ([Game Developer](https://gamedeveloper.com/design/conjuring-a-gestural-spellcasting-system-for-vr)). Wizard of Wii (FDG 2011) found real recognition accuracy of 69 to 79% across two sessions, far below lab figures, and that players disliked similar-looking circular gestures ([Cheema and LaViola](https://www.eecs.ucf.edu/~jjl/pubs/p265-cheema.pdf)). **The pattern across shipped games is identity from shape, magnitude from size or accuracy, and precision graded rather than gated.**

### Fiction and history already wrote the grammars

Two fictional systems are close to specifications. In Sanderson's Rithmatics, a Line of Warding's strength depends on "its evenness and its curvature", larger circles are weaker, a typical Line of Warding "can take about 6 hits from a Line of Vigor", Forbiddance strength depends on straightness with thickness setting its height (about 10 hits, about four seconds to dismiss), Vigor is a sine wave that must complete two intervals, Making strength depends on "complexity and aesthetic beauty", and bindpoints (2 on an ellipse, 6 from an inscribed hexagon, 9 from a non-obtuse triangle) are where other structures attach ([Coppermind: Rithmatics](https://coppermind.net/wiki/Rithmatics) (secondary)). In Witch Hat Atelier, "a spell will only activate if its ring is complete", a gap lets a spell be prepared and finished later, the central sigil sets the element (earth, air, water, fire, light), signs around it set the form in radial or bilateral symmetry, a flipped sign produces the opposite effect, linking and nesting combine spells, and **size sets power while neatness sets durability**, two separate axes ([WHA Fandom: Magic](https://witch-hat-atelier.fandom.com/wiki/Magic) (secondary)). Fullmetal Alchemist's circle as a conduit with triangle runes ([FMA Fandom](https://fma.fandom.com/wiki/Alchemy) (secondary)) offers less grammar. Mahouka's CAD stores "digitalised magic circle blueprints" with fixed variables, and the target and strength are filled in later ([Mahouka Fandom](https://mahouka-koukou-no-rettousei.fandom.com/wiki/Magic_Sequence) (secondary)); reading that as a compile-time/run-time split with partial application is an analogy, not the source's claim. Ars Magica's five Techniques by ten Forms is the cleanest published verb-by-noun spell grammar ([Ars Magica Wiki](https://arsmagica.fandom.com/wiki/Hermetic_Arts) (secondary)).

Historical devices offer real machinery. Llull's alphabet is nine letters, B C D E F G H I K, and his Fourth Figure is three concentric circles that "must be rotated to form the different combinations", stepping BCB to CCB to BDB ([Stanford Encyclopedia: Llull](https://plato.stanford.edu/entries/llull/)). A German lecture handout gives 9^3 = 729 combinations for the Ars as a whole, not for one disc ([Bremen handout](https://www.compart.uni-bremen.de/content/4-teaching/0-summer-2019/2-theorie-und-geschichte-des-berechenbaren/3-material/berechenbar19-04lull.pdf) (secondary)), and the view of the Ars as "a precursor to computer science" is scholarly opinion reported by Wikipedia, not something the Stanford entry discusses ([Wikipedia: Ars Magna](https://en.wikipedia.org/wiki/Ars_Magna_(Ramon_Llull)) (secondary)). Kamea sigils are an encoding algorithm: map a name's letters to numbers, find them on a planetary magic square, and join cell centres with lines, with loops for repeats and a bar at the end; a practitioner notes these are, "as far as we know, first documented in Agrippa", who applies them inconsistently ([David Rankine](https://www.davidrankine.com/post/agrippa-and-the-magic-squares) (secondary)). Spare's method deduplicates the letters of a written desire ("IDESRTHNGOFMY") and merges them into a monogram ([sacred-texts TOPY page](https://sacred-texts.com/eso/topy/black3.htm) (secondary)); he rejected the medieval view of spirits as external beings ([Wikipedia: Sigil](https://en.wikipedia.org/wiki/Sigil) (secondary)). Puzzle games round this out: Baba Is You makes rules out of aligned tiles, The Witness teaches a drawn-path grammar without text, and Cultist Simulator makes combinations discoverable by experiment ([Wikipedia: Baba Is You](https://en.wikipedia.org/wiki/Baba_Is_You); [Wikipedia: The Witness](https://en.wikipedia.org/wiki/The_Witness_(2016_video_game)); [Wikipedia: Cultist Simulator](https://en.wikipedia.org/wiki/Cultist_Simulator) (all secondary)). Magic: The Gathering is Turing complete under forced play ([Churchill, Biderman and Herrick, FUN 2021](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.FUN.2021.9)).

### The 2026 Witch Hat Atelier recognisers are the nearest working pipeline

The closest thing to the full idea appeared in May 2026. **wha-spell-simulator** (ytnrvdf, MIT) "turns a freehand spell diagram into parser output, compiled spell behavior, and animated canvas effects", and it is self-described as "an experimental prototype" ([README](https://raw.githubusercontent.com/ytnrvdf/wha-spell-simulator/main/README.md)). I rechecked its docs for this report. Its GlyphAST records the ring's completeness, roundness and a "combined ring quality score" called neatness, plus global neatness, radial symmetry and instability, and it lists `unsupportedNestedRings` as "detected inner rings that are not compiled" ([glyph-ast.md](https://raw.githubusercontent.com/ytnrvdf/wha-spell-simulator/main/docs/glyph-ast.md)). Its SpellIR derives duration "mostly from glyph quality and neatness", clamped to 0.65 to 8.5 seconds, and rejects multiple rings or multiple sigils as invalid with no fallback to another element ([spell-ir.md](https://raw.githubusercontent.com/ytnrvdf/wha-spell-simulator/main/docs/spell-ir.md)). An earlier API read showed around 900 GitHub stars; I could not recheck that figure. Relatives include a Rust port running on a reMarkable 2 ([aetherquill](https://github.com/rajyyug1132/aetherquill)), a Unity version classifying stroke groups with a Teachable Machine model ([Pancu](https://github.com/Pancu/Witch-Hat-Atelier-Spell-Recognition-Unity)), and a template-based one that sums sign strokes as force vectors and emits misfire warnings ([YatoVoid](https://github.com/YatoVoid/witch-atelier)). All of them are fixed-vocabulary spell systems with strokes as input. None handles nesting, sequencing or control flow, none reads photographs, and none runs in VR. A VR spellcasting prototype that already recognises strokes and glyphs sits in that last niche.

## 3. Recognition in 2026: geometry is cheap, topology is hard, VLMs judge badly

Per-stroke quality metrics (circle-fit residuals, closure gaps, template distances) were worked out in earlier prototyping, so this section covers only what sits above them: whole-diagram structure, calibration, and where models fail.

**Structure-level accuracy lags symbol-level accuracy everywhere.** Arrow R-CNN, which adds an arrow head-and-tail keypoint head to Faster R-CNN, raised whole-diagram recognition on a scanned flowchart dataset from 37.7% to 78.6% and recognised more than 68% of diagrams across four datasets combined, while symbol recall on FC_A reached 98.3%, in under 100 ms per diagram ([Springer](https://link.springer.com/article/10.1007/s10032-020-00361-1)). Its weak point is arrows: overlapping arrow boxes confuse head attribution. A 2025 pipeline that feeds a fine-tuned detector's graph to GPT-4o reports arrow-related detection mAP of 0.235 against 0.653 for other classes ([arXiv 2505.07864](https://arxiv.org/html/2505.07864v1)). In handwritten maths, a structural recogniser reaches 80.52, 83.63 and 74.14% expression rate on CROHME 2016, 2019 and 2023 with generated annotations, and 56.29, 54.63 and 52.82% without them ([arXiv 2508.19773](https://arxiv.org/pdf/2508.19773)). DECIMER, trained only on up to 152 million synthetic renders, reads 73.25% of 5,088 real hand-drawn molecules exactly, where earlier tools score 0.57 to 26.98%, and quadrupling the synthetic set from 38 million added under 3 points ([PMC11227129](https://pmc.ncbi.nlm.nih.gov/articles/PMC11227129)). **A fixed grammar plus synthetic renders with jitter is the transferable recipe**, and in a circle language the quality model doubles as the augmentation model.

**LADDER is the closest precedent for a declarative circle grammar.** Hammond and Davis describe shapes hierarchically from primitives (line, arc, ellipse, spiral and others) under a long predefined constraint list, about 44 named constraints across two lists with no stated total, plus draw order, rotation invariance and a beautifier that moves points as little as possible to satisfy constraints ([LADDER](https://groups.csail.mit.edu/mug/pubs/Hammond2005Ladder.pdf)). Its soft constraints were never implemented and it reports no accuracy figures. Turning each constraint into a normalised residual gives a quality score straight out of parsing, and the beautifier's total displacement is a second, calibratable precision signal.

**Vision-language models fail exactly where circles need them.** On FlowLearn's simulated flowcharts, 2024-era models counted nodes correctly 0.52 (Claude-3-Opus) and 0.58 (GPT-4V) of the time on a 100-sample subset, and in Mermaid generation Claude-3-Opus reached node F1 of about 0.94 but link F1 of only 0.30 ([FlowLearn](https://arxiv.org/html/2407.05183v2)). On SketchJudge, which asks 16 multimodal models to diagnose errors in 1,015 hand-drawn student diagrams, the best (GPT-5) scored 78.42% accuracy against 83.33% for three non-expert human raters on a 160-answer subset, a gap of about five points, with error-type F1 of 61.13 against 66.42 ([SketchJudge](https://arxiv.org/html/2601.06944)). The Visual Aesthetic Benchmark found the best of 20 frontier models identified both the best and worst image in only 26.5% of tasks against 68.9% for experts, and that scalar scores agree poorly with direct comparisons; its domain is fine art, photography and illustration, not drawings ([arXiv 2605.12684](https://arxiv.org/abs/2605.12684)). No study found for this report calibrates a VLM on drawing neatness. **Counting, link topology and judging neatness are three things a magic circle needs and three things VLMs do worst**, and their latency rules them out of a VR loop anyway.

**Calibrate quality with pairwise human judgments, and grade rather than gate.** The aesthetic benchmark's finding that ranking beats scoring, and the CHAED precedent of regressing hand-designed geometric features on 33 raters' handwriting scores ([IJCAI 2015](https://www.ijcai.org/Abstract/15/356)), both point to fitting existing geometric residuals to "which of these two is neater?" judgments. For converting a continuous error into tiers, osu! shrinks nested judgement windows linearly with difficulty (300 = 80 − 6·OD ms) and weights tiers non-uniformly at 100%, 33.33% and 16.67% ([osu! wiki](https://osu.ppy.sh/wiki/en/Gameplay/Judgement/osu%21)). Ido's kanji auto-scorer keeps stroke order, stroke count and shape deductions separate and stores penalty tables as data ([JSiSE 2019](https://www.jsise.org/taikai/2019/program/contents/pdf/F5-1.pdf)). For VR, the evidence is thin: a Würzburg project call notes that arm ergonomics curve intended-straight mid-air strokes ([Würzburg HCI](https://hci.uni-wuerzburg.de/topics/20250722-sketch-stroke-correction/)), and no controller noise or latency-tolerance numbers were found, so per-device and per-player baselines must be measured. Accessibility is a design input, not an afterthought: a 2022 adaptation of the VR game Spellcasters let clinicians customise gestures per stroke-rehabilitation patient ([eScholarship](https://escholarship.org/uc/item/0nf117zh)).

## 4. Five designs, five computational models

The design pass worked from five principles. Meaning goes in what classic geometry measures well (ring radii and concentricity, angles around a centre, containment, vertex counts) and stays out of arbitrary line topology and fine detail inside small glyphs. Identity and magnitude are separate channels: shape picks the operator, and quality, size or count sets how much, with precision graded and never a gate, except deliberately in Athanor. Evaluation is visible and errors are typed and theatrical, as in the Wand Simulator, HexDebug and Hex mishaps. Everything is bounded by a resource the player can see. And each language gets one central idea and its own model of computation. None of these designs has been built or tested; parameter values marked "(guess)" are ones the design pass itself flagged as guesses, and the foundational references it names (Joy, Lafont, Mazza, Lamping, Faust, Mackworth, Păun, Guo et al.) were cited from the design pass's own knowledge rather than fetched for this report.

### Shared machinery: the quality score q

Three designs consume a per-element quality q in [0, 1], defined once. For a ring, the features are RMS radial deviation over R, closure gap over 2πR, out-of-plane RMS over R (VR only), and the high-band elliptic Fourier energy fraction (wobble). For a glyph, they are the $Q distance to the matched template, the Procrustes residual after similarity alignment, the high-band EFD fraction, and DTW cost per point where stroke order matters. For placement, they are angular-spacing error against the intended symmetry and radial deviation from the band centre.

Each residual r_j is divided by a baseline b_j = b_dev,j^(1−λ) · b_player,j^λ, where b_dev is the device noise floor (controller jitter at arm's length measured once per headset, or scan resolution for a photo) and b_player is the player's median residual on five calibration circles and five lines drawn at setup. At λ = 0 the score is absolute and rewards skill; at λ = 1 it is fully relative, so a player with a tremor and a calligrapher both land mid-scale on a typical effort. **λ is a difficulty setting and the most important accessibility knob.** Aggregate as s = Σ_j w_j log(1 + r_j / b_j) and q = σ(α − s). Fit w by Bradley–Terry logistic regression on pairwise neatness judgments, choose α so the median casual drawing scores 0.5, and validate with Spearman correlation on held-out pairs; a few hundred pairs per glyph family should suffice for a hobby game (guess).

Where semantics consumes q, use the floored q' = q_floor + (1 − q_floor) q so anything recognisable works. A "steady" assist drops the wobble terms (high-band EFD and out-of-plane residuals), which helps tremor without excusing wrong shapes. A "snap" assist beautifies with LADDER-style least-displacement constraint solving and fixes q at a set value. Do not ask a VLM for q.

The parsing toolkit has two branches. In VR, the existing prototype's stack applies: button-gated strokes, a PCA plane fit to the first ring stroke with later strokes projected onto it (their out-of-plane residual kept as a quality term), a circle fit (Kåsa or Taubin initialisation, then geometric refinement), PaleoSketch-style primitive classification, and $Q for glyphs. For images: rectify by fitting an ellipse to the outer ring and mapping it to a circle (fine for near-frontal photos; steep angles need four printed corner fiducials), adaptive threshold, skeletonise, RANSAC or Hough for circles, Douglas–Peucker for polygons, and a small CNN for glyph crops trained on jittered synthetic renders in the DECIMER manner. VLMs serve only as explainers or fallback glyph labellers.

## 5. Widdershins: a stack language where neatness is mana

A spell is a ring of freehand glyphs read counter-clockwise from a keystone. Small rings tangent to the main ring are quotations, and leaving a ring open defers it. The program is an ordinary concatenative stack language in the line of Joy and Hex Casting, so its semantics is deterministic. **Drawing quality only changes what the spell costs**: neat glyphs are efficient, sloppy ones burn more mana, and because mana is also gas, every spell terminates. Widdershins is the VR design and casts through the existing VR stroke pipeline almost unchanged.

| Visual element | Meaning |
|---|---|
| Main ring, closed | Program; runs when the cast button is released |
| Main ring with a gap | Prepared spell: compiled and stored on the wand; a later stroke across the gap fires it |
| Keystone (a small ▸ wedge on the ring) | Program start; reading proceeds counter-clockwise (widdershins) from here |
| Glyph in the ring band, at angle θ | One operator; program order is angular order θ, not draw order |
| Sub-ring tangent to the band, with a gap | Quotation `[ … ]` pushed as a value; contents read CCW from the tangent point |
| Sub-ring tangent to the band, closed | `( … )`: quotation executed inline |
| Dot / bar / n-gon (3 ≤ n ≤ 6) / empty small circle | Numerals 1 / 2 / n / 0 |
| Glyph quality q | Efficiency of that token's mana cost |
| Main-ring quality q_R | Global efficiency multiplier (a "leaky" ring wastes everything) |

**Model and evaluation.** Values are numbers, vectors, entities, quotations and garbage. A program is the token sequence t₁…tₙ sorted by angle from the keystone, with each sub-ring parsed recursively. Operators include `target` (an eye glyph; pushes the entity under your gaze), `gaze` (an arrow; pushes your unit look vector), `+` (a cross), `×` (a saltire), `dup` (a fork), `drop` (a slash), `swap` (an hourglass), `impel` (a chevron; E v → E, pushes E along v), `ignite` (a zigzag; E → E), `i` (a spiral; executes the quotation on top), `times` (a lemniscate; n [Q] → runs Q n times) and `if` (a Y; b [T] [F]). Effects deliberately leave their target on the stack.

Execution is Joy-style left to right over the angular sequence. Each executed token t costs k(t, args) / η_t, where η_t = q'_t · q'_R, paid from the caster's pool M. An unrecognised glyph, a stack underflow or a type error pushes `garbage`, and an effect applied to garbage does nothing but still costs, which is Hex's limp-on approach. Every token costs at least k_min > 0, so a run executes at most M / k_min tokens and the language is total. Hex enforces a similar bound with a separate op counter; here the bound is the mana the player already sees. Loop bodies are charged per iteration at their own glyphs' η, so a sloppy glyph inside a loop is paid for every time round, which rewards neat loop bodies without an extra rule. Because program order is angular while draw order only groups strokes into glyphs, **a caster can insert a token by drawing it between two existing ones**, a real editing gesture.

**Worked example: "triple gust"** flings whatever you are looking at along your gaze, three times. Draw one closed main ring with the keystone at 3 o'clock and five tokens counter-clockwise at roughly 72° steps: an eye (`target`) at 0°, a triangle (`3`) at 72°, an open tangent sub-ring holding an arrow then a chevron (`[gaze impel]`) at 144°, a lemniscate (`times`) at 216°, and a slash (`drop`) at 288°.

```
                  Δ
          .-""""""""""-.
     C   /              \
         |              | ▸◉
         |      ·       |
     ∞   \              /
          '-.________.-'
                    /
   ◉ target (keystone)   Δ 3   C open sub-ring [→ ›]   ∞ times   / drop
```

Text form: `target 3 [gaze impel] times drop`. The trace uses pool M = 50, q_floor = 0.25 (example value), ring quality q_R = 0.9 (so q'_R = 0.925), and nominal costs target 1, numeral 0.5, quote 0.5, gaze 0.5, impel 4·|v|, times 1, drop 0.2 (example values).

| Step | Token (q) | Stack after | Cost |
|---|---|---|---|
| 1 | target (0.8) | E | 1/(0.85·0.925) = 1.27 |
| 2 | 3 (0.9) | E 3 | 0.58 |
| 3 | open sub-ring (0.7) | E 3 Q | 0.70 |
| 4 | times (0.5) pops 3, Q | E | 1.73 |
| 4a–c | gaze (0.8) ×3 | E v → … | 3 × 0.64 = 1.91 |
| 4a–c | impel (0.6) ×3, \|v\| = 1 | E | 3 × 6.18 = 18.53 |
| 5 | drop (0.9) | (empty) | 0.23 |

The total is about 24.96 of 50. Drawn perfectly, the same spell costs 16.7. The effect is identical either way: three unit pushes. Because the loop count is a literal, the parser can compute the cost statically while you draw, as Psi computes spell stats from constants at compile time; the ring's glow shows projected cost against the pool, and each glyph tints by its η as you finish it.

**Mishaps.** An unknown glyph renders as a grey smudge with a yellow flare, borrowing Hex's Invalid Pattern colour. An underflow makes the glyph flicker and pads the stack with garbage. When the pool runs out, in safe mode the ring goes dark mid-sequence and the remaining tokens dim; in overcast mode, as in Hex, the deficit comes out of health and the ring burns red. An unclosed ring is not a mishap: the spell stays prepared, hovering at the wand.

**Parsing.** In VR, the first closed stroke whose circle-fit residual passes threshold becomes the main ring and fixes a polar frame. Strokes are grouped into glyphs by time gap (a pen-up under about 400 ms, guess) and by centroid falling inside the band [0.6R, 1.0R]. Each glyph is rotated so its local radial direction points up before $Q matching, which makes the whole spell rotation-invariant, as Hex's turn-list key is, without discretising the input. Sub-ring tangency is a centre-distance test, |c_sub − c| ≈ R − r_sub. All of this costs well under a millisecond per stroke. From an image the steps are the same after rectification, but the keystone must be found (a filled wedge is easy) and band glyphs are small, exactly where detectors and VLMs are weakest. That is why Widdershins is VR-first.

**New versus borrowed.** The stack machine, garbage values and mishap colours come from Hex Casting, concatenative semantics from Joy, counter-clockwise reading and tangent auxiliary rings from Mystical, open-equals-prepared from Witch Hat Atelier, the wand as stored program from Noita, and the ring as the unit of control from Rotary. New, as far as this research found, are freehand glyphs in a polar frame, angular order as program order (which gives insert-editing), quality as cost efficiency rather than effect strength, and mana doubling as gas for totality. Untested: whether about 16 freehand glyphs stay separable in mid-air at speed. Wizard of Wii's finding that players dislike similar circular gestures says the glyph set should be strokes and corners, not loops.

## 6. Covenant: interaction combinators drawn as seals and chords

A Covenant circle is an interaction net. Seals (triangles inscribed in small circles) are agents, their vertices are ports, and straight chords between vertices are wires. Running the circle means rewriting it: when two seals face each other eye to eye, they react by a fixed local rule and the circle redraws itself. There are only three seal types, Lafont's interaction combinators, which are universal. **The semantics is purely topological, so the drawer can lay the circle out with any symmetry without changing its meaning: flair is free.** Covenant is the photograph-of-ink design, and its parser turns connectivity, the hardest part of diagram recognition, into a perfect-matching problem.

| Visual element | Meaning |
|---|---|
| Boundary ring, with notches ("gates") | The net's interface; free ports; the result is read from the gates |
| Seal: triangle inscribed in a small circle, plain | γ (constructor), 1 principal + 2 auxiliary ports |
| Seal with an inner crescent | δ (duplicator), 1 + 2 ports |
| Small circle with one tick and a cross | ε (eraser), principal port only |
| Filled dot ("eye") on one vertex | That vertex is the principal port |
| CCW from the eye: first vertex, second vertex | aux1, aux2 (so mirroring a seal swaps them) |
| Straight chord between two ports | A wire; every port has exactly one |
| Chord joining two eyes | An active pair, which will react |
| Seal size, position, rotation, chord crossings | Nothing |

**Model and evaluation.** This is the symmetric variant of Lafont's interaction combinators (Lafont 1997; the symmetric form studied by Mazza). A net is a set of agents plus a perfect matching on all ports and gates. Annihilation, for two agents of the same type α ∈ {γ, δ}: α(a, b) ⋈ α(c, d) → wires a–c and b–d. Commutation: γ(x, y) ⋈ δ(r₁, r₂) → γ'(r₁, a, b), γ''(r₂, c, d), δ'(x, a, c), δ''(y, b, d), where each new agent's principal points outward to the listed port and a, b, c, d are fresh internal wires. Erasure: ε ⋈ α(a, b) → ε at a and ε at b, and ε ⋈ ε → nothing. Interaction nets are strongly confluent, so every reduction order gives the same normal form, and the animation can fire every active pair at once with no scheduling rule to explain. Normal form is reached when no chord joins two eyes.

The λ-calculus compiles in the standard way: λx.M is a γ whose principal is the term's root, with aux1 = body and aux2 = x; application M N is a γ whose principal attaches to M, with aux1 = result and aux2 = N; δ shares variables and ε discards them. The honest caveat is that this plain encoding is correct only for terms where duplicators never need to tell each other apart. The general case needs labelled duplicators, as in Lamping's optimal reduction and in HVM.

**Worked example: (λx.x) y.** A boundary ring has two gates, Y at 1 o'clock and R at 5 o'clock. Inside are two plain γ seals side by side, eyes facing across the centre and joined by a horizontal chord. The left seal L is λx.x: its two aux vertices are joined by a short chord, the "identity knot". The right seal A is the application: its aux1 (lower-right vertex) runs to R and its aux2 (upper-right vertex) runs to Y.

```
                         ┌──────── gate Y
            aux1         │ aux2
        ┌────○           ○
        │     ╲         ╱
        │      ● ═════ ●        ● = eye (principal), ═ = active pair
        │     ╱  L:γ    ╲ A:γ
        └────○           ○
            aux2         │ aux1
                         └──────── gate R
```

In text form, each wire name appears exactly twice and gates once:

```
gates R Y
γ(w, k, k)     # L
γ(w, R, Y)     # A
```

| Step | What happens | Net after |
|---|---|---|
| 1 | The single active pair is L–A via w; annihilation connects k–R and k–Y | R–k–Y |
| 2 | Both seals vanish and wire k collapses | One chord R–Y |
| 3 | No eyes remain: normal form; the result gate is wired to the input gate | The answer is y |

On paper, the two facing triangles dissolve into a single chord sweeping down the right side of the ring. A second example shows growth: δ(w, R₁, R₂) facing γ(w, X, Y), with all four aux ports going to gates, commutes in one step into four seals, two γ's facing R₁ and R₂ and two δ's facing X and Y, cross-wired by four chords. A pair has been copied, and the circle visibly gains a square of seals.

**Mishaps.** A dangling or forked port (zero chords, or two or more) is a linearity violation, so the circle refuses to run and the port pulses red. A chord passing within ε of a third port is flagged as ambiguous, not guessed. A non-terminating net (a δ–γ pair feeding itself) grows until the step or agent budget runs out, and the circle fills with seals until they press against the boundary, then freezes. A "vicious circle", a cycle whose principal ports all point along it, never reduces and is shown greyed as inert.

**Parsing.** From an image, which is the reason for the design: rectify using the boundary ring; find seals with Hough circles in a radius band; take each seal's three vertices where its inner triangle meets its circle, the eye as the filled blob nearest a vertex, and the interior mark (none, crescent or cross) from a three-class template or tiny CNN. Ports and gates then form a known point set P, typically 10 to 40 points. For every pair (i, j), score straight-line ink coverage by sampling the segment and taking the fraction of dark pixels within the stroke width. Since each port has exactly one chord, take the maximum-weight perfect matching on those scores (Edmonds' blossom algorithm, for example `networkx.max_weight_matching`), and accept it if every chosen edge clears about 0.85 coverage (guess) and the runner-up matching is clearly worse; otherwise ask the user. This sidesteps arrowhead detection entirely, because direction comes from eyes, and it handles crossings, because each candidate is a straight segment between known points. The weak points are curved chords (disallowed for now; skeleton tracing could add them), chords grazing other ports, and an eye dot confused with an ink blot. A trained seal detector on synthetic nets is a reasonable upgrade; a VLM is not, since wire topology is exactly what FlowLearn shows it gets wrong. In VR, strokes give chords directly, with endpoints snapped to the nearest port.

**New versus borrowed.** Interaction nets and combinators come from Lafont (1990, 1997), the symmetric variant from Mazza, the λ-encoding and its labelling caveat from Lamping, rewriting as a visible game from Alligator Eggs, vertices as attachment points from Rithmatic bindpoints, and rewriting rings from VIPR. The seal-and-chord notation and the perfect-matching chord parser are new; the design pass had not seen either elsewhere. Untested: whether chord coverage stays separable at about 40 ports in a phone photo.

## 7. Choir: a signal-flow synth whose voices are the circle's symmetry

The circle is an audio patch. Signal flows inward from the rim to a focus at the centre, each ring band is a processing stage, and k-fold rotational symmetry is k parallel voices. Each glyph's drawing error becomes that voice's analog drift: systematic error sets a fixed detune and wobble sets pitch jitter. **Perfect symmetry collapses to one clean note; human imperfection becomes chorus.** Of the three designs where precision affects the result, this is the one where sloppiness changes the output and is still never wrong. Choir casts in VR as live coding, playing as you draw, and it also reads from paper.

| Visual element | Meaning |
|---|---|
| Rim band | Sources (0 inputs) |
| Inner bands, rim → centre | Successive processing stages (sequential composition) |
| Centre focus dot | Output; sums its inputs |
| Glyphs side by side in a band | Parallel blocks |
| No chord drawn | Default wire to the angularly nearest glyph in the next band inward; many-to-one sums |
| Explicit inward chord | Extra wire (fan-out / split) |
| Arc drawn outward | Feedback wire with a one-sample delay |
| Sine glyph with h humps | Sine oscillator at h · f0 (h-th harmonic of the played note) |
| Falling arc | AR envelope; release ∝ arc length / R |
| Glyph area / band area | Amplitude |
| k-fold rotational symmetry | k voices (no special rule: copies are just parallel blocks) |
| Low-band drawing error | Deterministic parameter offset (detune) |
| High-band drawing error (EFD wobble) | Random parameter jitter (temperature) |

**Model and evaluation.** This is synchronous dataflow with the semantics of Faust's block-diagram algebra (Orlarey, Fober and Letz): sequential, parallel, split, merge, and recursion with an implicit one-sample delay. The parse yields a graph whose forward edges form a DAG and whose outward arcs are feedback edges. At each sample t, nodes are evaluated in topological order, each computing y_v[t] = f_v(Σ forward inputs[t] + Σ feedback inputs[t−1]), and the output is y_F[t]. Note-on and note-off events supply f0 and the envelope gate. Because every feedback path carries a delay, the graph is always causal.

Precision is applied per glyph. A drawn parameter θ is realised as θ̃ = θ · 2^((D + J(t))/1200), working in cents for pitch. D is the deterministic part: for a sine glyph, D = −κ·τ, where τ is the normalised trend in hump period, (P_last − P_first)/P̄, and κ = 70 cents per unit (untested), clamped to ±25 cents. Humps that lengthen along the stroke go flat. J(t) is a slow random walk in the 2 to 8 Hz band with standard deviation proportional to the glyph's high-band EFD energy, seeded from the stroke so the same drawing always sounds the same. With every q = 1, the denotation is the exact deterministic Faust program. An "in tune" assist clamps D and J to zero, and replicating a wedge with a mirror tool gives identical copies, so perfect unison is a choice the player makes, not a penalty.

**Worked example: three-voice bell.** The rim band holds three sine glyphs with two humps each, at 90°, 210° and 330°. The second band holds a falling arc directly inward of each. There are no chords, and the centre is the focus dot.

```
                 ∿∿            rim, 90°   (osc, h = 2)
                  ⌒            band 2     (decay)
                  │
                  ●            focus (sum)
                ╱   ╲
             ⌒          ⌒      band 2, 210° / 330°
          ∿∿              ∿∿   rim, 210° / 330°
```

Faust-like text (written by the design pass, not compiled):

```
voice(d, a, rel) = os.osc(2*f0*2^(d/1200)) * a * en.ar(0.01, rel, gate);
process = voice(1.4, 0.30, 1.2), voice(-5.6, 0.25, 1.1), voice(10.5, 0.35, 1.3) :> _;
```

The trace for the note A3 (f0 = 220 Hz):

| Step | What happens | Values |
|---|---|---|
| 1 | Parse finds three wedges with h = 2 | Each voice nominally 440 Hz |
| 2 | Measured hump-period trends τ give D = −κτ | τ = −0.02, +0.08, −0.15 → D = +1.4, −5.6, +10.5 cents |
| 3 | Realised frequencies, 440 × 2^(D/1200) | 440.36, 438.58, 442.68 Hz |
| 4 | Beats between the pairs | 1.78, 2.32, 4.10 Hz: an audible slow shimmer |
| 5 | Amplitudes from glyph areas, releases from arc lengths | 0.30, 0.25, 0.35; 1.2, 1.1, 1.3 s |
| 6 | Each sample, the three enveloped sines sum at the focus | Output |

Drawn perfectly, all three voices sit at exactly 440 Hz and the circle is one sine of amplitude 0.9.

**Mishaps.** A glyph with no path to the focus is dead: silent and drawn grey. An explicit split or merge whose channel counts do not divide, which Faust would reject, is discord and shows as a red seam between bands. Loop gain above 1 is runaway feedback: a limiter clamps it, and the circle's glow saturates and flickers in time with the clipping.

**Parsing.** In VR, bands are concentric circle fits and glyphs are assigned to bands by radius. Hump count is the number of extrema of the stroke's signed distance from its chord after light smoothing, which is robust and cheap, and the period trend falls out of the extrema spacing. Each new glyph is spliced into the running graph, so latency is one audio buffer. From an image, bands come from Hough and hump count from the skeleton path; symmetry order k comes from the circular autocorrelation of each band's angular ink histogram (the k maximising correlation at lag 360°/k), used only for display since the semantics never needs it. Most wiring is implicit from angle and band, so line topology, the weakest recognition step, is rarely exercised. Feedback arcs are the exception and need skeleton tracing. Do not ask a VLM to count humps.

**New versus borrowed.** Faust's algebra, modular-synth patching, Piet's size-as-number, and Rithmatics' Line of Vigor, which is literally a sine wave whose tightness sets strength, are borrowed. Radial symmetry as polyphony, and splitting drawing error into deterministic detune (low band) and stochastic jitter (high band), are new. Untested: whether κ = 70 gives pleasant chorus or seasickness, and whether hump-count-as-harmonic is musically enough; the design pass suspects a ratio glyph is needed for inharmonic partials.

## 8. Volvelle: a Llull dial where rotation is the value

A program is a set of concentric rotatable rings that share n sectors, each ring lettered with an alphabet. A ring's state is its rotation. Bridges drawn across rings at fixed angles are constraints labelled with Llull's relational principles. Pinned rings are inputs, free rings are unknowns, and running the program means finding every rotation assignment that satisfies all the bridges. It is a finite-domain constraint language you can print, cut out and turn by hand, and **because checking a solution is easy even when finding one is hard, a photo of the turned wheel is a proof the camera can verify.**

| Visual element | Meaning |
|---|---|
| Ring with n lettered sectors (n = 9, letters B C D E F G H I K = 1…9, after Llull) | Variable with domain Z₉ |
| Index notch joining ring and frame | Pin: the drawn rotation is given (input) |
| Ring without a notch | Free variable |
| Frame north mark | Sector 0; sectors numbered clockwise |
| Bridge: short segment with end dots on two or more rings at sector s, plus a relation glyph | Constraint on the letters showing at s on those rings |
| Two bars (Concordance) / crossed bars (Contrariety) / wedge opening outward or inward (Majority / Minority) | = / ≠ / > / < |
| Plus-sign bridge across three rings | v₁ + v₂ ≡ v₃ (mod 9), with K = 9 ≡ 0 |

**Model and evaluation.** A program is (n, rings x with labellings σ_x : Z_n → Σ, pins r_x for pinned rings, bridges (ρ, s, ⟨x₁…x_k⟩)). The letter showing on ring x at sector s is σ_x[(s − r_x) mod n]. The solution set is every assignment of free rotations under which each bridge's relation ρ holds on the letters showing at its sector. The evaluator runs AC-3 propagation (Mackworth 1977), then backtracks in odometer order with the innermost ring fastest, which is Llull's Fourth Figure stepping BCB → CCB → BDB. The language is deliberately not Turing-complete, and solving is NP-complete. The reduction from graph 3-colouring is short: take n = 3, one ring per vertex labelled 1, 2, 3, and a Contrariety bridge at sector 0 for each edge, forcing r_u ≠ r_v. A bridge joins only the rings carrying its end dots, so any graph can be drawn, and membership in NP is obvious.

**Worked example.** Three rings, all lettered B…K clockwise: A outer and pinned at r_A = 6, B middle and free, C inner and free. Bridge 1 is a plus bridge at sector 0 across A, B and C (v_A + v_B ≡ v_C). Bridge 2 is a Majority bridge at sector 3 between A and B (v_A > v_B). Bridge 3 is a Concordance bridge at sector 4 with end dots on A and C only (v_A = v_C). The solution, unrolled:

```
sector:   0  1  2  3  4  5  6  7  8
A (r=6):  E  F  G  H  I  K  B  C  D      pinned
B (r=1):  K  B  C  D  E  F  G  H  I
C (r=6):  E  F  G  H  I  K  B  C  D
bridge:   +        >  =
          ABC      AB AC
```

| Step | Reasoning | Result |
|---|---|---|
| 1 | Pinned A shows E (4) at sector 0, H (7) at sector 3, I (8) at sector 4 | Known values |
| 2 | Bridge 3 becomes unary: C must show I at sector 4, so ((4 − r_C) mod 9) + 1 = 8 | r_C = 6 |
| 3 | Bridge 1: C shows E at sector 0, so v_B ≡ 4 − 4 ≡ 0, which is K; (−r_B mod 9) + 1 = 9 | r_B = 1 |
| 4 | Bridge 2 checks: H (7) > D (3) | Holds |
| 5 | The solution is unique; at north the reader sees E + K = E, the ninth letter acting as zero | Dial turns to it |

Without bridge 3, propagation leaves six candidates; adding a Minority bridge B < C at sector 6 instead would leave two.

**Mishaps.** No solution is a jam: the dial will not turn, and the minimal conflicting bridges glow, the unsat core coming from deletion-based extraction, which is cheap at this size. Several solutions is a hum: an index steps through them one by one. End dots that do not land on two rings make a loose bridge, ignored with a warning. A ring with the wrong sector count is refused.

**Parsing.** From an image, concentric ring fits give the bands. Because each ring's letter sequence is known in advance, reading a ring is a single correlation: slide the template alphabet's angular ink profile around the ring and take the best offset. All nine letters vote for one rotation, so a few illegible letters do not matter. **This is the strongest error correction of any design here.** Custom labellings lose it and fall back to per-letter classification, where small glyphs are the known weak point. Bridges are short segments whose endpoints lie on fitted rings, found with Hough plus a band-membership test and a four-class relation glyph, and pin notches are blobs straddling frame and ring. In VR, rings are grabbed and twisted with a controller, snapping to sectors: the Llull dial as a physical interface.

**New versus borrowed.** Llull's alphabet, Fourth Figure and Figure T relations, Alberti's cipher disc, rotor machines, CSP solving and the modular sums of kamea squares are borrowed. Bridges as drawn constraints and the photo-verified solution are new. Untested: how many bridges a hand-drawn wheel holds before it becomes unreadable, with about 10 per wheel as the design pass's guess.

## 9. Athanor: membrane chemistry where sloppiness is wild magic

Nested closed curves are membranes, and glyphs inside them are element tokens in a multiset, so order and position mean nothing, as with Magicka's queue for ordinary spells. Elements react by a priority table, opposing elements annihilating first and then combining. A membrane drawn with a gap dissolves once its contents go quiet, pouring them into the parent, so **nesting is evaluation order**: inner reactions finish before outer ones see the products. Here precision is semantic in the strongest sense, the design's deliberate exception to "graded, never a gate". Each drawn token denotes the recogniser's calibrated posterior over element classes, and casting samples from it. A neat glyph is near-certain; an ambiguous one sometimes casts as its confusable neighbour, and the glyph set is designed so neighbours are thematically close. You can preview the outcome distribution before you release.

| Visual element | Meaning |
|---|---|
| Closed curve (any shape) | Membrane; region holding a multiset |
| Membrane with a gap | Dissolvable: dissolves when its region is inert |
| Outermost membrane (skin) | Its contents at halt are the spell's effect |
| Gap in the skin | Backfire: effect lands on the caster |
| Element glyph | One token; multiplicity = count of copies = magnitude |
| Recipe seal (circle split by a diameter; reactants left, products right) | User rule; tangent to a membrane = local, in the outer legend band = global |
| Product drawn outside the recipe seal's rim | Sent out to the parent region |
| Glyph posterior, sharpened by β | Probability of each reading at cast time |

**Model and evaluation.** This is a P system (Păun's membrane computing; with cooperative rules, P systems are computationally universal). A configuration is a membrane tree with a multiset in each region, and rules u → v sit in ordered priority tiers. In one step, in every region in parallel: for each tier in order, apply each rule in order as many times as possible to objects not yet consumed, holding products back until the step ends; then move products marked "out" to the parent region, or to the environment from the skin; then dissolve every gapped membrane whose region applied no rule and received nothing this step, merging its multiset into the parent and dropping its local rules. Halt when a step changes nothing; the output is the environment plus the skin's contents. Greedy application in rule order always yields a maximal multiset of applications, so this is a deterministic refinement of the usual nondeterministic maximal parallelism. Dissolving on inertness, rather than through Păun's explicit δ object, is the design's own variation, and δ can still be written as a product.

The built-in chemistry is Magicka-inspired, not Magicka's actual rules. Tier 1 holds the oppositions: F + C → ∅, W + L → ∅, L + E → ∅, Life + Arcane → ∅. Tier 2 holds combinations: W + F → S (steam), W + C → I (ice), S + L → Z (storm, invented). For precision, token i has posterior π_i(c) = softmax_c(−d_i(c)/τ) over $Q template distances, with τ fitted by temperature scaling (Guo et al. 2017) on held-out labelled drawings so the probabilities mean what they say. Casting samples each token from p_i(c) ∝ π_i(c)^β. β is the sharpness: β → ∞ gives argmax, a fully deterministic "steady" mode that doubles as the accessibility setting. A drawing therefore denotes a distribution over programs, and the effect is a distribution over output multisets, which the caster previews by enumerating the few uncertain tokens.

**Worked example: "storm lance".** The skin is a closed ring holding one lightning glyph ϟ and an inner gapped membrane. Inside that membrane are two water glyphs ≈ and two fire glyphs ▲.

```
   .--------------------------.
   |   ϟ                       |     skin (closed)
   |      .- - - - - - .       |
   |     (   ≈     ≈    )      |     inner membrane, gapped
   |     (   ▲     ▲    )      |
   |      '- - - - - - '       |
   '--------------------------'
```

Text form, with `?` marking a gap: `skin{ L, inner?{ W, W, F, F } }`. With every token drawn cleanly:

| Step | What happens | State |
|---|---|---|
| 1 | Inner region: W + F → S twice; the skin's {L} is inert | inner {S, S}; skin {L} |
| 2 | Inner region is inert, so it dissolves | skin {L, S, S} |
| 3 | Skin: S + L → Z | skin {Z, S} |
| 4 | Nothing changes | Halt; emit storm + steam |

Draw the same tokens flat with no inner membrane, {L, W, W, F, F}, and tier 1 applies W + L → ∅ while tier 2 applies W + F → S, emitting {S, F}: steam and fire, no storm. **The membrane is what kept water away from lightning until the water had become steam.**

Now the wild-magic variant: one water glyph is drawn loosely, with posterior water 0.70, cold 0.25, life 0.05. In the cold case the inner region holds {W, C, F, F}; tier 1 applies F + C → ∅ and tier 2 applies W + F → S, and after dissolving, S + L → Z, so the output is {Z}, a weaker storm. In the life case the inner region yields {S, Life, F}; after dissolving, S + L → Z, so the output is {Z, Life, F}, a storm that heals and burns. At β = 1 the preview reads storm + steam 70%, storm 25%, storm + life + fire 5%. At β = 2 it reads 88%, 11% and 0.5%.

**Mishaps.** A gap in the skin is a backfire. User recipes that cycle hit the step budget, and the membranes bulge and pop (boil-over). If everything annihilates, the spell fizzles: a grey puff, paying only the cost of the attempt.

**Parsing.** In VR, membranes are closed strokes of any shape, containment is point-in-polygon on the projected plane, and a gap is endpoint separation over perimeter above a threshold; tokens get $Q posteriors. From an image this is the easiest structure of the five: OpenCV `findContours` with `RETR_TREE` returns the containment hierarchy directly, gaps show up as skeleton endpoints, and multiplicity is a connected-component count, which must not be left to a VLM. Small-glyph classification is the weak point, and the classifier must be calibrated, since raw CNN softmax and VLM "confidence" are not probabilities. The design rule is to choose glyph shapes so the recogniser's confusion matrix mirrors elemental adjacency (water near cold, fire near lightning), so wild magic produces plausible neighbours rather than noise. That rule is an inference and needs a confusion-matrix check on real drawings.

**New versus borrowed.** P systems (Păun), multiset rewriting (Gamma, by Banâtre and Le Métayer; the chemical abstract machine, by Berry and Boudol), Magicka's multisets and oppositions, Witch Hat Atelier's open ring and nesting, and Cultist Simulator's discovery by experiment are borrowed. The calibrated recogniser posterior as the execution distribution, confusions designed to be thematic, and inertness-triggered dissolution as sequencing are new. Untested: whether players read a 25% "wild" outcome as fun or as unfair; the preview is meant to make it a choice.

## 10. Widdershins first, Covenant for paper, Choir for sound

| | Widdershins | Covenant | Choir | Volvelle | Athanor |
|---|---|---|---|---|---|
| Model | Concatenative stack machine | Interaction combinators (rewriting) | Synchronous dataflow (Faust algebra) | Finite-domain CSP | P system (multiset rewriting) |
| Central visual idea | Angular order on a ring; open = deferred | Seals + chords; eyes meeting react | Rim → centre flow; symmetry = voices | Rotation = value; bridges = constraints | Nesting = evaluation order |
| Precision → semantics | Cost efficiency (mana as gas) | None (topology only) | Detune + jitter (temperature) | None | Posterior sampling (wild magic) |
| Primary surface | VR | Ink photo | VR live, or paper | Printed wheel + photo | Either |
| Expressiveness | Total (gas-bounded) | Universal | Causal signal graphs | NP-complete, not universal | Universal with cooperative recipes |
| Hardest parse step | Small band glyphs from images | Chord matching near ports | Feedback arcs | Custom-lettered rings | Calibrated small-glyph posteriors |
| Reuses an existing VR stroke recogniser | Almost all | Little | Most | Little | Most |

The table shows a real spread rather than five skins on one idea. The models span total, universal, causal-signal and NP-complete-but-not-universal; precision enters as cost, as timbre, as probability, or not at all; and the surfaces cover VR, ink and cut paper. Two designs (Covenant, Volvelle) deliberately give precision no semantic role, which is the cleanest answer to IRONSTRIKE's warning, and their flair comes from layout freedom and physical manipulation instead.

**The best weekend prototype is Widdershins.** It reuses the parts of an existing VR stroke recogniser that already work (button-gated strokes, plane projection, $Q and per-stroke quality metrics), and the only new pieces are a circle fit, a polar frame and a stack interpreter of about 200 lines. It also tests the question everything else rests on: can a player place freehand glyphs around a mid-air ring reliably enough that angular order works as program order, and does quality-as-cost feel fair rather than punishing? If that fails, Choir and Athanor in VR fail too. Choir is the runner-up for something that sounds good on day one with no game around it, and it suits anyone already working with audio. Covenant is the one to build for the photograph-of-ink path: its parser (Hough circles plus perfect matching) and reducer (about 100 lines) are both small, and it is the most novel design here. A suggestion beyond the design pass: if a VR prototype also has voice or body-stance input, those channels stay free in Widdershins for things the circle does not encode, such as choosing a cast mode the way Magicka's mouse buttons do.

**The smallest first experiment fits in one evening.** In the existing VR prototype, treat the first closed stroke as a ring and fit its centre and radius; record $Q templates for four glyphs (dot, triangle, chevron, slash) normalised to the radial-up frame; then draw 20 casts of "ring plus four glyphs placed counter-clockwise" and log the parsed token sequence, angular order against draw order, and per-glyph q. Three numbers come out: recognition accuracy with the polar normalisation versus without it, how often angular order matches what the drawer intended, and the spread of q within one player across casts, which decides whether q_floor and the λ blend are needed before anyone else plays. No interpreter is needed yet. If recognition holds above about 95% (the design pass's threshold) and angular order is never wrong, write the stack machine the next day.

## 11. What this research did not find or did not read

Several absences rest on shallow searches. Reddit was blocked, YouTube was not searched, and esolangs.org's category and search pages refused automated access, so the claim that no other compositional, executable magic-circle language exists rests on GitHub, Hacker News (Algolia), itch.io, the web and Japanese-language searches, not on an exhaustive sweep. The Witch Hat Atelier fan projects are a fast-moving 2026 snapshot; their README and docs were rechecked, but not their source code, star count, or forks beyond five, and nobody checked what cogerk's Mystical "interpreter" actually interprets. The only prior work this builds on is an earlier, unpublished exploration of grading drawn-circle quality.

Primary sources are missing for much of the history and fiction. No VIPR paper was retrieved, so its guard notation and data model are unknown. Llull, Agrippa and Spare were read through the Stanford Encyclopedia, a practitioner blog and a quoted passage; Rithmatics, Witch Hat Atelier, Mahouka and Fullmetal Alchemist through fan wikis, not the books or manga. Noita and Magicka mechanics come from fan wikis and Wikipedia, not game code, and Noita's iteration limit was never read. Street Fighter 6 frame data is community testing, not Capcom's. Game claims about precision scaling (War of Wizards, Lost Magic, The Magus Circle) are store text and reviews, not measured behaviour.

On the recognition side, no study calibrates VLMs on drawing neatness, no VR controller-noise or latency-tolerance data was found, and the aesthetic and handwriting-quality papers were read at abstract level only. The SketchJudge human baseline is three non-expert raters on 160 answers. FlowLearn's VLM numbers are 2024-era models, and newer frontier models are likely better at counting, though no 2026 hand-drawn-specific numbers turned up. The design pass's parameters (q_floor, κ, the 400 ms pen-up gap, the 0.85 coverage threshold, pairs needed for calibration, bridges per wheel) are untested starting points, and no part of any design has been built.

## 12. Conclusion

"Can a magic circle be a program?" turns out to be two separable questions, and prior art has answered each half in isolation: notation (Mystical, VIPR, Gallifreyan) and recognition (the 2026 fan simulators, Arrow R-CNN, DECIMER). The missing piece is a semantics chosen to suit the recogniser. Once meaning lives only in what circle fits, angles, containment and perfect matchings measure reliably, the parsing problem shrinks to something a headset CPU or a phone photo handles, and the familiar failure points (arrow topology, VLM counting, precision-gated frustration) are designed out instead of fought.

The more interesting finding is that "how well it's drawn" has no single right meaning. Wild magic from calibrated posteriors, analog drift as chorus, and neatness as mana efficiency are three distinct and defensible readings, each with a different fairness profile, and the accessibility knob (λ, β, or the steady assist) is part of the language definition rather than a setting bolted on afterwards. That is the part no shipped game or fan project has worked out, and the one-evening Widdershins experiment is the cheapest way to find out whether the first of those readings survives contact with a real hand in mid-air.

## 13. Sources

- [Mystical README](https://suberic.net/~dmm/projects/mystical/README.html)
- [wha-spell-simulator (GitHub)](https://github.com/ytnrvdf/wha-spell-simulator)
- [cogerk/mystical_ps fork (GitHub)](https://github.com/cogerk/mystical_ps)
- [MetaFilter: Mystical](https://www.metafilter.com/208819/Mystical)
- [Berkeley survey CSD-04-1368](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2004/Archive/CSD-04-1368.pdf)
- [Bremen lecture slides on VIPR](https://www.informatik.uni-bremen.de/agbkb/lehre/ss04/VS/Material/vipr.sxi.pdf)
- [Berger thesis (LMU), visual languages survey](https://www.en.pms.ifi.lmu.de/publications/diplomarbeiten/Sacha.Berger/THESIS/HTML-view/part2.html)
- [Esolangs: Rotary](https://esolangs.org/wiki/Rotary)
- [Sherman's Circular Gallifreyan guide](https://shermansplanet.com/gallifreyan/guide.pdf)
- [Scrapbox villagepump: Magical Circle language](https://scrapbox.io/villagepump/%E9%AD%94%E6%B3%95%E9%99%A3%E8%A8%80%E8%AA%9E)
- [danielstern/MagicCircles (GitHub)](https://github.com/danielstern/MagicCircles)
- [Wikipedia: ShotCode](https://en.wikipedia.org/wiki/ShotCode)
- [Spotify Codes and how they work (Level Up Coding)](https://levelup.gitconnected.com/spotify-codes-and-how-they-work-664f4e4b8489)
- [Esolangs: Piet](https://esolangs.org/wiki/Piet)
- [Esolangs: Wierd](https://esolangs.org/wiki/Wierd)
- [Esolangs: Hexagony](https://esolangs.org/wiki/Hexagony)
- [Esolangs: Aheui](https://esolangs.org/wiki/Aheui)
- [Funge-98 spec](https://github.com/catseye/Funge-98/blob/master/doc/funge98.markdown)
- [Alligator Eggs](https://worrydream.com/AlligatorEggs)
- [Tromp: Lambda diagrams](https://tromp.github.io/cl/diagrams.html)
- [Hex Casting source: HexPattern.kt](https://raw.githubusercontent.com/gamma-delta/HexMod/main/Common/src/main/java/at/petrak/hexcasting/api/casting/math/HexPattern.kt)
- [Hex Casting source: PatternRegistryManifest.java](https://raw.githubusercontent.com/gamma-delta/HexMod/main/Common/src/main/java/at/petrak/hexcasting/common/casting/PatternRegistryManifest.java)
- [Hex Casting source: ScrungledPatternsSave.java](https://raw.githubusercontent.com/gamma-delta/HexMod/main/Common/src/main/java/at/petrak/hexcasting/server/ScrungledPatternsSave.java)
- [Hex Casting source: HexActions.java](https://raw.githubusercontent.com/gamma-delta/HexMod/main/Common/src/main/java/at/petrak/hexcasting/common/lib/hex/HexActions.java)
- [Hex Casting source: SpecialHandlerNumberLiteral.kt](https://raw.githubusercontent.com/gamma-delta/HexMod/main/Common/src/main/java/at/petrak/hexcasting/common/casting/actions/math/SpecialHandlerNumberLiteral.kt)
- [Hex Casting en_us lang file](https://raw.githubusercontent.com/gamma-delta/HexMod/main/Common/src/main/resources/assets/hexcasting/lang/en_us.flatten.json5)
- [Hex Casting source: HexConfig.java](https://raw.githubusercontent.com/gamma-delta/HexMod/main/Common/src/main/java/at/petrak/hexcasting/api/mod/HexConfig.java)
- [Hex Casting source: CastingVM.kt](https://raw.githubusercontent.com/gamma-delta/HexMod/main/Common/src/main/java/at/petrak/hexcasting/api/casting/eval/vm/CastingVM.kt)
- [Hex Casting forum: FAQ (0.10.x)](https://forum.petra-k.at/viewtopic.php?p=130)
- [Hex Casting CHANGELOG](https://raw.githubusercontent.com/gamma-delta/HexMod/main/CHANGELOG.md)
- [Hex Casting forum: Game of Life spell circle](https://forum.petra-k.at/viewtopic.php?p=401)
- [s5bug: Hex Casting compiler design (gist)](https://gist.github.com/s5bug/5f453c9c159fb77bad9dff1a8954fb3b)
- [ModDex: HexParse](https://moddex.gg/mod/hexparse)
- [Modrinth: HexDebug](https://modrinth.com/mod/hexdebug)
- [Hex Casting forum: VS Code extension thread](https://forum.petra-k.at/viewtopic.php?p=52)
- [Psi source: SpellCompiler.java](https://raw.githubusercontent.com/VazkiiMods/Psi/master/Xplat/src/main/java/vazkii/psi/common/spell/SpellCompiler.java)
- [Psi en_us lang file](https://raw.githubusercontent.com/VazkiiMods/Psi/master/Xplat/src/main/resources/assets/psi/lang/en_us.json)
- [ars.guide: Introduction to glyphs](https://ars.guide/book/getting_started/introduction_to_glyphs/)
- [minecraft-guides: Ars Nouveau spell builder](https://www.minecraft-guides.com/mod/ars-nouveau/wiki/spell-builder/)
- [SiriusMC: Occultism rituals guide](https://wiki.siriusmc.net/books/modpack-guides-and-tutorials/page/occultism-rituals-atm10)
- [Noita wiki: Expert Guide: Draw](https://noita.wiki.gg/wiki/Expert_Guide:_Draw)
- [Noita wiki: Calling and Recursion](https://noita.wiki.gg/wiki/Expert_Guide:_Calling_and_Recursion)
- [Noita wiki: Divide By](https://noita.wiki.gg/wiki/Divide_By)
- [Noita wiki: Trigger Loop](https://noita.wiki.gg/wiki/Trigger_Loop)
- [Noita wiki: Wand Simulator](https://noita.wiki.gg/wiki/Tool:_Noita_Wand_Simulator)
- [Wikipedia: Magicka](https://en.wikipedia.org/wiki/Magicka)
- [Magicka wiki: Elements](https://magicka.fandom.com/wiki/Elements)
- [Magicka wiki: Magicks](https://magicka.fandom.com/wiki/Magicks_(Magicka_1))
- [Game Developer: Postmortem: Arrowhead Game Studios' Magicka](https://gamedeveloper.com/business/postmortem-arrowhead-game-studios-i-magicka-i-)
- [critpoints.net: How to code fighting game motion inputs](https://critpoints.net/2025/02/05/how-to-code-fighting-game-motion-inputs/)
- [EventHubs: SF6 input trouble breakdown](https://www.eventhubs.com/news/2023/jun/17/sf6-input-trouble-breakdown)
- [Wikipedia: Arx Fatalis](https://en.wikipedia.org/wiki/Arx_Fatalis)
- [Super Jump: Arx Fatalis magic was ahead of its time](https://superjumpmagazine.com/arx-fatalis-magic-was-ahead-of-its-time-and-technology)
- [Wikipedia: Okami](https://en.wikipedia.org/wiki/%C5%8Ckami)
- [Wikipedia: Dawn of Sorrow](https://en.wikipedia.org/wiki/Castlevania:_Dawn_of_Sorrow)
- [Steam: The Magus Circle](https://store.steampowered.com/app/2796640/The_Magus_Circle/)
- [Steam: War of Wizards](https://store.steampowered.com/app/2009460/War_of_Wizards/)
- [Wikipedia: Lost Magic](https://en.wikipedia.org/wiki/Lost_Magic)
- [Game Revolution: LostMagic review](https://www.gamerevolution.com/review/37102-lostmagic-review)
- [Skill & Spell devlog (itch.io)](https://totallynotdevs.itch.io/skill-and-spell/devlog/1676576/first-playable-prototype-drawing-runes-and-dueling-the-dummy)
- [4Gamer: mobile drawing game page](https://www.4gamer.net/games/335/G033541/)
- [Game Developer: Conjuring a gestural spellcasting system for VR (IRONSTRIKE)](https://gamedeveloper.com/design/conjuring-a-gestural-spellcasting-system-for-vr)
- [Cheema and LaViola: Wizard of Wii (FDG 2011)](https://www.eecs.ucf.edu/~jjl/pubs/p265-cheema.pdf)
- [Coppermind: Rithmatics](https://coppermind.net/wiki/Rithmatics)
- [WHA Fandom: Magic](https://witch-hat-atelier.fandom.com/wiki/Magic)
- [FMA Fandom: Alchemy](https://fma.fandom.com/wiki/Alchemy)
- [Mahouka Fandom: Magic Sequence](https://mahouka-koukou-no-rettousei.fandom.com/wiki/Magic_Sequence)
- [Ars Magica Wiki: Hermetic Arts](https://arsmagica.fandom.com/wiki/Hermetic_Arts)
- [Stanford Encyclopedia: Llull](https://plato.stanford.edu/entries/llull/)
- [Bremen handout on Llull](https://www.compart.uni-bremen.de/content/4-teaching/0-summer-2019/2-theorie-und-geschichte-des-berechenbaren/3-material/berechenbar19-04lull.pdf)
- [Wikipedia: Ars Magna](https://en.wikipedia.org/wiki/Ars_Magna_(Ramon_Llull))
- [David Rankine: Agrippa and the magic squares](https://www.davidrankine.com/post/agrippa-and-the-magic-squares)
- [sacred-texts TOPY page](https://sacred-texts.com/eso/topy/black3.htm)
- [Wikipedia: Sigil](https://en.wikipedia.org/wiki/Sigil)
- [Wikipedia: Baba Is You](https://en.wikipedia.org/wiki/Baba_Is_You)
- [Wikipedia: The Witness](https://en.wikipedia.org/wiki/The_Witness_(2016_video_game))
- [Wikipedia: Cultist Simulator](https://en.wikipedia.org/wiki/Cultist_Simulator)
- [Churchill, Biderman and Herrick, FUN 2021](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.FUN.2021.9)
- [wha-spell-simulator README](https://raw.githubusercontent.com/ytnrvdf/wha-spell-simulator/main/README.md)
- [wha-spell-simulator docs: glyph-ast.md](https://raw.githubusercontent.com/ytnrvdf/wha-spell-simulator/main/docs/glyph-ast.md)
- [wha-spell-simulator docs: spell-ir.md](https://raw.githubusercontent.com/ytnrvdf/wha-spell-simulator/main/docs/spell-ir.md)
- [aetherquill (GitHub)](https://github.com/rajyyug1132/aetherquill)
- [Pancu: Witch Hat Atelier spell recognition, Unity (GitHub)](https://github.com/Pancu/Witch-Hat-Atelier-Spell-Recognition-Unity)
- [YatoVoid: witch-atelier (GitHub)](https://github.com/YatoVoid/witch-atelier)
- [Arrow R-CNN (Springer, IJDAR)](https://link.springer.com/article/10.1007/s10032-020-00361-1)
- [arXiv 2505.07864: flowchart detector plus GPT-4o pipeline](https://arxiv.org/html/2505.07864v1)
- [arXiv 2508.19773: structural handwritten maths recognition](https://arxiv.org/pdf/2508.19773)
- [DECIMER hand-drawn molecules (PMC11227129)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11227129)
- [Hammond and Davis: LADDER](https://groups.csail.mit.edu/mug/pubs/Hammond2005Ladder.pdf)
- [FlowLearn (arXiv 2407.05183)](https://arxiv.org/html/2407.05183v2)
- [SketchJudge (arXiv 2601.06944)](https://arxiv.org/html/2601.06944)
- [Visual Aesthetic Benchmark (arXiv 2605.12684)](https://arxiv.org/abs/2605.12684)
- [CHAED handwriting aesthetics (IJCAI 2015)](https://www.ijcai.org/Abstract/15/356)
- [osu! wiki: Judgement](https://osu.ppy.sh/wiki/en/Gameplay/Judgement/osu%21)
- [Ido: kanji auto-scorer (JSiSE 2019)](https://www.jsise.org/taikai/2019/program/contents/pdf/F5-1.pdf)
- [Würzburg HCI: sketch stroke correction](https://hci.uni-wuerzburg.de/topics/20250722-sketch-stroke-correction/)
- [Spellcasters stroke-rehabilitation adaptation (eScholarship)](https://escholarship.org/uc/item/0nf117zh)
