# What rebuilding AlphaGo teaches us about self-play, RL, and future of LLMs - Eric Jang (2026-05-22)

## 🧵 VIRAL THREAD

Post 1: AlphaGo wasn't just a win for DeepMind. It was a blueprint for how to compress intractable complexity into a single neural network pass. I sat down with Eric Jang, who rebuilt AlphaGo from scratch on sabbatical. Here is why the future of LLM reasoning depends on this. 🧵
---
Post 2: The problem: Go is mathematically "intractable." The number of possible moves is greater than the atoms in the universe ($361^{300}$). Traditional search hits a wall. You can't brute-force your way to God-tier play.
---
Post 3: The breakthrough: AlphaGo used Neural Nets to "shrink" the tree.
• Policy Net handles the BREATH (pruning bad moves).
• Value Net handles the DEPTH (predicting winners without playing to the end).
It amortizes massive computation into a 10-layer forward pass.
---
Post 4: But the real magic is the training. Modern LLM RL is "sucking supervision through a straw"—high variance, low signal. AlphaGo does something much smarter. It uses MCTS (Search) as a "Teacher" to provide better labels for the Policy Net to imitate.
---
Post 5: Instead of just "playing and seeing if you win" (high variance RL), AlphaGo uses search to generate a "better" version of itself. It turns a hard Reinforcement Learning problem into a stable Supervised Learning problem. It's climbing a much cleaner gradient.
---
Post 6: The future of AI research? We are already automating the "Inner Loop" (hyperparams, experiments) using LLM agents. The next frontier is the "Outer Loop": using AI to decide *which* scientific questions are worth asking.
---
Post 7: THE ALPHA TAKE: Architecture is transitory. Compute is king. As GPUs get faster, the "clever tricks" of the past disappear, leaving only the raw power of scaling. The next era of AGI won't just be larger models—it will be better search-driven reasoning. 

Read the full breakdown here: [Link]

---

able

## 📰 SUMMARY ARTICLE

# The AlphaGo Blueprint: How Search-Based Supervision Could Solve the LLM Reasoning Crisis

**TL;DR:** By rebuilding AlphaGo from scratch, Eric Jang reveals that the path to advanced AI reasoning lies in using Monte Carlo Tree Search (MCTS) as a "teacher" to provide high-quality, low-variance labels, effectively turning difficult Reinforcement Learning problems into stable Supervised Learning tasks.

### 🔑 Key Insights
* **Complexity Compression:** Neural networks can "amortize" NP-hard or intractable computational problems (like Go or Protein Folding) by compressing massive simulations into a single, efficient forward pass.
* **The "Straw" Problem in LLM RL:** Current LLM reinforcement learning suffers from "sucking supervision through a straw"—the signal is too sparse and high-variance because the model only receives a reward at the end of a long sequence.
* **Search as a Teacher:** AlphaGo’s true innovation was using MCTS to generate "improved" action distributions, which the policy network then imitated, creating a stable, iterative improvement loop.
able
* **The Automation of Science:** We have already entered the era of the "Automated Inner Loop," where LLM agents can optimize hyperparameters and execute experiments. The next frontier is automating the "Outer Loop" (hypothesis generation).

### 🧠 Deep Dive

#### The Architecture of Intractability
The sheer scale of the game of Go—with a state space far exceeding the number of atoms in the observable universe—rendered traditional search algorithms useless. Eric Jang explains that AlphaGo’s brilliance was not just in playing the game, but in using deep learning to make the search tractable. By utilizing a **Policy Network** to prune the breadth of the search tree and a **Value Network** to truncate its depth, AlphaGo effectively "compressed" a nearly infinite simulation into a manageable 10-layer computational pass. This principle of "amortizing" complexity is likely the foundation for future breakthroughs in physical simulations, such as AlphaFold.

#### Moving Beyond "Sucking Supervision Through a Straw"
A critical tension in modern AI is the difference between how LLMs learn and how AlphaGo learned. Current LLM Reinforcement Learning (RL) is notoriously inefficient; as the horizon of a task grows longer, the "bits per FLOP" of learning decreases. As noted in the interview, current methods are akin to "sucking supervision through a straw"—waiting for a single reward at the end of a long trajectory to credit a sequence of thousands of tokens. 

In contrast, AlphaGo utilized MCTS to act as a continuous, high-quality teacher. By performing a search at every move, the system generates a "better" distribution of moves than the raw policy could suggest. The policy network then simply learns to imitate this search-enhanced distribution. This transforms a high-variance RL problem into a stable Supervised Learning problem, allowing for much more efficient and rapid scaling.

#### The Two Loops of Automated Research
The interview concludes with a profound look at the future of scientific discovery. We are currently witnessing the automation of the **"Inner Loop"** of research—the grunt work of hyperparameter tuning, data augmentation, and experiment execution. Using LLM-based agents, researchers can now "vibe-code" entire experimental pipelines. However, the **"Outer Loop"**—the high-level cognitive task of deciding *which* experiment to run next and identifying the true bottleneck in a research track—remains a human domain. The ultimate goal of AI-driven science is to bridge this gap, creating an agent capable of both executing the experiment and formulating the hypothesis.

### 💬 Notable Quotes
> "AlphaGo's core conceptual breakthrough was using neural nets to make this search problem tractable... It's profound how a ten-layer network can amortize the simulation of something so deep in the game tree."

> "Modern LLM RL is like 'sucking supervision through a straw.' You're trying to maximize your bits per FLOP, but the signal is incredibly sparse."

### 🏁 Conclusion
The reconstruction of AlphaGo serves as a reminder that while "The Bitter Lesson" (scaling compute) is the primary driver of AI progress, the structural way we use that compute—specifically through the marriage of search and learning—will determine whether we can move from pattern recognition to true, verifiable reasoning.

---
IMAGE GENERATION PROMPT: A cinematic, hyper-realistic wide shot of a futuristic, translucent neural network shaped like a Go board. Glowing white and black stones are suspended in a digital void. Streams of golden data (representing MCTS search paths) are weaving through the stones, connecting them in complex, fractal-like patterns. The background is a deep cosmic nebula, symbolizing the infinite complexity of the game tree. 8k resolution, cyberpunk aesthetic, intricate lighting, highly detailed.