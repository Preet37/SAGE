import { describe, it, expect } from "vitest";
import { cn } from "@/lib/utils";

describe("cn() — class name merging", () => {
  it("merges multiple class strings", () => {
    expect(cn("px-2", "py-1")).toBe("px-2 py-1");
  });

  it("handles conditional classes", () => {
    const active = true;
    const result = cn("base", active && "text-blue-500");
    expect(result).toContain("base");
    expect(result).toContain("text-blue-500");
  });

  it("resolves Tailwind conflicts (last wins)", () => {
    const result = cn("px-2", "px-4");
    expect(result).toBe("px-4");
  });

  it("ignores falsy values", () => {
    expect(cn("a", false, null, undefined, "b")).toBe("a b");
  });
});
