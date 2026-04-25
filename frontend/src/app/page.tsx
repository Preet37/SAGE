export default function Home() {
  return (
    <main className="grid h-screen grid-cols-[1fr_1.2fr_1fr] gap-4 p-4">
      <section
        aria-label="Chat"
        className="rounded-3xl border border-[var(--color-border)] bg-white p-5 shadow-sm"
      >
        <h2 className="text-lg font-semibold">Chat</h2>
        <p className="mt-2 text-sm opacity-70">Socratic dialogue with SAGE.</p>
      </section>
      <section
        aria-label="Concept Map"
        className="rounded-3xl border border-[var(--color-border)] bg-white p-5 shadow-sm"
      >
        <h2 className="text-lg font-semibold">Concept Map</h2>
        <p className="mt-2 text-sm opacity-70">Live graph of ideas.</p>
      </section>
      <section
        aria-label="Notes"
        className="rounded-3xl border border-[var(--color-border)] bg-white p-5 shadow-sm"
      >
        <h2 className="text-lg font-semibold">Notes</h2>
        <p className="mt-2 text-sm opacity-70">Auto-synthesized study notes.</p>
      </section>
    </main>
  );
}
