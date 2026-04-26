"use client";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useState, useRef, useEffect } from "react";
import { removeToken } from "@/lib/auth";
import { SageLogo } from "@/components/SageLogo";
import { LogOut, BookOpen, Compass, Sparkles, Smartphone, MoreHorizontal, Hammer, FolderOpen, Network } from "lucide-react";
import type { ReactNode } from "react";

const PRIMARY_NAV = [
  { href: "/learn",   icon: BookOpen,  label: "Learn"   },
  { href: "/explore", icon: Compass,   label: "Explore" },
  { href: "/create",  icon: Sparkles,  label: "Create"  },
  { href: "/pocket",  icon: Smartphone,label: "Pocket"  },
] as const;

const SECONDARY_NAV = [
  { href: "/projects",  icon: Hammer,    label: "Projects" },
  { href: "/documents", icon: FolderOpen,label: "My Docs"  },
  { href: "/network",   icon: Network,   label: "Network"  },
] as const;

const mono: React.CSSProperties = { fontFamily: "var(--font-dm-mono)" };

interface AppHeaderProps { leftSlot?: ReactNode; }

export function AppHeader({ leftSlot }: AppHeaderProps) {
  const pathname = usePathname();
  const router = useRouter();
  const [moreOpen, setMoreOpen] = useState(false);
  const moreRef = useRef<HTMLDivElement>(null);

  function handleLogout() { removeToken(); router.push("/login"); }

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (moreRef.current && !moreRef.current.contains(e.target as Node)) setMoreOpen(false);
    }
    if (moreOpen) document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [moreOpen]);

  const secondaryActive = SECONDARY_NAV.some(({ href }) => pathname.startsWith(href));

  return (
    <div
      className="flex items-center justify-between px-5 flex-shrink-0"
      style={{
        height: "3rem",
        background: "var(--ink-1)",
        borderBottom: "1px solid rgba(240,233,214,0.07)",
      }}
    >
      {/* Left */}
      <div className="flex items-center gap-4">
        <Link href="/" className="flex items-center" style={{ opacity: 1 }}>
          <SageLogo fontSize="0.78rem" />
        </Link>
        {leftSlot && (
          <>
            <div style={{ width: 1, height: "1rem", background: "rgba(240,233,214,0.12)" }} />
            <div className="flex items-center gap-2">{leftSlot}</div>
          </>
        )}
      </div>

      {/* Right — nav */}
      <div className="flex items-center gap-1">
        {PRIMARY_NAV.map(({ href, label }) => {
          const isActive = pathname.startsWith(href);
          return (
            <Link key={href} href={href}>
              <button
                style={{
                  ...mono,
                  fontSize: "0.58rem",
                  letterSpacing: "0.14em",
                  textTransform: "uppercase",
                  color: isActive ? "var(--cream-0)" : "var(--cream-2)",
                  background: "none",
                  border: "none",
                  cursor: "pointer",
                  padding: "0.35rem 0.75rem",
                  borderBottom: isActive ? "1px solid var(--gold)" : "1px solid transparent",
                  transition: "color 0.2s, border-color 0.2s",
                }}
                onMouseEnter={e => { if (!isActive) (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-1)"; }}
                onMouseLeave={e => { if (!isActive) (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-2)"; }}
              >
                {label}
              </button>
            </Link>
          );
        })}

        {/* More dropdown */}
        <div className="relative" ref={moreRef}>
          <button
            onClick={() => setMoreOpen(o => !o)}
            style={{
              ...mono,
              fontSize: "0.58rem",
              letterSpacing: "0.14em",
              textTransform: "uppercase",
              color: secondaryActive || moreOpen ? "var(--cream-0)" : "var(--cream-2)",
              background: "none",
              border: "none",
              cursor: "pointer",
              padding: "0.35rem 0.75rem",
              borderBottom: secondaryActive || moreOpen ? "1px solid var(--gold)" : "1px solid transparent",
              display: "flex",
              alignItems: "center",
              gap: "0.3rem",
              transition: "color 0.2s",
            }}
          >
            <MoreHorizontal style={{ width: "0.8rem", height: "0.8rem" }} />
            More
          </button>

          {moreOpen && (
            <div
              className="absolute right-0 top-full z-50 overflow-hidden"
              style={{
                marginTop: "0.25rem",
                minWidth: "9rem",
                background: "var(--ink-2)",
                border: "1px solid rgba(240,233,214,0.08)",
              }}
            >
              {SECONDARY_NAV.map(({ href, icon: Icon, label }) => {
                const isActive = pathname.startsWith(href);
                return (
                  <Link key={href} href={href} onClick={() => setMoreOpen(false)}>
                    <div
                      style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "0.6rem",
                        padding: "0.6rem 0.9rem",
                        ...mono,
                        fontSize: "0.6rem",
                        letterSpacing: "0.12em",
                        textTransform: "uppercase",
                        color: isActive ? "var(--cream-0)" : "var(--cream-2)",
                        cursor: "pointer",
                        transition: "color 0.15s, background 0.15s",
                      }}
                      onMouseEnter={e => { (e.currentTarget as HTMLDivElement).style.background = "rgba(240,233,214,0.04)"; (e.currentTarget as HTMLDivElement).style.color = "var(--cream-1)"; }}
                      onMouseLeave={e => { (e.currentTarget as HTMLDivElement).style.background = "transparent"; (e.currentTarget as HTMLDivElement).style.color = isActive ? "var(--cream-0)" : "var(--cream-2)"; }}
                    >
                      <Icon style={{ width: "0.75rem", height: "0.75rem", flexShrink: 0 }} />
                      {label}
                    </div>
                  </Link>
                );
              })}
            </div>
          )}
        </div>

        {/* Divider */}
        <div style={{ width: 1, height: "1rem", background: "rgba(240,233,214,0.1)", margin: "0 0.25rem" }} />

        {/* Logout */}
        <button
          onClick={handleLogout}
          title="Sign out"
          style={{
            background: "none",
            border: "none",
            cursor: "pointer",
            color: "var(--cream-2)",
            display: "flex",
            alignItems: "center",
            padding: "0.35rem 0.5rem",
            transition: "color 0.2s",
          }}
          onMouseEnter={e => (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-1)"}
          onMouseLeave={e => (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-2)"}
        >
          <LogOut style={{ width: "0.85rem", height: "0.85rem" }} />
        </button>
      </div>
    </div>
  );
}
