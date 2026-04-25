'use client';
import { useState, useRef } from 'react';
import { useAuthStore } from '@/lib/store';

interface UploadResult {
  imageUrl: string;
  extractedText: string;
}

interface Props {
  onUpload: (result: UploadResult) => void;
  disabled?: boolean;
}

export default function VisualUpload({ onUpload, disabled }: Props) {
  const { token } = useAuthStore();
  const [uploading, setUploading] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  async function handleFile(file: File) {
    if (!token || uploading) return;
    setUploading(true);
    try {
      const signRes = await fetch('/api/media/upload-signed', {
        headers: { Authorization: `Bearer ${token}` },
      });
      const { signature, timestamp, cloud_name, api_key, folder } = await signRes.json();

      const form = new FormData();
      form.append('file', file);
      form.append('api_key', api_key);
      form.append('timestamp', String(timestamp));
      form.append('signature', signature);
      form.append('folder', folder);

      const uploadRes = await fetch(
        `https://api.cloudinary.com/v1_1/${cloud_name}/image/upload`,
        { method: 'POST', body: form },
      );
      const uploadData = await uploadRes.json();
      const imageUrl: string = uploadData.secure_url;
      const publicId: string = uploadData.public_id ?? '';

      const ocrRes = await fetch('/api/media/ocr', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({ image_url: imageUrl, public_id: publicId }),
      });
      const ocrData = await ocrRes.json();

      onUpload({ imageUrl, extractedText: (ocrData.extracted_text as string) || '' });
    } catch {
      // upload failed silently — user can retry
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className="flex items-center gap-1.5">
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        className="hidden"
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) handleFile(file);
          e.target.value = '';
        }}
      />
      <button
        onClick={() => inputRef.current?.click()}
        disabled={disabled || uploading}
        title="Upload image for OCR analysis"
        className="w-8 h-8 rounded-full bg-orange-500/15 border border-orange-500/25 text-orange-400 flex items-center justify-center hover:bg-orange-500/25 transition-all disabled:opacity-40"
      >
        {uploading ? (
          <svg className="w-3.5 h-3.5 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
        ) : (
          <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        )}
      </button>
      <span className="text-[8px] font-bold px-1.5 py-0.5 rounded-full bg-orange-500/15 text-orange-400 border border-orange-500/20">
        cloudinary
      </span>
    </div>
  );
}
