import { useState, useRef } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useOfflineStore } from '../store/offlineStore';
import { runInference } from '../lib/melange';
import HardwareBadge from '../components/HardwareBadge';
import ModelDownloader from '../components/ModelDownloader';

export default function OfflineTutorScreen() {
  const {
    messages,
    addMessage,
    appendToLast,
    isInferring,
    setIsInferring,
    modelStatus,
    accelerator,
    privacyMode,
    togglePrivacyMode,
    clearMessages,
  } = useOfflineStore();

  const [input, setInput] = useState('');
  const [lastResult, setLastResult] = useState<{ inferenceMs: number; offlineProven: boolean } | null>(null);
  const scrollRef = useRef<ScrollView>(null);

  async function send() {
    const text = input.trim();
    if (!text || isInferring) return;
    setInput('');

    addMessage({ id: Date.now().toString(), role: 'user', content: text });
    addMessage({ id: Date.now().toString() + '-a', role: 'assistant', content: '' });
    setIsInferring(true);

    try {
      const result = await runInference(text, {
        maxTokens: 200,
        temperature: 0.7,
        privacyMode,
        onToken: (token) => {
          appendToLast(token);
          scrollRef.current?.scrollToEnd({ animated: true });
        },
      });
      setLastResult({ inferenceMs: result.inferenceMs, offlineProven: result.offlineProven });
    } catch (err) {
      appendToLast(`\n\n_Error: ${String(err)}_`);
    } finally {
      setIsInferring(false);
    }
  }

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.flex}
      >
        {/* Header */}
        <View style={styles.header}>
          <View>
            <Text style={styles.headerTitle}>SAGE Offline</Text>
            <Text style={styles.headerSub}>Fully on-device AI tutor</Text>
          </View>
          <View style={styles.headerRight}>
            <TouchableOpacity
              style={[styles.privacyBtn, privacyMode && styles.privacyBtnActive]}
              onPress={togglePrivacyMode}
            >
              <Text style={[styles.privacyText, privacyMode && styles.privacyTextActive]}>
                {privacyMode ? '🔒 Privacy' : '🔓 Standard'}
              </Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* Hardware badge */}
        <View style={styles.badgeRow}>
          <HardwareBadge
            accelerator={accelerator}
            offlineProven={lastResult?.offlineProven}
          />
          {lastResult && (
            <Text style={styles.latency}>{lastResult.inferenceMs}ms</Text>
          )}
        </View>

        {/* Model downloader */}
        {modelStatus !== 'ready' && (
          <View style={styles.downloaderWrap}>
            <ModelDownloader />
          </View>
        )}

        {/* Messages */}
        <ScrollView
          ref={scrollRef}
          style={styles.messages}
          contentContainerStyle={styles.messagesContent}
          onContentSizeChange={() => scrollRef.current?.scrollToEnd({ animated: true })}
        >
          {messages.length === 0 && (
            <View style={styles.empty}>
              <Text style={styles.emptyIcon}>◈</Text>
              <Text style={styles.emptyTitle}>Ask SAGE anything</Text>
              <Text style={styles.emptySub}>Runs entirely on your device — no internet required</Text>
            </View>
          )}
          {messages.map((msg) => (
            <View
              key={msg.id}
              style={[styles.bubble, msg.role === 'user' ? styles.userBubble : styles.aiBubble]}
            >
              {msg.role === 'assistant' && (
                <Text style={styles.sageLabel}>SAGE</Text>
              )}
              <Text style={styles.bubbleText}>{msg.content || (isInferring ? '…' : '')}</Text>
            </View>
          ))}
        </ScrollView>

        {/* Input */}
        <View style={styles.inputRow}>
          <TextInput
            style={styles.input}
            value={input}
            onChangeText={setInput}
            placeholder={isInferring ? 'Generating…' : 'Ask anything…'}
            placeholderTextColor="#64748b"
            multiline
            editable={!isInferring}
            onSubmitEditing={send}
          />
          <TouchableOpacity
            style={[styles.sendBtn, (!input.trim() || isInferring) && styles.sendBtnDisabled]}
            onPress={send}
            disabled={!input.trim() || isInferring}
          >
            <Text style={styles.sendIcon}>↑</Text>
          </TouchableOpacity>
        </View>

        {messages.length > 0 && (
          <TouchableOpacity style={styles.clearBtn} onPress={clearMessages}>
            <Text style={styles.clearText}>Clear chat</Text>
          </TouchableOpacity>
        )}
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0f0f11' },
  flex: { flex: 1 },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#ffffff0d',
  },
  headerTitle: { color: '#f1f5f9', fontWeight: '800', fontSize: 18 },
  headerSub: { color: '#64748b', fontSize: 11, marginTop: 1 },
  headerRight: { flexDirection: 'row', gap: 8 },
  privacyBtn: {
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 99,
    borderWidth: 1,
    borderColor: '#334155',
  },
  privacyBtnActive: { borderColor: '#22c55e60', backgroundColor: '#22c55e10' },
  privacyText: { color: '#64748b', fontSize: 11, fontWeight: '600' },
  privacyTextActive: { color: '#22c55e' },
  badgeRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingVertical: 8,
  },
  latency: { color: '#64748b', fontSize: 10 },
  downloaderWrap: { paddingHorizontal: 16, paddingBottom: 8 },
  messages: { flex: 1 },
  messagesContent: { padding: 16, gap: 12 },
  empty: { alignItems: 'center', paddingTop: 60, gap: 8 },
  emptyIcon: { fontSize: 32, color: '#14b8a6' },
  emptyTitle: { color: '#f1f5f9', fontWeight: '700', fontSize: 16 },
  emptySub: { color: '#64748b', fontSize: 13, textAlign: 'center' },
  bubble: {
    maxWidth: '85%',
    borderRadius: 16,
    paddingHorizontal: 14,
    paddingVertical: 10,
    gap: 4,
  },
  userBubble: {
    alignSelf: 'flex-end',
    backgroundColor: '#3b82f620',
    borderWidth: 1,
    borderColor: '#3b82f630',
  },
  aiBubble: {
    alignSelf: 'flex-start',
    backgroundColor: '#1e293b',
    borderWidth: 1,
    borderColor: '#ffffff0d',
  },
  sageLabel: { color: '#64748b', fontSize: 9, fontWeight: '700', textTransform: 'uppercase', letterSpacing: 1 },
  bubbleText: { color: '#e2e8f0', fontSize: 14, lineHeight: 20 },
  inputRow: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    gap: 8,
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderTopWidth: 1,
    borderTopColor: '#ffffff0d',
  },
  input: {
    flex: 1,
    backgroundColor: '#1e293b',
    borderWidth: 1,
    borderColor: '#334155',
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 10,
    color: '#f1f5f9',
    fontSize: 14,
    maxHeight: 100,
  },
  sendBtn: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#14b8a6',
    alignItems: 'center',
    justifyContent: 'center',
  },
  sendBtnDisabled: { opacity: 0.3 },
  sendIcon: { color: '#fff', fontSize: 18, fontWeight: '700' },
  clearBtn: { alignSelf: 'center', paddingVertical: 6 },
  clearText: { color: '#475569', fontSize: 12 },
});
