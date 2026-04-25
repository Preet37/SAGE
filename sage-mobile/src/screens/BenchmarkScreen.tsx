import { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ScrollView, ActivityIndicator } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useOfflineStore } from '../store/offlineStore';
import { runBenchmark, getHardwareInfo } from '../lib/melange';
import HardwareBadge from '../components/HardwareBadge';

interface BenchmarkRun {
  tokensPerSecond: number;
  accelerator: string;
  timestamp: number;
}

export default function BenchmarkScreen() {
  const { setBenchmarkResult, benchmarkResult, modelStatus, accelerator } = useOfflineStore();
  const [running, setRunning] = useState(false);
  const [history, setHistory] = useState<BenchmarkRun[]>([]);
  const [hwInfo, setHwInfo] = useState<{ device: string; accelerator: string; memoryMB: number } | null>(null);

  async function run() {
    if (running || modelStatus !== 'ready') return;
    setRunning(true);
    try {
      const hw = await getHardwareInfo();
      setHwInfo(hw);
      const result = await runBenchmark();
      setBenchmarkResult(result);
      setHistory(prev => [{ ...result, timestamp: Date.now() }, ...prev.slice(0, 4)]);
    } catch {
    } finally {
      setRunning(false);
    }
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.header}>
          <Text style={styles.title}>On-Device Benchmark</Text>
          <View style={styles.zeticBadge}>
            <Text style={styles.zeticText}>zetic ↗</Text>
          </View>
        </View>

        <Text style={styles.desc}>
          Measure inference speed on your device's NPU, GPU, or CPU. Privacy Mode ensures zero outbound requests during the test.
        </Text>

        {hwInfo && (
          <View style={styles.hwCard}>
            <Text style={styles.hwTitle}>Hardware</Text>
            <View style={styles.hwRow}>
              <Text style={styles.hwLabel}>Device</Text>
              <Text style={styles.hwValue}>{hwInfo.device}</Text>
            </View>
            <View style={styles.hwRow}>
              <Text style={styles.hwLabel}>Accelerator</Text>
              <HardwareBadge accelerator={hwInfo.accelerator} />
            </View>
            <View style={styles.hwRow}>
              <Text style={styles.hwLabel}>Memory</Text>
              <Text style={styles.hwValue}>{hwInfo.memoryMB} MB</Text>
            </View>
          </View>
        )}

        {benchmarkResult && (
          <View style={styles.resultCard}>
            <Text style={styles.resultLabel}>Latest Result</Text>
            <Text style={styles.tps}>{benchmarkResult.tokensPerSecond}</Text>
            <Text style={styles.tpsLabel}>tokens / second</Text>
            <HardwareBadge accelerator={benchmarkResult.accelerator} offlineProven />
          </View>
        )}

        {history.length > 1 && (
          <View style={styles.historyCard}>
            <Text style={styles.historyTitle}>Run History</Text>
            {history.map((run, i) => (
              <View key={run.timestamp} style={styles.historyRow}>
                <Text style={styles.historyIndex}>#{history.length - i}</Text>
                <Text style={styles.historyTps}>{run.tokensPerSecond} tok/s</Text>
                <Text style={styles.historyAccel}>{run.accelerator}</Text>
              </View>
            ))}
          </View>
        )}

        <TouchableOpacity
          style={[styles.btn, (running || modelStatus !== 'ready') && styles.btnDisabled]}
          onPress={run}
          disabled={running || modelStatus !== 'ready'}
        >
          {running ? (
            <ActivityIndicator color="#0f0f11" />
          ) : (
            <Text style={styles.btnText}>
              {modelStatus !== 'ready' ? 'Download model first' : 'Run Benchmark'}
            </Text>
          )}
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0f0f11' },
  content: { padding: 20, gap: 16 },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  title: { color: '#f1f5f9', fontWeight: '800', fontSize: 20 },
  zeticBadge: {
    backgroundColor: '#14b8a618',
    borderColor: '#14b8a640',
    borderWidth: 1,
    borderRadius: 99,
    paddingHorizontal: 10,
    paddingVertical: 4,
  },
  zeticText: { color: '#14b8a6', fontWeight: '700', fontSize: 11 },
  desc: { color: '#64748b', fontSize: 13, lineHeight: 20 },
  hwCard: {
    backgroundColor: '#1e293b',
    borderWidth: 1,
    borderColor: '#ffffff0d',
    borderRadius: 16,
    padding: 16,
    gap: 10,
  },
  hwTitle: { color: '#94a3b8', fontSize: 10, fontWeight: '700', textTransform: 'uppercase', letterSpacing: 1 },
  hwRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  hwLabel: { color: '#64748b', fontSize: 13 },
  hwValue: { color: '#f1f5f9', fontSize: 13, fontWeight: '600' },
  resultCard: {
    backgroundColor: '#14b8a608',
    borderWidth: 1,
    borderColor: '#14b8a630',
    borderRadius: 16,
    padding: 20,
    alignItems: 'center',
    gap: 4,
  },
  resultLabel: { color: '#64748b', fontSize: 11, fontWeight: '600', textTransform: 'uppercase', letterSpacing: 1 },
  tps: { color: '#14b8a6', fontSize: 48, fontWeight: '800', lineHeight: 56 },
  tpsLabel: { color: '#94a3b8', fontSize: 14, marginBottom: 8 },
  historyCard: {
    backgroundColor: '#1e293b',
    borderWidth: 1,
    borderColor: '#ffffff0d',
    borderRadius: 16,
    padding: 16,
    gap: 8,
  },
  historyTitle: { color: '#64748b', fontSize: 10, fontWeight: '700', textTransform: 'uppercase', letterSpacing: 1 },
  historyRow: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  historyIndex: { color: '#475569', fontSize: 12, width: 24 },
  historyTps: { color: '#f1f5f9', fontSize: 14, fontWeight: '700', flex: 1 },
  historyAccel: { color: '#64748b', fontSize: 12 },
  btn: {
    backgroundColor: '#14b8a6',
    borderRadius: 14,
    paddingVertical: 14,
    alignItems: 'center',
  },
  btnDisabled: { opacity: 0.4 },
  btnText: { color: '#0f0f11', fontWeight: '800', fontSize: 15 },
});
