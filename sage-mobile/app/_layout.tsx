import { Tabs } from 'expo-router';
import { StatusBar } from 'expo-status-bar';

export default function RootLayout() {
  return (
    <>
      <StatusBar style="light" />
      <Tabs
        screenOptions={{
          headerStyle: { backgroundColor: '#0f0f11' },
          headerTintColor: '#f1f5f9',
          headerTitleStyle: { fontWeight: '700' },
          tabBarStyle: { backgroundColor: '#0f0f11', borderTopColor: '#ffffff0d' },
          tabBarActiveTintColor: '#14b8a6',
          tabBarInactiveTintColor: '#475569',
        }}
      >
        <Tabs.Screen
          name="index"
          options={{
            title: 'SAGE Offline',
            tabBarLabel: 'Tutor',
          }}
        />
        <Tabs.Screen
          name="benchmark"
          options={{
            title: 'Benchmark',
            tabBarLabel: 'Benchmark',
          }}
        />
      </Tabs>
    </>
  );
}
