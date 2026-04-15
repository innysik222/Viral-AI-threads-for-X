# Inside Notion AI: The 5 Rebuilds Behind Custom Agents — Simon Last & Sarah Sachs, Notion (2026-04-15)

## 🧵 VIRAL THREAD

Post 1: Notion AI didn't just "launch." They rebuilt it 5 times. 🛠️

While the world was celebrating GPT-4, the team at @Notion was in the trenches, failing, pivoting, and re-architecting their entire AI strategy. 

Here is the "insider" blueprint of how they built the future of agents. 🧵

---
Post 2: The 2022 "Failure" Era 📉

In late 2022, Notion tried to build a coding agent. It sucked. 

Why? The models were too dumb and context windows were too short. They tried custom XML formats and complex tool-calling frameworks. 

The lesson: Don't fight the model. Work with it.

---
Post 3: The Breakthrough: "Give Models What They Want" 🧠

The pivot that changed everything? Abandoning Notion’s complex internal data model for the AI. 

Instead of forcing a heavy JSON structure, they moved to:
✅ Notion-flavored Markdown
✅ SQLite-based querying

The result? Massive velocity. If the model understands it, the agent can use it.

---
Post 4: "Notion is not a wrapper." 🛡️

The biggest criticism of AI startups: "You're just a wrapper on OpenAI."

Notion’s rebuttal is elite: "Notion is the DataDog of AWS." 

AWS provides the storage; DataDog provides the observability. Notion provides the system of record; the agents provide the execution.

---
Post  5: The Rise of the "Model Behavior Engineer" (MBE) 🧬

The AI era is creating new, non-traditional roles. Enter the MBE.

Forget traditional software engineering. This role is about:
• Linguistics & Prompt Craft
• Model evaluation & "Taste"
• Understanding the "human-agent" interface

It’s not about writing code; it’s about managing intelligence.

---
Post 6: The Vision: The "Software Factory" 🏭

The next frontier isn't just agents that "help" you. It's agents that bootstrap themselves.

Notion is building toward a "Software Factory" where agents:
• Write their own code
• Debug their own tools
• Maintain their own codebase

The human role shifts from "coder" to "observer of the system."

---
Post 7: The Alpha Take 💎

The real moat in the AI era isn't the LLM—it's the infrastructure. 

The winners won't be those with the best prompts, but those who build the best "agent-friendly" primitives (Markdown, SQLite, MCP) and the best "system of record" for agents to inhabit.

Follow for more deep dives into the frontier. 🚀

---

## 📰 SUMMARY ARTICLE

# Beyond the Wrapper: How Notion Rebuilt Its AI Core 5 Times to Power the Agentic Era

**TL;DR:** Notion's journey from failed 2022 coding agents to today's sophisticated custom agents reveals a fundamental truth: success in AI isn't about the model, but the infrastructure, tools, and "agent-friendly" data layers built around it.

### 🔑 Key Insights
* **The Death of Complexity:** Notion found success by abandoning their complex internal data models in favor of "what models want"—specifically Markdown and SQLite.
* **The DataDog Analogy:** Notion positions itself not as an OpenAI wrapper, but as the essential "observability and collaboration" layer (the DataDog) for the underlying cloud of AI models.
* **The Rise of the MBE:** A new engineering discipline, "Model Behavior Engineering," is emerging, prioritizing linguistics, evaluation, and "taste" over traditional algorithmic coding.
* **Agent-Centric Design:** The future of software lies in "Software Factories," where agents are the primary users, and humans act as high-level supervisors of autonomous, self-bootstrapping systems.

### 🧠 Deep Dive

#### The Archaeology of Rebuilds
The development of Notion AI has been a process of "stripping away" complexity. Since 2022, the team has undergone at least five major architectural shifts. Early attempts focused on complex XML representations designed to map perfectly to Notion's block model. However, these failed because they forced the LLM to learn a proprietary language. The breakthrough came when the team pivoted to a "model-first" approach, providing agents with familiar, lightweight primitives like Markdown and SQLite. By making the data "agent-friendly," they unlocked the ability to scale tool usage without breaking the model's reasoning capabilities.

#### Infrastructure as the Real Moat
A central theme of the discussion is the distinction between "wrappers" and "systems of record." While many fear that LLM advancements will commoditize AI startups, Notion argues that their value lies in the infrastructure. By building an ecosystem of "agent-friendly" tools, MCP (Model Context Protocol) integrations, and robust permission models, Notion is creating a "Software Factory." In this vision, agents don't just perform tasks; they inhabit a workspace, write their own code, and manage their own documentation, all within a secure, enterprise-grade environment.

#### The Evolution of Engineering Roles
The technical landscape is shifting the very definition of a software engineer. The interview highlights the emergence of "Model Behavior Engineers" (MBEs)—specialists who focus on the qualitative aspects of model performance, such as latency, precision, and "agentic find" (optimizing search for agents). As agents begin to handle more of the "lower-level" coding tasks, the human engineer's role is moving up the abstraction ladder, transitioning from a writer of code to an architect of the "outer loop"—the system of supervision, verification, and high-level intent.

### 💬 Notable Quotes
> "Notion is the DataDog of AWS. DataDog could not exist without cloud storage... we are experts on understanding how people want to collaborate."

> "The real trick is to not do that [swimming upstream] for too long, but realize that there was something there... Give models what they want."

### 🏁 Conclusion
The era of the "AI wrapper" is ending, and the era of the "Agentic System of Record" is beginning. As models become more capable, the competitive advantage shifts from the intelligence of the model to the utility of the environment in which that intelligence operates. For companies like Notion, the goal is to build a world where agents can seamlessly bootstrap, debug, and maintain the very software they use, turning the workspace into an autonomous factory of productivity.

---
IMAGE GENERATION PROMPT: A cinematic, hyper-realistic wide shot of a futuristic digital workspace. Transparent, glowing holographic layers of Notion-style documents, databases, and code snippets are being woven together by ethereal, flowing strands of light representing neural networks. In the background, a vast, organized "software factory" of glowing data nodes and interconnected streams. High-tech, sophisticated, 8k, deep blues and soft whites, concept of "The Agentic System of Record."