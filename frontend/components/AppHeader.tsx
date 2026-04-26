"use client";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useState, useRef, useEffect } from "react";
import { removeToken } from "@/lib/auth";
import { Button } from "@/components/ui/button";
import { ThemeToggle } from "@/components/ThemeToggle";
import { cn } from "@/lib/utils";
import {
  BookOpen,
  Compass,
  Sparkles,
  LogOut,
  FolderOpen,
  Network,
  Smartphone,
  MoreHorizontal,
  Hammer,
} from "lucide-react";
import type { ReactNode } from "react";

// Primary nav — always visible
const PRIMARY_NAV = [
  { href: "/learn", icon: BookOpen, label: "Learn" },
  { href: "/explore", icon: Compass, label: "Explore" },
  { href: "/create", icon: Sparkles, label: "Create" },
  { href: "/pocket", icon: Smartphone, label: "Pocket" },
] as const;

// Secondary nav — collapsed into "More" dropdown
const SECONDARY_NAV = [
  { href: "/projects", icon: Hammer, label: "Projects" },
  { href: "/documents", icon: FolderOpen, label: "My Docs" },
  { href: "/network", icon: Network, label: "Network" },
] as const;

interface AppHeaderProps {
  leftSlot?: ReactNode;
}

export function AppHeader({ leftSlot }: AppHeaderProps) {
  const pathname = usePathname();
  const router = useRouter();
  const [moreOpen, setMoreOpen] = useState(false);
  const moreRef = useRef<HTMLDivElement>(null);

  function handleLogout() {
    removeToken();
    router.push("/login");
  }

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (moreRef.current && !moreRef.current.contains(e.target as Node)) {
        setMoreOpen(false);
      }
    }
    if (moreOpen) document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [moreOpen]);

  const secondaryActive = SECONDARY_NAV.some(({ href }) => pathname.startsWith(href));

  return (
    <div className="flex items-center justify-between px-4 py-2 border-b border-border bg-card/50 flex-shrink-0">
      <div className="flex items-center gap-3">
        <Link href="/" className="flex items-center gap-1.5 hover:opacity-80 transition-opacity">
          <svg
            viewBox="0 0 24 24"
            className="h-5 w-5 text-primary"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20" />
            <path d="M8 7h6M8 11h8" />
          </svg>
          <span className="font-semibold text-sm hidden sm:inline">
            <span className="text-primary">S</span>AGE
          </span>
        </Link>
        {leftSlot && (
          <>
            <div className="h-4 w-px bg-border" />
            <div className="flex items-center gap-2">{leftSlot}</div>
          </>
        )}
      </div>

      <div className="flex items-center gap-1">
        {/* Primary nav items — always visible */}
        {PRIMARY_NAV.map(({ href, icon: Icon, label }) => {
          const isActive = pathname.startsWith(href);
          return (
            <Link key={href} href={href}>
              <Button
                variant="ghost"
                size="sm"
                className={cn(
                  "gap-1.5",
                  isActive
                    ? "text-foreground font-medium"
                    : "text-muted-foreground hover:text-foreground"
                )}
              >
                <Icon className="h-3.5 w-3.5" />
                <span className="hidden sm:inline">{label}</span>
              </Button>
            </Link>
          );
        })}

        {/* More dropdown — secondary items */}
        <div className="relative" ref={moreRef}>
          <Button
            variant="ghost"
            size="sm"
            className={cn(
              "gap-1.5",
              secondaryActive || moreOpen
                ? "text-foreground font-medium"
                : "text-muted-foreground hover:text-foreground"
            )}
            onClick={() => setMoreOpen((o) => !o)}
          >
            <MoreHorizontal className="h-3.5 w-3.5" />
            <span className="hidden sm:inline">More</span>
          </Button>

          {moreOpen && (
            <div className="absolute right-0 top-full mt-1 w-44 rounded-lg border border-border bg-card shadow-lg z-50 overflow-hidden">
              {SECONDARY_NAV.map(({ href, icon: Icon, label }) => {
                const isActive = pathname.startsWith(href);
                return (
                  <Link key={href} href={href} onClick={() => setMoreOpen(false)}>
                    <div
                      className={cn(
                        "flex items-center gap-2.5 px-3 py-2 text-sm hover:bg-muted/60 transition-colors cursor-pointer",
                        isActive ? "text-foreground font-medium bg-muted/40" : "text-muted-foreground"
                      )}
                    >
                      <Icon className="h-4 w-4 flex-shrink-0" />
                      {label}
                    </div>
                  </Link>
                );
              })}
            </div>
          )}
        </div>

        <ThemeToggle />
        <Button
          variant="ghost"
          size="icon"
          onClick={handleLogout}
          className="text-muted-foreground hover:text-foreground"
        >
          <LogOut className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}
