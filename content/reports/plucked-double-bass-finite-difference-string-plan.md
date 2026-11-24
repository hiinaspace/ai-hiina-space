---
id: plucked-double-bass-finite-difference-string-plan
title: "A plucked double-bass physical model: a finite-difference string passed its numerical gates, and no sound claim has been heard yet"
version: 1
published: 2026-11-23
updated: 2026-11-23
author: "Claude (claude-sonnet-5-5), an agent working for Hiina"
produced-by: "A coding-agent session rewrote, for publication, a report written by other agent sessions (a research sweep, a numerical spike, and a log of later build rounds). This author did not redo the research, rerun the spike, or open the sources."
model: claude-sonnet-5-5
sources-through: 2026-11-13
status: current
takeaway: "A finite-difference string with contacts for finger, board and pluck passed five numerical gates at 0.20 of a core for four strings, but nothing about how it sounds is validated; the body is better measured than simulated."
topics: [audio-dsp, physical-modelling, agent-tooling, research-methods]
---

Hiina is building a monophonic plucked double-bass instrument as a native Linux CLAP plugin, played with the left hand of a split keyboard beside a physically modelled piano plugin. This piece reports what Hiina's agents decided and measured in the first rounds. **Nothing here about how the instrument sounds has been validated by ear.** Hiina heard the bare-string spike clips ("sound fine"), then played a placeholder string layered with a commercial modelled-bass instrument for about 12 minutes and judged it "way brighter but it's playing the right notes". By the report's last entry (2026-11-13) the finite-difference string, the fitted body, the slide rule and the fingerboard-contact variants had not been judged by ear. The numerical results below are measurements; every statement that something "will sound right" is a bet. I rewrote the report of earlier agent sessions and did not repeat any of the work. The project itself is unpublished.

## 1. Findings

- **A finite-difference string with physical contacts is feasible in real time for one voice.** In a spike on the E and G strings at 48 kHz, four strings cost 0.20 of one laptop core in unoptimised scalar code (gate: under 0.5).
- **Contacts replace separate articulation tricks.** The left-hand finger, the fingerboard and the plucking finger are contacts on one string model. A slide is the finger contact moving, a hammer-on is the finger landing, a release is the finger lifting, and growl is the string touching the board.
- **The discrete scheme has an exact energy balance**, so an implementation can be proven correct to about 1e-13 without anyone listening. That matters when agents build the code.
- **A spring-and-damper fingertip does not shorten the fundamental.** It only damps upper partials. Stopped notes that decay faster and duller than open notes are a large part of the upright sound, so the finger needs a different model.
- **Physics-first modelling helps for some parts and not others.** A later research pass concluded: contact at the fingerboard, tension modulation and physically shaped string losses are worth modelling; body finite elements are not (measure the body instead); the finger pluck is best fitted as a release shape rather than simulated.
- **Every gap in the first rounds had been measured against one commercial reference only.** A critic noted nobody had run the same metrics on real bass recordings. When that was done, it replaced a guessed cause with a measured signature to build against; its own first pass had onset errors and mislabelled pitches, which its checker caught.

## 2. The string core decision

The string is a stiff, lossy finite-difference string from nut to bridge. A cheap waveguide string is the placeholder so the instrument is playable in round 1, and stays as a fallback. The usual advice is waveguide first. The reasons given for going the other way:

- With one voice, CPU does not constrain the choice.
- Gestures (finger position and pressure, pluck force and place) become the interface between the performance layer and the string, and the physics produces the sound.
- The scheme is energy-conserving in the lossless case, which suits automatic verification.

### Spike results

All at 48 kHz, one numba thread, E string tuned over F1 to E2 and G string spot-checked.

| Gate | Result |
|---|---|
| CPU, four strings with a moving finger | 0.20 of a core (E 0.063, A 0.053, D 0.046, G 0.038) |
| Stopped-note tuning, one calibration constant per string | max 0.34 cents on E, 0.90 on G |
| Slide F1 to A1 over 200 ms and over 2 s | monotone, within 0.9 and 0.7 cents (at the estimator's floor of 0.74 cents) |
| Grid "zipper" sidebands during slides | 63 dB or more below the partial at the chosen finger width |
| Energy, lossless, no finger | drift 8e-14 to 2.7e-13 |
| 60 s random-gesture soak | no NaN or Inf, displacement bounded near 12 mm |
| Fingerboard barrier | stable for contact stiffness 1e9 to 1e13; a 20 N pluck touches the board from 41 to about 420 ms; spectral centroid 210 Hz with the barrier against 82 Hz without; CPU up 32% |

### What the spike changed in the design

- **Finger width must be set in grid cells, at least 4, not in millimetres.** At a fixed 15 mm the bump is 4 cells wide on E and 2.4 on G, and G fails tuning and zipper tests. Narrower than about 1.2 cells is unusable.
- **Finger stiffness trades against smoothness.** At stiffness 1e9 and above pitch no longer depends on stiffness, but the termination snaps to the grid and pitch steps up to 9 cents between cells. At 1e7 to 3e7 steps nearly vanish, but pitch depends on stiffness by about 10 cents per decade. The scheme holds stiffness fixed and calibrates one length offset per string. This calibration breaks if stiffness is later modulated (pressing harder) without a lookup table.
- **The nut side must be damped.** Without damping standing in for the player's other fingers, the nut-side segment couples through the finger, the octave note splits, and tuning error reaches 2.5 to 6 cents.
- **Numerical dispersion flattens high partials**: about -2.8 cents at partial 20 and -12 cents at partial 40 at the spike's stiffness. Running at twice the sample rate would fix it; the report leaves that to a listening decision.
- **A pluck aimed straight at the board slaps along the whole string** (contact 12 to 444 mm from the finger), not as growl near the finger. Real pizzicato is mostly parallel to the board, so localised growl probably needs a second polarisation or a smaller vertical share.
- **The first barrier attempt blew up.** Linearising the penalty and treating it semi-implicitly fed energy in at stiffness 1e11 and above. An energy-conserving discrete-gradient penalty, one scalar Newton solve per contact point, fixed it and was conserved to 5e-14.

Not done in the spike: no listening test, only E and G tuned (A and D untested) and only at one stiffness parameter, no barrier during slides, no soak with the barrier on, no second polarisation, no real-time block implementation.

## 3. Body and performance layer

- **Body: a fitted parallel resonator bank, feedforward first.** Twenty-four to forty-eight resonators after the string, fitted to recordings with fixed poles at known bass landmarks (an air mode near 65 Hz and a top mode near 115 Hz, from Brown's 2004 measurements), using the method of Bank's papers reimplemented from the description. Coupling the body back into the string is deferred until notes sound too even. No open double-bass body impulse response exists. Fit targets are CC0 samples (Karoryfer's double basses, VSCO-2 CE) and the anechoic University of Iowa notes. None is a jazz-setup bass, so they are starting presets.
- **A later physics pass moved the body from "fit to a reference" toward "measure a real bass".** A bridge hammer test on any upright (strings damped, two directions) with a modal fit is the cheapest source of body Q, which decides bloom and partial decay. Rau, Abel and Smith (DAFx-18) did this on one upright bass and fitted 88 modes up to 6 kHz but published no mode table. Whole-bass finite elements were rejected: no bass geometry is public, and a 2026 violin model took 8 to 10 hours per run and was capped at 4 kHz.
- **Performance interpreter.** It copies the inputs that the commercial reference visibly uses (key overlap, the new note's velocity, the interval), assigns strings automatically with a causal cost function because the player has no free hand for keyswitches, and needs no lookahead, since overlap is known at note-on. It was built early with the placeholder string because rendered tests cannot stand in for the player's hands.

## 4. Tooling and verification

- **Tooling.** Plain Rust: a `dsp` crate with no plugin dependencies, a `render` command-line tool (MIDI to WAV through the same code) and a thin plugin crate on nice-plug, the maintained successor to nih-plug, which delivers note-off velocity and raw CCs. No custom GUI in v1, since the host's generic parameter view covers it. Faust was dropped for the product because it handles per-sample events, state machines and moving contacts poorly. The Rust crate pins the framework version and builds on a host with an older glibc so the `.clap` loads on a newer one.
- **Verification.** Every commit: energy and stability property tests, tuning within a cent, no allocation on the audio thread, and clap-validator. Every round: an analysis pack (pitch, per-partial decay, attack, spectral distance to references) validated first on synthetic signals with known answers. Realism, feel and timing are judged by the player's ear only. Embedding metrics and audio-language models are not used as verdicts, because the research found nothing validating them for this.
- **What the verification caught.** In the first build round all four independent checks failed their property line, and every fix pass found the failures real: a listening page (three faults), a pitch tracker (octave errors on decaying notes, a phantom slide), a reference index (63 unmeasured files and mislabelled "pitched" sets) and the Rust build (clap-validator never run, a broken release test build). A later fuzz test failed on a subnormal output sample that neither builder nor checker had run.

## 5. Round plan and what happened

Each planned round ends in something the player can hear or play: (1) repo, placeholder string, interpreter skeleton, plugin loads in the host; (2) a listening page for level-matched A/B, analysis pack, reference corpus; (3) the finite-difference string behind the gesture interface; (4) fingerboard barrier, second polarisation, finger noises, four strings; (5) fitted body and mic or pickup blend; (6) interpreter constants from recorded playing and the reference measurements, pedal modes, velocity curve. Stop condition: after round 4, if the player still ranks it well below the commercial reference on the same phrases, stop and re-plan before polishing.

Recorded outcomes through 2026-11-13:

- **Placeholder tone.** A spectral comparison on a recorded take put the synth 14 to 36 dB brighter from 500 Hz to 2 kHz and 7 dB quieter. A two-pole tilt and a +6 dB trim brought bands from 45 Hz to 2 kHz within about 3 dB and loudness within about 1 dB. Not yet heard after the fix.
- **Slide rule.** The rule for deciding legato versus new note, fitted to the reference, matched its decisions on 85% of note pairs on the old string and 77% on the new one (up from 62% and 57%). It failed its check twice and was committed with the gaps listed rather than built a third time.
- **Attack study.** An attempt to reproduce the reference's pizzicato bloom failed its check twice. The agreed findings: the string technique can stay; two-way bridge coupling and a second polarisation did not help in the tests; the reference starts bright and darkens fast (upper partials fall at 90 to 160 dB/s early, then slower) while the model starts dull and rings; and the reference's broadband peak time depends on which partial lands on a body mode. The researchers disagreed on the cause of the fast darkening, offering four untested explanations (winding friction, finger and bridge loss, bridge admittance, release angle).
- **Real-reference diagnosis.** Re-measuring the gaps on real recordings replaced a guessed cause with a measured signature. Its first pass failed its check: onsets were 20 ms early on most soft Iowa notes because the files start inside the previous note's ring, and 19 pitches were mislabelled. Three headline claims were withdrawn.
- **Fingerboard contact in the full engine.** A hard board with a finger-pad gap produced almost no partial ripple and a state bug; switching to a soft board at zero gap fixed the bug and gave ripple, but hard notes now go dark then bright. The trade between ripple and brightness arc is a taste call, so it went to the player as two variants.
- **An outside review by a model from another family** raised ten points, nine accepted and one partly accepted, on the gesture contract and the string plan, including that the contract could not tell hammer-on, pull-off and fresh placement apart, that tuning was shown only over about an octave per string, and that energy conservation was shown only for a static contact.

## 6. What generalises

- A gate that a builder can pass on its own (energy, tuning, CPU) is cheap to automate; the realism gate is not, and was left to a listener.
- Measure the reference before building against it. Every gap here was first measured against one commercial product, and the same metrics on real recordings changed the analysis.
- A checker with a different model from the builder earned its cost in nearly every round, catching bugs, a withdrawn recommendation, a misattributed citation and an instability under adversarial drive. Strike two on a design is the point to diagnose, not rebuild.

## 7. Not checked

Nobody has listened to the finite-difference string, the fitted body, the slide rule or the contact variants through the plugin. Only E and G were tuned. The cost of a second polarisation, oversampling and dense contact has not been measured; two derived estimates for a published guitar scheme disagree (20 to 33% and 25 to 45% of a core per string) and the paper states neither sample rate nor grid size. Several literature claims are secondary or recalled: finger-release kinematics from harp work, tolerance figures for decay and glide, double-bass string heights from forum posts, and string tensions from retailer data. Cello loss constants (Mansour, Woodhouse and Scavone 2016) do not carry over to a bass. The commercial reference's internals are unknown. I did not open any source.

## 8. Sources

Links are those given in the original research notes.

- Bilbao, Russo, Webb, Ducceschi, *Real-Time Guitar Synthesis*, DAFx-24. https://dafx.de/paper-archive/2024/papers/DAFx24_paper_50.pdf . Closest existing real-time finite-difference model: stiff string, penalty fingerboard, finger mass, single polarisation.
- Ducceschi, Russo, Webb, *Measurement-Informed Nonlinear Modal Synthesis of 65 Classical Guitars*, DAFx-26 paper 40. https://www.dafx.de/paper-archive/2026/papers/DAFx26_paper_40.pdf
- Rau, Abel, Smith, bridge hammer test and modal fit of an upright bass, DAFx-18. https://ccrma.stanford.edu/~mrau/papers/DAFx2018_Rau_Abel_Smith.pdf
- Brown, double-bass body mode studies, 2004. https://awbmusic.com/wp-content/uploads/2021/06/2004_Acoustical_Studies_on_the_Flat_backed_and_Round_backed_Double_Bass.pdf
- Bank, parallel filter design with fixed poles. http://home.mit.bme.hu/~bank/parfilt/
- Smith, *Tension Modulation* and *String Collisions* (online book chapters). https://ccrma.stanford.edu/%7Ejos/pasp/Tension_Modulation.html , https://ccrma.stanford.edu/~jos/SMAC03S/String_Collisions.html
- nice-plug (CLAP and VST3 framework, ISC). https://codeberg.org/RustAudio/nice-plug
- clap-validator. https://github.com/free-audio/clap-validator
- Mansour, Woodhouse, Scavone 2016 (cello plucked-string model with measured body); Issanchou et al., JASA 2018 (nonsmooth string-obstacle contact on electric bass); Bilbao and Torin 2015 (guitar fretboard collision). Named in the notes without a stable URL that I could confirm.
- Open audio: Karoryfer double basses (CC0), VSCO-2 CE solo contrabass (CC0), University of Iowa Musical Instrument Samples double bass. No URLs were given in the notes.
