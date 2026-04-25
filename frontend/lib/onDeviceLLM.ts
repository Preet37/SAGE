"use client";

/**
 * On-device LLM bridge — wraps @mlc-ai/web-llm so the rest of the app sees
 * a single API. Falls back to a clear error if WebGPU / web-llm aren't
 * available so the cloud path can take over.
 *
 * This is the ZETIC track's web equivalent: the model runs entirely in the
 * student's browser using WebGPU. No tokens leave the device.
 */

export interface OnDeviceModel {
  id: string;
  label: string;
  approxSizeMb: number;
  description: string;
}

export const ON_DEVICE_MODELS: OnDeviceModel[] = [
  {
    id: "Llama-3.2-1B-Instruct-q4f16_1-MLC",
    label: "Llama 3.2 1B · 4-bit",
    approxSizeMb: 880,
    description: "Fast and tiny. Best for instant Q&A and quick comprehension checks.",
  },
  {
    id: "Llama-3.2-3B-Instruct-q4f16_1-MLC",
    label: "Llama 3.2 3B · 4-bit",
    approxSizeMb: 2200,
    description: "Smarter — takes longer to load but reasons better on technical material.",
  },
  {
    id: "Phi-3.5-mini-instruct-q4f16_1-MLC",
    label: "Phi-3.5 mini · 4-bit",
    approxSizeMb: 1900,
    description: "Microsoft's reasoning-tuned model, good at step-by-step explanations.",
  },
];

export interface InitProgress {
  progress: number;       // 0–1
  text: string;
}

export interface OnDeviceEngine {
  modelId: string;
  generate: (
    messages: { role: "system" | "user" | "assistant"; content: string }[],
    onToken: (delta: string) => void,
    signal?: AbortSignal,
  ) => Promise<{ text: string; tokensPerSec: number; latencyMs: number }>;
  unload: () => Promise<void>;
}

let _engine: { id: string; instance: unknown } | null = null;

export async function isWebGPUAvailable(): Promise<boolean> {
  if (typeof navigator === "undefined") return false;
  // @ts-expect-error WebGPU types not in DOM lib by default
  if (!navigator.gpu) return false;
  try {
    // @ts-expect-error WebGPU
    const adapter = await navigator.gpu.requestAdapter();
    return !!adapter;
  } catch {
    return false;
  }
}

export async function loadOnDeviceEngine(
  modelId: string,
  onProgress: (p: InitProgress) => void,
): Promise<OnDeviceEngine> {
  if (_engine && _engine.id === modelId) {
    return wrapEngine(_engine.instance, modelId);
  }
  if (_engine) {
    try {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      await (_engine.instance as any).unload?.();
    } catch { /* ignore */ }
    _engine = null;
  }

  let webllm: typeof import("@mlc-ai/web-llm");
  try {
    webllm = await import("@mlc-ai/web-llm");
  } catch (err) {
    throw new Error(
      "On-device runtime not installed. Run `npm install @mlc-ai/web-llm` in frontend/."
    );
  }

  const engine = await webllm.CreateMLCEngine(modelId, {
    initProgressCallback: (rep: { progress: number; text: string }) => {
      onProgress({ progress: rep.progress, text: rep.text });
    },
  });
  _engine = { id: modelId, instance: engine };
  return wrapEngine(engine, modelId);
}

function wrapEngine(engine: unknown, modelId: string): OnDeviceEngine {
  return {
    modelId,
    async generate(messages, onToken, signal) {
      const start = performance.now();
      let text = "";
      let tokens = 0;
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const stream = await (engine as any).chat.completions.create({
        messages, stream: true, temperature: 0.6, max_tokens: 512,
      });
      for await (const chunk of stream) {
        if (signal?.aborted) break;
        const delta = chunk.choices?.[0]?.delta?.content || "";
        if (delta) {
          text += delta;
          tokens += 1;
          onToken(delta);
        }
      }
      const latencyMs = performance.now() - start;
      const tokensPerSec = tokens / Math.max(latencyMs / 1000, 0.001);
      return { text, tokensPerSec, latencyMs };
    },
    async unload() {
      try {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        await (engine as any).unload?.();
      } catch { /* ignore */ }
      _engine = null;
    },
  };
}
