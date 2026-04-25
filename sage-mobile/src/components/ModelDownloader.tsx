import { View, Text, TouchableOpacity, ActivityIndicator, StyleSheet } from 'react-native';
import * as FileSystem from 'expo-file-system';
import { useOfflineStore } from '../store/offlineStore';
import { getHardwareInfo } from '../lib/melange';

const MODEL_URL = 'https://huggingface.co/sage-ai/phi2-q4-melange/resolve/main/sage-phi2-q4.melange';
const MODEL_DIR = FileSystem.documentDirectory + 'models/';
const MODEL_PATH = MODEL_DIR + 'sage-phi2-q4.melange';
const MODEL_SIZE_APPROX = '1.2 GB';

export default function ModelDownloader() {
  const { modelStatus, modelProgress, modelError, setModelStatus, setModelProgress, setModelError, setAccelerator } =
    useOfflineStore();

  async function startDownload() {
    setModelStatus('downloading');
    setModelProgress(0);
    setModelError(null);

    try {
      await FileSystem.makeDirectoryAsync(MODEL_DIR, { intermediates: true });

      const callback: FileSystem.DownloadProgressCallback = ({ totalBytesWritten, totalBytesExpectedToWrite }) => {
        if (totalBytesExpectedToWrite > 0) {
          setModelProgress(totalBytesWritten / totalBytesExpectedToWrite);
        }
      };

      const download = FileSystem.createDownloadResumable(MODEL_URL, MODEL_PATH, {}, callback);
      const result = await download.downloadAsync();

      if (result?.status === 200) {
        const hw = await getHardwareInfo();
        setAccelerator(hw.accelerator);
        setModelStatus('ready');
      } else {
        throw new Error(`Download failed with status ${result?.status}`);
      }
    } catch (err) {
      setModelError(String(err));
      setModelStatus('error');
    }
  }

  if (modelStatus === 'ready') return null;

  return (
    <View style={styles.card}>
      <View style={styles.header}>
        <Text style={styles.title}>Offline AI Model</Text>
        <View style={styles.zeticBadge}>
          <Text style={styles.zeticText}>zetic</Text>
        </View>
      </View>

      <Text style={styles.desc}>
        Download the SAGE Phi-2 Q4 model (~{MODEL_SIZE_APPROX}) to enable fully on-device tutoring with zero cloud dependency.
      </Text>

      {modelStatus === 'idle' && (
        <TouchableOpacity style={styles.btn} onPress={startDownload}>
          <Text style={styles.btnText}>Download Model</Text>
        </TouchableOpacity>
      )}

      {modelStatus === 'downloading' && (
        <View style={styles.progressContainer}>
          <View style={styles.progressRow}>
            <ActivityIndicator size="small" color="#14b8a6" />
            <Text style={styles.progressText}>{(modelProgress * 100).toFixed(0)}%</Text>
          </View>
          <View style={styles.progressBar}>
            <View style={[styles.progressFill, { width: `${modelProgress * 100}%` }]} />
          </View>
        </View>
      )}

      {modelStatus === 'error' && (
        <View>
          <Text style={styles.error}>{modelError}</Text>
          <TouchableOpacity style={styles.btn} onPress={startDownload}>
            <Text style={styles.btnText}>Retry</Text>
          </TouchableOpacity>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#14b8a610',
    borderColor: '#14b8a630',
    borderWidth: 1,
    borderRadius: 16,
    padding: 16,
    gap: 12,
  },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  title: { color: '#f1f5f9', fontWeight: '700', fontSize: 14 },
  zeticBadge: {
    backgroundColor: '#14b8a618',
    borderColor: '#14b8a640',
    borderWidth: 1,
    borderRadius: 99,
    paddingHorizontal: 8,
    paddingVertical: 2,
  },
  zeticText: { color: '#14b8a6', fontWeight: '700', fontSize: 10 },
  desc: { color: '#94a3b8', fontSize: 12, lineHeight: 18 },
  btn: {
    backgroundColor: '#14b8a620',
    borderColor: '#14b8a640',
    borderWidth: 1,
    borderRadius: 12,
    paddingVertical: 10,
    alignItems: 'center',
  },
  btnText: { color: '#14b8a6', fontWeight: '700', fontSize: 13 },
  progressContainer: { gap: 8 },
  progressRow: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  progressText: { color: '#14b8a6', fontWeight: '700', fontSize: 12 },
  progressBar: { height: 4, backgroundColor: '#1e293b', borderRadius: 99, overflow: 'hidden' },
  progressFill: { height: '100%', backgroundColor: '#14b8a6', borderRadius: 99 },
  error: { color: '#f87171', fontSize: 12, marginBottom: 8 },
});
