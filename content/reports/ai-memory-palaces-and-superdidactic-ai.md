---
id: ai-memory-palaces-and-superdidactic-ai
title: AI memory palaces and superdidactic AI
version: 2
published: 2026-10-27
updated: 2026-10-27
author: Hiina
produced-by: "Claude deep-research run with citation checking"
model: claude-opus-5-5
sources-through: 2026-10-26
status: current
takeaway: "An AI-built memory palace is the wrong shape for project re-entry; self-written cues, stated intent and recall-before-reveal briefs are what restore a headspace, and AI tutoring helps only modestly."
topics: [agent-supervision, ai-tutoring, spaced-repetition, learning-science]
---

An AI-built memory palace is the wrong shape for getting someone back into a project, but the question behind it is right and mostly unstudied. Re-entry works through a few cues: the person's own earlier words, where things stand, what they meant to do next, and being made to recall the intent before being told it. Superdidactic AI is real but modest, and the limits sit on the learner's side. Everything past that, from sleep learning to uploads, either doesn't work yet or isn't close.

The motivating use case is a solo builder who supervises many agent projects through a decision queue: agents do the work and surface the choices that need a human. The question was whether AI could rebuild the builder's headspace for each choice, how far AI teaching can go, and where the spectrum ends, from memory palaces through sleep learning and brain-computer interfaces to uploads.

## 1. Summary

| Part of the spectrum | What's actually true | Status |
| --- | --- | --- |
| Memory palaces | Large effects for ordered lists only; a richer room doesn't help | Proven, wrong target |
| Project re-entry cues | Own-words cues \~90% vs 5–17%; automated traces 2x notes; showing agent reasoning catches bad plans 81% vs 55% | Strong pieces, never assembled; gap is real |
| AI tutoring | 0.1–0.3 SD at scale, \~0.6 in a tight trial; 2 sigma was never real | Real, modest |
| AI persuasion as mirror | Information density drives it; personalization adds \~0.4 pp | Teaching gets the dense part, not the retrieval |
| ML spaced repetition | Neural schedulers beat FSRS on log loss; LLM cards need human-picked targets; varied cues beat fixed | Scheduler solved, deck replacement promising |
| Sleep learning and TMR | New learning in sleep is tiny and implicit; TMR g ≈ 0.13–0.29; slow-wave stimulation ≈ 0 | Mostly no |
| Nudges and JITAIs | Bias-corrected effects small and decaying; capture and specific cues matter more than timing | Real, small |
| Neural UIs and BCI | Pixel-rendered desktops can't hold state or text; BCIs reached \~mouse parity at \~10 bits/s | Far |
| Uploads and "the soul" | Emulation not close even for a worm; distilling a work policy has 50 years of precedent | Policy yes, self no |

The most promising build is a re-entry card on each decision-queue item (section 7, build 1). It's a weekend of work, and the queue's own history gives the baseline: in the motivating setup, asks answered live took minutes, while asks left in notes took 12–62 days. This report builds on a [companion report on personal web-surfing models](https://ai.hiina.space/reports/personal-web-surfing-models.md) and the ought-driven tab feed it proposes, and doesn't repeat the companion reports on [AI enfeeblement and idle supervisors](https://ai.hiina.space/reports/ai-enfeeblement-and-the-peter-principle.md), or on [AI meditation and flow steering](https://ai.hiina.space/reports/ai-meditation-and-flow-steering.md).

## 2. Context reinstatement: prompt engineering the human

A literal memory palace is the wrong tool for getting someone back into a project: its evidence covers ordered lists, and a richer environment isn't what makes it work. What restores a headspace well enough to decide is a short set of externalized cues: where things stand, what the person meant to do next, and their own earlier words. It works best when the brief makes them retrieve the intent before it tells them. I found no controlled study of an AI building a palace or reinstatement environment for someone's project state; that gap is real.

The motivating setup has already measured the cost. An unpublished practice review of its decision queue found that asks answered live took minutes, while asks left in notes sat 12–62 days. Most of that gap is plausibly re-entry cost, the effort of getting back into a project before being able to answer.

### Memory palaces work for lists, not judgment

| Study | Result | Caveat |
| --- | --- | --- |
| [2025 meta-analysis](https://www.fss.muni.cz/vyzkum/publikace/prehled/2496979) | d = 0.88 for immediate serial recall | Evidence quality rated low to very low |
| [Twomey & Kroneisen 2021](https://journals.sagepub.com/doi/10.1177/1747021821993457), 13 RCTs | g = 0.65 | High risk of bias |
| [Dresler 2017](https://med.stanford.edu/news/all-news/2017/03/memorization-tool-bulks-up-brains-internal-connections.html) | 6 weeks of daily training took novices near memory-athlete level; held at 4 months | Word lists; one study |
| [Krokos et al. 2019](https://obj.umiacs.umd.edu/virtual_reality_study/10.1007-s10055-018-0346-3.pdf), VR headset vs desktop | 84% vs 75% recall, N = 40 | Immersion confounded with head-tracking |
| [Legge et al. 2012](https://www.psych.ualberta.ca/~cml/papers/LeggEtal2012.pdf), N ≈ 141 | A detailed virtual palace was no better than imagining one's own home (d = 0.03 between them) | Only 40–57% complied with the strategy |

Every outcome here is recall of arbitrary items. Nothing I found tests gist, understanding or decisions. Legge's result matters most for the AI-palace idea: the active ingredient is the learner doing the imagery work, not the fidelity of the room. An AI that builds the room removes the part that doesn't matter.

The AI-built versions so far are small. [SMART](https://www.umiacs.umd.edu/about-us/news/umd-team-uses-ai-enhance-mnemonic-learning) (EMNLP 2024) generates vocabulary keyword mnemonics and tunes on what actually produced learning rather than what students said helped. A [30-student pilot](https://www.jstage.jst.go.jp/article/his/27/4/27_261/_article/-char/en) of AI-suggested loci associations improved 24-hour recall, and its authors warn that AI examples far from the learner's own thinking can interfere. A 2026 ACM paper on AI-assisted loci in VR exists but its page wouldn't load. A [critique of MemPalace](https://arxiv.org/html/2604.21284v1), the agent-memory system, found the palace hierarchy adds nothing to retrieval over plain metadata filtering.

### Context helps a little, and strong cues cancel it

Physical context-dependent memory is real but modest: mean d ≈ .28 across Smith & Vela's meta-analysis, mostly in free recall ([Smith et al. 2014](https://people.tamu.edu/~stevesmith/Smithetal2014.pdf)). Two moderators decide whether it shows up. "Outshining": when other good cues are present at test, context stops mattering. And mental reinstatement at test reduces the cost of a changed environment ([Smith & Vela 2001 abstract](https://doi.org/10.3758%2fBF03196157)), though a [four-experiment thesis](https://scholars.wlu.ca/etd/1954) failed to get imagined reinstatement to help.

The applied version is strong. The cognitive interview, which has people mentally reinstate context and freely report before being asked specifics, raised correct details by d = 0.87 over 42 studies, with a small rise in errors (d = 0.28) ([Köhnken et al. 1999](https://researchportal.port.ac.uk/en/publications/the-cognitive-interview-a-meta-analysis/)).

The implication is uncomfortable for briefs. A brief that states everything is a strong recognition cue, which outshines the reader's own retrieval. A brief that first asks "what were you trying to get out of this, and what did you rule out?" and then reveals the record keeps more of the original intent in play.

### Mood boards and project rooms

There is no quantitative evidence that mood boards improve recall or decisions; the literature is qualitative ([McDonagh & Storer 2005](https://experts.illinois.edu/en/publications/mood-boards-as-a-design-catalyst-and-resource-researching-an-unde/)). The best "project room" evidence is [Teasley et al. 2000](https://public.websites.umich.edu/~igri/publications/Teasley%20et%20al_00.pdf): six collocated war-room teams at about double baseline productivity, confounded with timeboxing. The mechanism the authors saw was not ambience. It was visible artifacts that kept a permanent record of decisions and status at a glance. A browser full of deliberately kept-open tabs is a self-built version of that; whether AI curation beats self-curation is untested.

### Resumption after interruption

- **The "23 minutes" figure is a rounding.** [Mark et al. 2005](https://www.interruptions.net/literature/Mark-CHI05-p321-mark.pdf) followed 24 workers; same-day resumption averaged 25 min 26 s, after 2.26 other tasks. The paper has no 23:15.
- **Preparation is mostly about the next goal.** In [Trafton et al. 2003](https://interruptions.net/literature/Trafton-IJHCS03.pdf), 62% of pre-interruption rehearsal was prospective goal setting and 79% referred to information visible on screen.
- **A one-minute exit note works.** Leroy & Glomb's "ready-to-resume plan" (where you stopped, what's next, what's still hard) cut attention residue in two lab studies ([summary](https://www.futurity.org/ready-to-resume-plan-1656322/)).
- **Automated traces beat notes.** Programmers given automatic chronological, code-snippet cues had about twice the task success of those relying on their notes ([Parnin & DeLine 2010](https://www.microsoft.com/en-us/research/publication/evaluating-cues-for-resuming-interrupted-programming-tasks/)).
- **Open loops don't nag usefully.** A 2025 meta-analysis found no Zeigarnik effect: recall ratio of unfinished to finished tasks 0.99 ([Ghibellini & Meier](https://ideas.repec.org/a/pal/palcom/v12y2025i1d10.1057_s41599-025-05000-w.html)).

### What makes a brief restore intent

The causal evidence comes from medicine and human-automation work, not from decision memos:

- **Structure plus training cut errors.** The I-PASS handoff bundle reduced medical errors 23% and preventable adverse events 30% across 10,740 admissions, without longer handoffs ([Starmer 2014 via HMS](https://hms.harvard.edu/news/safer-patient-handoffs)). The format and the training can't be separated.
- **Showing reasoning and projection catches bad plans.** When an agent's display added its reasoning and its predicted outcome, people correctly rejected bad agent plans 81% of the time vs 55% with status alone, with no extra workload or time ([Mercado et al. 2016](https://journals.sagepub.com/doi/reader/10.1177/0018720815621206), N = 30). This maps directly onto reviewing agent proposals.
- **Intent transmits badly by default.** In Shattuck & Woods' study, subordinates' actions matched the commander's intent in 34% of 32 episodes once coincidental matches were removed ([summary](<https://en.wikipedia.org/wiki/Intent_(military)>)). Klein's intent template has seven parts: purpose, end state, sequence, rationale, key decisions, antigoals and constraints.
- **Self-written cues beat anyone else's.** Mäntylä 1986: people recalled about 90% of words from three cues they wrote themselves vs 5–17% from cues others wrote ([Wheeler & Gabbert 2017](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2017.01830/pdf)). The advantage shrinks with delay and with cues written for someone else. An agent summary is the "other-generated cue" condition.
- **People don't remember their reasons later.** Only about one in five students gave consistent reasons for a past choice months later ([Kaasa, Morris & Loftus 2011](https://bps.org.uk/research-digest/how-reliable-our-memory-our-own-previous-intentions)). Reasons have to be captured when they are given.
- **Rationale capture fails on cost, not value.** Design-rationale tools like IBIS and QOC failed because the writer pays and someone else benefits ([Buckingham Shum et al.](https://research-archive.stem.open.ac.uk/stemra-data/uploads/files/KMI-05-18.pdf)). In agent-run projects the agents pay that cost, so my inference is that the old objection mostly disappears.

No study compares an AI-written brief, the person's own notes and raw artifacts for decision quality after a delay, and I found no controlled test of narrative vs bulleted decision memos. Those are real gaps.

Putting it together, "prompt engineering the human" for one decision-queue item would look like this (my synthesis, not a tested format):

1. Ask the decision-maker one or two open questions about the project's purpose and antigoals before showing anything.
2. Show their own earlier words on it, verbatim and dated.
3. Give state plus the intended next step, Leroy-style, and the decision with its default.
4. Give the agent's reasoning and its predicted outcome per option, Mercado-style.
5. Link a chronological trace of what changed since they last looked, Parnin-style.
6. Capture the reason with the answer, so the next re-entry has the decision-maker's words to show.

## 3. Superdidactic AI

AI tutors are good but not magic: about 0.1–0.3 SD at scale and around 0.6 SD in a tight lab trial, against a 2-sigma benchmark that was never real. Persuasion and teaching share one active ingredient, dense relevant information, and personalization adds little to either. The binding constraints are on the learner's side: engagement, retrieval effort and an encoding rate near 2 bits/s.

### Tutoring effect sizes

| Study | Effect | What limits it |
| --- | --- | --- |
| Bloom 1984 "2 sigma" ([von Hippel 2024](https://www.educationnext.org/wp-content/uploads/2024/03/ednext_XIV_2_von_hippel.pdf)) | 2.0 SD | Two PhD studies, \~200 students, 3 weeks, aligned tests; mastery learning alone gave \~1.1 |
| Human tutoring, 263 RCTs ([Kraft, Schueler & Falken 2026](https://journals.sagepub.com/doi/10.3102/00346543261446660)) | \~0.40 SD | 0.16–0.22 on independent tests; 0.16 for programs over 1,000 students |
| Harvard physics AI tutor ([Kestin 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12179260/), N = 194) | 0.63 SD vs active-learning class (0.73–1.3 by quantile regression) | First exposure only; a [re-analysis](https://clayford.net/posts/ai_tutoring_nature/index.html) puts it nearer 12–26% higher scores |
| GPT-4 after-school, Nigeria ([De Simone 2025](https://openknowledge.worldbank.org/bitstreams/cd9cca5b-2ffd-4be1-8313-0f4d2ed6ef4f/download)) | 0.23–0.31 SD in 6 weeks | Attrition; one school drives significance |
| Khanmigo, 2-year cluster RCT ([Oreopoulos & Low 2026](https://www.nber.org/papers/w35620)) | 0.06–0.08 SD per year | Students messaged it on a median \~33% of practice days, mostly bare answers |
| AI and adaptive ed-tech, 14 RCTs ([World Bank 2026](https://thedocs.worldbank.org/en/doc/2fba81cd6cd60d2f54532fc7062395fb-0050062026/original/Can-EdTech-Close-Learning-Gaps.pdf)) | 0.125 SD | No evidence generative AI beats older adaptive tech |
| Unrestricted GPT-4 for practice ([Bastani 2025](https://ideas.repec.org/a/nas/journl/v122y2025pe2422633122.html)) | +48% practice, −17% later test | A guardrailed tutor removed the harm but didn't beat control |
| DARPA Digital Tutor ([IDA D-5358](https://apps.dtic.mil/sti/pdfs/AD1002362.pdf)) | g = 4.19 vs fleet techs | Non-randomized, 12 per group, \~8 hours a day, evaluated by its promoter |

One thing to drop: the Wang & Fan ChatGPT meta-analysis (g = 0.867) was [retracted in 2026](https://www.plagiarismtoday.com/2026/07/15/study-claiming-ai-helps-students-learn-retracted/).

### Persuasion as the mirror

The largest persuasion study, [Hackenburg et al. in Science 2025](https://researchonline.lse.ac.uk/id/eprint/130605) (76,977 people, 19 models), maps the levers cleanly. Information density correlated r = 0.76 with persuasion and an information-focused prompt added +2.29 pp. Personalization added +0.43 pp, and each 10x of model scale about +1.6 pp. 36–42% of the effect remained a month later. The warning sign: GPT-4o's claims were 62% accurate under the information prompt, against 78% under another prompt. [Costello, Pennycook & Rand](https://www.niemanlab.org/2024/09/an-ai-chatbot-helped-americans-who-believe-in-conspiracy-theories-exit-the-rabbit-hole/) found \~20% durable reductions in conspiracy belief, again from tailored evidence.

So "superpersuasive" mostly means "superdense with relevant claims", and teaching gets that part for free. What persuasion doesn't need and learning does is the learner's own retrieval: belief can update from one conversation, but a skill needs effortful practice spread over time. Khanmigo shows the failure mode, a well-built tutor students barely used. Bastani shows the other: an AI that does the work for the learner raises practice scores and lowers learning. I found no study comparing one model's persuasion effect with its teaching effect.

The ceiling is the human. [Landauer 1986](https://home.cs.colorado.edu/~mozer/Teaching/syllabi/7782/readings/Landauer1986.pdf) estimated long-term memory takes in about 2 bits/s, reaching \~10⁹ bits by midlife. Deliberate practice explains only \~12% of performance variance overall and under 1% in professions ([Macnamara 2014](https://www.psychologicalscience.org/news/releases/becoming-an-expert-takes-more-than-practice.html)). A superdidactic AI can remove dead time and choose what to practice; it can't raise the encoding rate.

### ML spaced repetition: scheduler, cards, deck

**The scheduler is mostly solved, and better models buy little.** On the [srs-benchmark](https://github.com/open-spaced-repetition/srs-benchmark) (\~10k Anki collections, \~350M reviews, no same-day reviews):

| Model | Parameters | Log loss | AUC |
| --- | --- | --- | --- |
| RWKV-Instant (pooled) | 2.76M | 0.277 | 0.833 |
| GRU / LSTM | 503 / 8,869 | 0.333 | 0.73 |
| FSRS-7 | 35 | 0.340 | 0.717 |
| FSRS-6 (Anki default lineage) | 21 | 0.346 | 0.703 |
| DASH | 9 | 0.368 | 0.631 |
| HLR (Duolingo 2016) | 3 | 0.469 | 0.637 |

The neural models predict recall noticeably better, but a better recall predictor mostly saves review time at a fixed target retention rather than raising retention. FSRS's 21–35 interpretable parameters and its desired-retention knob are a plausible reason it ships and RWKV doesn't; the README gives no reason. I found no RCT of FSRS vs SM-2 on learning outcomes.

**Content-aware scheduling looks better offline than online.** [KAR3L](https://arxiv.org/pdf/2402.12291) (EMNLP 2024) used card text to reach AUC 0.864 vs FSRS's 0.752 offline, but in its 27-user online test accuracy was no better (0.86 vs 0.88). [LECTOR](https://arxiv.org/html/2508.03275)'s gains come from simulated learners only.

**LLM-written cards need a human to pick the targets.** In a [Brown medical school pipeline](https://www.medrxiv.org/content/10.1101/2025.05.13.25327518v1.full.pdf), 4.8–6.4% of generated cards were hallucinated and \~21.5% needed edits for information density, too much or too little. Matuschak's [notes](https://notes.andymatuschak.org/zomoPzCNzSi5GqtfTeVWgm7RjmiArjS8vvM5) found GPT-4 writes usable declarative prompts when given pre-selected targets and an angle hint, and fails on conceptual material. A personal anime-subtitle vocabulary premine pipeline, which mines candidate words and example lines from subtitle files into Anki, already works this way: the pipeline picked targets, and the hard part was filtering, not generation.

**Replacing the deck has one good result behind it.** Varied retrieval cues beat a fixed cue across seven experiments, and learners wrongly judged the fixed cue better ([Butowska-Buczynska et al., PNAS 2024](https://share.swps.edu.pl/handle/swps/1120)). That supports an LLM generating fresh questions per review from a learner's notes. Nobody has tested conversational review against fixed cards over months, or LLM grading of free recall inside the loop; both gaps look real. The base effects are solid: retrieval practice g = 0.50 ([Rowland 2014](https://courseware.epfl.ch/assets/courseware/v1/fdde2f0aa590bf3b1324077a6bf1540c/asset-v1%3AEPFL%2BDEMO%2B2020%2Btype%40asset%2Bblock/Rowland2014-meta-analysis.pdf), 0.73 with feedback), and the optimal gap shrinks from 20–40% of a one-week retention interval to 5–10% of a one-year one ([Cepeda 2008](https://pubmed.ncbi.nlm.nih.gov/19076480/)).

### The realistic "I know kung fu"

The closest real thing to a download is perceptual learning. Kellman-style modules in histopathology gave effect sizes of 0.8–1.6 on a speed-plus-accuracy score after 11–18 minutes of training, with speed gains lasting 6–7 weeks ([Krasne et al. 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3908489)). They work by many short trials over varied examples, adaptive sequencing, and retiring items after three fast correct answers. That is spaced repetition applied to pattern recognition.

My inference for the near-term stack: an LLM picks targets from the learner's own material, generates varied retrieval prompts, a neural or FSRS scheduler spaces them, perceptual modules cover recognition-heavy parts, and a coach keeps engagement up. That might compress the declarative and perceptual parts of a skill several-fold. It does nothing for motor skill or the judgment that comes from consequences, and I found no sourced figure for what share of a skill is declarative.

## 4. Sleep, subliminal and targeted memory reactivation

You can't learn anything useful from scratch while asleep, and subliminal persuasion is dead. Re-cueing memories learned awake (targeted memory reactivation, TMR) works a little in the lab, about g = 0.13–0.29 depending on how one corrects for publication bias. The one technique that looked strong, closed-loop auditory stimulation, has regressed to roughly zero for memory. Nobody has tested whether personalization rescues any of it.

### What the evidence says

| Claim | Best evidence | Verdict |
| --- | --- | --- |
| Learn new material in sleep | [Koroma 2022](https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2022.801666/pdf): N=22, 59% vs 50% chance, implicit only; [Züst 2019](https://mediarelations.unibe.ch/media_releases/2019/medienmitteilungen_2019/learning_new_vocabulary_during_deep_sleep/index_eng.html) word pairs in slow-wave up-states | Real but tiny and unconscious. Awake learning hit 88% after 4 exposures vs 59% after \~40 in sleep |
| TMR boosts awake-learned memories | [Hu et al. 2020](https://faculty.wcas.northwestern.edu/paller/PsychBulletin2020.pdf): 91 experiments, 2,004 people, g = 0.29; skills \~0.44–0.51, language 0.40, declarative 0.23, REM \~0 | Small, bias-adjusted 0.13–0.18, I² = 71%. Effects fade by 6–8 weeks ([Carbone & Diekelmann 2024](https://www.nature.com/articles/s41539-024-00244-8)) |
| TMR changes attitudes or habits | Implicit-bias result failed replication ([Humiston & Wamsley 2019](https://ideas.repec.org/a/plo/pone00/0211416.html), power 0.9) | Don't count on it |
| Closed-loop slow-wave stimulation | [Harlow et al. 2023](https://public-pages-files-2025.frontiersin.org/journals/sleep/articles/10.3389/frsle.2023.1082253/text): 12 studies, effect falls from d ≈ +0.99 (2013) to −0.39 (2021); publication year explains 92% of heterogeneity | Boosts slow waves, not memory ([Henin 2019](https://www.eneuro.org/content/6/6/ENEURO.0306-19.2019)) |
| Consumer sleep headbands for memory | Elemind's evidence is sleep onset ([IEEE Spectrum](https://spectrum.ieee.org/elemind-neuromodulation)); no peer-reviewed memory RCT found for any device | Don't buy one for learning |
| Home TMR | [Göldi & Rasch 2019](https://link.springer.com/article/10.1038/s41539-019-0044-2): N=66, null overall; helped undisturbed sleepers, hurt those the cues woke | Possible only if the cues never wake the sleeper |
| Subliminal self-help audio | [Greenwald 1991](https://www.Gwern.net/doc/psychology/1991-greenwald.pdf) double-blind, 237 people: content did nothing, perceived gains followed the label | Placebo |
| Subliminal priming generally | Independent replications average d ≈ 0.002 vs 0.40 when an original author is involved ([Meta-Psychology](https://open.lnu.se/index.php/metapsychology/article/view/3308)) | Mostly not real |

Two things sit outside memory. Targeted dream incubation (Dormio) reported creativity scores 43% higher than an unincubated nap in N=49, per [MIT News](https://news.mit.edu/2023/sleep-sweet-spot-dreams-creativity-0515), with no standardized statistics. Two-way communication with lucid dreamers works but rarely: 29 correct answers from 158 attempts ([Konkoly 2021](https://bpb-us-e1.wpmucdn.com/sites.northwestern.edu/dist/4/2492/files/2026/04/Konkoly_2021_Curr_Biol.pdf)).

### Would fine-tuning to one human help?

The gap is real: I found no study where personalized cue timing, cue selection or a per-person model improved a memory outcome. Phase-targeting algorithms work technically, and one [2025 preprint](https://www.medrxiv.org/content/10.1101/2025.11.12.25340010v1.full.pdf) (N=28) predicted memory responders with AUC 0.92, post hoc and with trends only at p ≈ 0.07.

The harder problem is the target. Harlow et al. found the memory-benefit score has test-retest reliability of about r = .01, so per-person optimization would be fitting noise. And because slow waves can be pushed up without memory following, a closed-loop optimizer would happily optimize the wrong variable. A personalization project here would need many nights per person and a within-person cued-vs-uncued design before it could learn anything.

The defensible practice is boring: study before sleep and spread material across nights. For tinkerers, low-volume odor or sound cues on half of tonight's items, with the other half as control, is cheap. Expect a small effect at best.

## 5. Anki for what you ought to do, and the interface endgame

Prompting people toward their own goals works, but after bias correction the effects are small and they decay. The value of a personal agent assistant is more likely in capturing intentions that would otherwise be lost and tying them to concrete cues than in clever timing. Nobody has framed intentions as a spaced-repetition problem; the gap is real, and the building blocks exist.

### The effect sizes, corrected

| Intervention | Naive effect | After bias correction or at scale |
| --- | --- | --- |
| Implementation intentions ([Sheeran, Listroma & Gollwitzer 2025](https://kops.uni-konstanz.de/server/api/core/bitstreams/d703c468-46e9-47fc-8900-d32d7d19c8d9/content), 642 tests) | d = .36 | d = .15 (RoBMA); field about half of lab |
| Nudges in general ([Maier et al. 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9351501)) | d = .43 (Mertens 2022) | d ≈ .04 |
| Nudge units ([DellaVigna & Linos 2022](https://www.nber.org/papers/w27594), 126 RCTs, 23M people) | 8.7 pp in journals | 1.4 pp in deployed trials |
| Gym megastudy ([Milkman 2021](https://authors.library.caltech.edu/records/mys88-cc756), 61,293 people) | 45% of 54 interventions beat control | 8% still worked after the program ended |
| Flu-shot texts ([Milkman 2022](https://knowledge.uchicago.edu/record/9653/files/milkman-et-al-2022-a-680-000-person-megastudy-of-nudges-to-encourage-vaccination-in-pharmacies.pdf), N = 689,693) | best +2.7 pp | experts couldn't predict winners (r = 0.03) |
| HeartSteps just-in-time prompts ([Klasnja 2019](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:30192907%20AND%20SRC:MED&resultType=core&format=json), N = 44) | +107% steps early | +14% overall (p = .06), fading over weeks |
| Chatbot exercise coaching ([meta-analysis, 12 RCTs](https://pmc.ncbi.nlm.nih.gov/articles/PMC12254675)) | SMD .29 under 8 weeks | .06 past 8 weeks; no LLM trials included |
| Commitment contracts ([Giné, Karlan & Zinman](https://poverty-action.org/sites/default/files/publications/put_your_money_where_your_butt_is.pdf)) | +3.4–5.7 pp quit at 12 months | only 11% took the contract |

LLM-specific evidence on behavior is close to nil. The one randomized field trial found is a [2026 preprint](https://arxiv.org/abs/2604.03881) with 233 dorm residents: LLM-personalized messages cut electricity use relative to plain text feedback, with no significant effect on hot water. [GPTCoach](https://hci.stanford.edu/publications/2025/Joerke_GPTCoach.pdf) measured no behavior at all.

### What the literature says to build

- **Specific cues beat reminders.** Plans with a time and a place outperform time alone (d = .46 vs .25 in the 2025 meta-analysis). An assistant that turns "I should look at that design decision" into "after coffee Saturday, at the desk, open the queue" is doing the active ingredient.
- **Timing by receptivity is worth something.** ML-timed messages got up to 40% better receptivity than random timing ([Mishra 2021](https://arxiv.org/abs/2011.08302)), with predictors like phone use, activity and time of day ([Künzler 2019](https://cs.dartmouth.edu/dfk/research/kunzler-receptivity/index.html)).
- **Novelty decays, so rotate.** Duolingo's recovering bandit penalizes recently used message templates with a 15-day half-life ([Yancey & Settles 2020](https://research.Duolingo.com/papers/yancey.kdd20.pdf)). The online gain was +0.4–0.5%, a reminder that timing optimization is a small lever.
- **People under-offload.** Gilbert's lab finds people are underconfident in unaided memory yet set reminders by perceived rather than actual need, and reminders help most under high load ([Chiu & Gilbert 2023](https://discovery.ucl.ac.uk/10176285/1/chiu-gilbert-2023-express-influence-of-the-physical-effort-of-reminder-setting-on-strategic-offloading-of-delayed.pdf)). Capture is the bigger win.
- **Fade prompts to build a habit.** [Wood & Rünger 2016](https://dornsife.usc.edu/wendy-wood/wp-content/uploads/sites/183/2023/10/wood.runger.2016.pdf) argue habits bind to stable context cues; an external prompt that never fades substitutes for the internal cue. That is the same tension the [companion report on AI enfeeblement](https://ai.hiina.space/reports/ai-enfeeblement-and-the-peter-principle.md) covers from the other side.

An "SRS for intentions" would treat each commitment as a card: dense prompts right after a plan is formed, lengthening intervals when the person acts, shorter ones and a changed cue after a miss, a contextual bandit with a dose penalty picking time and channel, and rotated wording. HeartSteps and Oralytics already encode prompt "dosage" as a decaying count with a burden cost ([Oralytics design](https://arxiv.org/html/2406.13127v1)). The difference from flashcards is the outcome signal: "did it" is sparse and late, where recall is graded instantly. The ought-driven tab feed in the [companion report on personal web-surfing models](https://ai.hiina.space/reports/personal-web-surfing-models.md) is the reading-side instance of the same scheduler.

### Model-rendered computers

Pixel-rendering world models went from DOOM at \~20 fps ([GameNGen](https://arxiv.org/abs/2408.14837), 2024) to 720p at 24 fps with about a minute of visual memory ([Genie 3](https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/), 2025). Memory horizons are still minutes. The only real "neural desktop", [NeuralOS](https://arxiv.org/abs/2507.08800) (ICLR 2026), runs 512×384 at 18 fps on an H100 after \~23k GPU-hours. It tracks the cursor to 1.6 px but predicts the right state transition only 37.7% of the time, recalls a created folder about half the time after 64 frames, and can't reliably render typed characters. Its authors call inference too costly for practical use.

Production generative UI is LLM-written code, not pixels: [Google's Generative UI](https://research.google/blog/generative-ui-a-rich-custom-visual-interactive-user-experience-for-any-prompt/) (Gemini 3, Nov 2025) and Anthropic's five-day Imagine with Claude preview. The evidence is rater preference over chat, not task performance. The only measured performance gain for generated personalized UIs is old and narrow: [SUPPLE++](https://www.eecs.harvard.edu/~kgajos/papers/2008/gajos08improving.shtml) made motor-impaired users 26.4% faster with 73% fewer errors. Adaptive-UI research also warns that interfaces that keep changing break motor memory ([Findlater 2009](https://www.cs.ubc.ca/labs/edapt/papers/findlater2009.pdf)). For the "computer optimized for what one ought to do" endpoint, that argues for model-generated but stable surfaces with state kept in ordinary program memory, not a model streaming pixels.

### BCI as the endpoint

| System | Throughput | Caveat |
| --- | --- | --- |
| [Willett 2023](https://www.nature.com/articles/s41586-023-06377-x) speech implant | 62 wpm, 23.8% WER at 125k words | 1 participant |
| Metzger 2023 ECoG ([summary](https://physicsworld.com/a/high-performance-brain-implants-restore-communication-to-those-who-cannot-speak/)) | 78 wpm, \~25% WER | 1 participant |
| [Card 2024](https://profiles.wustl.edu/en/publications/an-accurate-and-rapidly-calibrating-speech-neuroprosthesis/) speech implant | \~32 wpm, 97.5% over 8.4 months | 1 participant |
| Neuralink cursor ([Decrypt](https://decrypt.co/230021/neuralink-implant-patient-gaming-sets-bci-record)) | 8 bits/s (2024); "above 10" claimed 2026 | company-reported only |
| Meta sEMG wristband ([The Register](https://www.theregister.com/2025/07/23/meta_wristband_ui_control/)) | 20.9 wpm handwriting, no calibration | phone keyboard is \~36 wpm |
| [Brain2Qwerty](https://arxiv.org/abs/2502.17480) non-invasive | 32% character error (MEG), 67% (EEG) | 35 volunteers |

Writing into the brain is much further behind. Tactile microstimulation halved a grasp task's time in one participant ([Flesher 2021](https://pubmed.ncbi.nlm.nih.gov/34016775/)), visual-cortex arrays give crude phosphenes and a few letters ([Fernández 2021](https://research.vu.nl/en/publications/visual-percepts-evoked-with-an-intracortical-96-channel-microelec/)), and nothing credible writes semantic content.

The deeper constraint is [Zheng & Meister](https://arxiv.org/abs/2408.10234): human behavior runs at about 10 bits/s against \~10⁹ bits/s of sensory input. Motor BCIs have reached roughly mouse parity, which is about where that ceiling sits. If the bottleneck is central, a better pipe doesn't help much. The "computer optimized for what you ought to do" is then the one that spends a person's 10 bits/s only on decisions and taste calls and expands each into rich output. That is a decision queue, which brings this back to section 2.

## 6. The far end: uploads, distillation and the "soul"

The chain from "distill me" to "upload me" has two links that come apart: "distill a person into a narrow task policy" is an empirical question with 50 years of evidence behind it, while "upload the brain" and "is the result you" are open science and open philosophy.

### Emulation is nowhere close

The [State of Brain Emulation Report 2025](https://arxiv.org/abs/2510.15745v3) (Zanichelli, Schons, Freeman, Shiu, Arkhipov) gives no mouse or human timeline. It says whole-brain single-neuron recording in mammals will likely stay extremely hard for the foreseeable future. Structure is ahead of dynamics:

| Milestone | Scale | Note |
| --- | --- | --- |
| [FlyWire](https://earth.com/news/first-complete-map-of-every-neuron-in-the-brain-revealed) whole adult fly brain (2024) | 139,255 neurons, \~50M connections | \~33 person-years of proofreading |
| [Shiu et al. connectome model](https://ls.berkeley.edu/node/1426) (2024) | same, on a laptop | predicted taste and touch responses only |
| [MICrONS](https://www.nih.gov/news-events/news-releases/scientists-map-unprecedented-detail-connections-visual-perception-mouse-brain) (2025) | 1 mm³ mouse cortex, >524M synapses | 1.6 PB, 7+ years |
| Mouse recording today ([report](https://arxiv.org/pdf/2510.15745v2)) | \~1M neurons, \~1% of brain | 100M is the next-decade goal |
| Mouse connectome cost ([E11 Bio, quoting Wellcome](https://e11.bio/news/roadmap)) | $7–21B, >95% proofreading | E11 targets 100x cheaper; a target, not a result |

Even the 302-neuron worm isn't emulated: in *C. elegans* 40–50% of synapses differ worm to worm, no simulation includes neuropeptides, and the report estimates \~8,400 worms' recordings would be needed against 284 today. A human connectome at 10 nm is 2–2.8 zettabytes of raw data.

### The cheap route already exists, and it is "distillation"

The nearest real thing to "distill an upload to what's in distribution for my project work" is **judgmental bootstrapping**. [Dawes 1979](https://www.cmu.edu/dietrich/sds/docs/dawes/the-robust-beauty-of-improper-linear-models-in-decision-making.pdf) summarizes it: linear models of 26 of 29 clinical judges beat the judges themselves (validity .31 vs .28), and models of admissions faculty beat the faculty (.25 vs .19). The model keeps the judge's stable policy and drops their day-to-day noise. The sting is that equal-weight models did about as well, so the judge's real contribution was choosing which variables matter and in which direction.

LLM-era versions measure attitudes, not work. [Park et al.](https://arxiv.org/abs/2411.10109v1) agents built from 2-hour interviews match people's GSS answers at 83–86% of their own two-week test-retest consistency (74% from demographics alone), but show no gain on economic games. [Twin-2K-500](https://arxiv.org/abs/2505.17479) twins reach 88% of human test-retest yet are "more rational" than people: 4% of twins refuse a vaccine in an omission-bias item against \~45% of humans. Individual [Maia chess models](https://arxiv.org/abs/2008.10086v2) predict a specific player's moves well enough to identify them. I found no evaluation of an LLM clone of someone's professional judgment.

So what's "in distribution" for one person's project work is probably small: which features they attend to, which direction they lean on each, their taste vetoes, and their stated goals. A builder's own decision-queue answers are exactly that training set. That suggests a concrete test (build 3 in section 7): how often can a model predict the builder's queue answer from the item alone?

### Is the distillate you?

No major position says a narrow task policy is the self. My reading of each view applied to a "work-only distillate":

- **Functionalism** ([Chalmers 1995](https://consc.net/papers/qualia.html), fading and dancing qualia): a faithful upload could be conscious, but a distillate drops most of the organization, so it is a different, smaller system.
- **Parfit** ([SEP summary](https://plato.stanford.edu/entries/identity-personal/)): identity isn't what matters; psychological continuity is. A work distillate carries a thin slice of it. This is the view friendliest to the distillation framing, and it still says "some of what matters", not "the soul".
- **Copy views** ([Schneider, *Artificial You*](https://archive.philosophersmag.com/artificial-you-ai-and-the-future-of-your-mind-by-susan-schneider-a-review/)): even a full upload is a distinct individual.
- **Substrate views** ([Searle](https://plato.stanford.edu/entries/chinese-room/); [Seth 2025](https://sussex.figshare.com/articles/journal_contribution/Conscious_artificial_intelligence_and_biological_naturalism/28649519); IIT per [Koch](https://www.technologyreview.com/2014/10/02/171077/what-it-will-take-for-computers-to-be-conscious/)): a digital simulation is a model of a person's outputs, not a subject. Seth and Koch leave room for brain-like or neuromorphic hardware.
- **[Hanson, *The Age of Em*](https://mason.gmu.edu/~rhanson/ageofem)**: copied, job-trained ems are the economic case, and he doesn't need identity settled.

The bootstrapping result cuts against "the soul is what silicon runs better": what transfers and improves is the policy, and it improves precisely by discarding the variability that makes someone a person on a given day.

## 7. Five things to build

Start with the re-entry card: it's a weekend, it sits on a decision queue the builder already uses, and the queue's timestamps give a baseline to beat. The others reuse its pieces.

| # | Build | Effort | Rests on |
| --- | --- | --- | --- |
| 1 | Re-entry card per decision-queue item | Weekend | Cognitive interview, Mäntylä, Leroy, Parnin, Mercado |
| 2 | Intent cards in Anki | 1–2 days after #1 | Retrieval practice, Shattuck/Klein intent, Kaasa |
| 3 | Bootstrapped model of the builder's queue answers | 1–2 days | Dawes, Park, Twin-2K |
| 4 | Varied-cue subtitle vocabulary cards | Weekend | Butowska-Buczynska 2024, FSRS |
| 5 | Spaced repetition for intentions | 1–2 weeks | HeartSteps, Duolingo bandit, implementation intentions |

### 1. Re-entry card (weekend)

A page generated for each open decision-queue item that runs the section-2 sequence: ask, then show the builder's own words, then the state, the options with reasoning, and the trace.

- **Stack:** an agent skill that reads the project's status note (state, next step, log), the repo's git log since the builder's last answer on that project, past answers from the decision queue, and dated lines the builder wrote in the log. It writes one HTML page per item and attaches it to the queue item. The page opens with one or two questions ("what was this for?", "what did you rule out?") and a reveal button. The builder's typed answer and the reason for the final choice are saved back to the project notes, so the next card has their words to quote.
- **How to tell:** randomize open items to card vs no card for a month. Compare time from item creation to answer against the 12–62 day baseline, how often a decision is reversed within 14 days, and whether the pre-reveal answer matches the project's stated purpose. A null on time with fewer reversals still counts as a win.

### 2. Intent cards in Anki

For each active project, extract five to ten cards from the builder's own words: purpose, end state, antigoals, key decisions and their reasons. That is Klein's template, filled from log lines and queue answers. Push them through AnkiConnect into a low-volume project deck, with one card due the day before any queue item for that project.

- **Why it might work:** retrieval practice is one of the most robust effects in learning (g = 0.50), intent transmits badly by default (34%), and people lose their own reasons within months (one in five consistent months later).
- **How to tell:** FSRS retention on the deck, plus the pre-reveal match score from build 1 for projects with cards vs without.

### 3. Bootstrapped model of the builder

Give a model each past queue item, the project note at that time, and the builder's earlier answers, and ask it to predict the choice and reason. Run it on the answer history first, holding out the latest answers.

- **Why:** Dawes-style bootstrapping says a model of a person's policy can match them and is less noisy. Park and Twin-2K say LLM clones get 80–90% of test-retest on attitudes but are "more rational" than people, so look for where it misses the builder's taste calls.
- **How to tell:** accuracy against "always pick the default" and against base rates, plus calibration. If it's good on some item types, those items can show "you'd probably pick B because of X", which is itself a re-entry cue. The rubber-stamping risk from the [companion report on AI enfeeblement](https://ai.hiina.space/reports/ai-enfeeblement-and-the-peter-principle.md) applies: show the prediction after the builder's pre-reveal answer, not before.

### 4. Varied-cue subtitle vocabulary cards (weekend)

The subtitle premine pipeline already finds every subtitle line where a word appears. Add an Anki card template that shows a different matching subtitle line each review, chosen at review time from a field holding all of them. Split the deck's cards randomly in half: fixed sentence vs rotating sentence.

- **Why:** the 2024 PNAS result that varied cues beat constant ones, and that learners misjudge it, is the cleanest evidence for "the model replaces the deck". This tests it on a real personal study deck with no LLM in the loop.
- **How to tell:** FSRS stability and lapse rates per half after a month, and recognition of the word in the next episode watched. Cards with no example sentence go in neither half.

### 5. Spaced repetition for intentions (1–2 weeks)

A scheduler on a home server where each intention is a card: a cue (time and place), an action and a deadline. Prompts start dense after a plan is formed, lengthen when the person acts, shorten and change the cue after a miss. A contextual bandit picks the time slot with a dose penalty, and message wording rotates with a recovery penalty, Duolingo-style. Deliver through whatever already reaches the person's phone.

- **Why:** the corrected effect sizes say timing is a small lever, so the real test is whether capture and specific cues move anything.
- **How to tell:** run it as a micro-randomized trial on oneself. At each decision point, flip a coin for prompt vs no prompt and log whether the intention was touched within 24 hours. That's the HeartSteps design with one participant.

A VR memory palace for a project is a natural fit for someone already building in Godot and VR, but Legge's result predicts it won't beat build 1. If one gets built anyway, test it against build 1 on the same items.

## 8. Conclusion

The memory-palace idea points at a real problem, re-entry cost on decisions left waiting, but the evidence says the palace itself is the inert part: its benefits are for ordered lists, and a richer room adds nothing over the learner's own imagery work. What restores intent is cheaper and better supported: the decision-maker's own earlier words, a short state-and-next-step note, the agent's reasoning and predicted outcome, an automatic trace of what changed, and a question that makes them recall the purpose before the record is revealed. Nobody has assembled these pieces into one tested brief, which makes a re-entry card the most useful weekend build.

Superdidactic AI holds up only in its modest form. Tutors help by 0.1–0.3 SD at scale, the dense-information lever that drives persuasion transfers to teaching, and spaced-repetition scheduling is close to solved; the remaining headroom is in what gets practiced and in varied retrieval cues, while the learner's engagement and encoding rate cap everything. Sleep learning, subliminal audio, closed-loop stimulation, neural desktops and brain uploads are either near-null or far off. At the far end, the one thing that works today is distilling a person's stable decision policy, which improves on them by dropping exactly what makes them a person on a given day.

## 9. Sources

Every claim links to the page it came from, inline. Pages were read through a summarizing fetch tool and two verification passes re-checked load-bearing claims. Where a primary paper couldn't be opened (several Nature, NEJM, Cell and PMC pages blocked automated reads), the figure comes from an abstract, press release or review, and the link says which. The weakest-sourced figures are Neuralink's (company claims relayed by secondary sites) and the Shattuck 34% intent figure (Wikipedia plus an unofficial mirror).

- [Method of loci meta-analysis (2025), Masaryk University record](https://www.fss.muni.cz/vyzkum/publikace/prehled/2496979)
- [Twomey & Kroneisen 2021, method of loci meta-analysis](https://journals.sagepub.com/doi/10.1177/1747021821993457)
- [Dresler et al. 2017, memorization training (Stanford Medicine news)](https://med.stanford.edu/news/all-news/2017/03/memorization-tool-bulks-up-brains-internal-connections.html)
- [Krokos, Plaisant & Varshney 2019, virtual memory palaces](https://obj.umiacs.umd.edu/virtual_reality_study/10.1007-s10055-018-0346-3.pdf)
- [Legge et al. 2012, virtual vs imagined method of loci](https://www.psych.ualberta.ca/~cml/papers/LeggEtal2012.pdf)
- [SMART: AI-enhanced mnemonic learning (UMIACS news)](https://www.umiacs.umd.edu/about-us/news/umd-team-uses-ai-enhance-mnemonic-learning)
- [AI-suggested loci associations pilot (J-STAGE)](https://www.jstage.jst.go.jp/article/his/27/4/27_261/_article/-char/en)
- [Critique of MemPalace agent memory (arXiv 2604.21284)](https://arxiv.org/html/2604.21284v1)
- [Smith et al. 2014, environmental context-dependent memory](https://people.tamu.edu/~stevesmith/Smithetal2014.pdf)
- [Smith & Vela 2001, context-dependent memory meta-analysis (abstract)](https://doi.org/10.3758%2fBF03196157)
- [Imagined context reinstatement thesis (Wilfrid Laurier University)](https://scholars.wlu.ca/etd/1954)
- [Köhnken et al. 1999, the cognitive interview: a meta-analysis](https://researchportal.port.ac.uk/en/publications/the-cognitive-interview-a-meta-analysis/)
- [McDonagh & Storer 2005, mood boards as a design catalyst](https://experts.illinois.edu/en/publications/mood-boards-as-a-design-catalyst-and-resource-researching-an-unde/)
- [Teasley et al. 2000, war rooms and collocated teams](https://public.websites.umich.edu/~igri/publications/Teasley%20et%20al_00.pdf)
- [Mark, González & Harris 2005, no task left behind (CHI)](https://www.interruptions.net/literature/Mark-CHI05-p321-mark.pdf)
- [Trafton et al. 2003, preparing to resume an interrupted task](https://interruptions.net/literature/Trafton-IJHCS03.pdf)
- [Leroy & Glomb ready-to-resume plan (Futurity summary)](https://www.futurity.org/ready-to-resume-plan-1656322/)
- [Parnin & DeLine 2010, evaluating cues for resuming interrupted programming tasks](https://www.microsoft.com/en-us/research/publication/evaluating-cues-for-resuming-interrupted-programming-tasks/)
- [Ghibellini & Meier 2025, Zeigarnik effect meta-analysis](https://ideas.repec.org/a/pal/palcom/v12y2025i1d10.1057_s41599-025-05000-w.html)
- [Starmer et al. 2014, I-PASS handoffs (Harvard Medical School news)](https://hms.harvard.edu/news/safer-patient-handoffs)
- [Mercado et al. 2016, agent transparency in human-agent teaming](https://journals.sagepub.com/doi/reader/10.1177/0018720815621206)
- [Intent (military), Wikipedia](<https://en.wikipedia.org/wiki/Intent_(military)>)
- [Wheeler & Gabbert 2017, self-generated cues and memory](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2017.01830/pdf)
- [Kaasa, Morris & Loftus 2011, memory for past intentions (BPS Research Digest)](https://bps.org.uk/research-digest/how-reliable-our-memory-our-own-previous-intentions)
- [Buckingham Shum et al., design rationale capture](https://research-archive.stem.open.ac.uk/stemra-data/uploads/files/KMI-05-18.pdf)
- [von Hippel 2024, two-sigma tutoring revisited (Education Next)](https://www.educationnext.org/wp-content/uploads/2024/03/ednext_XIV_2_von_hippel.pdf)
- [Kraft, Schueler & Falken 2026, tutoring meta-analysis of 263 RCTs](https://journals.sagepub.com/doi/10.3102/00346543261446660)
- [Kestin et al. 2025, AI tutoring in Harvard physics](https://pmc.ncbi.nlm.nih.gov/articles/PMC12179260/)
- [Re-analysis of the Harvard AI tutoring study (Clay Ford)](https://clayford.net/posts/ai_tutoring_nature/index.html)
- [De Simone et al. 2025, GPT-4 after-school tutoring in Nigeria (World Bank)](https://openknowledge.worldbank.org/bitstreams/cd9cca5b-2ffd-4be1-8313-0f4d2ed6ef4f/download)
- [Oreopoulos & Low 2026, Khanmigo cluster RCT (NBER w35620)](https://www.nber.org/papers/w35620)
- [World Bank 2026, can ed-tech close learning gaps?](https://thedocs.worldbank.org/en/doc/2fba81cd6cd60d2f54532fc7062395fb-0050062026/original/Can-EdTech-Close-Learning-Gaps.pdf)
- [Bastani et al. 2025, generative AI can harm learning (PNAS)](https://ideas.repec.org/a/nas/journl/v122y2025pe2422633122.html)
- [IDA D-5358, DARPA Digital Tutor evaluation](https://apps.dtic.mil/sti/pdfs/AD1002362.pdf)
- [Retraction of the Wang & Fan ChatGPT meta-analysis (Plagiarism Today)](https://www.plagiarismtoday.com/2026/07/15/study-claiming-ai-helps-students-learn-retracted/)
- [Hackenburg et al. 2025, the levers of political persuasion with AI (Science)](https://researchonline.lse.ac.uk/id/eprint/130605)
- [Costello, Pennycook & Rand, AI dialogues reduce conspiracy belief (Nieman Lab)](https://www.niemanlab.org/2024/09/an-ai-chatbot-helped-americans-who-believe-in-conspiracy-theories-exit-the-rabbit-hole/)
- [Landauer 1986, how much do people remember?](https://home.cs.colorado.edu/~mozer/Teaching/syllabi/7782/readings/Landauer1986.pdf)
- [Macnamara et al. 2014, deliberate practice meta-analysis (APS)](https://www.psychologicalscience.org/news/releases/becoming-an-expert-takes-more-than-practice.html)
- [open-spaced-repetition srs-benchmark (GitHub)](https://github.com/open-spaced-repetition/srs-benchmark)
- [KAR3L, content-aware flashcard scheduling (arXiv 2402.12291)](https://arxiv.org/pdf/2402.12291)
- [LECTOR (arXiv 2508.03275)](https://arxiv.org/html/2508.03275)
- [LLM-generated medical flashcards pipeline (medRxiv)](https://www.medrxiv.org/content/10.1101/2025.05.13.25327518v1.full.pdf)
- [Andy Matuschak, notes on LLM-generated prompts](https://notes.andymatuschak.org/zomoPzCNzSi5GqtfTeVWgm7RjmiArjS8vvM5)
- [Butowska-Buczynska et al. 2024, varied retrieval cues (PNAS)](https://share.swps.edu.pl/handle/swps/1120)
- [Rowland 2014, testing effect meta-analysis](https://courseware.epfl.ch/assets/courseware/v1/fdde2f0aa590bf3b1324077a6bf1540c/asset-v1%3AEPFL%2BDEMO%2B2020%2Btype%40asset%2Bblock/Rowland2014-meta-analysis.pdf)
- [Cepeda et al. 2008, spacing effects in learning](https://pubmed.ncbi.nlm.nih.gov/19076480/)
- [Krasne et al. 2013, perceptual learning modules in histopathology](https://pmc.ncbi.nlm.nih.gov/articles/PMC3908489)
- [Koroma et al. 2022, learning during sleep](https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2022.801666/pdf)
- [Züst et al. 2019, learning new vocabulary during deep sleep (University of Bern)](https://mediarelations.unibe.ch/media_releases/2019/medienmitteilungen_2019/learning_new_vocabulary_during_deep_sleep/index_eng.html)
- [Hu et al. 2020, targeted memory reactivation meta-analysis](https://faculty.wcas.northwestern.edu/paller/PsychBulletin2020.pdf)
- [Carbone & Diekelmann 2024, TMR durability (npj Science of Learning)](https://www.nature.com/articles/s41539-024-00244-8)
- [Humiston & Wamsley 2019, failed replication of implicit-bias TMR](https://ideas.repec.org/a/plo/pone00/0211416.html)
- [Harlow et al. 2023, closed-loop auditory stimulation meta-analysis](https://public-pages-files-2025.frontiersin.org/journals/sleep/articles/10.3389/frsle.2023.1082253/text)
- [Henin et al. 2019, closed-loop stimulation and memory (eNeuro)](https://www.eneuro.org/content/6/6/ENEURO.0306-19.2019)
- [Elemind neuromodulation headband (IEEE Spectrum)](https://spectrum.ieee.org/elemind-neuromodulation)
- [Göldi & Rasch 2019, home TMR](https://link.springer.com/article/10.1038/s41539-019-0044-2)
- [Greenwald et al. 1991, subliminal self-help audiotapes](https://www.Gwern.net/doc/psychology/1991-greenwald.pdf)
- [Subliminal priming replications (Meta-Psychology)](https://open.lnu.se/index.php/metapsychology/article/view/3308)
- [Targeted dream incubation and creativity (MIT News)](https://news.mit.edu/2023/sleep-sweet-spot-dreams-creativity-0515)
- [Konkoly et al. 2021, two-way communication with lucid dreamers](https://bpb-us-e1.wpmucdn.com/sites.northwestern.edu/dist/4/2492/files/2026/04/Konkoly_2021_Curr_Biol.pdf)
- [Predicting memory responders to sleep stimulation (medRxiv 2025 preprint)](https://www.medrxiv.org/content/10.1101/2025.11.12.25340010v1.full.pdf)
- [Sheeran, Listroma & Gollwitzer 2025, implementation intentions meta-analysis](https://kops.uni-konstanz.de/server/api/core/bitstreams/d703c468-46e9-47fc-8900-d32d7d19c8d9/content)
- [Maier et al. 2022, no evidence for nudging after bias adjustment (PNAS)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9351501)
- [DellaVigna & Linos 2022, RCTs to scale: nudge units (NBER w27594)](https://www.nber.org/papers/w27594)
- [Milkman et al. 2021, gym megastudy (Nature)](https://authors.library.caltech.edu/records/mys88-cc756)
- [Milkman et al. 2022, 680,000-person vaccination nudge megastudy](https://knowledge.uchicago.edu/record/9653/files/milkman-et-al-2022-a-680-000-person-megastudy-of-nudges-to-encourage-vaccination-in-pharmacies.pdf)
- [Klasnja et al. 2019, HeartSteps micro-randomized trial (Europe PMC)](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:30192907%20AND%20SRC:MED&resultType=core&format=json)
- [Chatbot physical activity coaching meta-analysis, 12 RCTs](https://pmc.ncbi.nlm.nih.gov/articles/PMC12254675)
- [Giné, Karlan & Zinman, commitment contracts for smoking cessation](https://poverty-action.org/sites/default/files/publications/put_your_money_where_your_butt_is.pdf)
- [LLM-personalized energy feedback field trial (arXiv 2604.03881)](https://arxiv.org/abs/2604.03881)
- [Jörke et al. 2025, GPTCoach](https://hci.stanford.edu/publications/2025/Joerke_GPTCoach.pdf)
- [Mishra et al. 2021, detecting receptivity for mHealth interventions](https://arxiv.org/abs/2011.08302)
- [Künzler et al. 2019, receptivity to just-in-time interventions](https://cs.dartmouth.edu/dfk/research/kunzler-receptivity/index.html)
- [Yancey & Settles 2020, recovering bandit for Duolingo notifications (KDD)](https://research.Duolingo.com/papers/yancey.kdd20.pdf)
- [Chiu & Gilbert 2023, reminder setting and strategic offloading](https://discovery.ucl.ac.uk/10176285/1/chiu-gilbert-2023-express-influence-of-the-physical-effort-of-reminder-setting-on-strategic-offloading-of-delayed.pdf)
- [Wood & Rünger 2016, psychology of habit](https://dornsife.usc.edu/wendy-wood/wp-content/uploads/sites/183/2023/10/wood.runger.2016.pdf)
- [Oralytics reinforcement learning design (arXiv 2406.13127)](https://arxiv.org/html/2406.13127v1)
- [GameNGen, diffusion models as game engines (arXiv 2408.14837)](https://arxiv.org/abs/2408.14837)
- [Genie 3 (Google DeepMind)](https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/)
- [NeuralOS (arXiv 2507.08800)](https://arxiv.org/abs/2507.08800)
- [Generative UI (Google Research)](https://research.google/blog/generative-ui-a-rich-custom-visual-interactive-user-experience-for-any-prompt/)
- [Gajos et al. 2008, SUPPLE++ improving performance for motor-impaired users](https://www.eecs.harvard.edu/~kgajos/papers/2008/gajos08improving.shtml)
- [Findlater et al. 2009, adaptive interfaces and motor memory](https://www.cs.ubc.ca/labs/edapt/papers/findlater2009.pdf)
- [Willett et al. 2023, high-performance speech neuroprosthesis (Nature)](https://www.nature.com/articles/s41586-023-06377-x)
- [Metzger et al. 2023, brain implants restore communication (Physics World)](https://physicsworld.com/a/high-performance-brain-implants-restore-communication-to-those-who-cannot-speak/)
- [Card et al. 2024, accurate and rapidly calibrating speech neuroprosthesis](https://profiles.wustl.edu/en/publications/an-accurate-and-rapidly-calibrating-speech-neuroprosthesis/)
- [Neuralink cursor record (Decrypt)](https://decrypt.co/230021/neuralink-implant-patient-gaming-sets-bci-record)
- [Meta sEMG wristband (The Register)](https://www.theregister.com/2025/07/23/meta_wristband_ui_control/)
- [Brain2Qwerty non-invasive typing decoding (arXiv 2502.17480)](https://arxiv.org/abs/2502.17480)
- [Flesher et al. 2021, tactile microstimulation in a BCI](https://pubmed.ncbi.nlm.nih.gov/34016775/)
- [Fernández et al. 2021, visual percepts from an intracortical microelectrode array](https://research.vu.nl/en/publications/visual-percepts-evoked-with-an-intracortical-96-channel-microelec/)
- [Zheng & Meister, the unbearable slowness of being (arXiv 2408.10234)](https://arxiv.org/abs/2408.10234)
- [State of Brain Emulation Report 2025 (arXiv 2510.15745v3)](https://arxiv.org/abs/2510.15745v3)
- [FlyWire whole fly brain connectome (Earth.com)](https://earth.com/news/first-complete-map-of-every-neuron-in-the-brain-revealed)
- [Shiu et al. 2024, fly connectome model (UC Berkeley)](https://ls.berkeley.edu/node/1426)
- [MICrONS mouse visual cortex map (NIH)](https://www.nih.gov/news-events/news-releases/scientists-map-unprecedented-detail-connections-visual-perception-mouse-brain)
- [State of Brain Emulation Report 2025, v2 PDF](https://arxiv.org/pdf/2510.15745v2)
- [E11 Bio roadmap](https://e11.bio/news/roadmap)
- [Dawes 1979, the robust beauty of improper linear models](https://www.cmu.edu/dietrich/sds/docs/dawes/the-robust-beauty-of-improper-linear-models-in-decision-making.pdf)
- [Park et al. 2024, generative agent simulations of 1,000 people (arXiv 2411.10109)](https://arxiv.org/abs/2411.10109v1)
- [Twin-2K-500 (arXiv 2505.17479)](https://arxiv.org/abs/2505.17479)
- [Maia individual chess models (arXiv 2008.10086)](https://arxiv.org/abs/2008.10086v2)
- [Chalmers 1995, absent qualia, fading qualia, dancing qualia](https://consc.net/papers/qualia.html)
- [Personal identity, Stanford Encyclopedia of Philosophy](https://plato.stanford.edu/entries/identity-personal/)
- [Review of Susan Schneider, Artificial You (The Philosophers' Magazine)](https://archive.philosophersmag.com/artificial-you-ai-and-the-future-of-your-mind-by-susan-schneider-a-review/)
- [The Chinese Room Argument, Stanford Encyclopedia of Philosophy](https://plato.stanford.edu/entries/chinese-room/)
- [Seth 2025, conscious AI and biological naturalism](https://sussex.figshare.com/articles/journal_contribution/Conscious_artificial_intelligence_and_biological_naturalism/28649519)
- [Koch on what it will take for computers to be conscious (MIT Technology Review)](https://www.technologyreview.com/2014/10/02/171077/what-it-will-take-for-computers-to-be-conscious/)
- [Robin Hanson, The Age of Em](https://mason.gmu.edu/~rhanson/ageofem)
