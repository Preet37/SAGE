interface VideoPlayerProps {
  youtubeId?: string | null;
  vimeoUrl?: string | null;
  title?: string;
}

function getVimeoEmbedUrl(vimeoUrl: string): string {
  // Handle formats: https://vimeo.com/123456789/hash or https://vimeo.com/123456789
  const match = vimeoUrl.match(/vimeo\.com\/(\d+)(?:\/([a-zA-Z0-9]+))?/);
  if (!match) return vimeoUrl;
  const videoId = match[1];
  const hash = match[2];
  return hash
    ? `https://player.vimeo.com/video/${videoId}?h=${hash}`
    : `https://player.vimeo.com/video/${videoId}`;
}

export function VideoPlayer({ youtubeId, vimeoUrl, title }: VideoPlayerProps) {
  const embedSrc = youtubeId
    ? `https://www.youtube.com/embed/${youtubeId}`
    : vimeoUrl
      ? getVimeoEmbedUrl(vimeoUrl)
      : null;

  if (!embedSrc) return null;

  return (
    <div className="rounded-lg overflow-hidden bg-black">
      <div className="relative w-full" style={{ paddingBottom: "56.25%" }}>
        <iframe
          className="absolute inset-0 w-full h-full"
          src={embedSrc}
          title={title || "Lesson Video"}
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; fullscreen"
          allowFullScreen
        />
      </div>
    </div>
  );
}
