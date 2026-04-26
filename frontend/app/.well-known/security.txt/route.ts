export function GET() {
  const body = `Contact: https://github.com/pratik008/SAGE/issues
Expires: 2027-04-11T00:00:00.000Z
Preferred-Languages: en
Canonical: https://socratictutor.dev/.well-known/security.txt
`;
  return new Response(body, {
    headers: { "Content-Type": "text/plain" },
  });
}
