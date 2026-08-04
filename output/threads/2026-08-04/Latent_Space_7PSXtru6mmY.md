# Next 100x in AI: Inference, Networking, & Self-Optimizing Models — Philip Kiely & Ali Taha, Baseten (2026-08-04)

## 🧵 VIRAL THREAD

Post 1: **"Did you know JLM52 can self-write GPU kernels? Here's how it optimizes models 10x faster!" #AIInnovation #SelfOptimization**

---
Post 2: **"How Base 10 handles long queries: Cache-aware routing, speculative decoding, and more. It’s like magic!" #Base10Tech #InferenceMagic**

---
Post 3: **"Quantization isn’t always worse! Baseten showed a 20% better quantized model than Nvidia. Game changer!" #QuantizationOptimization #BasetenTech**

---
Post 4: **"Why some models can be 10x faster? Key steps: KV caching, speculators, and disaggregation. It’s all about efficiency!" #ModelSpeedup #InferenceEngineering**

---
Post 5: **"Rubens vs Blackwell: The GPU that kills your kernels? Rubens might just change everything in AI inference." #RubensGPU #AIHardware**

---
Post 6: **"Auto-regressive video models are coming. They will revolutionize how we generate videos, but quality is still a big issue." #AutoRegVideo #InnovationHype**

---
Post 7: **"Join the Alpha Program to get access to cutting-edge AI optimization tools and stay ahead of the curve! Click here to sign up now!" #AIAlphaProgram #StayInformed**

---

## 📰 SUMMARY ARTICLE

# Inference Engineering's Next Frontier: Optimizing AI Models for Speed and Efficiency

**TL;DR:** The next 100x improvements in AI will come from optimizing inference models through advanced techniques like quantization, speculators, and disaggregation. Baseten is leading the way with groundbreaking methods.

### 🔑 Key Insights
*   **Quantization Improvements:** Quantization can now improve model performance rather than just degrade it, thanks to mathematical proofs that show how certain layers cancel out errors.
*   **KV Caching & Speculators:** These techniques significantly speed up inference by caching and predicting tokens, making models run faster without losing fidelity.
*   **Disaggregation & Tensor Parallelism:** Breaking down models into smaller chunks and using tensor parallelism can dramatically increase throughput while maintaining performance.

### 🧠 Deep Dive
#### Optimizing Inference Models with Quantization

Philip Kiely from Baseten reveals a breakthrough in quantization: rather than simply reducing precision, it is now possible to optimize layers for better performance. The team's research shows that choosing the right layers to quantize can actually enhance model accuracy and speed.

#### Speculators & Speculative Decoding

Ali Taha explains how speculators work—small models that predict tokens to reduce latency. These speculative decoders can be trained on hidden states from the main model, making them more accurate over time. This technique significantly speeds up inference while maintaining high fidelity.

#### Disaggregation & Tensor Parallelism

Disaggregating models across multiple GPUs and using tensor parallelism are key strategies for achieving higher throughput. Baseten has shown that these techniques can boost performance by orders of magnitude without compromising model quality.

### 💬 Notable Quotes
> "The main lossy optimization is quantization. It comes down to data format, which layers you choose to quantize, and doing a lot of calibration on the quantized weights." - Philip Kiely

### 🏁 Conclusion

Inference engineering is evolving rapidly, with new techniques like speculators, disaggregation, and optimized quantization pushing the boundaries of what's possible. Baseten’s advances could lead to AI models that are not only faster but also more efficient in resource usage.

---

IMAGE GENERATION PROMPT: A cutting-edge AI model being optimally deployed across multiple GPUs, with a focus on the advanced techniques discussed in the article.