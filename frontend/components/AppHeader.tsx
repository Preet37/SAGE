"use client";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { removeToken } from "@/lib/auth";
import { Button } from "@/components/ui/button";
import { ThemeToggle } from "@/components/ThemeToggle";
import { cn } from "@/lib/utils";
import {
  BookOpen,
  Compass,
  Hammer,
  Sparkles,
  Library,
  LogOut,
  FolderOpen,
  Network,
  ImagePlus,
  Smartphone,
} from "lucide-react";
import type { ReactNode } from "react";

const NAV_ITEMS = [
  { href: "/learn", icon: BookOpen, label: "Learn" },
  { href: "/explore", icon: Compass, label: "Explore" },
  { href: "/projects", icon: Hammer, label: "Projects" },
  { href: "/create", icon: Sparkles, label: "Create" },
  { href: "/memory", icon: FolderOpen, label: "My Docs" },
  { href: "/network", icon: Network, label: "Network" },
  { href: "/sketch", icon: ImagePlus, label: "Sketch" },
  { href: "/pocket", icon: Smartphone, label: "Pocket" },
] as const;

interface AppHeaderProps {
  leftSlot?: ReactNode;
}

export function AppHeader({ leftSlot }: AppHeaderProps) {
  const pathname = usePathname();
  const router = useRouter();

  function handleLogout() {
    removeToken();
    router.push("/login");
  }

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
        {NAV_ITEMS.map(({ href, icon: Icon, label }) => {
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
        <a
          href="https://socratic-tutor-pi.vercel.app"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Button
            variant="ghost"
            size="sm"
            className="gap-1.5 text-muted-foreground hover:text-foreground"
          >
            <Library className="h-3.5 w-3.5" />
            <span className="hidden sm:inline">Wiki</span>
          </Button>
        </a>
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
