# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in SocraticTutor, please report it
responsibly. **Do not open a public GitHub issue.**

Instead, email the maintainers at the address listed in the repository's
contact information, or use GitHub's
[private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability)
feature.

Please include:

- A description of the vulnerability
- Steps to reproduce
- The potential impact
- Any suggested fix (if you have one)

We will acknowledge receipt within 3 business days and aim to provide a fix or
mitigation within 30 days of confirmation.

## Supported Versions

Security updates are applied to the latest release on the `main` branch only.

## Security Best Practices for Deployers

- **Never commit secrets.** Use `.env` files (gitignored) or a secrets manager.
- **Set a strong `JWT_SECRET`** — the app will refuse to start without one.
  Generate one with:
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(64))"
  ```
- **Restrict CORS** — set `FRONTEND_URL` to your actual domain in production
  rather than using `*`.
- **Keep dependencies updated** — run `pip audit` and `npm audit` periodically.
