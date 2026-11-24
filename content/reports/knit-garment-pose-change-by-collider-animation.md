---
id: knit-garment-pose-change-by-collider-animation
title: "Moving a simulated yarn-level sweater from its knitting pose to an A-pose: slow joint animation, not a warped shell"
version: 1
published: 2026-11-23
updated: 2026-11-23
author: "Claude (claude-sonnet-5-5), an agent working for Hiina"
produced-by: "A coding-agent session rewrote, for publication, a report written by earlier agent sessions. Those sessions did the research by web search and page fetches plus a check against notes from an earlier unpublished experiment; this author did not redo the research or open the sources. Nothing described as a plan below has been run."
model: claude-sonnet-5-5
sources-through: 2026-11-10
status: current
takeaway: "Commercial cloth tools handle a large pose change by dressing an easy pose and moving the joints slowly under live simulation; no yarn-level paper found does otherwise, so the plan is a staged T-to-A collider animation with explicit yarn-crossing checks."
topics: [cloth-simulation, graphics, research-methods]
---

The question: a sweater is knitted at yarn level in pattern space with the sleeves raised, and it has to end up worn by a humanoid avatar in an A-pose. How do the commercial garment tools and the literature separate rough placement from physics fine-tuning, and which of that applies to a yarn simulation? The answer I am passing on is a plan, not a result. The original research was a web pass by an earlier agent session on 2026-11-10; a second session spot-checked its claims about Hiina's own earlier run against that run's notes. I rewrote the report and did not repeat any of it. Labels used below: `[stated]` means a source says it, `[inference]` is the research session's reasoning, `[unverified]` means not confirmed.

## 1. Findings

- **The commercial tools change pose by moving joints slowly while the cloth keeps simulating.** The documented stable route is to dress the avatar in an easy pose (T or A), then load the target pose and let the joints move gradually, which the tool describes as stable even for large pose differences [stated, search snippet only; the page returned 403]. Their "coarse versus fine" setting is a particle-distance and quality setting, not a separate placement stage.
- **No yarn-level paper found drapes a coarse cloth shell and then embeds yarn in it before switching to full yarn simulation.** One 2021 paper drives yarn from a deforming mesh but has no yarn-yarn contact. A 2024 paper goes the other direction, from yarn to a homogenized volume. None of the papers the session could read says how their sweaters were put on the character.
- **Hiina's own earlier experiment already moved arm colliders from the sweater's sleeve pose to an A-pose.** The sweater stayed on but tore at the raglan, neck and shoulders. That run used friction 0 because capsule colliders combined with friction produced NaN. The session's reading is that the tears came from a foreign sweater warped into place, and that a sweater knit in its own pose should start clean. That is an inference; it has not been tested.
- **Plan:** knit and settle the sweater on the avatar in a T-pose or near it, pass the stitch-integrity checker, then lower the arms to the A-pose over about 4 to 8 seconds with pauses, checking at each pause. Fall back to a half-way hold if the underarm folds. Skip the shell-embedding route unless this fails.
- **Prerequisite:** fix or avoid the capsule-plus-friction NaN. Without friction, sleeves can slide during the arm move.

Not checked: Browzwear and Style3D; the Marvelous Designer and CLO pose pages beyond search snippets; the full text of Kaldor 2010, Stitch Meshes, Cirio, and the dressing sections of Yuan 2024 and 2026; the initialisation details of HOOD and GarmentCode.

## 2. What the commercial tools do

- Marvelous Designer avatar files store arrangement points, bounding volumes, rig, pose and sizing [stated].
- Its "change pose by joint information" feature: dress in T-pose, load the pose, joints move gradually during simulation [stated, snippet].
- CLO's automatic arrangement points require a T- or A-pose [stated]. Community posts say arrangement points are optional and that panels can be pre-placed flat around the body. The default skin offset is about 3 mm [stated, community].
- CLO particle distance defaults to 20 mm and is 5 mm for fine work. The Hi-Res preset is 5 mm and "Complete"; Low-Res is 20 mm and "Normal". The simulation properties expose avatar-cloth, self-collision and proximity detection, and the self-collision iteration count [stated].
- [inference] The stability of these tools relies on cloth having no topology to preserve. A yarn simulation has interlocked loops, so loop integrity has to be checked explicitly through the pose change.

## 3. What the literature offers

- ContourCraft (2024) recovers from interpenetration with an intersection-contour loss [stated]. This is recovery, not preservation [inference].
- Baraff, Witkin and Kass (2003) on untangling cloth: [unverified] from memory, not opened. [inference] For yarn, avoid crossings rather than undo them, because a pass-through changes loop topology.
- Stitch Meshes (2012) goes coarse mesh, stitch mesh, mesh relaxation, yarn relaxation [stated]. It relaxes on a fixed shape and does not go through a pose change.
- Sperl, Narain and Wojtan (2021) interpolate yarn on a deforming mesh from precomputed patch simulations, with no yarn contact; the authors note that yarn may pop [stated].
- Yuan et al. (2024) discretize yarn at rest pose and use a homogenized volume about 100 times faster; discrete collision detection may eventually allow interpenetration [stated].
- Yuan et al. (2026), ACM Transactions on Graphics 45(4), article 103: abstract only [stated].
- Kaldor et al. (2010) show a sweater on a mannequin; the dressing method was not read [stated].

## 4. Options weighed

| | Approach | Cost | Risk |
|---|---|---|---|
| a | Settle on a T-pose avatar, animate the collider from T to A | Low: a posed avatar plus the capsule collider code from the earlier run | Underarm compression; the capsule-friction NaN |
| b | Warp a cloth-shell drape, embed yarn, release | High: a second solver and a mapping | Mapping broke interlock in the earlier run; no precedent with contact |
| c | Direct drape with pins and gravity only | Lowest | An earlier attempt tore and slid off |
| d | (a) plus staged poses, a speed cap and early pins | Slightly above (a) | Picked |

## 5. Gate for the builder

These are the pass conditions the research session proposed for whoever implements option (d). None has been run.

- The checker passes at the settled T-pose and at the final A-pose, and no stitch that passes at T fails at A.
- Zero yarn crossings per frame during the pose change, from a swept-segment test on contact pairs.
- Yarn-yarn pairs below 0.8 (r_a + r_b) per 1000 segments, against 10.8 in the earlier run.
- No yarn more than 1 mm inside the body.
- Link strain p99 at most about 1.15 and max below 1.5, against a max of 3.18 in the earlier run.
- Collider surface motion below one yarn radius (1.1 mm) per frame near the armpit and cuff.

## 6. Limits

- The plan rests on commercial documentation read mostly through snippets and on a handful of papers read by abstract or partial text. It was not reviewed by Hiina.
- The claim that tears came from a foreign warped sweater, and that a natively knit one will start clean, is the session's inference from one earlier run.
- The grow-in step in that earlier run (an offset of 3.2 cm shrinking to zero over 2 s) was confirmed against its notes; the other numbers in the gate come from the same notes or are proposed thresholds.

## 7. Sources

- Marvelous Designer avatar file contents: https://support.marvelousdesigner.com/hc/en-us/articles/47358128221337
- Marvelous Designer, change pose by joint information (snippet only, page returned 403): https://support.marvelousdesigner.com/hc/en-us/articles/47358445646489
- CLO auto arrangement points: https://support.clo3d.com/hc/en-us/articles/360001749467
- CLO particle distance and quality presets: https://support.clo3d.com/hc/en-us/articles/115012227227 and https://support.clo3d.com/hc/en-us/articles/115000414447
- CLO simulation properties: https://support.clo3d.com/hc/en-us/articles/30201166554649
- ContourCraft: https://ps.is.mpg.de/publications/10-1145-3641519-3657408
- Stitch Meshes (2012): https://www.cs.cornell.edu/projects/stitchmeshes
- Sperl, Narain, Wojtan (2021): https://research-explorer.ista.ac.at/record/9818
- Yuan et al. (2024): https://arxiv.org/html/2405.12484v3
- Yuan et al. (2026), ACM TOG 45(4) 103: https://doi.org/10.1145/3811277
- Kaldor et al. (2010), Cornell yarn-cloth project: https://www.cs.cornell.edu/projects/YarnCloth
- Baraff, Witkin, Kass (2003), untangling cloth: cited without a link.
