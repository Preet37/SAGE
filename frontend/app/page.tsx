"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { getToken } from "@/lib/auth";
import { Button } from "@/components/ui/button";
import { ThemeToggle } from "@/components/ThemeToggle";
import {
  BookOpen,
  BotMessageSquare,
  Compass,
  Library,
  Sparkles,
  ArrowRight,
  Brain,
  GraduationCap,
  Youtube,
  FileText,
  MessageSquare,
  RefreshCw,
  Zap,
  ExternalLink,
} from "lucide-react";


const SUBJECTS = [
  "Neural Networks",
  "Large Language Models",
  "Agents & Reasoning",
  "Multimodal AI",
  "Generative Models",
  "ML Engineering",
  "And more...",
];

export default function Home() {
  const router = useRouter();
  const [authed, setAuthed] = useState<boolean | null>(null);

  useEffect(() => {
    setAuthed(!!getToken());
  }, []);

  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Nav */}
      <header className="border-b border-border/50 bg-card/30 backdrop-blur-sm sticky top-0 z-40">
        <div className="max-w-6xl mx-auto flex items-center justify-between px-6 py-3">
          <div className="flex items-center gap-2">
            <svg
              viewBox="0 0 24 24"
              className="h-6 w-6 text-primary"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20" />
              <path d="M8 7h6M8 11h8" />
            </svg>
            <span className="font-semibold text-lg">
              <span className="text-primary">Socratic</span>Tutor
            </span>
          </div>
          <div className="flex items-center gap-2">
            <ThemeToggle />
            {authed === null ? null : authed ? (
              <Link href="/learn">
                <Button size="sm" className="gap-1.5">
                  <BookOpen className="h-4 w-4" />
                  Continue Learning
                </Button>
              </Link>
            ) : (
              <div className="flex gap-2">
                <Link href="/login">
                  <Button variant="ghost" size="sm">
                    Sign In
                  </Button>
                </Link>
                <Link href="/register">
                  <Button size="sm">Get Started</Button>
                </Link>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="py-24 px-6">
        <div className="max-w-4xl mx-auto text-center space-y-6">
          <div className="inline-flex items-center gap-2 rounded-full border border-border px-4 py-1.5 text-sm text-muted-foreground bg-card/50">
            <GraduationCap className="h-4 w-4 text-primary" />
            AI-powered learning platform
          </div>
          <h1 className="text-5xl sm:text-6xl font-bold tracking-tight leading-tight">
            Master ML & AI{" "}
            <span className="text-primary">the Socratic way</span>
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
            An AI tutor that teaches through questions, not lectures. Powered
            by LLM Wiki, an LLM-curated knowledge base that grows with every
            topic &mdash; grounded in the best educators&apos; content.
          </p>
          <div className="flex flex-col items-center gap-3 pt-4">
            <div className="flex items-center justify-center gap-3">
              <Link href={authed ? "/learn" : "/register"}>
                <Button size="lg" className="gap-2 text-base px-8">
                  {authed ? "Continue Learning" : "Start Learning"}
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
              <Link href={authed ? "/create" : "/register?returnTo=/create"}>
                <Button variant="outline" size="lg" className="gap-2 text-base px-8">
                  <Sparkles className="h-4 w-4" />
                  Design Your Course
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Subjects */}
      <section className="py-12 px-6 border-y border-border/50 bg-muted/30">
        <div className="max-w-5xl mx-auto">
          <p className="text-center text-sm text-muted-foreground mb-6">
            Covering topics across
          </p>
          <div className="flex flex-wrap justify-center gap-2">
            {SUBJECTS.map((s) => (
              <span
                key={s}
                className="px-4 py-1.5 rounded-full border border-border bg-card text-sm text-foreground"
              >
                {s}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* Socratic Learning — spotlight */}
      <section className="py-20 px-6 border-t border-border/50">
        <div className="max-w-5xl mx-auto">
          <div className="rounded-2xl border border-border bg-card overflow-hidden">
            <div className="grid md:grid-cols-2 gap-0">
              <div className="p-10 md:p-12 flex flex-col justify-center space-y-5">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-sm font-medium w-fit">
                  <BotMessageSquare className="h-3.5 w-3.5" />
                  How it teaches
                </div>
                <h2 className="text-3xl font-bold tracking-tight">
                  Learning that builds{" "}
                  <span className="text-primary">real understanding</span>
                </h2>
                <p className="text-muted-foreground leading-relaxed">
                  Most AI tools give you the answer. SocraticTutor asks you the
                  question. The AI tutor guides you through concepts using
                  dialogue &mdash; probing your reasoning, surfacing
                  misconceptions, and adapting to how you think. You don&apos;t
                  just read; you engage.
                </p>
                <div className="flex flex-col gap-3 pt-2">
                  <div className="flex items-center gap-3 text-sm">
                    <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                      <MessageSquare className="h-4 w-4 text-primary" />
                    </div>
                    <span className="text-foreground">
                      Dialogue over lecture &mdash; the tutor asks, you reason,
                      understanding deepens
                    </span>
                  </div>
                  <div className="flex items-center gap-3 text-sm">
                    <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                      <Brain className="h-4 w-4 text-primary" />
                    </div>
                    <span className="text-foreground">
                      Adapts to your thinking &mdash; misconceptions surface and
                      get corrected in real time
                    </span>
                  </div>
                  <div className="flex items-center gap-3 text-sm">
                    <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                      <Compass className="h-4 w-4 text-primary" />
                    </div>
                    <span className="text-foreground">
                      Start from any concept &mdash; pick a topic or let the AI
                      guide your path
                    </span>
                  </div>
                </div>
                <div className="pt-2">
                  <Link href={authed ? "/learn" : "/register"}>
                    <Button className="gap-2">
                      {authed ? "Continue Learning" : "Start Learning"}
                      <ArrowRight className="h-4 w-4" />
                    </Button>
                  </Link>
                </div>
              </div>
              <div className="bg-muted/50 p-10 md:p-12 flex flex-col justify-center border-t md:border-t-0 md:border-l border-border">
                <p className="text-sm font-medium text-muted-foreground uppercase tracking-wider mb-5">
                  What a session looks like
                </p>
                <div className="space-y-3">
                  {[
                    {
                      role: "tutor",
                      text: "Before we look at how attention works — what do you think the bottleneck is in a standard encoder-decoder RNN?",
                    },
                    {
                      role: "you",
                      text: "I think it's the fixed-size context vector?",
                    },
                    {
                      role: "tutor",
                      text: "Exactly right. So if that vector has to carry everything — what breaks down first with long sequences?",
                    },
                    {
                      role: "you",
                      text: "Early parts of the input get compressed out... it forgets?",
                    },
                    {
                      role: "tutor",
                      text: "Precisely. That's the problem attention was designed to solve. Want to explore how?",
                    },
                  ].map((msg, i) => (
                    <div
                      key={i}
                      className={`flex gap-2.5 ${msg.role === "you" ? "flex-row-reverse" : ""}`}
                    >
                      <div className="w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                        <span className="text-xs font-bold text-primary">
                          {msg.role === "tutor" ? "T" : "Y"}
                        </span>
                      </div>
                      <div
                        className={`rounded-2xl px-4 py-2.5 text-sm leading-relaxed max-w-[85%] ${
                          msg.role === "tutor"
                            ? "bg-card border border-border text-foreground rounded-tl-sm"
                            : "bg-primary/10 text-foreground rounded-tr-sm"
                        }`}
                      >
                        {msg.text}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Design Your Course — spotlight */}
      <section className="py-20 px-6">
        <div className="max-w-5xl mx-auto">
          <div className="rounded-2xl border border-border bg-card overflow-hidden">
            <div className="grid md:grid-cols-2 gap-0">
              <div className="p-10 md:p-12 flex flex-col justify-center space-y-5">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-sm font-medium w-fit">
                  <Sparkles className="h-3.5 w-3.5" />
                  What makes this different
                </div>
                <h2 className="text-3xl font-bold tracking-tight">
                  Design a course on{" "}
                  <span className="text-primary">anything</span>
                </h2>
                <p className="text-muted-foreground leading-relaxed">
                  Paste a YouTube video, upload a transcript, or just describe
                  what you want to learn. The AI builds a structured course
                  grounded in curated sources — with Socratic tutoring, quizzes,
                  and reference materials generated for every lesson.
                </p>
                <div className="flex flex-col gap-3 pt-2">
                  <div className="flex items-center gap-3 text-sm">
                    <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                      <Youtube className="h-4 w-4 text-primary" />
                    </div>
                    <span className="text-foreground">
                      Drop a YouTube link &mdash; get a full course from the video
                    </span>
                  </div>
                  <div className="flex items-center gap-3 text-sm">
                    <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                      <FileText className="h-4 w-4 text-primary" />
                    </div>
                    <span className="text-foreground">
                      Paste a transcript or paper &mdash; structured into lessons
                    </span>
                  </div>
                  <div className="flex items-center gap-3 text-sm">
                    <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                      <MessageSquare className="h-4 w-4 text-primary" />
                    </div>
                    <span className="text-foreground">
                      Describe a topic &mdash; AI curates sources and builds the course
                    </span>
                  </div>
                </div>
                <div className="pt-2">
                  <Link href={authed ? "/create" : "/register?returnTo=/create"}>
                    <Button className="gap-2">
                      {authed ? "Start Building" : "Build a Course"}
                      <ArrowRight className="h-4 w-4" />
                    </Button>
                  </Link>
                </div>
              </div>
              <div className="bg-muted/50 p-10 md:p-12 flex flex-col justify-center border-t md:border-t-0 md:border-l border-border">
                <div className="space-y-4">
                  <p className="text-sm font-medium text-muted-foreground uppercase tracking-wider">How it works</p>
                  {[
                    { step: "1", text: "Describe what you want to learn, or paste a source" },
                    { step: "2", text: "AI generates a course outline grounded in wiki sources" },
                    { step: "3", text: "Review, edit, and publish — each lesson gets notes, a tutor KB, and quizzes" },
                    { step: "4", text: "Learn with a Socratic AI tutor that knows your course material deeply" },
                  ].map((item) => (
                    <div key={item.step} className="flex items-start gap-3">
                      <div className="w-7 h-7 rounded-full bg-primary/15 flex items-center justify-center flex-shrink-0 text-sm font-bold text-primary">
                        {item.step}
                      </div>
                      <p className="text-sm text-foreground leading-relaxed pt-0.5">{item.text}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Living Wiki */}
      <section className="py-20 px-6 border-t border-border/50 bg-muted/30">
        <div className="max-w-5xl mx-auto">
          <div className="rounded-2xl border border-border bg-card overflow-hidden">
            <div className="grid md:grid-cols-2 gap-0">
              <div className="p-10 md:p-12 flex flex-col justify-center space-y-5">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-sm font-medium w-fit">
                  <Library className="h-3.5 w-3.5" />
                  Under the hood
                </div>
                <h2 className="text-3xl font-bold tracking-tight">
                  A wiki that{" "}
                  <span className="text-primary">learns as you do</span>
                </h2>
                <p className="text-muted-foreground leading-relaxed">
                  Most learning platforms freeze their content the day it ships.
                  SocraticTutor is backed by an LLM-curated wiki &mdash; a living
                  knowledge base that&apos;s continuously enriched with new sources,
                  connections, and explanations. Every course, every tutor
                  conversation, every concept lookup draws from this evolving
                  foundation.
                </p>
                <div className="pt-2">
                  <a
                    href="https://socratic-tutor-pi.vercel.app"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <Button variant="outline" className="gap-2">
                      Browse the Wiki
                      <ExternalLink className="h-4 w-4" />
                    </Button>
                  </a>
                </div>
              </div>
              <div className="bg-muted/50 p-10 md:p-12 flex flex-col justify-center border-t md:border-t-0 md:border-l border-border">
                <div className="space-y-6">
                  {[
                    {
                      icon: RefreshCw,
                      title: "Always current",
                      text: "New research and educator content is continuously curated and integrated by LLMs",
                    },
                    {
                      icon: Zap,
                      title: "Start from anywhere",
                      text: "Prompt a topic, paste a video, or jump into a concept — the wiki meets you where you are",
                    },
                    {
                      icon: BookOpen,
                      title: "Deeply grounded",
                      text: "Grounded in curated sources from leading educators and researchers across the field",
                    },
                  ].map((item) => (
                    <div key={item.title} className="flex items-start gap-4">
                      <div className="w-9 h-9 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                        <item.icon className="h-4 w-4 text-primary" />
                      </div>
                      <div>
                        <p className="font-semibold text-foreground text-sm">{item.title}</p>
                        <p className="text-sm text-muted-foreground leading-relaxed mt-0.5">{item.text}</p>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="mt-8 pt-6 border-t border-border flex items-center gap-2 text-xs text-muted-foreground">
                  <RefreshCw className="h-3 w-3 flex-shrink-0" />
                  <span>Hundreds of curated sources, and growing</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>


      {/* CTA */}
      <section className="py-20 px-6">
        <div className="max-w-2xl mx-auto text-center space-y-6">
          <h2 className="text-3xl font-bold">Ready to learn differently?</h2>
          <p className="text-muted-foreground">
            Pick a curated course or design your own — either way, you get an AI
            tutor that builds understanding through questioning, backed by the
            best ML/AI content on the internet.
          </p>
          <div className="flex items-center justify-center gap-3">
            <Link href={authed ? "/learn" : "/register"}>
              <Button size="lg" className="gap-2 text-base px-8">
                {authed ? "Go to Dashboard" : "Create Account"}
                <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
            <Link href={authed ? "/create" : "/register?returnTo=/create"}>
              <Button variant="outline" size="lg" className="gap-2 text-base px-8">
                <Sparkles className="h-4 w-4" />
                Design a Course
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border py-8 px-6">
        <div className="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-muted-foreground">
          <div className="flex items-center gap-2">
            <svg
              viewBox="0 0 24 24"
              className="h-4 w-4 text-primary"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20" />
              <path d="M8 7h6M8 11h8" />
            </svg>
            <span>Built by Pratik Mehta</span>
          </div>
          <div className="flex items-center gap-4">
            <a
              href="https://github.com/pratik008"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-foreground transition-colors"
            >
              GitHub
            </a>
            <a
              href="https://linkedin.com/in/pratik008"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-foreground transition-colors"
            >
              LinkedIn
            </a>
            <a
              href="mailto:pratik008@gmail.com"
              className="hover:text-foreground transition-colors"
            >
              Email
            </a>
            <a
              href="https://socratic-tutor-pi.vercel.app"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-foreground transition-colors"
            >
              Wiki
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
