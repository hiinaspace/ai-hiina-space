---
id: jp-learning-and-anki-tooling
title: "Project status: Japanese immersion learning with Anki and selective glossing"
version: 1
published: 2026-10-27
updated: 2026-10-27
author: Hiina
produced-by: "Claude deep-research run with citation checking"
model: claude-opus-5-5
sources-through: 2026-10-25
status: current
takeaway: "Hiina's Japanese project is at the plan stage: fix Anki settings, leeches and sentence-cued cards first, then build a thin learner model and a hint-first selective-gloss overlay for anime, games and VNs."
topics: [japanese-learning, spaced-repetition, ai-tutoring, agents]
---

This page is a status record of Hiina's Japanese-learning project, written for agents (and people) who need to know what the project is, where it stands, and what is planned. It covers the goal, the current deck and tooling, the recommended Anki configuration, a five-part tool plan with build order and evaluation gates, open questions, and sources. Status is as of 25 Oct 2026: the plan is proposed and nothing in it has been built or changed yet.

## 1. Summary

- **What the project is.** A staged plan to make Anki serve anime, game, visual novel (VN) and reading immersion in Japanese, and then to build one shared learner model with selective-gloss tools on top of it.
- **Current state (25 Oct 2026).** Plan proposed; no settings changed and no tools built. Kaishi 1.5k is finished. The collection, last inventoried 30 Jul 2026, holds 269 radical notes, 432 hand-mined Lapis notes and 202 premined cards for the anime *Katanagatari*.
- **Next gate.** Four weeks after a settings, leech and sentence-rotation pass, recall on a word-only probe of 50 mature Lapis cards should be within 5 points of the deck's normal true retention. That measures whether cards are being recalled from the word or from their example sentence.
- **Build order.** (1) Anki settings plus a manual leech and Click-card pass; (2) a thin read-only learner model; (3) an agent-maintained deck-hygiene loop and a premine pipeline rebuilt on Jiten.moe; (4) a hint-first selective-gloss overlay for games, VNs and anime; (5) a Japanese-page gloss mode; (6) a revived concept-level grammar tutor; (7) an English-to-Japanese hybrid-reading rewriter, last.
- **Strongest evidence.** Varying the sentence cue across retrievals beats a constant cue for foreign vocabulary (PNAS 2024, six experiments). Retrieved corpus sentences are preferred over LLM-generated ones for Japanese learners (ACL SRW 2024). Glossed reading beats unglossed reading. Hint-first AI tutoring avoids the learning loss seen with unrestricted AI help in a field RCT.
- **Limits.** No study tests any of these tools on Japanese learners. The supporting evidence (glossing, varied retrieval cues, hint-first tutoring) comes from other materials and settings. Many community guides failed to load during research, so community-consensus claims rest on vnclub, TheMoeWay, Donkuri and tool documentation.
- **Clearest gap found.** No existing tool glosses only the words a learner probably does not know, or offers graded hints instead of translation, for games, VNs or anime. No tool puts immersion exposures and lookups into the same table as SRS reviews.

## 2. Goal and current state

### What "optimal" means for this project

The goal is to enjoy Japanese anime, games, visual novels and articles while learning from them. Anki supports that goal and is not the goal. The project's question is therefore not "how to get the most Anki retention per minute" but "what is the least Anki, and the smallest amount of tooling, that maximises comprehension of the media Hiina actually wants to watch, play and read". Mining frameworks the community still uses put it the same way. TheMoeWay says that after the beginner stage, mining "will essentially become the heart of your Japanese study", and its advice after that is simply to "immerse a lot and learn words and grammar" ([TheMoeWay guide](https://learnjapanese.moe/guide/)).

A companion report on AI memory palaces and superdidactic AI found a constraint that fits this framing: the binding constraint on AI tutors in the field is engagement, not explanation quality. In the large Khanmigo trial, students messaged the tutor on a median of about a third of practice days, and the effect was about 0.06-0.08 SD per year ([NBER w35620](https://www.nber.org/papers/w35620)). The design consequence for this project: a tool that makes watching or reading more fun is worth more than one that makes studying slightly more efficient but gets used less.

### Current deck and tooling

- **Decks.** Kaishi 1.5k finished. 269 radical notes. 432 hand-mined Lapis notes. 202 premined *Katanagatari* cards.
- **Premine pipeline.** A small script built the *Katanagatari* cards: a Jiten.moe vocabulary CSV plus fugashi/UniDic tokenisation over the show's .ass subtitles, minus words already known in Anki, with JMdict definitions, written into Lapis fields. Known failures from that run: a wrong sense picked for 一寸, character names that are also ordinary words, and 9 cards missing sentences.
- **Mining.** Yomitan in the browser, writing to Anki through AnkiConnect. Anki runs on a Linux desktop.
- **Prior attempt.** An earlier prototype (2025, now archived) was an MCP-based concept-level SRS tutor run with Claude. Its sessions found that comprehension of grammar such as conditionals and nominalisation was strong. Production was blocked mostly by vocabulary gaps, particles and collocations, and dictionary lookups broke the flow of grammar practice. Its retrospective named "integrate Anki vocabulary state" as the missing piece. The shared learner model in section 8 is that piece. The prototype also lapsed as a daily habit.

### Three immediate to-dos

The three open to-dos are all deck hygiene: mine more anime, fix confusing leeches, and stop cards being cued by their example sentence. Each has a cheap manual answer now and a natural automation later (sections 3 to 5). The larger ideas (a revived concept tutor, a hybrid-reading rewriter, a selective-gloss overlay for games and VNs) share one dependency: knowing which words and grammar the learner knows right now. The build order follows from that dependency.

## 3. Scheduler settings (FSRS-6 on Anki 26.x)

Anki is on a 26.x release train. 26.08.1 is the latest stable release listed, 26.09 betas ship FSRS 6.6.2, and FSRS-6 (21 parameters) is the current scheduler ([Anki releases](https://github.com/ankitects/anki/releases); [awesome-fsrs: The Algorithm](https://github.com/open-spaced-repetition/awesome-fsrs/wiki/The-Algorithm)). The years on the release page are inferred from ordering. 26.08 also added an "Experiments" section, including an editor rework that "may affect addon compatibility" ([Anki 26.08](https://github.com/ankitects/anki/releases/tag/26.08)). Since Yomitan, asbplayer and any agent tooling all go through add-ons, the plan leaves those experiments off (inference).

Planned values, sourced from the Anki manual and the vnclub Japanese guide, the two primary sources that loaded:

| Setting | Value | Source / reason |
|---|---|---|
| FSRS | On | Current scheduler |
| Desired retention | 0.90 (manual default); 0.85 if daily load is uncomfortable; stay below 0.97 | Workload climbs steeply above 0.90 ([Deck Options](https://docs.ankiweb.net/deck-options.html); [vnclub Anki guide](https://vnclub.org/anki-guide/)). "Help Me Decide" shows the workload curve; it replaced the minimum-retention tool in 25.07 |
| Optimise | Monthly, with "Check health when optimizing" on | The health check flags pressing Hard on a forgotten card as a data problem |
| Grading | Again and Good only, via the PassFail2 add-on (876946123) | Set "Ignore cards reviewed before" to the date pass/fail grading started if earlier history used Hard/Easy |
| Steps | One 10-minute learning step; about 3 minutes relearning | [vnclub](https://vnclub.org/anki-guide/); [TheMoeWay mining](https://learnjapanese.moe/mining/) |
| Limits | Max reviews/day 9999; next day starts at 4 AM | Same |
| New cards | 10-15 a day, set to 0 when reviews pile up | Cap by load, not a fixed number (vnclub) |
| Load balancing, Easy Days | Core features; 26.05 improved load balancing | Older advice to install FSRS Helper for these is probably dated (inference; the Helper repo did not load) |
| Avoid | "Reschedule cards on change" without a backup; the AutoReorder add-on | Lapis's README warns AutoReorder has sometimes reset learned cards to new ([Lapis README](https://github.com/donkuri/lapis)) |

The plan keeps one preset unless the health check says otherwise, because the manual reserves separate presets for decks of very different difficulty. One inference to test: newer Anki allows per-deck retention within a preset, so `Lapis::<show>` premine decks could run at 0.85 while that show is being watched, since the episodes re-expose those words for free. No primary source makes that argument.

## 4. Deck hygiene: leeches and sentence-cued cards

### Leeches ("rewrite the leech cards so they're less confusing")

Set the leech threshold to 6 with action Tag Only, as vnclub recommends. Cards then join a `tag:leech` rewrite queue instead of disappearing into suspension. Anki's default is 8 lapses with tag plus suspend ([Anki manual: Leeches](https://docs.ankiweb.net/leeches.html)). The queue is worked with a four-way triage. The taxonomy is a synthesis, but each branch follows the manual or forum advice:

1. **Interference with a similar word or kanji.** Suspend one of the pair until the other is solid, or build a contrast card that shows both and focuses on the difference ([forum thread](https://forums.ankiweb.net/t/how-do-i-deal-with-pairs-of-cards-that-i-confuse-for-each-other/55515)).
2. **Overloaded card.** Several senses or a long definition. Shrink Lapis's MainDefinition to the sense actually met, and push the rest into Glossary.
3. **Sentence-cued recall.** Handled by the sentence-cue fix below.
4. **Low-value word.** Delete it.

When a rewrite changes the cue substantially, the card is Reset. Reset keeps review history, so the FSRS optimiser still sees reviews of the old cue ([Anki manual: Studying](https://docs.ankiweb.net/studying.html)). That is a mild contamination risk whose size nobody has verified.

For mnemonics on stubborn leeches, the companion memory-palace report supplies a constraint. Cues learners make themselves beat other-generated cues by a wide margin in lab studies (Mäntylä, via [Wheeler & Gabbert 2017](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2017.01830/pdf)). A 30-student pilot also found that AI-generated associations far from the learner's own thinking can interfere with memory ([J-STAGE](https://www.jstage.jst.go.jp/article/his/27/4/27_261/_article/-char/en)). So in this project an LLM may propose a mnemonic or a contrast card, but the learner edits and chooses it.

### Sentence-cued cards ("swap out the example sentences so cards cued by the sentence get reset")

This to-do has the best evidence behind it. A 2024 PNAS paper (six experiments on foreign vocabulary) found that varying the sentence cue across retrieval cycles beat a constant cue, immediately and after 24 hours, and more so when practice was spaced. Learners nonetheless judged constant cues more effective ([PNAS via SWPS](https://share.swps.edu.pl/handle/swps/1120)). That metacognitive illusion explains why sentence-cued cards feel fine until the word turns up somewhere else.

Lapis has four card types (word plus sentence, Click, sentence, audio) but no sentence rotation, and no add-on that rotates sentences per note turned up ([Lapis README](https://github.com/donkuri/lapis)). That is absence in a limited search. The closest existing tool, anki-ai-dynamic-cards, generates a fresh LLM sentence at review time but supports English only and stores nothing ([GitHub](https://github.com/AleksandrFurmenkovOfficial/anki-ai-dynamic-cards)).

The manual sequence planned now:

1. **Find the sentence-cued cards.** Build a filtered deck of mature Lapis cards, temporarily flip them to a word-only front, and see which ones fail. Those are the sentence-cued ones (inference; this is a self-test, not a published method). This is the probe used in the next gate.
2. **Switch every mined note to Click cards** (`IsClickCard`), which hide the sentence until clicked, as Donkuri recommends ([Donkuri mining](https://donkuri.github.io/learn-japanese/mining/)).
3. **Reset only the probe failures.** Leave the passes alone so their stability survives.

Real rotation needs a custom template: an extra field holding several sentences, with JavaScript picking one at render time. Anki templates support JS, and a forum script already shuffles content on a card front ([forum thread](https://forums.ankiweb.net/t/how-do-i-deal-with-pairs-of-cards-that-i-confuse-for-each-other/55515)).

The extra sentences should come from real text, not free generation. The one Japanese-specific study found that all rater groups preferred retrieved corpus sentences over zero-shot generated ones ([ACL SRW 2024](https://preview.aclanthology.org/setup/2024.acl-srw.55)). The project's own subtitle lines and Jiten's example sentences are the obvious corpus. Updating Lapis means importing a new APKG, which resets custom CSS ([Lapis releases](https://github.com/donkuri/lapis/releases)), so template edits are kept in a file that can be re-applied.

## 5. Mining from more anime

### Rebuilding the premine pipeline on Jiten.moe

The open question from the *Katanagatari* premine was whether its filter thresholds were right. Research reframed it: much of that pipeline now exists upstream, and a better threshold is personal coverage, not a frequency cut-off. Jiten.moe is open source (Apache-2.0, Sudachi.rs plus JMdict). It has per-title vocabulary lists with Anki/CSV export, and a public API with `/api/media-deck/{id}/vocabulary` (sort by deck or global frequency, 200 per page) and `/api/vocabulary/parse`. Rate limits are 120 a minute anonymously and 300 with a key, and the endpoints are unversioned ([Sirush/Jiten](https://github.com/Sirush/Jiten); [Jiten API](https://jiten.moe/guides/using-the-api)).

Jiten also has Word Sets that address the project's two main premine failure modes, function words and proper nouns: Particles & Common Grammar, Kaishi 1.5k, and Names (300k+), People, Place names, Other names. Each can be marked Mastered or Blacklisted without creating cards. Jiten's recommended setup for experienced learners is to master particles plus Kaishi and blacklist the names sets ([Jiten word sets](https://jiten.moe/guides/word-sets)). Known words can be imported from Anki into Jiten through AnkiConnect (add `https://jiten.moe` to `webCorsOriginList`), and Jiten then reports coverage of any show before it is started ([Jiten import](https://jiten.moe/guides/importing-known-words-from-anki)). Its rule of thumb: 80% coverage is challenging (about 2 lookups per sentence), 90% is a good immersion level (about 1), and 98% or more is comfortable ([Jiten: choosing media](https://jiten.moe/guides/choosing-media-at-your-level)). The project will use this to choose the next anime.

Planned changes to the premine pipeline:

- **Keep:** the Lapis field mapping, the offline known-word subtraction, and the JMdict definitions.
- **Replace:** frequency ranking and tokenisation, with Jiten's per-title list or parse endpoint.
- **Add:** a cheap LLM pass with two jobs. Given the line and the numbered JMdict senses, it picks a sense index (which would have fixed the 一寸 gloss). It also decides whether a token is a character name in that context. No public tool or evaluation was found for either job. The ecosystem offers only list-based name handling, such as Jiten's Names word sets, and Sudachi's Full dictionary with its named-entity split mode ([Sudachi](https://github.com/WorksApplications/Sudachi)). The *Katanagatari* failures serve as a regression set.
- **Output route:** whether Jiten's Anki export is Lapis-compatible is unverified, so the Jiten API plus the project's own Lapis writer is the safer route.

Two alternatives were noted:

- **Anki Miner.** GPL-3.0, v3.10.1 on 22 Oct 2026. Turns video plus subs into cards, with i+1, frequency-range, blacklist and wordset filters, a Word Curator step, and Whisper subtitle generation. Single source, fast-moving, and it does not document how it decides a word is known ([PyPI](https://pypi.org/project/anki-miner/)).
- **AnkiMorphs.** Reorders new cards so those with the fewest unknown morphs come first, which suits a 200-card premine dump ([AnkiMorphs docs](https://mortii.github.io/anki-morphs/)).

### Reactive mining while watching (Linux)

- **asbplayer in Firefox:** v1.22.0, October 2026, with Jimaku auto-locate for subtitles. Its new Anki add-on (v1.0.0, needs Anki 25.02+, installed from a `.ankiaddon` file rather than AnkiWeb) lets Yomitan create the Lapis card while asbplayer patches in the screenshot, audio and subtitle sentence ([asbplayer releases](https://github.com/killergerbah/asbplayer/releases); [one-click mining](https://docs.asbplayer.dev/docs/guides/one-click-mining)). asbplayer can also colour subtitle words by known status, using a word database rebuilt from Anki fields ([annotation guide](https://docs.asbplayer.dev/docs/guides/annotation)). That is a free first cut of the selective-gloss idea.
- **mpv with mpvacious:** v26.7.28.0, Linux-first, needs mpv 0.41+. Its README favours GoldenDict-ng or Rikaitan over Yomitan ([mpvacious](https://github.com/Ajatt-Tools/mpvacious)).

Subtitles come from Jimaku and are retimed with alass, which can align to the video or to another subtitle track ([alass](https://github.com/kaegi/alass)). Kitsunekko's 2026 status could not be checked.

Infrastructure note: AnkiConnect's GitHub repo was archived on 4 Nov 2025 and moved to sr.ht ([FooSoft/anki-connect](https://github.com/FooSoft/anki-connect)). Yomitan, asbplayer and Jiten import all depend on it, so the project pins its AnkiConnect version rather than assuming upstream updates.

## 6. Planned tools: deck-hygiene agent and concept tutor

### (a) Agent-maintained deck hygiene

**What it is.** A scripted or agentic loop on the machine that runs Anki, with three jobs: triage and rewrite `tag:leech` cards, rotate example sentences with selective reset, and run the premine pipeline (Jiten list, then the LLM sense/name pass, then Lapis notes) for each new show.

**What exists.** raine/anki-llm is a CLI/TUI that bulk-processes notes with LLMs through AnkiConnect. It stores prompts as versionable files and supports previews, snapshots, rollback and resume, plus Ollama (MIT, 299 stars) ([anki-llm](https://github.com/raine/anki-llm)). The ankimcp add-on runs a local MCP server inside Anki. It exposes forget, reposition and set-due actions, atomic multi-note `update_notes`, and four FSRS tools that read memory state and run the optimiser (AGPL, v0.20.0) ([ankimcp](https://github.com/ankimcp/anki-mcp-server-addon)). AnkiConnect-based MCP servers also exist (nailuoGG, ujisati). The gap: nothing targets Japanese leech rewriting or sentence rotation, and nothing does word-sense disambiguation against JMdict.

**Build sketch.** ankimcp for anything that reads FSRS state or needs atomic undo; anki-llm's workspace for batch rewrites that should be diffed first. The leech pass:

1. Query `tag:leech` plus the lapse history.
2. Classify each card into the four-way triage. The LLM can also flag interference pairs, an idea LECTOR tested only on simulated learners ([LECTOR](https://papers.cool/arxiv/2508.03275)).
3. Propose a rewrite as a diff, which the learner approves.
4. Apply it, and Reset only when the cue changed.

The sentence pass fills a `Sentences` field from the project's own subtitle corpus and Jiten examples, using the LLM as ranker and verifier rather than generator. The premine pass is the *Katanagatari* premine script refactored around the Jiten API.

| Field | Assessment |
|---|---|
| Effort | S for leech triage and sentence fill; M with the premine refactor |
| Payoff | High and immediate: clears all three to-dos, and every later tool reuses the premine and corpus code |
| Risks | Plausible-but-wrong LLM edits (about 5% hallucination in a medical flashcard pipeline, [medRxiv](https://www.medrxiv.org/content/10.1101/2025.05.13.25327518v1.full.pdf)); FSRS contamination from resets; add-on breakage from Anki's editor experiments |
| Evidence gate | The word-only probe (section 1), plus the leech count trending down over two optimiser cycles |
| Stop condition | If more than about a third of proposed rewrites are rejected, drop to manual triage with LLM suggestions only |

### (b) Revived concept-level SRS tutor

**What it is.** The 2025 tutor prototype brought back for grammar points and other knowledge components that flashcards encode badly. An LLM (Claude in the prototype) runs short lessons for due concepts. The difference from 2025 is that it reads live vocabulary state, so exercises stop stalling on unknown words.

**What exists.** Math Academy's Fractional Implicit Repetition (FIRe) is the best-documented concept-level scheduler. Passing an advanced topic gives fractional credit to the topics it "encompasses", but the weights are built by an expert, and the evidence is from the vendor or personal use ([Skycak](https://justinmath.com/individualized-spaced-repetition-in-hierarchical-knowledge-structures/); [Matuschak notes](https://notes.andymatuschak.org/Math_Academy)). Bunpro schedules grammar points with plain SRS stages, and its users complain about the SRS ([Bunpro forum](https://community.bunpro.jp/t/how-does-bunpro-choose-which-sentence-to-review-for-a-given-grammar-point/45486)). Japanese AI tutor projects that could be inspected were prompt packs ([Manabi Mentor](https://github.com/c0m/manabi-mentor-preplugin/blob/master/README.md)). The gap is a grammar-level scheduler that is open, integrated with Anki state and designed hint-first.

**Design constraints from the evidence.** Bastani et al. ran about 1,000 maths students in a field RCT. Unrestricted GPT-4 raised practice scores, but exam scores were 17% lower once the AI was removed. A tutor that gave hints and teacher-written solutions removed the harm but did not beat control ([Wharton summary](https://knowledge.wharton.upenn.edu/article/without-guardrails-generative-ai-can-harm-education); [PNAS](https://www.pnas.org/doi/10.1073/pnas.2422633122)). The Harvard physics tutor that beat active learning used a structured sequence and pre-written solutions ([PMC12179260](https://pmc.ncbi.nlm.nih.gov/articles/PMC12179260/)). LLMs are poor zero-shot knowledge tracers: GPT-4o-mini scored 58.6% accuracy against 72.7% for a small SAKT model, at orders of magnitude higher cost ([Eedi](https://eedi.com/news/we-benchmarked-llms-against-purpose-built-models-it-wasnt-close)). Resulting design rules:

- **Scheduling:** FSRS-style state per concept; the LLM never predicts memory.
- **The LLM's role:** content and grading only.
- **Help:** hints come before answers, and every session ends with an unaided check.
- **Exercise sentences:** retrieved from the learner's own mined corpus and tagged by grammar point, so they vary between reviews (varied-cue finding) and stay natural (ACL finding).

**Build sketch.** Keep the prototype's MCP surface (`get_current_state`, `batch_update_reviews`, `add_concepts`, `add_note`), but move concept state into the learner model in section 8. Add implicit credit: when an Anki card whose sentence contains a grammar point is passed, that concept gets a small FIRe-style partial review (inference; language items co-occur rather than nest, so the weights are guesses). Trigger lessons from immersion, for example "three new uses of らしい in last night's episode", rather than from a separate study habit, in response to the engagement result.

| Field | Assessment |
|---|---|
| Effort | M for the revival; L if implicit credit and corpus tagging are done properly |
| Payoff | Medium. Grammar was where flashcards had failed before, but the prototype's sessions found production limited more by vocabulary than grammar |
| Risks | Becomes another daily obligation that lapses, as in 2025; LLM grading noise |
| Evidence gate | Concepts the tutor marks mastered are recognised in unseen episode lines at a higher rate than unscheduled control concepts |
| Stop condition | If sessions are skipped more than half the time after a month, fold the useful parts into the overlay (d) as on-demand grammar hints and stop scheduling concepts |

## 7. Planned tools: hybrid reading and the selective-gloss overlay

### (c) Graded hybrid-reading browser rewriter

**What it is.** A Nuenki-style browser extension that is aware of the learner's known words. A stated sub-goal of the project, reading Japanese game-programming blogs, points to two distinct modes. Mode c1 rewrites English pages into a hybrid that weaves Japanese into English. Mode c2 glosses Japanese pages, showing a known-word-aware gloss only on words the learner probably does not know.

**What exists.** Nuenki is alive (v2.0.0, July 2026, $5.42/month, closed licence). It is a sentence-level swapper: it scores English source sentences against a generic CEFR model, using Bloom filters in WASM, and replaces whole sentences. There is no sign it imports a personal word list ([nuenki.app](https://nuenki.app/); [difficulty estimator](https://nuenki.app/sentencedifficulty)). illa-helper is an MIT-licensed, LLM-based word replacer (about 2.9k stars, apparently stalled). It controls a replacement ratio but has no Japanese tokeniser and no known-word tracking ([illa-helper](https://github.com/xiao-zaiyi/illa-helper)). Lingoku swaps English words for JLPT-level Japanese, closed source with undisclosed logic ([AMO](https://addons.mozilla.org/firefox/addon/lingoku-ai/)). Toucan lists Japanese as not optimised for web use ([Babbel support](https://support.babbel.com/hc/en-gb/articles/18269893246738-Toucan-browser-extension)). Within the search done, nothing combines a personal known-lemma set, Japanese morphology and LLM rewriting.

**What the evidence says.** Re-RIGHT (ACL 2026) found that prompted frontier models are poor at hitting low vocabulary levels, and worse in Japanese. On Japanese vocabulary coverage GPT-5.2 scored 58.8%, against 76.0% for a 4B model tuned with RL. Claude Sonnet 4.5 is named among the weak prompted baselines ([Re-RIGHT](https://arxiv.org/pdf/2604.05302)). So any rewrite must be verified in code and retried: tokenise, lemmatise, check against the known set, regenerate the spans that miss. Storyfier found that LLM stories containing target words raised engagement but not learning in read-only sessions ([Storyfier](https://arxiv.org/pdf/2308.03864)). A glossing meta-analysis found glossed reading beat unglossed (about 45% versus 27% of targets recalled immediately), L1 glosses beat L2, and multiple-choice glosses were most effective ([SSLA](https://cambridge.org/core/journals/studies-in-second-language-acquisition/article/how-do-different-forms-of-glossing-contribute-to-l2-vocabulary-learning-from-reading/38124150D59DF3039EE1FF5AE88FE922)). The code-switching evidence behind c1 is a master's replication with 8 participants analysed ([UFSC](https://repositorio.ufsc.br/xmlui/handle/123456789/276447)). Read together (inference): c2, glossing Japanese and letting the learner resolve it, is better supported than c1, weaving Japanese into English. Japanese SOV order and particles also make word-level weaving into English produce broken hybrids, so c1 would need clause-level swaps.

**Build sketch.** c2 is the same engine as (d), running as a content script: tokenise with Sudachi, query the learner model, mark unknown lemmas, and resolve each with a dictionary gloss plus an LLM sense pick, cached by page hash and vocabulary version. c1 would fork illa-helper, add Sudachi on the Japanese side and clause-level replacement, and use a cheap local model with verify-and-retry. Nuenki's own developer keeps slower multi-model translation out of the extension for latency reasons ([Nuenki hybrid post](https://nuenki.app/blog/the_best_translator_is_a_hybrid_translator)).

| Field | Assessment |
|---|---|
| Effort | c2: S once (d) and (e) exist. c1: L |
| Payoff | c2: medium-high for the blog-reading goal. c1: low-medium, mainly passive exposure |
| Risks | c1 trains reading of broken Japanese; c2 glosses can be too easy to click (the Bastani crutch effect) |
| Evidence gate (c1) | A one-week Nuenki trial first. If sentence-level swapping does not change how much Japanese gets read, a better version will not either |
| Stop condition | Drop c1 if, after two weeks of use, it does not raise later recall of words met only through it above words met in plain reading |

### (d) Selective-gloss, hint-first game and VN overlay

**What it is.** A texthooker client that receives each line from a game, VN or subtitle track. It leaves known words alone, marks words the learner probably does not know, and offers a hint ladder instead of a translation:

1. Highlight the unknown lemma.
2. Show its reading.
3. Show a multiple-choice L1 gloss.
4. Give a contextual sense or grammar note.
5. Give the full line translation, as a last resort.

Every rung climbed is logged as evidence for the learner model and as a mining candidate.

**What exists.** GameSentenceMiner (GSM) is the notable 2026 development. v2026.9.0 added Linux Wine/Proton text hooking and Wayland-compatible OBS and overlay capture; v2026.9.2 is the latest stable. It also has OCR through an OwOCR fork, a texthooker that merges lines, and automated screenshot and audio capture for Anki ([GSM releases](https://github.com/bpwhelan/GameSentenceMiner/releases)). Linux distribution packaging lags; one packaging effort is only a forum to-do ([NixOS Discourse](https://discourse.nixos.org/t/packaging-gamesentenceminer/74203)). LunaTranslator does full translation with LLM backends and has Yomitan and Anki hooks, but nothing known-word-aware. VN Club advises turning its machine translation off for learning ([Luna](https://github.com/HIllya51/LunaTranslator); [VN Club tools](https://vnclub.org/tools/)). One learner's 2026 workflow is GSM plus texthooker plus Yomitan, with grammar pasted into an LLM by hand ([skerritt.blog](https://skerritt.blog/my-current-way-to-mine-visual-novels/)). No tool found glosses only unknown words or gives graded hints. This is the clearest gap in the research.

**Build sketch.** Subscribe to the texthooker websocket: GSM, or owocr on its default port 7331 ([owocr guide](https://vnclub.org/owocr-guide/)). For anime, read asbplayer's subtitle stream or the .ass file. Render in a browser window on a second monitor; that avoids Wayland overlay compositing, which is undocumented for most tools, and keeps Yomitan available. Tokenise with Sudachi, look up the learner model, and pre-fetch JMdict senses. Rungs 1-3 are deterministic and instant. Rung 4 calls a local 7-14B instruct model on a single 24 GB consumer GPU. VRAM is not the constraint, but latency has not been measured anywhere; hint output is shorter than full translation, which should help (inference). Rung 5 calls the same model or a cloud model. A "would this spoil the plot" flag is out of scope.

| Field | Assessment |
|---|---|
| Effort | M |
| Payoff | High. One engine covers anime, VNs, games and (via c2) Japanese web pages. It improves the enjoyment side directly and generates the best learner-model signal: what was looked up, in context, at what rung |
| Risks | GSM Linux hooking is weeks old and unpackaged; OCR noise; hint rungs that are too easy (multiple-choice glosses are best-evidenced, but from reading tests, not real-time play); a CALICO gloss-density meta-analysis that points in both directions ([CALICO](https://journal.equinoxpub.com/Calico/article/view/16993)) |
| Evidence gate | Within-subject experiment: randomly assign each unknown lemma to the hint-ladder condition or a plain-Yomitan condition, and test recognition of both groups a week later |
| Stop condition | If hint-ladder words are not recalled better than plain-Yomitan words, keep the overlay only for known-word highlighting and logging |

## 8. Planned tool: the shared learner model

### (e) A shared service and data contract

All four tool ideas need the same answer: for this lemma or grammar point, right now, how likely is the learner to know it? Today, Jiten's import, asbplayer's annotation database and the premine script each rebuild that answer from an Anki word field, separately. Surface form versus dictionary form is the main source of mismatch, which is why Jiten has a "parse words instead of importing directly" option ([Jiten import](https://jiten.moe/guides/importing-known-words-from-anki); [asbplayer annotation](https://docs.asbplayer.dev/docs/guides/annotation)).

**Contract (proposal).**

- **Key:** each lemma keyed by JMdict entry ID, with surface and reading as attributes.
- **State per lemma:** status (unknown, encountered, learning, known, blacklisted-name, mastered-by-wordset); linked Anki card IDs; FSRS stability, difficulty and current retrievability, read through ankimcp; encounter count and last-seen time per media; lookup count and highest hint rung reached.
- **Grammar points:** a stable ID, linked cards and corpus sentences, and their own FSRS-style state from (b).
- **Event log:** an append-only log of reviews, exposures, lookups and hint-rung events from every tool.

**Service.** Runs next to Anki as SQLite plus a small local HTTP API:

- `GET /known?lemmas=…` returns status and retrievability.
- `POST /tokenize` runs Sudachi with JMdict linking.
- `POST /event` appends to the log.
- `GET /coverage?text=…` returns known-token share.

Sync from Anki runs on a timer and on demand. Jiten can serve as an optional second source and as a coverage cross-check. Using retrievability rather than a binary known flag is the point: a word with R = 0.6 deserves a rung-1 highlight, not silence.

**Why modest machinery.** Duolingo's HLR and Anki's FSRS are both per-item memory models. The companion memory-palace report found that on the 10k-user benchmark, per-user FSRS-6 trails per-user GRU/LSTM models only slightly in log loss (0.346 against about 0.333). Only a pooled 2.8M-parameter RWKV model does clearly better, and it is not a drop-in scheduler ([srs-benchmark](https://github.com/open-spaced-repetition/srs-benchmark)). Content-aware models mainly help cold-start cards ([KAR3L](https://arxiv.org/pdf/2402.12291)). The new value is not a better memory model. It is putting immersion exposures and lookups into the same table as reviews, which no existing tool does.

| Field | Assessment |
|---|---|
| Effort | S for v0 (known-lemma set plus R, read-only); M with events and grammar points |
| Payoff | Enabling: everything else gets better or becomes possible |
| Risks | Sync drift when Anki is closed; dependence on AnkiConnect or ankimcp |
| Gate | v0 reproduces Jiten's coverage figure for a show within a few points |

## 9. Ranking and staged plan

| Rank | Idea | Effort | Expected payoff | Evidence behind the mechanism | Depends on |
|---|---|---|---|---|---|
| 1 | Anki settings plus manual leech/Click-card pass | S | High, immediate | Manual and guides; varied-cue RCTs | nothing |
| 2 | (e) learner model v0 | S | Enabling | FSRS/HLR lineage | Anki, ankimcp |
| 3 | (a) deck-hygiene agent and Jiten-based premine | S-M | High | Varied cues; retrieval beats generation | 1, 2 |
| 4 | (d) selective-gloss overlay | M | High | Glossing meta-analysis; hint-first RCT (other domain) | 2 |
| 5 | (c2) Japanese-page gloss mode | S after 4 | Medium-high | Same as (d) | 2, 4 |
| 6 | (b) concept tutor revival | M-L | Medium | Hint-first tutoring RCTs (maths/physics) | 2, corpus from 3 |
| 7 | (c1) English-to-hybrid weave | L | Low-medium | Small code-switching studies; Storyfier caution | 2 |

Rationale for the order:

- **Stage 1 first** because it changes the daily experience immediately at no build cost. The settings and the Click-card/leech pass address two to-dos by hand, and the varied-cue result is the strongest evidence in the plan.
- **Learner model second**, as a thin read-only service. It is small, and without it every later tool repeats the known-word plumbing that the premine script, Jiten and asbplayer each already rebuild.
- **Hygiene agent and Jiten-based premine third**, because they finish the third to-do and produce the corpus of real sentences that the tutor and the overlay both need.
- **Overlay above tutor**, because it sits inside the activity the learner already enjoys; the engagement evidence says tools that need a separate habit decay. It also yields the richest learner-model signal, and its Japanese-page mode covers the blog-reading goal almost for free.
- **Concept tutor sixth**, worth reviving only once it can draw on vocabulary state and the learner's own corpus, which fixes what stalled it in 2025.
- **English-to-hybrid weave last**: weakest evidence, hardest Japanese-specific engineering, and a paid baseline (Nuenki) that can be trialled in an afternoon.

## 10. Open questions and evaluation plan

### Open questions

- **Jiten's Anki export.** Does it map onto Lapis fields? How accurate are Jiten's per-title media decks? Its accuracy and data-source pages did not load.
- **Name and sense handling.** How well does an LLM pick JMdict senses and spot character names in anime dialogue? No evaluation exists. The *Katanagatari* set (一寸, character names that are ordinary words, the 9 cards missing sentences) is the first test set.
- **FSRS after Reset.** Does resetting rewritten cards distort the optimiser? Reset keeps history, but the effect on parameter fits is unmeasured.
- **Retention target.** Should immersion-heavy learners run lower desired retention, around 0.85, on show-specific decks? No primary source argues it either way.
- **Linux tooling.** Will GSM's Linux hooking and Wayland capture hold up on the project's Linux desktop, and will the asbplayer Anki add-on work in Firefox on Linux? Both are newer than any guide.
- **Infrastructure.** Will AnkiConnect keep working from its new sr.ht home, or should agent work standardise on ankimcp (Anki must be open either way)?
- **Latency.** What is the per-line latency of a local 7-14B model on a single 24 GB consumer GPU for rung-4 hints? No measurement was found.
- **Kanji.** What to do with the 269 radical notes was not covered by any source; kanji handling is a research gap.
- **Anki time versus immersion.** No source gives a ratio for intermediates. The guides only say to keep Anki subordinate to immersion.

### Evaluation plan

The Bastani result says to measure without the tool in the loop. Each measurement below has that property.

- **Retention:** Anki's true retention by maturity, before and after the changes, plus the `tag:leech` count per optimiser cycle.
- **Sentence cueing:** the word-only probe (the next gate), repeated quarterly.
- **Immersion difficulty:** lookups per 100 tokens and the share of lines needing rung 4 or 5, from overlay logs, tracked per show and over time. A falling lookup rate on comparable shows is the most direct sign of learning.
- **Choosing shows:** Jiten coverage for the next three candidate shows.
- **Comprehension of an unseen episode:** at the start of a new season, watch one episode with Japanese subtitles and no lookups, write a short summary, and compare it with the episode synopsis. Repeat at the same point the next season.
- **Time in Japanese:** hours per week from GSM and asbplayer stats, compared with Anki minutes. If the tooling raises Anki time and lowers immersion time, it is failing on the project's own definition of success.
- **Gloss experiment:** the within-subject randomisation in (d). Words, not sessions, are the unit, which gives a personal test with real statistical power from a single season of watching.

### Research method and coverage

Pages were read through a summarizing fetch tool. Sources that failed to load: animecards.site subpages, learnjapanese.moe anki-settings, the FrequencyMan and FSRS Helper repos, AnkiWeb add-on pages, r/LearnJapanese and r/Anki threads, Jiten's accuracy and data-source pages, jimaku.cc, kitsunekko, and the GitHub API. Community-consensus claims above therefore rest on vnclub, TheMoeWay, Donkuri and tool documentation rather than broad community polling.

## 11. Conclusion

Hiina's Japanese-learning project is at the plan stage as of 25 Oct 2026. The near-term work is configuration, not code: FSRS-6 settings, a Tag Only leech queue with four-way triage, Click cards, and a word-only probe to find and reset sentence-cued cards. The first gate is whether that probe's recall comes within 5 points of normal retention after four weeks. The build work that follows centres on a small learner-model service keyed by JMdict entry, which lets a Jiten-based premine pipeline, a deck-hygiene agent and a hint-first selective-gloss overlay share one view of what the learner knows. The overlay addresses the clearest gap found in existing tools and fits the project's governing constraint: tooling should increase time spent enjoying Japanese media, not time spent in Anki. Each stage has a stop condition, and the main unknowns are LLM sense and name picking on anime dialogue, FSRS behaviour after resets, local-model hint latency, and how well 2026's Linux hooking tools hold up.

## 12. Sources

- [TheMoeWay guide](https://learnjapanese.moe/guide/)
- [Khanmigo RCT, NBER w35620](https://www.nber.org/papers/w35620)
- [Anki releases](https://github.com/ankitects/anki/releases)
- [awesome-fsrs: The Algorithm](https://github.com/open-spaced-repetition/awesome-fsrs/wiki/The-Algorithm)
- [Anki 26.08](https://github.com/ankitects/anki/releases/tag/26.08)
- [Anki manual: Deck Options](https://docs.ankiweb.net/deck-options.html)
- [vnclub Anki guide](https://vnclub.org/anki-guide/)
- [TheMoeWay mining](https://learnjapanese.moe/mining/)
- [Lapis README](https://github.com/donkuri/lapis)
- [Anki manual: Leeches](https://docs.ankiweb.net/leeches.html)
- [Anki forum: confusable pairs](https://forums.ankiweb.net/t/how-do-i-deal-with-pairs-of-cards-that-i-confuse-for-each-other/55515)
- [Anki manual: Studying](https://docs.ankiweb.net/studying.html)
- [Wheeler & Gabbert 2017](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2017.01830/pdf)
- [AI associative exemplification pilot](https://www.jstage.jst.go.jp/article/his/27/4/27_261/_article/-char/en)
- [Variable retrieval, PNAS 2024](https://share.swps.edu.pl/handle/swps/1120)
- [anki-ai-dynamic-cards](https://github.com/AleksandrFurmenkovOfficial/anki-ai-dynamic-cards)
- [Donkuri mining](https://donkuri.github.io/learn-japanese/mining/)
- [ACL SRW 2024 example sentences](https://preview.aclanthology.org/setup/2024.acl-srw.55)
- [Lapis releases](https://github.com/donkuri/lapis/releases)
- [Sirush/Jiten](https://github.com/Sirush/Jiten)
- [Jiten API](https://jiten.moe/guides/using-the-api)
- [Jiten word sets](https://jiten.moe/guides/word-sets)
- [Jiten: importing from Anki](https://jiten.moe/guides/importing-known-words-from-anki)
- [Jiten: choosing media](https://jiten.moe/guides/choosing-media-at-your-level)
- [Sudachi](https://github.com/WorksApplications/Sudachi)
- [Anki Miner](https://pypi.org/project/anki-miner/)
- [AnkiMorphs docs](https://mortii.github.io/anki-morphs/)
- [asbplayer releases](https://github.com/killergerbah/asbplayer/releases)
- [asbplayer one-click mining](https://docs.asbplayer.dev/docs/guides/one-click-mining)
- [asbplayer annotation](https://docs.asbplayer.dev/docs/guides/annotation)
- [mpvacious](https://github.com/Ajatt-Tools/mpvacious)
- [alass](https://github.com/kaegi/alass)
- [FooSoft/anki-connect (archived)](https://github.com/FooSoft/anki-connect)
- [raine/anki-llm](https://github.com/raine/anki-llm)
- [ankimcp add-on](https://github.com/ankimcp/anki-mcp-server-addon)
- [LECTOR](https://papers.cool/arxiv/2508.03275)
- [Brown medical LLM flashcards](https://www.medrxiv.org/content/10.1101/2025.05.13.25327518v1.full.pdf)
- [Skycak, FIRe](https://justinmath.com/individualized-spaced-repetition-in-hierarchical-knowledge-structures/)
- [Matuschak on Math Academy](https://notes.andymatuschak.org/Math_Academy)
- [Bunpro forum](https://community.bunpro.jp/t/how-does-bunpro-choose-which-sentence-to-review-for-a-given-grammar-point/45486)
- [Manabi Mentor](https://github.com/c0m/manabi-mentor-preplugin/blob/master/README.md)
- [Wharton on Bastani et al.](https://knowledge.wharton.upenn.edu/article/without-guardrails-generative-ai-can-harm-education)
- [Bastani et al., PNAS](https://www.pnas.org/doi/10.1073/pnas.2422633122)
- [Kestin et al. RCT](https://pmc.ncbi.nlm.nih.gov/articles/PMC12179260/)
- [Eedi LLM knowledge tracing](https://eedi.com/news/we-benchmarked-llms-against-purpose-built-models-it-wasnt-close)
- [Nuenki](https://nuenki.app/)
- [Nuenki sentence difficulty](https://nuenki.app/sentencedifficulty)
- [illa-helper](https://github.com/xiao-zaiyi/illa-helper)
- [Lingoku on AMO](https://addons.mozilla.org/firefox/addon/lingoku-ai/)
- [Toucan](https://support.babbel.com/hc/en-gb/articles/18269893246738-Toucan-browser-extension)
- [Re-RIGHT](https://arxiv.org/pdf/2604.05302)
- [Storyfier](https://arxiv.org/pdf/2308.03864)
- [Glossing meta-analysis, SSLA](https://cambridge.org/core/journals/studies-in-second-language-acquisition/article/how-do-different-forms-of-glossing-contribute-to-l2-vocabulary-learning-from-reading/38124150D59DF3039EE1FF5AE88FE922)
- [UFSC code-switching replication](https://repositorio.ufsc.br/xmlui/handle/123456789/276447)
- [Nuenki hybrid translator](https://nuenki.app/blog/the_best_translator_is_a_hybrid_translator)
- [GameSentenceMiner releases](https://github.com/bpwhelan/GameSentenceMiner/releases)
- [NixOS Discourse: packaging GSM](https://discourse.nixos.org/t/packaging-gamesentenceminer/74203)
- [LunaTranslator](https://github.com/HIllya51/LunaTranslator)
- [VN Club tools](https://vnclub.org/tools/)
- [skerritt.blog VN mining](https://skerritt.blog/my-current-way-to-mine-visual-novels/)
- [VN Club owocr guide](https://vnclub.org/owocr-guide/)
- [CALICO gloss density](https://journal.equinoxpub.com/Calico/article/view/16993)
- [srs-benchmark](https://github.com/open-spaced-repetition/srs-benchmark)
- [KAR3L](https://arxiv.org/pdf/2402.12291)
- [Anki 26.05](https://github.com/ankitects/anki/releases/tag/26.05)
- [ABC of FSRS](https://github.com/open-spaced-repetition/awesome-fsrs/wiki/ABC-of-FSRS)
- [Donkuri setup](https://donkuri.github.io/learn-japanese/setup/)
- [Anki forum: FSRS workload](https://forums.ankiweb.net/t/since-switching-to-fsrs-workload-has-gone-up-dramatically/56350.md)
- [animecards.site](https://animecards.site/)
- [asbplayer blog](https://docs.asbplayer.dev/blog)
- [mpvacious releases](https://github.com/Ajatt-Tools/mpvacious/releases)
- [Jiten features](https://jiten.moe/features)
- [Jiten frequency dictionaries](https://jiten.moe/frequency-dictionaries)
- [Jiten vs JPDB](https://jiten.moe/guides/jpdb-alternative)
- [jpdb changelog](https://jpdb.io/changelog)
- [ffsubsync](https://github.com/smacke/ffsubsync)
- [Yomitan releases](https://github.com/yomidevs/yomitan/releases)
- [learnjapanese.moe autocards](https://learnjapanese.moe/autocards/)
- [nailuoGG/anki-mcp-server](https://github.com/nailuoGG/anki-mcp-server)
- [ujisati/anki-mcp](https://github.com/ujisati/anki-mcp)
- [Saarela et al. meta-analysis record](https://jyx.jyu.fi/jyx/Record/jyx_123456789_109005/Description)
- [SRS-Stories](https://arxiv.org/abs/2512.18362v1)
- [Laufer & Ravenhorst-Kalovski](https://cris.haifa.ac.il/en/publications/lexical-threshold-revisited-lexical-text-coverage-learners-vocabu/)
- [GameSentenceMiner](https://github.com/bpwhelan/GameSentenceMiner)
- [TheMoeWay VN on Linux](https://learnjapanese.moe/vn-linux)
- [meikipop docs](https://mintlify.wiki/rtr46/meikipop/introduction.md)
- [Shintaku 2023, LLT](https://scholarspace.manoa.hawaii.edu/items/cf2700ff-d95e-4ddc-a4eb-32a0662f97a5)
- [Sakura-GalTransl-7B](https://huggingface.co/SakuraLLM/Sakura-GalTransl-7B-v3.7)
