import { View, Text, StyleSheet } from 'react-native';

interface Props {
  accelerator: string;
  offlineProven?: boolean;
}

const COLORS: Record<string, string> = {
  NPU: '#3b82f6',
  GPU: '#8b5cf6',
  CPU: '#6b7280',
};

export default function HardwareBadge({ accelerator, offlineProven }: Props) {
  const color = COLORS[accelerator] ?? COLORS.CPU;

  return (
    <View style={styles.row}>
      <View style={[styles.badge, { borderColor: color + '60', backgroundColor: color + '18' }]}>
        <View style={[styles.dot, { backgroundColor: color }]} />
        <Text style={[styles.text, { color }]}>{accelerator}</Text>
      </View>
      <View style={[styles.badge, { borderColor: '#14b8a640', backgroundColor: '#14b8a610' }]}>
        <Text style={styles.zeticText}>zetic</Text>
      </View>
      {offlineProven && (
        <View style={[styles.badge, { borderColor: '#22c55e40', backgroundColor: '#22c55e10' }]}>
          <Text style={[styles.text, { color: '#22c55e' }]}>✓ offline proven</Text>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: 'row', gap: 6, flexWrap: 'wrap' },
  badge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 99,
    borderWidth: 1,
  },
  dot: { width: 5, height: 5, borderRadius: 99 },
  text: { fontSize: 10, fontWeight: '700' },
  zeticText: { fontSize: 10, fontWeight: '700', color: '#14b8a6' },
});
