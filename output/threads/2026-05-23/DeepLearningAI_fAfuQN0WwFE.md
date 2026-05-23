# AI Dev 26 x SF | Ara Khan: Evals Are Broken Use Them Anyway (2026-05-23)

## 🧵 VIRAL THREAD

Post 1: AI benchmarks are a lie. ❌

Most people are either obsessed with chasing meaningless numbers or they rely entirely on "vibes." Both approaches are wrong.

If you want to build production-grade AI agents, you need a new way to think about Evals. 🧵
---
Post 2: There are two camps of "wrong" when it comes to Evals:

1/ The Objective Metrics Camp: Believing every benchmark score is "truth." In reality, labs often game these scores for clout.

2/ The Vibes Camp: Thinking numbers are useless and only "feeling" matters.

The truth? The truth is in the middle. ⚖️
---
Post 3: How to actually interpret Evals (The 3 Heuristics):

1️⃣ Don't take model lab evals as "word of God." Use your own discernment.
2️⃣ Stay current, but don't be an early adopter. Let the dust settle for a few weeks.
3️⃣ Use problem-specific evals. Generic benchmarks (like Fibonacci) are useless for real-world coding agents.
---
Post 4: To build great agents, you must move to "Agentic Evals."

Don't measure single-turn answers. Measure 40-minute runs. ⏳

Track:
• Tool call efficiency
• Token usage & cost
• Latency
• Success via deterministic unit tests

This is how you find the sweet spot between "Frontier Model" and "Cheap/Fast Model."
---
Post 5: The 3 Zones of Agent Improvement:

🟢 Zone 1: Fixing obvious flaws (broken tools, bad checkpoints).
🟡 Zone 2: The "Hill Climbing" zone. Real engineering. Optimizing prompts, tools, and logic.
🔴 Zone 3: The Danger Zone. Overfitting your prompt just to "game" the benchmark score.
---
Post 6: The ultimate engineering stack for Evals:

• Use Terminal Bench for real-world software tasks (race conditions, DB bugs).
• Use Containerization to isolate environments.
• Use Modal to parallelize runs so you aren't waiting 7 hours for a result. 🚀
---
Post 7: The Golden Rule:

Use Evals to drive your engineering, but never stop performing the "Vibe Check." If the agent doesn't feel sensible and solve the actual problem, the score doesn't matter.

Build, test, and hill climb. 🛠️

If you found this useful, follow for more AI agent alpha.

---

## 📰 SUMMARY ARTICLE

# Beyond the Benchmark: How to Navigate the "Broken" World of AI Evals

**TL;DR:** While traditional AI benchmarks are increasingly gamed and often irrelevant to real-world use cases, they remain an essential engineering discipline. By moving from generic metrics to problem-specific, agentic evaluations and tracking operational costs, developers can "hill climb" toward superior AI agents.

### 🔑 Key Insights
* **The Fallacy of Two Camps:** Both the "Objective Metrics" crowd (who believe all scores are truth) and the "Vibe" crowd (who ignore numbers entirely) are fundamentally wrong.
* **The Importance of Specificity:** Generic benchmarks like Fibonacci sequences are useless for coding agents; developers must use benchmarks that reflect real-world software engineering (e.g., database issues, race conditions).
* **The Three Zones of Optimization:** Engineering progress moves from fixing fundamental tool flaws (Zone 1), to nuanced prompt/logic optimization (Zone 2), to the dangerous trap of overfitting to metrics (Zone 3).
* **Operational Metrics Matter:** True evaluation requires tracking not just success/failure, but turns, tool calls, latency, and cost-per-run.

### 🧠 Deep Dive

#### The Death of the Generic Benchmark
In the current AI arms race, model laboratories are under immense pressure to produce high benchmark scores to capture social media attention. This has led to a "gaming" of the system where models are optimized for specific, easily solvable benchmarks that do not translate to real-world utility. Ara Khan argues that the industry is split between those who blindly trust these inflated numbers and those who dismiss them as "vibes." The path to mastery lies in using evals as a tool for discernment rather than a source of absolute truth.

#### Engineering Agentic Evals
For complex AI agents—such as coding agents that may run for 40 minutes at a time—traditional single-turn evaluations are insufficient. The next frontier is "Agentic Eval," which measures the entire lifecycle of an agent's execution. This involves setting up isolated, containerized environments (using tools like Harbor) and running the agent through long-duration tasks that end in deterministic unit tests. By leveraging infrastructure like Modal to parallelize these heavy workloads, developers can rapidly iterate on their agent's performance without waiting hours for sequential results.

#### The Strategy of "Hill Climbing"
The ultimate goal of using evals is "hill climbing"—the iterative process of improving an agent's performance through systematic testing. This involves moving through three distinct stages. First, fixing "broken" foundational elements like tool-calling errors. Second, the heavy lifting of engineering: optimizing the "harness" (the agent's scaffolding) and the prompts. Finally, developers must avoid the "Danger Zone," where they optimize purely for a metric at the expense of actual utility, leading to models that pass tests but fail in production.

### 💬 Notable Quotes
> "Don't ever believe model lab eval... you have to use your own discernment. They're close approximations, but they're not perfect."

> "You got to start somewhere... and even if you get a good score, you always need to make sure that you're passing the vibe check."

### 🏁 Conclusion
The future of AI development belongs to those who treat evaluation as a rigorous engineering discipline. By moving away from the hype of generic benchmarks and toward the granular, cost-aware, and problem-specific evaluation of agentic workflows, developers can move beyond "vibes" to build truly reliable, production-ready AI systems.

---
IMAGE GENERATION PROMPT: A cinematic, high-tech visualization of an AI agent navigating a complex, multi-dimensional software architecture. Glowing neural networks intertwining with lines of code and containerized environments. Deep blues and vibrant teals, hyper-realistic, 8k, symbolizing the intersection of engineering precision and algorithmic intelligence.