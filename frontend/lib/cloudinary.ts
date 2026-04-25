const CLOUD = process.env.NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME ?? '';

function cdnUrl(publicId: string, transforms: string): string {
  if (!CLOUD) return publicId;
  return `https://res.cloudinary.com/${CLOUD}/image/upload/${transforms}/${publicId}`;
}

export function buildDiagramUrl(publicId: string, width = 800): string {
  if (publicId.startsWith('http')) return publicId;
  return cdnUrl(publicId, `c_scale,w_${width},q_auto`);
}

export function buildThumbnailUrl(publicId: string): string {
  if (publicId.startsWith('http')) return publicId;
  return cdnUrl(publicId, 'c_fill,w_200,h_133,q_auto');
}

export function buildEnhancedUrl(publicId: string, width = 1200): string {
  if (publicId.startsWith('http')) return publicId;
  return cdnUrl(publicId, `c_scale,w_${width},q_auto,e_auto_contrast,e_sharpen`);
}

export function formatOcrContext(extractedText: string): string {
  const t = extractedText.trim();
  return t ? `The student shared an image. Extracted text:\n\n${t}\n\n` : '';
}
