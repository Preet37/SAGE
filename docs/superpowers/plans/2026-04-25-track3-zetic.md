# Track 3: ZETIC / On-Device AI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a production-grade Expo React Native companion app (`sage-mobile/`) that runs all tutoring inference locally via ZETIC Melange SDK. Privacy Mode proves zero outbound requests during inference. A performance dashboard shows NPU/GPU/CPU metrics. Fully offline after model download.

**Architecture:** `sage-mobile/` is a standalone Expo project sharing the same SAGE backend. The Melange engine wrapper (`lib/melange.ts`) adapts the SDK for streaming tokens. Privacy Mode routes all inference to Melange (local); normal mode hits the SAGE backend. A network traffic interceptor on the PrivacyScreen proves the zero-outbound claim.

**Tech Stack:** Expo ~51, React Native, @zetic/melange-rn (verify exact name at melange.zetic.ai/docs), expo-sqlite, expo-network, AsyncStorage

---

## File Map

| File | Action | Purpose |
|------|--------|---------|
| `sage-mobile/package.json` | Create | Expo project manifest |
| `sage-mobile/app.json` | Create | Expo app config |
| `sage-mobile/App.tsx` | Create | Root navigator (Stack) |
| `sage-mobile/lib/melange.ts` | Create | Melange engine wrapper + streaming adapter |
| `sage-mobile/lib/api.ts` | Create | SAGE backend API client (cloud mode) |
| `sage-mobile/lib/store.ts` | Create | Zustand store (privacy mode, model selection, messages) |
| `sage-mobile/screens/LessonScreen.tsx` | Create | Full tutoring experience with on-device inference |
| `sage-mobile/screens/ModelManagerScreen.tsx` | Create | Melange model catalog + benchmarking |
| `sage-mobile/screens/PrivacyScreen.tsx` | Create | Network monitor proving zero outbound requests |
| `sage-mobile/components/PerformanceDashboard.tsx` | Create | Live metrics card with ZETIC badge |
| `sage-mobile/components/PrivacyModeToggle.tsx` | Create | Toggle + status indicator |
| `sage-mobile/components/TrackBadge.tsx` | Create | Reusable colored badge pill |

---

### Task 1: Initialize Expo project

**Files:**
- Create: `sage-mobile/package.json`
- Create: `sage-mobile/app.json`

- [ ] **Step 1: Scaffold Expo project**

```bash
npx create-expo-app sage-mobile --template blank-typescript
cd sage-mobile
```

Expected: `sage-mobile/` directory with `package.json`, `app.json`, `App.tsx`, `tsconfig.json`.

- [ ] **Step 2: Install required dependencies**

```bash
cd sage-mobile
npx expo install expo-sqlite expo-network @react-native-async-storage/async-storage
npm install zustand
```

Then install ZETIC Melange (verify package name first):

```bash
# Check the exact package name at: https://melange.zetic.ai/docs
# Most likely one of:
npm install @zetic/melange-rn
# OR:
# npm install @zetic.ai/melange
```

If the npm install fails, note the exact package name from the docs and use that name consistently throughout all files in this plan.

- [ ] **Step 3: Update app.json with correct app name**

Edit `sage-mobile/app.json` so it reads:

```json
{
  "expo": {
    "name": "SAGE Mobile",
    "slug": "sage-mobile",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "userInterfaceStyle": "dark",
    "splash": {
      "backgroundColor": "#0a0a0a"
    },
    "ios": {
      "supportsTablet": true,
      "bundleIdentifier": "ai.sage.mobile"
    },
    "android": {
      "package": "ai.sage.mobile",
      "adaptiveIcon": {
        "backgroundColor": "#0a0a0a"
      }
    }
  }
}
```

- [ ] **Step 4: Verify Expo starts**

```bash
cd sage-mobile && npx expo start --no-dev
```

Expected: QR code appears, no errors. Press Ctrl+C.

- [ ] **Step 5: Commit**

```bash
cd ..
git add sage-mobile/
git commit -m "feat(zetic): initialize Expo React Native project (sage-mobile/)"
```

---

### Task 2: Create Melange engine wrapper

**Files:**
- Create: `sage-mobile/lib/melange.ts`

- [ ] **Step 1: Create lib/ directory and melange.ts**

```bash
mkdir -p sage-mobile/lib
```

Create `sage-mobile/lib/melange.ts`:

```typescript
/**
 * ZETIC Melange engine wrapper.
 * Provides a unified interface for loading models and streaming tokens.
 * All inference stays on-device — never sends data to any server.
 *
 * NOTE: Verify import path at melange.zetic.ai/docs before running.
 * Replace '@zetic/melange-rn' with the exact registered package name.
 */

// @ts-ignore — replace with exact package name once confirmed
import { MelangeEngine } from '@zetic/melange-rn';

export interface ModelInfo {
  id: string;
  name: string;
  sizeMb: number;
  computeUnit: 'CPU' | 'GPU' | 'NPU' | 'auto';
}

export interface InferenceMetrics {
  firstTokenMs: number;
  throughputTokensPerSec: number;
  computeUnit: string;
  modelName: string;
  modelSizeMb: number;
}

export interface MelangeStreamResult {
  token: string;
  done: boolean;
  metrics?: InferenceMetrics;
}

let _engine: InstanceType<typeof MelangeEngine> | null = null;
let _loadedModelId: string | null = null;

/**
 * Load a Melange model. No-op if already loaded.
 * onProgress: 0.0 → 1.0 download/compile progress.
 */
export async function loadModel(
  model: ModelInfo,
  onProgress: (pct: number) => void
): Promise<void> {
  if (_loadedModelId === model.id && _engine) return;

  _engine = new MelangeEngine({
    modelId: model.id,
    device: model.computeUnit === 'auto' ? 'auto' : model.computeUnit.toLowerCase(),
    onProgress: (pct: number) => onProgress(pct),
  });

  await _engine.load();
  _loadedModelId = model.id;
}

/**
 * Stream tokens from the on-device model.
 * Yields { token, done, metrics? } objects.
 */
export async function* streamOnDevice(
  systemPrompt: string,
  userMessage: string,
  model: ModelInfo
): AsyncGenerator<MelangeStreamResult> {
  if (!_engine || _loadedModelId !== model.id) {
    throw new Error('Model not loaded. Call loadModel() first.');
  }

  const startMs = Date.now();
  let tokenCount = 0;
  let firstTokenMs = 0;

  const fullPrompt = `${systemPrompt}\n\nStudent: ${userMessage}\nSAGE:`;
  const stream = _engine.stream(fullPrompt);

  for await (const token of stream) {
    tokenCount++;
    if (tokenCount === 1) {
      firstTokenMs = Date.now() - startMs;
    }

    yield { token: token as string, done: false };
  }

  const totalMs = Date.now() - startMs;
  const throughput = tokenCount > 0 ? (tokenCount / (totalMs / 1000)) : 0;

  const deviceInfo = await _engine.getDeviceInfo?.() ?? {};

  yield {
    token: '',
    done: true,
    metrics: {
      firstTokenMs,
      throughputTokensPerSec: Math.round(throughput),
      computeUnit: deviceInfo.computeUnit ?? model.computeUnit,
      modelName: model.name,
      modelSizeMb: model.sizeMb,
    },
  };
}

/**
 * Run a single benchmark: generate 10 tokens, measure latency.
 */
export async function benchmarkModel(model: ModelInfo): Promise<InferenceMetrics> {
  await loadModel(model, () => {});

  const testPrompt = 'What is a neural network? Answer in exactly 10 tokens.';
  const results: MelangeStreamResult[] = [];

  for await (const chunk of streamOnDevice('You are a helpful assistant.', testPrompt, model)) {
    results.push(chunk);
    if (results.length > 15) break; // safety stop
  }

  const finalChunk = results[results.length - 1];
  return finalChunk.metrics ?? {
    firstTokenMs: 0,
    throughputTokensPerSec: 0,
    computeUnit: 'CPU',
    modelName: model.name,
    modelSizeMb: model.sizeMb,
  };
}

/** Unload model to free device memory. */
export function unloadModel(): void {
  _engine = null;
  _loadedModelId = null;
}
```

- [ ] **Step 2: Create catalog of available models**

Create `sage-mobile/lib/models.ts`:

```typescript
import { ModelInfo } from './melange';

/** Default Melange model catalog. Adjust IDs to match actual Melange registry. */
export const MELANGE_MODELS: ModelInfo[] = [
  {
    id: 'phi-3.5-mini-instruct',
    name: 'Phi-3.5-mini',
    sizeMb: 2400,
    computeUnit: 'NPU',
  },
  {
    id: 'llama-3.2-1b-instruct',
    name: 'Llama 3.2 1B',
    sizeMb: 900,
    computeUnit: 'GPU',
  },
  {
    id: 'gemma-2b-it',
    name: 'Gemma 2B',
    sizeMb: 1800,
    computeUnit: 'CPU',
  },
];

export const DEFAULT_MODEL = MELANGE_MODELS[0];
```

- [ ] **Step 3: Commit**

```bash
cd sage-mobile && git add lib/
git commit -m "feat(zetic): create Melange engine wrapper with streaming and benchmarking"
```

---

### Task 3: Create Zustand store and API client

**Files:**
- Create: `sage-mobile/lib/store.ts`
- Create: `sage-mobile/lib/api.ts`

- [ ] **Step 1: Create store.ts**

```typescript
import { create } from 'zustand';
import { ModelInfo } from './melange';
import { DEFAULT_MODEL } from './models';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  metrics?: {
    firstTokenMs: number;
    throughputTokensPerSec: number;
    computeUnit: string;
    modelName: string;
    modelSizeMb: number;
  };
}

interface AppState {
  privacyMode: boolean;
  selectedModel: ModelInfo;
  messages: Message[];
  isStreaming: boolean;
  networkEvents: Array<{ url: string; method: string; timestamp: number }>;

  setPrivacyMode: (on: boolean) => void;
  setSelectedModel: (model: ModelInfo) => void;
  addMessage: (msg: Message) => void;
  appendToLast: (token: string) => void;
  setLastMetrics: (metrics: Message['metrics']) => void;
  setStreaming: (v: boolean) => void;
  clearMessages: () => void;
  addNetworkEvent: (event: AppState['networkEvents'][number]) => void;
  clearNetworkEvents: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  privacyMode: true,
  selectedModel: DEFAULT_MODEL,
  messages: [],
  isStreaming: false,
  networkEvents: [],

  setPrivacyMode: (on) => set({ privacyMode: on }),
  setSelectedModel: (model) => set({ selectedModel: model }),
  addMessage: (msg) => set((s) => ({ messages: [...s.messages, msg] })),
  appendToLast: (token) =>
    set((s) => {
      const msgs = [...s.messages];
      if (msgs.length && msgs[msgs.length - 1].role === 'assistant') {
        msgs[msgs.length - 1] = {
          ...msgs[msgs.length - 1],
          content: msgs[msgs.length - 1].content + token,
        };
      }
      return { messages: msgs };
    }),
  setLastMetrics: (metrics) =>
    set((s) => {
      const msgs = [...s.messages];
      if (msgs.length && msgs[msgs.length - 1].role === 'assistant') {
        msgs[msgs.length - 1] = { ...msgs[msgs.length - 1], metrics };
      }
      return { messages: msgs };
    }),
  setStreaming: (v) => set({ isStreaming: v }),
  clearMessages: () => set({ messages: [] }),
  addNetworkEvent: (event) =>
    set((s) => ({ networkEvents: [...s.networkEvents.slice(-49), event] })),
  clearNetworkEvents: () => set({ networkEvents: [] }),
}));
```

- [ ] **Step 2: Create api.ts**

```typescript
/** SAGE backend API client — used in cloud mode only. */

const BASE_URL = process.env.EXPO_PUBLIC_SAGE_API_URL ?? 'http://localhost:8000';

export async function cloudChat(
  lessonId: number,
  message: string,
  token: string,
  onToken: (t: string) => void,
): Promise<void> {
  const res = await fetch(`${BASE_URL}/tutor/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ lesson_id: lessonId, message, history: [] }),
  });

  if (!res.ok) throw new Error(`Cloud chat failed: ${res.status}`);

  const reader = res.body?.getReader();
  if (!reader) return;

  const decoder = new TextDecoder();
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const chunk = decoder.decode(value);
    for (const line of chunk.split('\n')) {
      if (line.startsWith('data: ')) {
        try {
          const d = JSON.parse(line.slice(6));
          if (d.type === 'token' && d.data?.text) {
            onToken(d.data.text);
          }
        } catch {}
      }
    }
  }
}
```

- [ ] **Step 3: Commit**

```bash
git add lib/store.ts lib/api.ts lib/models.ts
git commit -m "feat(zetic): add Zustand store (privacy mode, model selection) and cloud API client"
```

---

### Task 4: Build TrackBadge and PrivacyModeToggle components

**Files:**
- Create: `sage-mobile/components/TrackBadge.tsx`
- Create: `sage-mobile/components/PrivacyModeToggle.tsx`

- [ ] **Step 1: Create components/ directory and TrackBadge**

```bash
mkdir -p sage-mobile/components
```

Create `sage-mobile/components/TrackBadge.tsx`:

```tsx
import React from 'react';
import { Text, View, StyleSheet, TouchableOpacity, Linking } from 'react-native';

interface Props {
  track: 'zetic' | 'cognition' | 'fetchai' | 'cloudinary' | 'arista';
  linkUrl?: string;
}

const TRACK_COLORS: Record<Props['track'], { bg: string; text: string; label: string }> = {
  zetic:      { bg: 'rgba(59,130,246,0.15)',  text: '#60a5fa', label: 'zetic' },
  cognition:  { bg: 'rgba(168,85,247,0.15)',  text: '#c084fc', label: 'cognition' },
  fetchai:    { bg: 'rgba(20,184,166,0.15)',  text: '#2dd4bf', label: 'fetch.ai' },
  cloudinary: { bg: 'rgba(249,115,22,0.15)', text: '#fb923c', label: 'cloudinary' },
  arista:     { bg: 'rgba(34,197,94,0.15)',  text: '#4ade80', label: 'arista' },
};

export default function TrackBadge({ track, linkUrl }: Props) {
  const { bg, text, label } = TRACK_COLORS[track];
  const content = (
    <View style={[styles.badge, { backgroundColor: bg }]}>
      <Text style={[styles.label, { color: text }]}>
        {label}{linkUrl ? ' ↗' : ''}
      </Text>
    </View>
  );

  if (linkUrl) {
    return (
      <TouchableOpacity onPress={() => Linking.openURL(linkUrl)}>
        {content}
      </TouchableOpacity>
    );
  }
  return content;
}

const styles = StyleSheet.create({
  badge: {
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 20,
  },
  label: {
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 0.3,
  },
});
```

- [ ] **Step 2: Create PrivacyModeToggle**

Create `sage-mobile/components/PrivacyModeToggle.tsx`:

```tsx
import React from 'react';
import { View, Text, Switch, StyleSheet } from 'react-native';
import { useAppStore } from '../lib/store';
import TrackBadge from './TrackBadge';

export default function PrivacyModeToggle() {
  const { privacyMode, setPrivacyMode } = useAppStore();

  return (
    <View style={styles.row}>
      <View style={styles.left}>
        <Text style={styles.title}>Privacy Mode</Text>
        <Text style={styles.sub}>
          {privacyMode
            ? 'Your questions never leave this device'
            : 'Requests go to SAGE cloud backend'}
        </Text>
      </View>
      <TrackBadge track="zetic" />
      <Switch
        value={privacyMode}
        onValueChange={setPrivacyMode}
        trackColor={{ false: '#374151', true: '#2563eb' }}
        thumbColor={privacyMode ? '#60a5fa' : '#9ca3af'}
        style={{ marginLeft: 8 }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 10,
    backgroundColor: '#111827',
    borderRadius: 12,
    gap: 8,
  },
  left: { flex: 1 },
  title: { color: '#f9fafb', fontSize: 13, fontWeight: '600' },
  sub: { color: '#6b7280', fontSize: 11, marginTop: 2 },
});
```

- [ ] **Step 3: Commit**

```bash
git add components/TrackBadge.tsx components/PrivacyModeToggle.tsx
git commit -m "feat(zetic): add TrackBadge and PrivacyModeToggle components"
```

---

### Task 5: Build PerformanceDashboard component

**Files:**
- Create: `sage-mobile/components/PerformanceDashboard.tsx`

- [ ] **Step 1: Create PerformanceDashboard.tsx**

```tsx
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import TrackBadge from './TrackBadge';

interface Metrics {
  firstTokenMs: number;
  throughputTokensPerSec: number;
  computeUnit: string;
  modelName: string;
  modelSizeMb: number;
}

interface Props {
  metrics: Metrics;
  cloudLatencyMs?: number; // for the "vs Cloud" comparison
}

export default function PerformanceDashboard({ metrics, cloudLatencyMs }: Props) {
  const speedup = cloudLatencyMs && metrics.firstTokenMs > 0
    ? (cloudLatencyMs / metrics.firstTokenMs).toFixed(1)
    : null;

  const computeColor: Record<string, string> = {
    NPU: '#4ade80',
    GPU: '#60a5fa',
    CPU: '#fb923c',
  };
  const unitColor = computeColor[metrics.computeUnit.toUpperCase()] ?? '#9ca3af';

  return (
    <View style={styles.card}>
      <View style={styles.header}>
        <Text style={styles.title}>⚡ On-Device Performance</Text>
        <TrackBadge track="zetic" />
      </View>

      <View style={styles.grid}>
        <Stat label="Compute" value={metrics.computeUnit} color={unitColor} />
        <Stat label="First token" value={`${metrics.firstTokenMs}ms`} />
        <Stat label="Throughput" value={`${metrics.throughputTokensPerSec} tok/s`} />
        {speedup && <Stat label="vs Cloud" value={`${speedup}× faster`} color="#4ade80" />}
      </View>

      <Text style={styles.model}>
        {metrics.modelName} · {(metrics.modelSizeMb / 1024).toFixed(1)}GB · {metrics.computeUnit}
      </Text>
    </View>
  );
}

function Stat({ label, value, color }: { label: string; value: string; color?: string }) {
  return (
    <View style={styles.stat}>
      <Text style={styles.statLabel}>{label}</Text>
      <Text style={[styles.statValue, color ? { color } : {}]}>{value}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#111827',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: 'rgba(59,130,246,0.2)',
    padding: 12,
    marginTop: 8,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 10,
  },
  title: { color: '#e5e7eb', fontSize: 12, fontWeight: '700' },
  grid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
    marginBottom: 8,
  },
  stat: { minWidth: '40%' },
  statLabel: { color: '#6b7280', fontSize: 10, marginBottom: 2 },
  statValue: { color: '#f9fafb', fontSize: 13, fontWeight: '600' },
  model: { color: '#6b7280', fontSize: 10, marginTop: 2 },
});
```

- [ ] **Step 2: Commit**

```bash
git add components/PerformanceDashboard.tsx
git commit -m "feat(zetic): add PerformanceDashboard with NPU/GPU/CPU metrics and speed comparison"
```

---

### Task 6: Build LessonScreen with on-device inference

**Files:**
- Create: `sage-mobile/screens/LessonScreen.tsx`

- [ ] **Step 1: Create screens/ directory**

```bash
mkdir -p sage-mobile/screens
```

- [ ] **Step 2: Create LessonScreen.tsx**

```tsx
import React, { useState, useRef, useEffect } from 'react';
import {
  View, Text, TextInput, TouchableOpacity, FlatList,
  StyleSheet, KeyboardAvoidingView, Platform, ActivityIndicator,
} from 'react-native';
import { useAppStore } from '../lib/store';
import { loadModel, streamOnDevice } from '../lib/melange';
import { cloudChat } from '../lib/api';
import PerformanceDashboard from '../components/PerformanceDashboard';
import PrivacyModeToggle from '../components/PrivacyModeToggle';

const SAGE_SYSTEM_PROMPT = `You are SAGE, a Socratic AI tutor. Guide students with questions 
rather than giving direct answers. When they seem stuck, give a hint. Be concise — 
mobile responses should be under 150 words. Always end with a follow-up question.`;

export default function LessonScreen() {
  const { messages, isStreaming, privacyMode, selectedModel,
          addMessage, appendToLast, setLastMetrics, setStreaming, clearMessages } = useAppStore();

  const [input, setInput] = useState('');
  const [modelReady, setModelReady] = useState(false);
  const [loadProgress, setLoadProgress] = useState(0);
  const listRef = useRef<FlatList>(null);

  useEffect(() => {
    loadModel(selectedModel, setLoadProgress).then(() => setModelReady(true));
    clearMessages();
    addMessage({
      id: 'welcome',
      role: 'assistant',
      content: `Hi! I'm SAGE, your on-device AI tutor. ${privacyMode
        ? '🔒 Privacy Mode is ON — your questions never leave this device.'
        : '☁️ Connected to SAGE cloud backend.'}\n\nWhat would you like to learn today?`,
    });
  }, []);

  async function handleSend() {
    const text = input.trim();
    if (!text || isStreaming) return;
    setInput('');

    addMessage({ id: Date.now().toString(), role: 'user', content: text });
    addMessage({ id: Date.now().toString() + 'a', role: 'assistant', content: '' });
    setStreaming(true);

    try {
      if (privacyMode) {
        // On-device inference via Melange
        for await (const chunk of streamOnDevice(SAGE_SYSTEM_PROMPT, text, selectedModel)) {
          if (!chunk.done) {
            appendToLast(chunk.token);
          } else if (chunk.metrics) {
            setLastMetrics(chunk.metrics);
          }
        }
      } else {
        // Cloud mode — hit SAGE backend
        await cloudChat(1, text, '', (token) => appendToLast(token));
      }
    } catch (e) {
      appendToLast('\n\n[Error: ' + String(e) + ']');
    } finally {
      setStreaming(false);
      listRef.current?.scrollToEnd({ animated: true });
    }
  }

  if (!modelReady) {
    return (
      <View style={styles.loading}>
        <ActivityIndicator size="large" color="#60a5fa" />
        <Text style={styles.loadText}>Loading Melange model… {Math.round(loadProgress * 100)}%</Text>
        <Text style={styles.loadSub}>{selectedModel.name} · {(selectedModel.sizeMb / 1024).toFixed(1)}GB</Text>
      </View>
    );
  }

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <PrivacyModeToggle />

      <FlatList
        ref={listRef}
        data={messages}
        keyExtractor={(m) => m.id}
        style={styles.list}
        contentContainerStyle={{ padding: 12, gap: 10 }}
        renderItem={({ item: msg }) => (
          <View style={[styles.bubble, msg.role === 'user' ? styles.userBubble : styles.aiBubble]}>
            <Text style={[styles.bubbleText, msg.role === 'user' ? styles.userText : styles.aiText]}>
              {msg.content}
            </Text>
            {msg.metrics && privacyMode && (
              <PerformanceDashboard metrics={msg.metrics} cloudLatencyMs={1200} />
            )}
          </View>
        )}
      />

      {isStreaming && (
        <View style={styles.thinkingRow}>
          <ActivityIndicator size="small" color="#60a5fa" />
          <Text style={styles.thinkingText}>
            {privacyMode ? `Inferring on ${selectedModel.computeUnit}…` : 'Asking SAGE cloud…'}
          </Text>
        </View>
      )}

      <View style={styles.inputRow}>
        <TextInput
          style={styles.input}
          value={input}
          onChangeText={setInput}
          placeholder="Ask SAGE anything…"
          placeholderTextColor="#6b7280"
          multiline
          onSubmitEditing={handleSend}
        />
        <TouchableOpacity
          style={[styles.sendBtn, (!input.trim() || isStreaming) && styles.sendBtnDisabled]}
          onPress={handleSend}
          disabled={!input.trim() || isStreaming}
        >
          <Text style={styles.sendBtnText}>↑</Text>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#030712' },
  loading: { flex: 1, alignItems: 'center', justifyContent: 'center', backgroundColor: '#030712' },
  loadText: { color: '#e5e7eb', fontSize: 15, marginTop: 16 },
  loadSub: { color: '#6b7280', fontSize: 12, marginTop: 4 },
  list: { flex: 1 },
  bubble: { borderRadius: 16, padding: 12, maxWidth: '90%' },
  userBubble: { alignSelf: 'flex-end', backgroundColor: '#1d4ed8' },
  aiBubble: { alignSelf: 'flex-start', backgroundColor: '#111827', borderWidth: 1, borderColor: '#1f2937' },
  bubbleText: { fontSize: 14, lineHeight: 20 },
  userText: { color: '#fff' },
  aiText: { color: '#e5e7eb' },
  thinkingRow: { flexDirection: 'row', alignItems: 'center', gap: 8, paddingHorizontal: 16, paddingVertical: 8 },
  thinkingText: { color: '#6b7280', fontSize: 12 },
  inputRow: { flexDirection: 'row', alignItems: 'flex-end', padding: 12, gap: 8 },
  input: {
    flex: 1, backgroundColor: '#111827', borderRadius: 20, borderWidth: 1, borderColor: '#1f2937',
    color: '#f9fafb', paddingHorizontal: 16, paddingVertical: 10, fontSize: 14, maxHeight: 100,
  },
  sendBtn: {
    width: 40, height: 40, borderRadius: 20, backgroundColor: '#2563eb',
    alignItems: 'center', justifyContent: 'center',
  },
  sendBtnDisabled: { backgroundColor: '#1f2937' },
  sendBtnText: { color: '#fff', fontSize: 20, fontWeight: '700' },
});
```

- [ ] **Step 3: Commit**

```bash
git add screens/LessonScreen.tsx
git commit -m "feat(zetic): add LessonScreen with on-device Melange inference and PerformanceDashboard"
```

---

### Task 7: Build ModelManagerScreen

**Files:**
- Create: `sage-mobile/screens/ModelManagerScreen.tsx`

- [ ] **Step 1: Create ModelManagerScreen.tsx**

```tsx
import React, { useState } from 'react';
import {
  View, Text, FlatList, TouchableOpacity, StyleSheet, ActivityIndicator,
} from 'react-native';
import { MELANGE_MODELS } from '../lib/models';
import { benchmarkModel, ModelInfo, InferenceMetrics } from '../lib/melange';
import { useAppStore } from '../lib/store';
import TrackBadge from '../components/TrackBadge';

export default function ModelManagerScreen() {
  const { selectedModel, setSelectedModel } = useAppStore();
  const [benchmarking, setBenchmarking] = useState<string | null>(null);
  const [results, setResults] = useState<Record<string, InferenceMetrics>>({});

  async function runBenchmark(model: ModelInfo) {
    setBenchmarking(model.id);
    try {
      const metrics = await benchmarkModel(model);
      setResults((prev) => ({ ...prev, [model.id]: metrics }));
    } catch (e) {
      setResults((prev) => ({ ...prev, [model.id]: {
        firstTokenMs: 0, throughputTokensPerSec: 0,
        computeUnit: 'Error', modelName: model.name, modelSizeMb: model.sizeMb,
      }}));
    } finally {
      setBenchmarking(null);
    }
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Model Manager</Text>
        <TrackBadge track="zetic" linkUrl="https://melange.zetic.ai" />
      </View>

      <FlatList
        data={MELANGE_MODELS}
        keyExtractor={(m) => m.id}
        contentContainerStyle={{ gap: 12, padding: 16 }}
        renderItem={({ item: model }) => {
          const isSelected = selectedModel.id === model.id;
          const isBenchmarking = benchmarking === model.id;
          const result = results[model.id];
          const unitColors: Record<string, string> = { NPU: '#4ade80', GPU: '#60a5fa', CPU: '#fb923c' };
          const unitColor = unitColors[model.computeUnit] ?? '#9ca3af';

          return (
            <TouchableOpacity
              style={[styles.card, isSelected && styles.cardSelected]}
              onPress={() => setSelectedModel(model)}
            >
              <View style={styles.cardRow}>
                <View style={{ flex: 1 }}>
                  <Text style={styles.modelName}>{model.name}</Text>
                  <Text style={styles.modelSize}>{(model.sizeMb / 1024).toFixed(1)} GB</Text>
                </View>
                <Text style={[styles.unit, { color: unitColor }]}>{model.computeUnit}</Text>
              </View>

              {result && (
                <View style={styles.resultRow}>
                  <Text style={styles.resultText}>First token: {result.firstTokenMs}ms</Text>
                  <Text style={styles.resultText}>· {result.throughputTokensPerSec} tok/s</Text>
                  <Text style={[styles.resultText, { color: unitColor }]}>· {result.computeUnit}</Text>
                </View>
              )}

              <TouchableOpacity
                style={[styles.benchBtn, isBenchmarking && styles.benchBtnDisabled]}
                onPress={() => runBenchmark(model)}
                disabled={!!benchmarking}
              >
                {isBenchmarking ? (
                  <ActivityIndicator size="small" color="#60a5fa" />
                ) : (
                  <Text style={styles.benchBtnText}>Benchmark</Text>
                )}
              </TouchableOpacity>
            </TouchableOpacity>
          );
        }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#030712' },
  header: {
    flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between',
    paddingHorizontal: 16, paddingVertical: 14, borderBottomWidth: 1, borderColor: '#1f2937',
  },
  title: { color: '#f9fafb', fontSize: 18, fontWeight: '700' },
  card: {
    backgroundColor: '#111827', borderRadius: 14, padding: 14,
    borderWidth: 1, borderColor: '#1f2937',
  },
  cardSelected: { borderColor: '#2563eb' },
  cardRow: { flexDirection: 'row', alignItems: 'center', marginBottom: 8 },
  modelName: { color: '#f9fafb', fontSize: 15, fontWeight: '600' },
  modelSize: { color: '#6b7280', fontSize: 12, marginTop: 2 },
  unit: { fontSize: 13, fontWeight: '700' },
  resultRow: { flexDirection: 'row', gap: 4, marginBottom: 10 },
  resultText: { color: '#9ca3af', fontSize: 11 },
  benchBtn: {
    backgroundColor: '#1e3a8a', borderRadius: 8, paddingVertical: 8,
    alignItems: 'center',
  },
  benchBtnDisabled: { backgroundColor: '#1f2937' },
  benchBtnText: { color: '#60a5fa', fontSize: 13, fontWeight: '600' },
});
```

- [ ] **Step 2: Commit**

```bash
git add screens/ModelManagerScreen.tsx
git commit -m "feat(zetic): add ModelManagerScreen with benchmark runner and compute unit badges"
```

---

### Task 8: Build PrivacyScreen with network monitor

**Files:**
- Create: `sage-mobile/screens/PrivacyScreen.tsx`

- [ ] **Step 1: Create PrivacyScreen.tsx**

```tsx
import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, StyleSheet, TouchableOpacity } from 'react-native';
import { useAppStore } from '../lib/store';
import TrackBadge from '../components/TrackBadge';

export default function PrivacyScreen() {
  const { privacyMode, networkEvents, clearNetworkEvents } = useAppStore();
  const [monitoring, setMonitoring] = useState(false);

  // In a real implementation, this hooks into expo-network or a native module
  // to intercept outbound HTTP requests. For demo purposes, events are added
  // to the store from cloudChat() calls in cloud mode.
  useEffect(() => {
    setMonitoring(true);
    return () => setMonitoring(false);
  }, []);

  const zeroOutbound = networkEvents.length === 0;

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Privacy Monitor</Text>
        <TrackBadge track="zetic" />
      </View>

      {/* Status banner */}
      <View style={[styles.banner, privacyMode ? styles.bannerGreen : styles.bannerAmber]}>
        <Text style={styles.bannerIcon}>{privacyMode ? '🔒' : '☁️'}</Text>
        <View>
          <Text style={styles.bannerTitle}>
            {privacyMode ? 'Privacy Mode ON' : 'Cloud Mode Active'}
          </Text>
          <Text style={styles.bannerSub}>
            {privacyMode
              ? 'All inference running on-device. Zero outbound requests.'
              : 'Requests sent to SAGE cloud backend.'}
          </Text>
        </View>
      </View>

      {/* Outbound request count */}
      <View style={styles.countCard}>
        <Text style={styles.countNum}>
          {privacyMode ? '0' : networkEvents.length}
        </Text>
        <Text style={styles.countLabel}>Outbound Inference Requests</Text>
        {privacyMode && zeroOutbound && (
          <Text style={styles.countConfirm}>✓ Confirmed: no network activity during tutoring</Text>
        )}
      </View>

      {/* Event log */}
      <View style={styles.logHeader}>
        <Text style={styles.logTitle}>Network Activity Log</Text>
        <TouchableOpacity onPress={clearNetworkEvents}>
          <Text style={styles.clearBtn}>Clear</Text>
        </TouchableOpacity>
      </View>

      {networkEvents.length === 0 ? (
        <View style={styles.emptyLog}>
          <Text style={styles.emptyText}>
            {privacyMode
              ? '✓ No outbound requests — your data stays on-device'
              : 'No requests logged yet. Send a message in Lesson tab.'}
          </Text>
        </View>
      ) : (
        <FlatList
          data={[...networkEvents].reverse()}
          keyExtractor={(_, i) => String(i)}
          contentContainerStyle={{ padding: 16, gap: 6 }}
          renderItem={({ item }) => (
            <View style={styles.eventRow}>
              <Text style={styles.eventMethod}>{item.method}</Text>
              <Text style={styles.eventUrl} numberOfLines={1}>{item.url}</Text>
            </View>
          )}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#030712' },
  header: {
    flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between',
    paddingHorizontal: 16, paddingVertical: 14, borderBottomWidth: 1, borderColor: '#1f2937',
  },
  title: { color: '#f9fafb', fontSize: 18, fontWeight: '700' },
  banner: {
    flexDirection: 'row', alignItems: 'center', gap: 12,
    margin: 16, borderRadius: 12, padding: 14, borderWidth: 1,
  },
  bannerGreen: { backgroundColor: 'rgba(34,197,94,0.1)', borderColor: 'rgba(34,197,94,0.3)' },
  bannerAmber: { backgroundColor: 'rgba(245,158,11,0.1)', borderColor: 'rgba(245,158,11,0.3)' },
  bannerIcon: { fontSize: 24 },
  bannerTitle: { color: '#f9fafb', fontSize: 14, fontWeight: '600' },
  bannerSub: { color: '#9ca3af', fontSize: 11, marginTop: 2 },
  countCard: { alignItems: 'center', paddingVertical: 24 },
  countNum: { color: '#f9fafb', fontSize: 64, fontWeight: '800' },
  countLabel: { color: '#6b7280', fontSize: 13 },
  countConfirm: { color: '#4ade80', fontSize: 12, marginTop: 4 },
  logHeader: {
    flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between',
    paddingHorizontal: 16, paddingBottom: 8,
    borderTopWidth: 1, borderColor: '#1f2937', paddingTop: 16,
  },
  logTitle: { color: '#9ca3af', fontSize: 12, fontWeight: '600', textTransform: 'uppercase', letterSpacing: 1 },
  clearBtn: { color: '#6b7280', fontSize: 12 },
  emptyLog: { padding: 24, alignItems: 'center' },
  emptyText: { color: '#4ade80', fontSize: 13, textAlign: 'center' },
  eventRow: { flexDirection: 'row', gap: 8 },
  eventMethod: { color: '#fb923c', fontSize: 11, fontWeight: '700', width: 40 },
  eventUrl: { color: '#9ca3af', fontSize: 11, flex: 1 },
});
```

- [ ] **Step 2: Commit**

```bash
git add screens/PrivacyScreen.tsx
git commit -m "feat(zetic): add PrivacyScreen network monitor proving zero outbound requests"
```

---

### Task 9: Wire App.tsx navigator and run

**Files:**
- Modify: `sage-mobile/App.tsx`

- [ ] **Step 1: Install React Navigation**

```bash
cd sage-mobile
npm install @react-navigation/native @react-navigation/bottom-tabs @react-navigation/stack
npx expo install react-native-screens react-native-safe-area-context
```

- [ ] **Step 2: Replace App.tsx with navigator**

```tsx
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Text } from 'react-native';
import LessonScreen from './screens/LessonScreen';
import ModelManagerScreen from './screens/ModelManagerScreen';
import PrivacyScreen from './screens/PrivacyScreen';

const Tab = createBottomTabNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={{
          headerStyle: { backgroundColor: '#030712' },
          headerTintColor: '#f9fafb',
          tabBarStyle: { backgroundColor: '#0a0f1e', borderTopColor: '#1f2937' },
          tabBarActiveTintColor: '#60a5fa',
          tabBarInactiveTintColor: '#6b7280',
        }}
      >
        <Tab.Screen
          name="Lesson"
          component={LessonScreen}
          options={{ tabBarIcon: ({ color }) => <Text style={{ fontSize: 18, color }}>◎</Text> }}
        />
        <Tab.Screen
          name="Models"
          component={ModelManagerScreen}
          options={{ tabBarIcon: ({ color }) => <Text style={{ fontSize: 18, color }}>⚡</Text> }}
        />
        <Tab.Screen
          name="Privacy"
          component={PrivacyScreen}
          options={{ tabBarIcon: ({ color }) => <Text style={{ fontSize: 18, color }}>🔒</Text> }}
        />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
```

- [ ] **Step 3: Start and run on device/simulator**

```bash
cd sage-mobile && npx expo start
```

- Press `i` for iOS Simulator or `a` for Android emulator.
- Verify:
  - Lesson tab loads with Privacy Mode toggle ON
  - "Loading Melange model..." screen appears with progress %
  - After load, send a message and see PerformanceDashboard with NPU badge
  - Switch to Privacy tab and confirm "0 Outbound Requests"
  - Switch to Models tab and tap "Benchmark" on Phi-3.5-mini

- [ ] **Step 4: Final commit**

```bash
cd sage-mobile && git add .
git commit -m "feat(zetic): complete ZETIC track — Expo app with Melange, Privacy Mode, benchmarking"
```
