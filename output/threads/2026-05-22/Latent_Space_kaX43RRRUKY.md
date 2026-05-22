# AI Agents Need Computers: 74% MoM Growth, 850K/Day Runs, & New Agent Cloud — Ivan Burazin, Daytona (2026-05-22)

## 🧵 VIRAL THREAD

Post 1: The era of the API is ending. The era of the Agent Computer is beginning. 🤖💻

I just sat down with Ivan Burazin, CEO of Daytona, and the numbers are staggering: 74% MoM growth and 850K runs per day. 

The thesis? AI Agents don't just need code; they need computers. 🧵

---
Post 2: Most people think AI agents live in a "sandbox"—a tiny, ephemeral box to run a script. 

They're wrong. ❌

Agents need "composable computers." They need state, persistence, and the ability to "open the lid" and resume work exactly where they left off. 

---
Post 3: The technical moat is insane. Daytona is hitting 60ms spin-up times. ⚡️

By running on bare metal with a custom scheduler, they've bypassed the latency of traditional VMs. 

When you're running 50,000 concurrent tasks, you don't need a "function"—you need an engine.

---
Post 4: The next trillion-dollar frontier? "Computer Use." 🖥️

Agents are hitting a wall with headless APIs. To unlock the real world (healthcare, finance, gov), they need to use legacy Windows and Mac apps just like humans do. 

Daytona is building the infra to make this scalable.

---
Post 5: The macro shift is real: The bottleneck is moving from GPUs to CPUs. 📉

We've mastered GPU scaling, but the massive influx of agentic workloads is creating a massive demand for high-performance, scalable CPU compute. 

The "Agent Cloud" is the next Stripe or Twilio.

---
Post 6: The "spiky" workload problem is the new frontier for infra engineers. 📈

Unlike human traffic (follow-the-sun), Agent RL and Evals are unpredictable. They go from 0 to 100,000 CPUs instantly. 

If your infra can't handle the burst, you've already lost.

---
Post 7: THE ALPHA: Don't just watch the models; watch the primitives. 💎

The winners won't just be the LLM labs, but the companies providing the sandboxes, the web search, and the databases specifically for agents.

The Agent Cloud is being built right now. 🚀

Follow for more deep dives into the AI infra revolution.

---

## 📰 SUMMARY ARTICLE

# The Rise of the Agent Cloud: Why AI Agents Need Computers, Not Just APIs

**TL;DR:** As AI agents evolve from simple script-runners to autonomous workers, the underlying infrastructure is undergoing a fundamental shift. Daytona, experiencing 74% month-over-month growth, is pioneering the "Agent Cloud"—a specialized infrastructure layer providing stateful, high-performance, composable computers designed specifically for non-human users.

### 🔑 Key Insights
* **From APIs to Computers:** Agents require more than ephemeral execution; they need persistent, stateful environments that mimic the "open-and-close" workflow of a human laptop.
 
* **The Infrastructure Bottleneck is Shifting:** While the world has focused on GPU shortages, the explosion of agentic workloads is creating a massive, unpredictable demand for high-performance CPU compute and specialized networking.

* **The "Computer Use" Revolution:** To unlock trillions in value from legacy sectors (Finance, Healthcare, Gov), agents must move beyond headless APIs and interact with legacy Windows and Mac software via scalable sandboxes.

* **The "Spiky" Workload Challenge:** Unlike human-centric "follow-the-sun" usage patterns, agentic workloads (like RL and Evals) are highly unpredictable, requiring infra that can scale from zero to hundreds of thousands of CPUs instantly.

### 🧠 Deep Dive

#### The Death of the Ephemeral Sandbox
For years, the industry has treated AI execution as a "serverless" problem—short-lived, stateless, and isolated. However, as Ivan Burazin explains, agents are not just executing code; they are performing tasks that require context, persistence, and the ability to resume work. Daytona is moving away from the "sandbox" nomenclature toward "composable computers." This infrastructure allows agents to maintain state, much like a human user closing a laptop lid and returning later to find their work intact.

#### Engineering for Extreme Scale and Speed
The technical differentiation of Daytona lies in its "bare metal" approach. By utilizing a custom-built scheduler and bypassing the overhead of traditional virtualization layers, Daytona achieves a 60ms spin-up time for single instances. This is critical for the massive concurrency required by the next generation of AI. As the company handles nearly 850,000 runs per day, the ability to manage massive, "spiky" bursts of activity—where a single customer might request 50,000 concurrent CPUs—is becoming the primary differentiator for compute providers.

#### The Trillion-Dollar Opportunity in Legacy Integration
The most profound implication of the "Agent Cloud" is the automation of "Computer Use." A massive portion of the global economy remains locked within legacy Windows and Mac applications that lack modern APIs. For agents to become truly autonomous, they must be able to navigate these interfaces. Daytona is investing heavily in the ability to run these environments at scale. If agents can effectively use the tools humans use, the addressable market for automation expands from simple data processing to the entirety of global knowledge work.

### 💬 Notable Quotes
> "The market for every single agent that will exist ever in the future is just... what is that market? How big is that? ... We are all in on this."

> "The most efficient way for an agent to work is essentially headless... but [most work] is still locked into legacy apps inside of Windows which is not going anywhere for a very, very long time."

### 🏁 Conclusion
The transition from human-centric cloud computing to agent-centric "Agent Cloud" computing is one of the most significant shifts in the history of the internet. As the workload moves from predictable, human-driven cycles to the massive, unpredictable, and high-throughput demands of autonomous agents, the winners will be those who provide the specialized primitives—the sandboxes, the state, and the compute—necessary to power the autonomous workforce.

---
IMAGE GENERATION PROMPT: A cinematic, high-tech visualization of a digital "Agent Cloud." In the center, a glowing, translucent, multi-layered 3D computer interface is being constructed by millions of tiny, luminous autonomous particles (representing agents). The background shows a vast, dark network of interconnected nodes and glowing data streams, symbolizing global scale. The aesthetic is "cybernetic minimalism"—sleek, professional, and futuristic, with a color palette of deep navy, electric cyan, and sharp white light. 8k resolution, hyper-realistic, Unreal Engine 5 render style.