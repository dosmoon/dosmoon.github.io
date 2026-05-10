---
title: "In the AI Coding Era, Software With Fewer Dependencies Wins"
description: AI Coding flattened the cost of building vs borrowing a wheel. Dependency count quietly became the most reliable indicator of engineering quality — and the dosmoon studio's working philosophy.
sidebar:
  order: 1
---

## The afternoon that started this train of thought

A while back I built the aistack project in a single day with Claude Code — wrapping Ollama, ASR, and TTS into a local proxy layer, with some performance tuning across a few models thrown in for good measure. In 2023, this would have been roughly two months of work for a three-person team.

The gap isn't really about lines of code. The 2023 version of this work would have spent almost all its time on **non-coding work**: figuring out how to tune Whisper's CTranslate2 backend, finding how to pass `keep_alive` to Ollama, digging through GitHub issues for the holes other people had already fallen into, fiddling with parameters against the piper-tts README, debugging why some quantized model was emitting empty tokens. Each of these is fifteen minutes; stack them up and it's weeks.

What AI Coding really saved wasn't the time spent writing code. It was the time spent **reading docs, looking up APIs, hitting potholes, and integrating libraries**.

But staring at this one-day project, I noticed something more important than "I went faster" —

**The dependency list was just a few lines long.**

No LangChain. No AI agent framework. No "integration SDK". Ollama's API, the ASR engine, the TTS engine — all spoken to directly over HTTP or stdio. The proxy layer is mine, a thousand-something lines of Python, with no "middleware" wedged in between.

In 2020, this kind of project would have been mocked as "unprofessional". In 2026, it's what "modern" actually means.

Pushing on that observation — it's not just about my tiny project. It points at a trend that's already underway but hasn't been named:

**The standard for evaluating software is being rewritten. In the AI Coding era, software with fewer dependencies wins.**

## Why this didn't hold before AI Coding

Let me start by being clear about why "few dependencies" wasn't an evaluation criterion in the past.

For the last twenty years, the mainstream criteria for software quality have been: how many features, how good the benchmarks, how complete the docs, how active the community, how rich the ecosystem, how much modern tech it uses.

Those criteria made sense for that era — because the cost of "writing it yourself" was extreme, so "leaning on something else" was inevitable. A project that pulled in 50 open-source dependencies, wired up 10 cloud services, and integrated 20 SDKs would be praised as "really thorough".

But that evaluation framework had an internal contradiction from the start — **the more dependencies you have, the more fragile, harder to maintain, more rot-prone, and less time-resilient the software becomes**. Under the constraint of "writing it yourself is expensive", these costs were suppressed. Nobody wanted to look directly at them.

Underneath was a simple cost curve: implementing a feature yourself = 100 units of cost, using an off-the-shelf library = 5 units. At 20× difference, "don't use the library" is irrational. So engineering culture inevitably evolved into "find a library first, write your own only if you can't find one". The explosive growth of npm / Maven / pip is a product of this curve.

**After AI Coding arrived, the curve flattened.**

Implementing it yourself = 8 units, using a library = 5 units. The 20× gap collapsed to 1.6×.

That gap is no longer enough to compensate for the hidden cost of using someone else's library — learning its domain concepts, reading its docs (often outdated), adapting to its design philosophy, dealing with its transitive dependencies, racing against its version churn, waiting for it to fix bugs or working around them, and the act of maintaining "our project's dependency list" itself.

These hidden costs used to be hidden under the weight of "rolling your own takes 100 units". Now that rolling your own only takes 8, those costs surface immediately as visible burden.

**Many libraries flipped from "tools that save you time" to "burdens that consume your time"** — and a lot of people haven't realized the inflection point yet.

## The forgotten metric

Now let's address head-on: why does **dependency count** become a core metric for evaluating software in the new era?

Because dependency count caps several of software's most important engineering properties.

**First, dependency count caps comprehensibility.** There's an upper bound to how much code one engineer can fully understand — somewhere around hundreds of thousands of lines for a single person. If your software itself is a few thousand lines but pulls in 200 open-source libraries totaling tens of millions of lines — in theory no single human can fully understand this software. The "understanding" is just "understanding the thin layer I wrote myself". This pseudo-understanding is fine in simple scenarios but breaks immediately under hard bugs or performance issues.

**Second, dependency count caps evolvability.** Every dependency has its own evolution rhythm — when it ships a new version, when it changes its API, when it stops being maintained — none of which you control. The more dependencies, the more your software is dragged along by uncontrollable external forces. A project with 200 dependencies has a massive yearly load of "keeping up with dependency updates" — work that's pure overhead, generating no business value.

**Third, dependency count determines attack surface.** Every dependency is a potential security hole. The npm left-pad incident, the Log4j catastrophe, the xz utils backdoor — these are all real cases of dependencies being poisoned. The more dependencies, the higher the probability of a supply-chain attack.

**Fourth, dependency count determines distributability.** A zero-dependency piece of software can be shipped as one binary that just runs. A Node.js project with 500 dependencies needs `npm install` for half an hour, and may fail because some package vanished from the registry. Self-containment is inversely proportional to dependency count — and self-containment directly determines whether normal users can use the software, whether it can run in restricted environments, and whether it can be preserved long-term.

**Fifth, dependency count determines lifespan.** SQLite still runs after 30 years — because it has almost no external dependencies. If a C compiler runs, SQLite runs. A 2010 Rails project today probably won't start — because among its hundreds of gems, just a few being unmaintained or incompatible with new Ruby is enough to kill it. **Dependency count is essentially software's "shelf life" — more dependencies, shorter shelf life.**

Comprehensibility, evolvability, security, distributability, lifespan — software's most important engineering properties all correlate negatively with dependency count. This isn't a coincidence; it's a mathematical regularity.

And this metric is unusually hard to fake. Performance benchmarks can be specially optimized for the test, community activity can be bought with stars, user counts can be subsidized — but **your dependency list is public, countable, and unforgeable**. Open the `package.json` / `requirements.txt` / `Cargo.toml` of a project that claims to be "lightweight" and the truth shows up immediately.

**This transparency is what makes dependency count the most reliable objective evidence of engineering quality.**

## The software that survived across eras

The most convincing evidence for this rule is looking at which software actually crossed eras and survived.

The desktop / general-purpose software that's still around after thirty years is almost uniformly small projects with a pure-C core:

- **SQLite** — possibly the most widely deployed software in the world. Single-file pure C. In planes, phones, browsers, operating systems.
- **FFmpeg** — the substrate for everyone's transcoding, editing, and streaming. Pure C.
- **curl** — the de facto standard for sending HTTP requests. Pure C.
- **Redis** — the standard answer for the cache layer. Single process, pure C.
- **Nginx** — the winner in the web server space. Pure C.
- **Vim** — an editor that's been alive for thirty-plus years. Pure C.
- **Lua** — the king of embedded scripting, from game engines to Redis. Pure C.
- **VLC / mpv** — the multimedia playback standard. C/C++ core.

This isn't coincidence — it's the result of industrial selection. Thirty years of engineering evolution is an extremely cruel survival-of-the-fittest process. What lives isn't what was "marketed well" — it's what **doesn't have a weak point on any concrete engineering axis**.

What do they have in common?

**Extremely short dependency lists.** SQLite's dependencies are basically just libc. FFmpeg is modular and can be compiled into a near-zero-external-dependency build. curl's main body is libc plus a few optional libraries. The Lua interpreter and standard library are under 20K lines, zero external dependencies.

**Self-contained, consumable from any environment.** A SQLite library can be embedded in Python, Java, Go, Rust, or Swift. An FFmpeg binary runs on any OS. A `curl` invocation behaves the same on a 1995 server and a 2026 edge device.

**The entire codebase can be read by one person.** SQLite's main body is around 150K lines; early Redis was tens of thousands; the entire codebase of these projects is readable by a single human — meaning the project never falls into a "no one understands it" state.

**Independent of OS, independent of hardware evolution.** They only speak the minimum POSIX subset; they don't depend on any particular OS's GUI / event / IPC model. The result: however the OS evolves, however hardware turns over, they keep running.

The desktop software that didn't survive shares a pattern in hindsight: **its core was bound to a particular era's "modern framework"**.

90s programs in MFC — bound to Windows + C++/MFC, no cross-platform path, no continued maintenance. 2000s Java Swing desktop apps — bound to the JVM, slow to start, memory-heavy. The various .NET desktop apps — bound to the Windows ecosystem. Heavyweight Electron apps — core fused with UI, hundreds of MB to start.

**None of this is because "the team didn't try hard enough" — it's because they picked the wrong core substrate. They wrote the core logic inside a framework or runtime that had a shelf life. The framework expired, the product expired with it.** Whereas SQLite / FFmpeg / curl wrote their core logic on top of the most plain, most stable C standard. So they don't have a shelf life.

**The secret to long-lived software isn't "use the most advanced technology" — it's "use the technology that won't change". Advanced becomes outdated. Only "won't change" can cross eras.** And the physical expression of "won't change" is: extremely few dependencies, all of them on stable foundations that have been time-tested.

## The dependency list as a window into engineering taste

There's a property of this new evaluation criterion I particularly like — **it exposes the engineering philosophy of the software's author**.

Open a project's dependency file — `package.json`, `requirements.txt`, `Cargo.toml`, whichever — and you can see far more than "which libraries it uses". You can see how the author thinks about engineering, how they make tradeoffs, how they treat long-term maintenance.

- A web framework that calls itself a "full-stack solution" with 300 dependencies — its author has **framework thinking**, believing complexity is managed by stacking abstractions.
- A database engine that calls itself "feature complete" but only depends on the C standard library — its author has **kernel thinking**, believing complexity is managed by deep mastery.
- An AI app that pitches "fast integration" and depends on LangChain plus 50 other packages — its author is leaning, outsourcing every uncertainty upstream.
- An AI app that talks directly to the OpenAI HTTP API, with stdlib + httpx as its only dependencies — its author is autonomous, every line of code is something they can explain.

**These differences aren't just technical choices — they're externalizations of different engineering philosophies.** Read the dependency list, and you can see the taste of the human behind the software.

This kind of taste-recognition is becoming more important in hiring and collaboration. A candidate whose résumé says "expert in Spring Cloud, fluent in 50+ frameworks" — that was an asset in the old era; in the new one it's a question mark. **The truly scarce skill isn't "knowing how to use lots of things" — it's "knowing which things not to use".** The latter judgment is far harder to develop, and far more valuable, than the former.

## The implication

This rule matters because it lines up with several other engineering rules and reinforces them:

- **Code is documentation, code is design** — provided the code is yours, readable, and not scattered across external dependencies.
- **Self-contained, OS-independent, hardware-independent** — that's just dependency count approaching zero.
- **The plain trio of core + UI + CLI** — this structure naturally has few dependencies.
- **Consumer-internet giants build their wheels at the lowest layer** — that's external dependencies being replaced with internal components.
- **Throw it out when it should be thrown out, throw it fast** — what gets thrown out is redundant dependencies.

The unified statement of all these observations is **"fewer external dependencies win"**. It's the umbrella metric that pulls all the scattered observations together.

It also explains some technical outcomes that previously looked "anomalous":

- Why is SQLite respected by engineers more than MongoDB? SQLite has near-zero dependencies.
- Why did nginx beat Apache? nginx has fewer dependencies and is more focused.
- Why did Linux win over GNU/Hurd? The Linux kernel is highly self-contained and design-focused.
- Why did Go win in the cloud-native era? Go's culture encourages "few dependencies" and compiles to a single binary.
- Why is Tauri displacing Electron in the next-gen desktop? Tauri's dependencies are an order of magnitude smaller than Electron's.
- Why did VSCode displace Visual Studio? VSCode's core (Monaco editor) is thin, with extensions loaded on demand; VS Studio is heavy and bundles everything.

**Across these technical outcomes, dependency count is a highly accurate predictor variable.**

Conversely, projects on the way down almost all have a dependency-bloat story. The Node.js `node_modules` black hole has become an industry joke. Java enterprise apps' jar hell, Python projects' version-conflict disasters, the various "build a simple system out of 50 microservices" overengineering — **all symptoms of "too many dependencies", once celebrated as "modern, professional", will in the AI Coding era be recognized as cautionary tales**.

## The engineering renaissance of the AI Coding era

A layer deeper —

AI Coding doesn't just change "the criteria for evaluating software". It does something more profound: **it converts the engineering aesthetic that previously only top-tier engineers could afford into a standard ordinary engineers can hit.**

This aesthetic of "zero-dependency, self-contained, core + UI + CLI" used to be a luxury available only to a few top-tier engineers — D. Richard Hipp writing SQLite, Fabrice Bellard writing FFmpeg, Bram Moolenaar writing Vim. Ordinary engineers couldn't pull it off; they had to use other people's wheels and accept the cost of dependency bloat.

**AI Coding turns this luxury into a commodity.** Any serious engineer, paired with AI, can write something smaller than LangChain, lighter than Spring, more direct than React — purpose-built for their own needs, clean, self-contained, controllable.

Once everyone can do it, the market standard naturally rises to demand it of every product.

**This is a real engineering renaissance** — not a return to the past, but a renewed embrace, on top of new technical capability (AI Coding), of engineering virtues that industrialization had suppressed: self-containment, simplicity, independence, longevity. The 70s Unix philosophy of "small composable tools + text protocols + single responsibility" is coming back to the mainstream on the back of AI Coding.

I expect that in the next five to ten years, the mainstream aesthetic of software engineering will visibly shift — **"less is more" will move from a minority slogan to industry consensus.**

## Concrete suggestions

If you buy this new evaluation rule, a few things to start doing today:

**First, open whatever project you're working on and count the dependencies.** Ask yourself: is each one truly necessary, or did you bring it in for convenience? How many of them are pulled in for a tiny fraction of their functionality? This exercise forces you to re-examine the project's real structure.

**Second, before introducing a new dependency, ask "could I write a minimal version myself?"** Before AI Coding, the answer was usually "no, too expensive". Now the answer is increasingly "yes, half a day". **Every time you implement it yourself instead of pulling in a dependency, you're investing in the project's long-term life.**

**Third, do a "dependency audit" on old projects.** List every dependency, sort them into three buckets: must keep, can be replaced with something lighter, can be cut entirely. Then start with the easiest cuts, one a week. Three months later you'll be surprised at how clean the project has become.

**Fourth, recalibrate your selection taste.** When evaluating a tool or framework, look at its dependency list first. A tool that pitches itself as "modern, ecosystem-rich" but pulls in hundreds of packages, vs. one that's "more basic but only depends on a handful" — in the new era, the latter is often the better choice.

**Fifth, develop "anti-framework" judgment.** A framework's promise is always seductive — "it handles everything for you". But the cost is that your code is shaped by its worldview, your fate is bound to its evolution. **A library is something you call; a framework is something that calls you. Inverting the call relationship means losing control.** When you can pick a library, don't pick a framework.

## Closing

Software engineering is a craft that re-evaluates itself as technical capability changes.

For the last twenty years, the cost curve of "writing it yourself is expensive, using something else is cheap" determined software's mainstream form — dependency bloat, framework prosperity, ecosystem assemblage. That form was reasonable for its era, but its reasonableness rested on a specific cost structure.

**AI Coding changed that cost structure.** When the cost of building a wheel approaches zero, the old rule of "don't reinvent the wheel" needs re-examination. It hasn't died, but its applicable range is shrinking sharply.

The software that wins in the new era will be the kind that saw the new rules early and adopted the new evaluation standard — **fewer dependencies wins.**

Not because few dependencies "looks clean", but because few dependencies is genuinely better on every engineering axis that matters — comprehensibility, evolvability, security, distributability, lifespan. This is a mathematical regularity, not an aesthetic preference.

**Over the next three to five years, more and more projects with confusingly few dependencies, suspiciously simple, unsettlingly independent, will win their markets one after another.** By the time the majority realizes the evaluation standard has changed, the people who saw the trend first will already have shipped the next-generation product.

So what's worth doing today is starting to apply this new yardstick to all software — other people's, and especially your own.

Less is more. This time, the era has finally caught up with the saying.
