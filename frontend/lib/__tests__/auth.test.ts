import { describe, it, expect, beforeEach } from "vitest";
import { getToken, setToken, removeToken, isAuthenticated } from "@/lib/auth";

const store: Record<string, string> = {};
const mockLocalStorage = {
  getItem: (key: string) => store[key] ?? null,
  setItem: (key: string, value: string) => {
    store[key] = value;
  },
  removeItem: (key: string) => {
    delete store[key];
  },
} as unknown as Storage;

Object.defineProperty(globalThis, "window", { value: {}, writable: true });
Object.defineProperty(globalThis, "localStorage", {
  value: mockLocalStorage,
  writable: true,
});

beforeEach(() => {
  for (const key of Object.keys(store)) delete store[key];
});

describe("auth token helpers", () => {
  it("getToken returns null when nothing is stored", () => {
    expect(getToken()).toBeNull();
  });

  it("setToken / getToken round-trip", () => {
    setToken("abc123");
    expect(getToken()).toBe("abc123");
  });

  it("removeToken clears the stored token", () => {
    setToken("xyz");
    removeToken();
    expect(getToken()).toBeNull();
  });

  it("isAuthenticated reflects token presence", () => {
    expect(isAuthenticated()).toBe(false);
    setToken("tok");
    expect(isAuthenticated()).toBe(true);
    removeToken();
    expect(isAuthenticated()).toBe(false);
  });
});
