"use client";

import { api, MediaAssetResponse, MediaSignResponse } from "./api";
import { getToken } from "./auth";

interface UploadOptions {
  lessonId?: string;
  kind?: string;
  folder?: string;
  tags?: string[];
  eager?: string;
  onProgress?: (pct: number) => void;
}

interface CloudinaryUploadResponse {
  public_id: string;
  secure_url: string;
  resource_type: string;
  format: string;
  width: number;
  height: number;
  bytes: number;
  folder?: string;
  tags?: string[];
}

export async function uploadToCloudinary(
  file: File,
  opts: UploadOptions = {},
): Promise<MediaAssetResponse> {
  const token = getToken();
  if (!token) throw new Error("Not authenticated");

  const sign: MediaSignResponse = await api.media.sign({
    folder: opts.folder,
    upload_preset: undefined,
    tags: opts.tags,
    eager: opts.eager,
  }, token);

  const url = `https://api.cloudinary.com/v1_1/${sign.cloud_name}/auto/upload`;
  const form = new FormData();
  form.append("file", file);
  form.append("api_key", sign.api_key);
  form.append("timestamp", String(sign.timestamp));
  form.append("folder", sign.folder);
  form.append("upload_preset", sign.upload_preset);
  if (sign.tags) form.append("tags", sign.tags);
  if (sign.eager) form.append("eager", sign.eager);
  form.append("signature", sign.signature);

  const cloudinaryRes = await xhrUpload(url, form, opts.onProgress);

  const recorded = await api.media.recordAsset({
    public_id: cloudinaryRes.public_id,
    secure_url: cloudinaryRes.secure_url,
    resource_type: cloudinaryRes.resource_type,
    format: cloudinaryRes.format,
    width: cloudinaryRes.width,
    height: cloudinaryRes.height,
    bytes: cloudinaryRes.bytes,
    folder: cloudinaryRes.folder ?? sign.folder,
    tags: cloudinaryRes.tags ?? opts.tags ?? [],
    lesson_id: opts.lessonId,
    kind: opts.kind ?? "upload",
  }, token);

  return recorded;
}

function xhrUpload(url: string, form: FormData, onProgress?: (pct: number) => void): Promise<CloudinaryUploadResponse> {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", url);
    xhr.upload.onprogress = (evt) => {
      if (evt.lengthComputable && onProgress) onProgress(Math.round((evt.loaded / evt.total) * 100));
    };
    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        try {
          resolve(JSON.parse(xhr.responseText) as CloudinaryUploadResponse);
        } catch (err) {
          reject(err);
        }
      } else {
        reject(new Error(`Upload failed: ${xhr.status} ${xhr.responseText}`));
      }
    };
    xhr.onerror = () => reject(new Error("Network error during upload"));
    xhr.send(form);
  });
}

/** Build a Cloudinary delivery URL with chained transformations. */
export function cloudinaryUrl(
  cloudName: string,
  publicId: string,
  transformations: string[] = [],
  resourceType: string = "image",
): string {
  const chain = transformations.filter(Boolean).join("/");
  const base = `https://res.cloudinary.com/${cloudName}/${resourceType}/upload`;
  return chain ? `${base}/${chain}/${publicId}` : `${base}/${publicId}`;
}
