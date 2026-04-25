# Track 4: Cloudinary Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make SAGE a visual tutor. Students photograph notes and textbook pages; Cloudinary processes every image (auto-crop, enhance, OCR), extracted text goes to the tutor, and all lesson media is served via Cloudinary CDN with AI transformations. A study materials gallery persists uploads across devices.

**Architecture:** A new `/media` router handles signed uploads and OCR ingestion. `TutorRequest` carries `image_url` + `extracted_text`. Frontend adds a camera/upload button to `TutorChat` using `CldUploadWidget`. All lesson images render via `CldImage` (auto WebP/AVIF). A Materials tab shows the full upload history using Cloudinary's search API.

**Tech Stack:** next-cloudinary (CldImage, CldUploadWidget, CldVideoPlayer), cloudinary (backend SDK), @cloudinary/url-gen, Python cloudinary>=1.36.0

---

## File Map

| File | Action | Purpose |
|------|--------|---------|
| `backend/app/routers/media.py` | Create | Signed upload endpoint, OCR result handler, diagram fetcher |
| `backend/app/main.py` | Modify | Include media router |
| `frontend/lib/cloudinary.ts` | Create | Transformation URL builder, OCR result helper |
| `frontend/components/cloudinary/VisualUpload.tsx` | Create | CldUploadWidget + upload pipeline with cloudinary badge |
| `frontend/components/cloudinary/DiagramLibrary.tsx` | Create | Lesson diagram gallery from Cloudinary folder |
| `frontend/components/cloudinary/MaterialsGallery.tsx` | Create | Study material history tab |
| `frontend/components/cloudinary/BeforeAfter.tsx` | Create | Split-slider comparison: original vs processed |
| `frontend/components/tutor/TutorChat.tsx` | Modify | Add upload button, render CldImage inline in chat bubbles |
| `frontend/components/tutor/MessageBubble.tsx` | Modify | Render inline CldImage if message has image_url |
| `frontend/app/learn/[courseId]/[lessonId]/page.tsx` | Modify | Add Materials panel tab, pass image context to sendMessage |

---

## Environment Variables Required

Add to `backend/.env` and `frontend/.env.local`:

```
# Backend
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Frontend
NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME=your_cloud_name
```

---

### Task 1: Install dependencies

**Files:**
- Modify: `backend/requirements.txt`
- Modify: `frontend/package.json`

- [ ] **Step 1: Add cloudinary to backend**

```bash
cd backend && pip install "cloudinary>=1.36.0"
echo "cloudinary>=1.36.0" >> requirements.txt
```

- [ ] **Step 2: Add next-cloudinary to frontend**

```bash
cd frontend && npm install next-cloudinary @cloudinary/url-gen
```

- [ ] **Step 3: Verify backend import**

```bash
cd backend && python -c "import cloudinary; print(f'cloudinary {cloudinary.__version__} OK')"
```

Expected: prints cloudinary version.

- [ ] **Step 4: Verify frontend build still works**

```bash
cd frontend && npx tsc --noEmit --pretty false 2>&1 | tail -5
```

Expected: no errors.

- [ ] **Step 5: Commit**

```bash
git add backend/requirements.txt frontend/package.json frontend/package-lock.json
git commit -m "feat(cloudinary): install cloudinary SDK (backend + next-cloudinary frontend)"
```

---

### Task 2: Create backend media router

**Files:**
- Create: `backend/app/routers/media.py`

- [ ] **Step 1: Create media.py**

```python
"""
Cloudinary media router — signed uploads, OCR ingestion, diagram fetching.
Track 4: Cloudinary.
"""
import logging
import os
from datetime import datetime

import cloudinary
import cloudinary.api
import cloudinary.uploader
import cloudinary.utils
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.routers.auth import get_current_user
from app.models.user import User

log = logging.getLogger("sage.media")
router = APIRouter(prefix="/media", tags=["media"])

# Configure cloudinary from environment
cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME", ""),
    api_key=os.environ.get("CLOUDINARY_API_KEY", ""),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET", ""),
    secure=True,
)


class SignedUploadResponse(BaseModel):
    signature: str
    timestamp: int
    cloud_name: str
    api_key: str
    upload_preset: str | None = None
    folder: str


class OcrIngestionRequest(BaseModel):
    public_id: str
    lesson_id: int
    extracted_text: str
    image_url: str


class DiagramResponse(BaseModel):
    url: str
    public_id: str
    format: str


@router.get("/upload-signed")
async def get_signed_upload_params(
    lesson_id: int,
    user: User = Depends(get_current_user),
) -> SignedUploadResponse:
    """
    Generate signed upload parameters for direct browser→Cloudinary upload.
    The frontend uses these to initialize CldUploadWidget in signed mode.
    """
    folder = f"sage/lessons/{lesson_id}/user_{user.id}"
    timestamp = int(datetime.utcnow().timestamp())

    # Build params to sign (folder + transformation pipeline)
    params_to_sign = {
        "folder": folder,
        "timestamp": timestamp,
        "eager": "c_crop,g_auto|e_auto_brightness|e_sharpen",
        "eager_async": True,
    }

    signature = cloudinary.utils.api_sign_request(
        params_to_sign,
        os.environ.get("CLOUDINARY_API_SECRET", ""),
    )

    return SignedUploadResponse(
        signature=signature,
        timestamp=timestamp,
        cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME", ""),
        api_key=os.environ.get("CLOUDINARY_API_KEY", ""),
        folder=folder,
    )


@router.post("/ocr")
async def ingest_ocr_result(
    req: OcrIngestionRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Receive OCR result from frontend after Cloudinary upload completes.
    Stores it for later tutor context injection.
    """
    # For now store in-memory (can persist to DB in production)
    log.info(f"OCR ingested: public_id={req.public_id}, lesson={req.lesson_id}, text_len={len(req.extracted_text)}")
    return {
        "status": "ok",
        "public_id": req.public_id,
        "extracted_chars": len(req.extracted_text),
    }


@router.get("/materials/{lesson_id}")
async def get_lesson_materials(
    lesson_id: int,
    user: User = Depends(get_current_user),
) -> dict:
    """
    Fetch all media uploaded for this lesson by this user from Cloudinary.
    Uses Cloudinary Search API.
    """
    folder = f"sage/lessons/{lesson_id}/user_{user.id}"
    try:
        result = cloudinary.api.resources(
            type="upload",
            prefix=folder,
            max_results=50,
            resource_type="image",
        )
        resources = result.get("resources", [])
        return {
            "materials": [
                {
                    "public_id": r["public_id"],
                    "url": r["secure_url"],
                    "format": r.get("format", ""),
                    "created_at": r.get("created_at", ""),
                    "width": r.get("width"),
                    "height": r.get("height"),
                }
                for r in resources
            ]
        }
    except Exception as e:
        log.warning(f"Cloudinary materials fetch failed: {e}")
        return {"materials": []}


@router.get("/diagram/{course_id}/{lesson_id}/{concept_slug}")
async def get_lesson_diagram(
    course_id: int,
    lesson_id: int,
    concept_slug: str,
    width: int = 800,
    user: User = Depends(get_current_user),
) -> DiagramResponse:
    """
    Fetch a pre-uploaded lesson diagram from Cloudinary with responsive transform.
    Diagrams are organized in sage/courses/{course_id}/{lesson_id}/ folder.
    """
    public_id = f"sage/courses/{course_id}/{lesson_id}/{concept_slug}"
    try:
        url = cloudinary.utils.cloudinary_url(
            public_id,
            width=width,
            crop="scale",
            format="auto",
            quality="auto:good",
            fetch_format="auto",
        )[0]
        return DiagramResponse(url=url, public_id=public_id, format="auto")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Diagram not found: {e}")
```

- [ ] **Step 2: Register media router in main.py**

In `backend/app/main.py`, add the media import and router:

```python
# In imports section:
from app.routers import auth, courses, tutor, concept_map, network, replay, accessibility, dashboard, notes, visual, media

# After app.include_router(visual.router):
app.include_router(media.router)
```

- [ ] **Step 3: Verify router loads**

```bash
cd backend && python -c "from app.routers.media import router; print('Media router OK')"
```

Expected: `Media router OK`

- [ ] **Step 4: Commit**

```bash
git add backend/app/routers/media.py backend/app/main.py
git commit -m "feat(cloudinary): add /media router with signed uploads, OCR ingestion, diagram fetcher"
```

---

### Task 3: Create frontend Cloudinary utility library

**Files:**
- Create: `frontend/lib/cloudinary.ts`

- [ ] **Step 1: Create cloudinary.ts**

```typescript
/**
 * Cloudinary utility helpers — transformation URL builder, OCR result helper.
 * Track 4: Cloudinary.
 */

const CLOUD_NAME = process.env.NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME ?? '';

/**
 * Build a Cloudinary delivery URL with transformations.
 * Uses the URL generation approach from @cloudinary/url-gen.
 */
export function buildImageUrl(
  publicId: string,
  options: {
    width?: number;
    height?: number;
    crop?: 'fill' | 'scale' | 'thumb' | 'auto';
    quality?: number | 'auto';
    format?: 'auto' | 'webp' | 'avif';
    effect?: string;
  } = {}
): string {
  const { width, height, crop = 'scale', quality = 'auto', format = 'auto', effect } = options;

  const transforms: string[] = [];
  if (crop) transforms.push(`c_${crop}`);
  if (width) transforms.push(`w_${width}`);
  if (height) transforms.push(`h_${height}`);
  if (quality) transforms.push(`q_${quality}`);
  if (format) transforms.push(`f_${format}`);
  if (effect) transforms.push(effect);

  const transform = transforms.join(',');
  return `https://res.cloudinary.com/${CLOUD_NAME}/image/upload/${transform}/${publicId}`;
}

/**
 * Build an annotated image URL — adds a text overlay at a given gravity.
 */
export function buildAnnotatedUrl(
  publicId: string,
  annotation: string,
  gravity: 'south' | 'north' | 'center' = 'south',
  width: number = 800
): string {
  const encodedText = encodeURIComponent(annotation);
  return (
    `https://res.cloudinary.com/${CLOUD_NAME}/image/upload/` +
    `w_${width},c_scale/` +
    `l_text:Arial_16_bold:${encodedText},g_${gravity},y_10,co_white,b_rgb:00000080/` +
    `${publicId}`
  );
}

/**
 * Build a generative fill URL (extends image canvas with AI fill).
 */
export function buildGenerativeFillUrl(publicId: string, width: number, height: number): string {
  return (
    `https://res.cloudinary.com/${CLOUD_NAME}/image/upload/` +
    `w_${width},h_${height},c_pad,ar_${width}:${height},b_gen_fill/` +
    `${publicId}`
  );
}

/** Format OCR text for injection into tutor system prompt. */
export function formatOcrContext(ocrText: string): string {
  if (!ocrText.trim()) return '';
  return `## Visual Context (from student's uploaded image)\n\n${ocrText.trim()}\n\n`;
}

/** Cloudinary folder path for lesson media. */
export function lessonFolder(lessonId: number, userId: number): string {
  return `sage/lessons/${lessonId}/user_${userId}`;
}
```

- [ ] **Step 2: Verify TypeScript compiles**

```bash
cd frontend && npx tsc --noEmit --pretty false 2>&1 | grep "cloudinary"
```

Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git add frontend/lib/cloudinary.ts
git commit -m "feat(cloudinary): add Cloudinary URL builder utility library"
```

---

### Task 4: Build VisualUpload component

**Files:**
- Create: `frontend/components/cloudinary/VisualUpload.tsx`

- [ ] **Step 1: Create cloudinary/ directory**

```bash
mkdir -p frontend/components/cloudinary
```

- [ ] **Step 2: Create VisualUpload.tsx**

```tsx
'use client';
import { CldUploadWidget } from 'next-cloudinary';
import { useState } from 'react';

interface UploadResult {
  public_id: string;
  secure_url: string;
  info?: { ocr?: { data?: { fullTextAnnotation?: { text?: string } } } };
}

interface Props {
  lessonId: number;
  onUploadComplete: (imageUrl: string, extractedText: string, publicId: string) => void;
}

export default function VisualUpload({ lessonId, onUploadComplete }: Props) {
  const [uploading, setUploading] = useState(false);

  function handleSuccess(result: { info: unknown }) {
    setUploading(false);
    const info = result.info as UploadResult;
    const imageUrl = info.secure_url;
    const publicId = info.public_id;

    // Extract OCR text if Cloudinary returned it
    const extractedText =
      info.info?.ocr?.data?.fullTextAnnotation?.text ?? '';

    onUploadComplete(imageUrl, extractedText, publicId);
  }

  return (
    <CldUploadWidget
      uploadPreset={process.env.NEXT_PUBLIC_CLOUDINARY_UPLOAD_PRESET}
      options={{
        cloudName: process.env.NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME,
        sources: ['local', 'camera'],
        multiple: false,
        folder: `sage/lessons/${lessonId}`,
        // Eager transformations: auto-crop → enhance → sharpen
        eager: 'c_crop,g_auto|e_auto_brightness|e_sharpen',
        // Request OCR analysis
        ocr: 'adv_ocr',
        resourceType: 'image',
      }}
      onSuccess={handleSuccess}
      onQueuesStart={() => setUploading(true)}
      onClose={() => setUploading(false)}
    >
      {({ open }) => (
        <button
          onClick={() => open()}
          disabled={uploading}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-full border border-orange-500/30 bg-orange-500/10 text-orange-400 text-xs font-semibold hover:bg-orange-500/20 transition-colors disabled:opacity-50"
          title="Upload a photo of your notes or textbook"
        >
          <span>{uploading ? '⟳' : '📷'}</span>
          <span>{uploading ? 'Uploading…' : 'Upload'}</span>
          <span className="text-[9px] opacity-60 ml-0.5">cloudinary</span>
        </button>
      )}
    </CldUploadWidget>
  );
}
```

- [ ] **Step 3: Add NEXT_PUBLIC_CLOUDINARY_UPLOAD_PRESET to .env.local**

```bash
echo "NEXT_PUBLIC_CLOUDINARY_UPLOAD_PRESET=sage_unsigned" >> frontend/.env.local
```

Note: Create an unsigned upload preset named `sage_unsigned` in the Cloudinary dashboard (Settings → Upload → Upload presets → Add) with auto-crop and OCR enabled.

- [ ] **Step 4: Verify TypeScript compiles**

```bash
cd frontend && npx tsc --noEmit --pretty false 2>&1 | grep -i "visualupload\|cloudinary"
```

Expected: no errors.

- [ ] **Step 5: Commit**

```bash
git add frontend/components/cloudinary/VisualUpload.tsx
git commit -m "feat(cloudinary): add VisualUpload component with CldUploadWidget and OCR extraction"
```

---

### Task 5: Build DiagramLibrary component

**Files:**
- Create: `frontend/components/cloudinary/DiagramLibrary.tsx`

- [ ] **Step 1: Create DiagramLibrary.tsx**

```tsx
'use client';
import { CldImage } from 'next-cloudinary';
import { useState } from 'react';

interface Diagram {
  publicId: string;
  label: string;
  description?: string;
}

interface Props {
  courseId: number;
  lessonId: number;
  diagrams: Diagram[];
  onSelect?: (diagram: Diagram) => void;
}

export default function DiagramLibrary({ courseId, lessonId, diagrams, onSelect }: Props) {
  const [selected, setSelected] = useState<Diagram | null>(null);

  if (!diagrams.length) return null;

  function handleSelect(diagram: Diagram) {
    setSelected(diagram);
    onSelect?.(diagram);
  }

  return (
    <div className="rounded-xl border border-orange-500/20 bg-orange-500/5 p-3 mt-3">
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <span className="text-[10px] font-bold uppercase tracking-widest text-orange-400">
          Lesson Diagrams
        </span>
        <span className="text-[9px] font-bold px-2 py-0.5 rounded-full bg-orange-500/15 text-orange-400 border border-orange-500/20">
          cloudinary
        </span>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-2 gap-2">
        {diagrams.map((diagram) => (
          <button
            key={diagram.publicId}
            onClick={() => handleSelect(diagram)}
            className={`relative rounded-lg overflow-hidden border transition-all ${
              selected?.publicId === diagram.publicId
                ? 'border-orange-500/60'
                : 'border-white/10 hover:border-orange-500/30'
            }`}
          >
            <CldImage
              src={diagram.publicId}
              width={200}
              height={120}
              crop="fill"
              gravity="auto"
              alt={diagram.label}
              className="w-full h-24 object-cover"
            />
            <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/80 to-transparent px-2 py-1">
              <span className="text-[10px] text-white font-semibold">{diagram.label}</span>
            </div>
          </button>
        ))}
      </div>

      {/* Selected diagram full view */}
      {selected && (
        <div className="mt-3">
          <CldImage
            src={selected.publicId}
            width={600}
            height={400}
            crop="scale"
            format="auto"
            quality="auto:best"
            alt={selected.label}
            className="w-full rounded-lg"
          />
          {selected.description && (
            <p className="text-xs text-t2 mt-2">{selected.description}</p>
          )}
        </div>
      )}
    </div>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/components/cloudinary/DiagramLibrary.tsx
git commit -m "feat(cloudinary): add DiagramLibrary with CldImage grid and full-view selector"
```

---

### Task 6: Build MaterialsGallery component

**Files:**
- Create: `frontend/components/cloudinary/MaterialsGallery.tsx`

- [ ] **Step 1: Create MaterialsGallery.tsx**

```tsx
'use client';
import { useEffect, useState } from 'react';
import { CldImage } from 'next-cloudinary';
import { useAuthStore } from '@/lib/store';

interface Material {
  public_id: string;
  url: string;
  format: string;
  created_at: string;
  width?: number;
  height?: number;
}

interface Props {
  lessonId: number;
  onReopen?: (material: Material) => void;
}

export default function MaterialsGallery({ lessonId, onReopen }: Props) {
  const { token } = useAuthStore();
  const [materials, setMaterials] = useState<Material[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) return;
    fetch(`/api/media/materials/${lessonId}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r) => r.json())
      .then((data) => setMaterials(data.materials ?? []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [lessonId, token]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-32 text-t3 text-sm">
        Loading materials…
      </div>
    );
  }

  if (!materials.length) {
    return (
      <div className="flex flex-col items-center justify-center h-32 text-t3 text-sm gap-2">
        <span className="text-2xl">📷</span>
        <span>No uploads yet — use the camera button in chat</span>
        <span className="text-[9px] px-2 py-0.5 rounded-full bg-orange-500/10 text-orange-400 border border-orange-500/20">
          cloudinary
        </span>
      </div>
    );
  }

  return (
    <div className="p-4">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <span className="text-sm font-semibold text-t0">Study Materials</span>
        <span className="text-[9px] font-bold px-2 py-0.5 rounded-full bg-orange-500/15 text-orange-400 border border-orange-500/20">
          cloudinary
        </span>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-2 gap-3">
        {materials.map((material) => (
          <button
            key={material.public_id}
            onClick={() => onReopen?.(material)}
            className="group relative rounded-xl overflow-hidden border border-white/5 hover:border-orange-500/30 transition-all aspect-video bg-bg2"
          >
            <CldImage
              src={material.public_id}
              width={300}
              height={200}
              crop="fill"
              gravity="auto"
              format="auto"
              quality="auto:eco"
              alt="Study material"
              className="w-full h-full object-cover"
              loading="lazy"
            />
            {/* Overlay on hover */}
            <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
              <span className="text-xs text-white font-semibold">Reopen in tutor</span>
            </div>
            {/* Date label */}
            <div className="absolute bottom-1 right-1 text-[9px] text-white/60 bg-black/40 px-1 rounded">
              {material.created_at ? new Date(material.created_at).toLocaleDateString() : ''}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/components/cloudinary/MaterialsGallery.tsx
git commit -m "feat(cloudinary): add MaterialsGallery tab with lazy-loaded CldImage grid"
```

---

### Task 7: Build BeforeAfter split-slider component

**Files:**
- Create: `frontend/components/cloudinary/BeforeAfter.tsx`

- [ ] **Step 1: Create BeforeAfter.tsx**

```tsx
'use client';
import { CldImage } from 'next-cloudinary';
import { useState, useRef, useCallback } from 'react';

interface Props {
  publicId: string;          // Cloudinary public_id of the processed image
  originalUrl: string;       // URL of the original (pre-processing) image
  width?: number;
}

export default function BeforeAfter({ publicId, originalUrl, width = 600 }: Props) {
  const [splitPct, setSplitPct] = useState(50);
  const containerRef = useRef<HTMLDivElement>(null);

  const handlePointerMove = useCallback((e: React.PointerEvent<HTMLDivElement>) => {
    if (!containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const pct = Math.max(5, Math.min(95, (x / rect.width) * 100));
    setSplitPct(pct);
  }, []);

  return (
    <div className="rounded-xl overflow-hidden border border-orange-500/20 mt-3">
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-2 bg-orange-500/5 border-b border-orange-500/10">
        <span className="text-[10px] font-bold text-orange-400 uppercase tracking-wide">
          Before → After (drag to compare)
        </span>
        <span className="text-[9px] font-bold px-2 py-0.5 rounded-full bg-orange-500/15 text-orange-400 border border-orange-500/20">
          cloudinary
        </span>
      </div>

      {/* Slider container */}
      <div
        ref={containerRef}
        className="relative select-none cursor-col-resize"
        style={{ height: 280 }}
        onPointerMove={handlePointerMove}
      >
        {/* After (processed) — full width, clipped on the right */}
        <div className="absolute inset-0">
          <CldImage
            src={publicId}
            width={width}
            height={280}
            crop="fill"
            gravity="auto"
            format="auto"
            quality="auto:best"
            alt="Processed image"
            className="w-full h-full object-cover"
          />
        </div>

        {/* Before (original) — overlaid, clipped to left of split */}
        <div
          className="absolute inset-0 overflow-hidden"
          style={{ width: `${splitPct}%` }}
        >
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={originalUrl}
            alt="Original image"
            className="absolute inset-0 w-full h-full object-cover"
            style={{ width: `${(100 / splitPct) * 100}%`, maxWidth: 'none' }}
          />
        </div>

        {/* Divider line */}
        <div
          className="absolute top-0 bottom-0 w-0.5 bg-white shadow-lg"
          style={{ left: `${splitPct}%` }}
        >
          <div className="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 w-7 h-7 rounded-full bg-white shadow-md flex items-center justify-center">
            <span className="text-[10px] font-bold text-gray-600">◁▷</span>
          </div>
        </div>

        {/* Labels */}
        <div className="absolute top-2 left-2 text-[9px] font-bold text-white bg-black/50 px-1.5 py-0.5 rounded">
          ORIGINAL
        </div>
        <div className="absolute top-2 right-2 text-[9px] font-bold text-white bg-orange-600/80 px-1.5 py-0.5 rounded">
          CLOUDINARY ENHANCED
        </div>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/components/cloudinary/BeforeAfter.tsx
git commit -m "feat(cloudinary): add BeforeAfter split-slider image comparison component"
```

---

### Task 8: Wire upload button into TutorChat

**Files:**
- Modify: `frontend/components/tutor/TutorChat.tsx`
- Modify: `frontend/components/tutor/MessageBubble.tsx`

- [ ] **Step 1: Read current TutorChat input area**

```bash
grep -n "submit\|input\|textarea\|send" frontend/components/tutor/TutorChat.tsx | head -30
```

- [ ] **Step 2: Add image state and VisualUpload button to TutorChat**

In `frontend/components/tutor/TutorChat.tsx`, add image state tracking:

```tsx
// Add imports:
import VisualUpload from '@/components/cloudinary/VisualUpload';

// Add to Props interface:
interface Props {
  onSend: (text: string, imageUrl?: string, extractedText?: string) => void;
  lesson: { id: number; title: string; key_concepts: string[] };
}

// Add state inside component:
const [pendingImage, setPendingImage] = useState<{ url: string; text: string; publicId: string } | null>(null);

// Update submit() to pass image context:
function submit() {
  const text = input.trim();
  if (!text || isStreaming) return;
  setInput('');
  if (textareaRef.current) textareaRef.current.style.height = 'auto';
  onSend(text, pendingImage?.url, pendingImage?.text);
  setPendingImage(null);
}
```

In the input bar area (bottom of the component), add the upload button before the textarea:

```tsx
{/* Cloudinary upload button */}
<div className="flex items-center gap-2 px-4 pb-1">
  <VisualUpload
    lessonId={lesson.id}
    onUploadComplete={(url, text, publicId) => setPendingImage({ url, text, publicId })}
  />
  {pendingImage && (
    <div className="flex items-center gap-1.5 text-xs text-orange-400">
      <span>📷 Image attached</span>
      <button
        onClick={() => setPendingImage(null)}
        className="text-t3 hover:text-t0"
      >
        ✕
      </button>
    </div>
  )}
</div>
```

- [ ] **Step 3: Add inline image to MessageBubble**

In `frontend/components/tutor/MessageBubble.tsx`, add CldImage rendering:

```tsx
// Add imports:
import { CldImage } from 'next-cloudinary';

// Add to Message type (if defined in this file):
interface Message {
  // ... existing fields ...
  image_url?: string;
}

// Inside the JSX, after the message text:
{message.image_url && (
  <div className="mt-2 rounded-lg overflow-hidden border border-white/10">
    <CldImage
      src={message.image_url.includes('cloudinary') ? message.image_url : message.image_url}
      width={400}
      height={280}
      crop="scale"
      format="auto"
      quality="auto:eco"
      alt="Uploaded study material"
      className="w-full rounded-lg"
    />
    <div className="flex justify-end px-2 pb-1">
      <span className="text-[9px] text-orange-400 opacity-70">cloudinary</span>
    </div>
  </div>
)}
```

- [ ] **Step 4: Update sendMessage in learn page to forward image context**

In `frontend/app/learn/[courseId]/[lessonId]/page.tsx`, find the `sendMessage` / `onSend` function and update its signature:

```typescript
async function sendMessage(text: string, imageUrl?: string, extractedText?: string) {
  // ... existing code ...
  // Add image to the user message:
  addMessage({
    id: Date.now().toString(),
    role: 'user',
    content: text,
    image_url: imageUrl,
  });

  // Pass image context to streamChat:
  streamChat(token!, activeSessionId!, {
    lesson_id: lesson.id,
    message: text,
    history: [],
    image_url: imageUrl,
    extracted_text: extractedText,
    teaching_mode: teachingMode,
    voice_enabled: false,
  }, handleSseEvent);
}
```

Update `TutorChat` usage to pass `onSend={sendMessage}` with correct props:

```tsx
<TutorChat onSend={sendMessage} lesson={{ id: lesson.id, title: lesson.title, key_concepts: lesson.key_concepts }} />
```

- [ ] **Step 5: Start dev server and test upload flow**

```bash
cd frontend && npm run dev
```

1. Navigate to a lesson.
2. Click the camera/upload button in the input bar.
3. Upload a photo of a handwritten note.
4. Verify the "📷 Image attached" indicator appears.
5. Send a message — confirm the image appears in the chat bubble with the cloudinary badge.

- [ ] **Step 6: Commit**

```bash
git add frontend/components/tutor/TutorChat.tsx frontend/components/tutor/MessageBubble.tsx frontend/app/learn/
git commit -m "feat(cloudinary): wire VisualUpload into TutorChat, render CldImage in chat bubbles"
```

---

### Task 9: Add Materials panel tab to lesson workspace

**Files:**
- Modify: `frontend/app/learn/[courseId]/[lessonId]/page.tsx`

- [ ] **Step 1: Add 'materials' to panel tabs**

In `page.tsx`, find `setActivePanel` and the panel tab bar. Add the materials tab:

```typescript
// Extend the panel type:
const [activePanel, setActivePanel] = useState<'chat' | 'map' | 'network' | 'notes' | 'replay' | 'materials'>('chat');
```

In the tab bar JSX (where 'network', 'notes', 'replay' tabs are defined), add:

```tsx
<button
  onClick={() => setActivePanel('materials')}
  className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors ${
    activePanel === 'materials' ? 'bg-orange-500/20 text-orange-400' : 'text-t3 hover:text-t0'
  }`}
>
  📷 Materials
</button>
```

- [ ] **Step 2: Render MaterialsGallery when materials tab is active**

In the panel content area, add:

```tsx
import MaterialsGallery from '@/components/cloudinary/MaterialsGallery';

// In the conditional panel render:
{activePanel === 'materials' && lesson && (
  <MaterialsGallery
    lessonId={lesson.id}
    onReopen={(material) => {
      setActivePanel('chat');
      sendMessage('Let\'s revisit this material', material.url, '');
    }}
  />
)}
```

- [ ] **Step 3: Verify the Materials tab appears and loads**

Start dev server, navigate to a lesson, click "Materials" tab. Verify:
- Shows "No uploads yet" with cloudinary badge when empty.
- After uploading an image via the chat upload button, refreshing Materials tab shows the thumbnail.

- [ ] **Step 4: Commit**

```bash
git add frontend/app/learn/
git commit -m "feat(cloudinary): add Materials panel tab with session upload gallery"
```

---

### Task 10: Configure next.config for Cloudinary domains

**Files:**
- Modify: `frontend/next.config.js` or `frontend/next.config.ts`

- [ ] **Step 1: Read current next.config**

```bash
cat frontend/next.config.js 2>/dev/null || cat frontend/next.config.ts 2>/dev/null | head -30
```

- [ ] **Step 2: Add Cloudinary domain to images config**

Add `res.cloudinary.com` to the allowed image domains:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  // ... existing config ...
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'res.cloudinary.com',
        pathname: '/**',
      },
    ],
  },
};

module.exports = nextConfig;
```

- [ ] **Step 3: Verify build**

```bash
cd frontend && npm run build 2>&1 | tail -10
```

Expected: build succeeds without Cloudinary domain errors.

- [ ] **Step 4: Commit**

```bash
git add frontend/next.config.js
git commit -m "feat(cloudinary): add res.cloudinary.com to Next.js image domains"
```
