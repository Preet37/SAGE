import { ExternalLink } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

interface Resource {
  title: string;
  url: string;
  snippet: string;
}

interface ResourceCardProps {
  resources: Resource[];
  query?: string;
}

export function ResourceCard({ resources, query }: ResourceCardProps) {
  if (!resources || resources.length === 0) return null;
  return (
    <div className="mt-3 space-y-2">
      {query && (
        <p className="text-xs text-muted-foreground font-medium">
          Search results for: <span className="text-primary">"{query}"</span>
        </p>
      )}
      {resources.slice(0, 3).map((r, i) => (
        <a
          key={i}
          href={r.url}
          target="_blank"
          rel="noopener noreferrer"
          className="block"
        >
          <Card className="hover:border-primary/50 transition-colors cursor-pointer">
            <CardContent className="py-2 px-3">
              <div className="flex items-start gap-2">
                <ExternalLink className="h-3.5 w-3.5 text-primary mt-0.5 flex-shrink-0" />
                <div className="min-w-0">
                  <p className="text-sm font-medium text-primary hover:underline truncate">
                    {r.title}
                  </p>
                  <p className="text-xs text-muted-foreground mt-0.5 line-clamp-2">
                    {r.snippet}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </a>
      ))}
    </div>
  );
}
