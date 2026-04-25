import { describe, it, expect, vi, beforeEach } from "vitest";
import { api, API_URL } from "@/lib/api";

const mockFetch = vi.fn();
global.fetch = mockFetch;

beforeEach(() => {
  mockFetch.mockReset();
});

function jsonResponse(body: unknown, status = 200) {
  return Promise.resolve({
    ok: status >= 200 && status < 300,
    status,
    statusText: status === 200 ? "OK" : "Error",
    json: () => Promise.resolve(body),
  });
}

describe("api.auth.login", () => {
  it("calls the correct URL with POST and JSON body", async () => {
    mockFetch.mockReturnValue(
      jsonResponse({ access_token: "tok123", token_type: "bearer" })
    );

    const result = await api.auth.login("user@test.com", "pass");

    expect(mockFetch).toHaveBeenCalledOnce();
    const [url, opts] = mockFetch.mock.calls[0];
    expect(url).toBe(`${API_URL}/auth/login`);
    expect(opts.method).toBe("POST");
    expect(JSON.parse(opts.body)).toEqual({
      email: "user@test.com",
      password: "pass",
    });
    expect(result.access_token).toBe("tok123");
  });
});

describe("api.auth.register", () => {
  it("calls the correct URL with POST and JSON body", async () => {
    mockFetch.mockReturnValue(
      jsonResponse({ access_token: "newtok", token_type: "bearer" })
    );

    const result = await api.auth.register("new@test.com", "newuser", "pw");

    const [url, opts] = mockFetch.mock.calls[0];
    expect(url).toBe(`${API_URL}/auth/register`);
    expect(opts.method).toBe("POST");
    expect(JSON.parse(opts.body)).toEqual({
      email: "new@test.com",
      username: "newuser",
      password: "pw",
    });
    expect(result.access_token).toBe("newtok");
  });
});

describe("authenticated requests", () => {
  it("passes Authorization header when token is provided", async () => {
    mockFetch.mockReturnValue(jsonResponse([]));

    await api.learningPaths.list("my-jwt-token");

    const [, opts] = mockFetch.mock.calls[0];
    expect(opts.headers["Authorization"]).toBe("Bearer my-jwt-token");
  });
});

describe("error handling", () => {
  it("throws with detail message from error response", async () => {
    mockFetch.mockReturnValue(
      jsonResponse({ detail: "Email already registered" }, 400)
    );

    await expect(
      api.auth.register("dup@test.com", "user", "pw")
    ).rejects.toThrow("Email already registered");
  });

  it("throws with statusText when JSON parse fails", async () => {
    mockFetch.mockReturnValue(
      Promise.resolve({
        ok: false,
        status: 500,
        statusText: "Internal Server Error",
        json: () => Promise.reject(new Error("bad json")),
      })
    );

    await expect(api.learningPaths.list("tok")).rejects.toThrow(
      "Internal Server Error"
    );
  });
});
