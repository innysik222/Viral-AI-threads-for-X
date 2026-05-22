# AI Dev 26 x SF | Ashwyn Sharma: Every App Needs a Voice UI. Here's How to Build It (2026-05-22)

## 🧵 VIRAL THREAD

Post 1: The "STT -> LLM -> TTS" sandwich is dead. 🥪

If you're building voice AI by just layering models, you're building a "hot mess" of latency and context bloat. 

The future isn't just text-to-speech; it's bidirectional, multimodal, and seamless. 🧵

---
Post 2: We've all been there. 

A "2-week" voice project turns into a 2-year nightmare of "alphabet soup":
• VAD (Voice Activity Detection)
• Prosody
• Endpointing
• Turn detection

The complexity kills the product. There's a better way. 🛠️

---
Post 3: The new standard: The 3 Surfaces of Voice AI.

1️⃣ **Applications:** Adding voice to React apps.
2️⃣ **Agents:** Giving a "voice" to existing LLM agents.
3️⃣ **Tools:** Using voice as a functional modality for the agent to trigger.

This is how you achieve true multimodality. 🌊

---
Post 4: True Voice UI requires bidirectional awareness. 🔄

It's not just the agent talking to the app. The app must talk back. 

Using hooks like `onAction` and `sendAction`, your agent can "see" the UI state (like a Tic-Tac-Toe board) and react to mouse clicks or keyboard inputs in real-time.

---
Post 5: Stop bloating your context window. 🧠

The biggest mistake? Forcing your LLM to manage the entire conversation state. 

The pro move: Use a dedicated voice layer with its own "brain" that knows when to handle small talk and when to delegate complex queries to your primary agent (like Claude).

---
Post 6: The "Alpha" take: Voice is the new Mobile. 📱

Just as every web app eventually required a mobile surface to survive, every AI agent and application will eventually require a voice interface. 

If you aren't building for voice today, you're building for a dying interface.

---
Post 7: The dev experience is moving to:
`npm install vocalbridge-ai-sdk-react`

The stack is disappearing. The interface is all that remains.

Want to stay ahead of the multimodal wave? Follow for more deep dives into the AI infra stack. 🚀

---

## 📰 SUMMARY ARTICLE

# Beyond the Sandwich: Why the Future of AI is Bi-Directional Voice

**TL;DR:** At AI Dev 26, Ashwyn Sharma (CEO of Vocal Bridge) demonstrated how to move past the inefficient "STT-LLM-TTS" architecture. By leveraging a managed voice platform, developers can integrate high-awareness, bidirectional voice interfaces into applications and agents, treating voice not just as an output, but as a functional tool.

### 🔑 Key Insights
* **The Death of the "Sandwich" Architecture:** Traditional methods of layering speech-to-text, LLMs, and text-to-speech create massive latency and "context window pollution," where the LLM is distracted by managing dialogue state rather than tasks.
* **Bidirectional UI Awareness:** The next generation of Voice UI (VUI) requires the application to send events back to the agent (e.g., `user place mark`), allowing the agent to have complete contextual awareness of the application's state.
* **Voice as a Functional Tool:** Multimodality is evolving. Agents can now decide to switch modalities—moving from text to voice for complex brainstorming—or use voice to trigger real-world actions, such as making outbound phone calls.
* **Eliminating the "Alphabet Soup":** Managed platforms allow developers to bypass the grueling engineering required for Voice Activity Detection (VAD), prosody, and endpointing.

### 🧠 Deep Dive

#### The Engineering Nightmare of Legacy Voice AI
For years, developers attempting to implement voice have fallen into a "complexity trap." What begins as a simple implementation of speech-to-text and text-to-speech quickly devolves into a massive infrastructure challenge involving turn detection and complex handling of audio streams. Ashwyn Sharma notes that this often extends project timelines from weeks to years, creating a "hot mess" of fragmented components that are difficult to maintain in production.

#### The Three Surfaces of Integration
The presentation highlighted three distinct ways to deploy voice:
1. **Voice-Enabled Applications:** Integrating voice into existing React-based UIs. Through the use of `onAction` and `sendAction` hooks, the agent and the UI become a single, cohesive entity where voice commands and manual inputs (mouse/keyboard) are synchronized.
2. **Voice-Enabled Agents:** Providing a vocal layer to text-based LLM agents (like Claude). This layer acts as a "brain" that handles conversational nuances, preventing the primary LLM from being overwhelmed by the mechanics of speech.
3. **Voice as a Tool:** The most advanced frontier, where the agent uses voice as a modality switch. An agent can recognize that a task (like brainstorming) is better suited for voice and can even use voice to execute tools, such as initiating a phone call to a third party.

#### The Shift Toward Multimodal Ubiquity
The overarching vision is a paradigm shift in user interface design. Much like the transition from desktop-only to mobile-first web design, the industry is moving toward a "voice-included" standard. By utilizing declarative JSON formats to define client actions, the barrier to entry for creating sophisticated, multimodal AI experiences is being drastically lowered, allowing developers to focus on logic rather than audio infrastructure.

### 💬 Notable Quotes
> "What starts off as... a couple of weeks worth of project work... ends up with 6 months, sometimes years, of time it takes for the team to deploy the product in production."

> "Every interface, every application, every AI agent is going to have voice as an interface in the future. Just like every web application eventually got a mobile surface."

### 🏁 Conclusion
The era of treating voice as a mere "add-on" is ending. As the complexity of managing audio pipelines becomes a bottleneck for innovation, managed platforms like Vocal Bridge are enabling a new era of bidirectional, multimodal intelligence. The goal is no longer just to make machines talk, but to make them part of a seamless, interactive loop between human intent and digital action.

---
IMAGE GENERATION PROMPT: A cinematic, high-tech visualization of a human voice transforming into digital data streams. Glowing blue and violet sound waves morphing into complex React code and 3D user interface elements. Hyper-realistic, futuristic laboratory aesthetic, deep depth of field, 8k resolution, symbolizing the bridge between speech and software.