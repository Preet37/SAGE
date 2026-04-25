/**
 * Cloudinary URL builders.
 *
 * Cloudinary's transformation API lets us build derivative images on the fly
 * from URL alone — no server round-trip. We use this to produce thumbnails,
 * dark-mode versions, and annotated overlays without uploading 8 copies.
 */

const CLOUD_NAME = process.env.NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME || 'demo';
const BASE = `https://res.cloudinary.com/${CLOUD_NAME}/image/upload`;

export interface OcrAnnotation {
  description: string;
  bounding_box?: { x: number; y: number; w: number; h: number };
}

export interface CloudinaryUpload {
  public_id: string;
  secure_url: string;
  width: number;
  height: number;
  bytes: number;
  format: string;
}

export function buildThumbnailUrl(publicId: string, w = 240, h = 135): string {
  return `${BASE}/w_${w},h_${h},c_fill,q_auto,f_auto/${publicId}`;
}

export function buildDiagramUrl(publicId: string, opts?: { dark?: boolean; contrast?: number }): string {
  const tx: string[] = ['w_960', 'h_540', 'c_fill', 'q_auto', 'f_auto'];
  if (opts?.dark) tx.push('e_invert');
  if (opts?.contrast) tx.push(`e_contrast:${opts.contrast}`);
  return `${BASE}/${tx.join(',')}/${publicId}`;
}

export function buildEnhancedUrl(publicId: string): string {
  return `${BASE}/e_improve,e_auto_color,e_auto_contrast,q_auto,f_auto/${publicId}`;
}

/**
 * Format an OCR text dump into a compact context string the LLM can consume
 * without burning a thousand tokens.
 */
export function formatOcrContext(text: string, maxChars = 1200): string {
  if (!text) return '';
  const compact = text.replace(/\s+/g, ' ').trim();
  if (compact.length <= maxChars) return compact;
  return compact.slice(0, maxChars) + '…';
}
