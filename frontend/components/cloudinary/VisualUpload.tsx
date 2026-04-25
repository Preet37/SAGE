'use client';
import { useState, useRef } from 'react';
import { useAuthStore } from '@/lib/store';
import { getSignedUpload, ingestOcr, type SignedUploadParams } from '@/lib/api';

interface Props {
  lessonId: number;
  onUpload: (imageUrl: string, extractedText: string) => void;
  disabled?: boolean;
}

export default function VisualUpload({ lessonId, onUpload, disabled }: Props) {
  const { token } = useAuthStore();
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  async function uploadToCloudinary(file: File, params: SignedUploadParams) {
    const form = new FormData();
    form.append('file', file);
    form.append('api_key', params.api_key);
    form.append('timestamp', String(params.timestamp));
    form.append('signature', params.signature);
    form.append('folder', params.folder);
    if (params.public_id) form.append('public_id', params.public_id);
    if (params.use_ocr) form.append('ocr', 'adv_ocr');

    const res = await fetch(params.upload_url, { method: 'POST', body: form });
    if (!res.ok) {
      const msg = await res.text().catch(() => '');
      throw new Error(`Cloudinary upload failed: ${res.status} ${msg.slice(0, 200)}`);
    }
    return res.json() as Promise<{
      secure_url: string;
      public_id: string;
      width: number;
      height: number;
      bytes: number;
      info?: { ocr?: { adv_ocr?: { data?: { textAnnotations?: { description: string }[] }[] } } };
    }>;
  }

  function extractOcrFromUploadResponse(resp: { info?: { ocr?: { adv_ocr?: { data?: { textAnnotations?: { description: string }[] }[] } } } }): string {
    const data = resp.info?.ocr?.adv_ocr?.data ?? [];
    const lines = data
      .map(d => d.textAnnotations?.[0]?.description ?? '')
      .filter(Boolean);
    return lines.join('\n').trim();
  }

  async function handleFile(file: File) {
    if (!token) return;
    setIsUploading(true);
    setError(null);
    try {
      const sig = await getSignedUpload(token, lessonId);
      const upload = await uploadToCloudinary(file, sig);

      // Cloudinary returns OCR inline in the upload response when add-on is on.
      // Fallback: ask backend to fetch via API.
      let extracted = extractOcrFromUploadResponse(upload);
      if (!extracted) {
        const ocr = await ingestOcr(token, {
          image_url: upload.secure_url,
          public_id: upload.public_id,
          lesson_id: lessonId,
          width: upload.width,
          height: upload.height,
          bytes: upload.bytes,
        });
        extracted = ocr.extracted_text;
      }
      onUpload(upload.secure_url, extracted);
    } catch (e) {
      setError((e as Error).message || 'Upload failed');
    } finally {
      setIsUploading(false);
      if (inputRef.current) inputRef.current.value = '';
    }
  }

  return (
    <div className="inline-flex items-center gap-2">
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        className="hidden"
        onChange={(e) => {
          const f = e.target.files?.[0];
          if (f) handleFile(f);
        }}
        disabled={disabled || isUploading}
      />
      <button
        type="button"
        onClick={() => inputRef.current?.click()}
        disabled={disabled || isUploading}
        title="Upload an image — SAGE will OCR it"
        className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg border border-ora/25 bg-ora/10 text-ora hover:bg-ora/20 transition-all text-xs font-semibold disabled:opacity-40"
      >
        {isUploading ? (
          <>
            <svg className="w-3 h-3 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            OCR…
          </>
        ) : (
          <>
            <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            Image
          </>
        )}
      </button>
      <span className="text-[9px] font-bold text-ora/70 uppercase tracking-wider">cloudinary</span>
      {error && <span className="text-[10px] text-pnk">{error}</span>}
    </div>
  );
}
