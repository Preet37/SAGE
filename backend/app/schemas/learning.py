from typing import Optional, List
from pydantic import BaseModel


class LessonImageMeta(BaseModel):
    file: str
    topic: str
    source_page: str = ""
    caption: str = ""
    when_to_show: str = ""
    concepts: List[str] = []
    description: str = ""


class LessonResponse(BaseModel):
    id: str
    title: str
    slug: str
    content: str
    summary: str
    concepts: List[str]
    order_index: int
    youtube_id: Optional[str]
    video_title: Optional[str]
    vimeo_url: Optional[str]
    module_id: str
    image_metadata: List[LessonImageMeta] = []
    sources_used: List[str] = []
    reference_kb: Optional[str] = None


class ModuleResponse(BaseModel):
    id: str
    title: str
    order_index: int
    lessons: List[LessonResponse]


class LearningPathResponse(BaseModel):
    id: str
    slug: str
    title: str
    description: str
    level: str
    visibility: str = "public"
    is_mine: bool = False
    modules: List[ModuleResponse]


class LearningPathSummary(BaseModel):
    id: str
    slug: str
    title: str
    description: str
    level: str
    visibility: str = "public"
    is_mine: bool = False


class ShareEntry(BaseModel):
    user_id: str
    email: str
    username: str
