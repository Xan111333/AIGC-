from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from jose import jwt
from pydantic import BaseModel
from typing import Optional
import json
import hashlib
import io
import os
import requests
from dotenv import load_dotenv

load_dotenv()

ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY", "")
ZHIPU_TEXT_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
ZHIPU_IMAGE_API_URL = "https://open.bigmodel.cn/api/paas/v4/images/generations"

def has_zhipu():
    return bool(ZHIPU_API_KEY)

SECRET_KEY = "test-secret-key-for-development-only"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(title="AIGC 实训平台 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def simple_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_simple_hash(plain_password: str, hashed_password: str) -> bool:
    return simple_hash(plain_password) == hashed_password

users_db = {}

def init_default_users():
    users_db["admin"] = {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "hashed_password": simple_hash("admin123"),
        "role": "admin",
        "full_name": "Admin User",
        "is_active": True
    }
    users_db["teacher"] = {
        "id": 2,
        "username": "teacher",
        "email": "teacher@example.com",
        "hashed_password": simple_hash("teacher123"),
        "role": "teacher",
        "full_name": "Teacher User",
        "is_active": True
    }
    users_db["student"] = {
        "id": 3,
        "username": "student",
        "email": "student@example.com",
        "hashed_password": simple_hash("student123"),
        "role": "student",
        "full_name": "Student User",
        "is_active": True
    }
    users_db["student2"] = {
        "id": 4,
        "username": "student2",
        "email": "student2@example.com",
        "hashed_password": simple_hash("student123"),
        "role": "student",
        "full_name": "张三",
        "is_active": True
    }
    users_db["student3"] = {
        "id": 5,
        "username": "student3",
        "email": "student3@example.com",
        "hashed_password": simple_hash("student123"),
        "role": "student",
        "full_name": "李四",
        "is_active": True
    }

init_default_users()

user_id_counter = 6

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    full_name: Optional[str]
    is_active: Optional[bool]

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None

class TextGenerationRequest(BaseModel):
    prompt: str
    length: str = "medium"
    style: str = "neutral"
    tone: str = "neutral"
    language: str = "zh"

class GenerationRecordResponse(BaseModel):
    id: int
    type: str
    prompt: str
    params: Optional[str]
    result_url: Optional[str]
    status: str
    created_at: datetime
    completed_at: Optional[datetime]

MOCK_TEXT_RESPONSES = {
    "story": [
        "在一个遥远的星球上，住着一群善良的外星人。他们用音乐来交流，用星光来照明。有一天，一位年轻的外星人发现了一颗流星，里面藏着来自地球的信号...",
        "从前有一只会说话的小猫，它的梦想是成为一名画家。它每天都在练习，终于有一天，它的画感动了整个城市...",
        "深海里有一座神秘的城堡，里面住着美人鱼公主。她渴望看看外面的世界，于是开始了一段奇妙的旅程..."
    ],
    "poem": [
        "月光如水洒窗前，思绪万千夜难眠。遥望星河遥无际，梦里寻你到天边。春风拂面心微动，月色朦胧意阑珊。",
        "春风拂面柳丝摇，细雨绵绵润麦苗。鸟语花香人欲醉，江山如画分外娇。日出东方天地晓，霞飞云涌万里遥。"
    ],
    "article": [
        "人工智能正在改变我们的生活方式。从智能家居到自动驾驶，从医疗诊断到金融分析，AI的应用越来越广泛。本文将探讨AI如何重塑各个行业，以及未来的发展趋势。",
        "阅读是一种享受，它能开阔我们的视野，丰富我们的知识。在信息爆炸的时代，如何高效阅读、深度思考，成为现代人必备的技能。"
    ],
    "neutral": [
        "根据您的需求，我为您生成了以下内容。希望能够满足您的期望。如果需要调整，请告诉我具体的修改方向。",
        "这是根据您提供的提示生成的文本。您可以根据实际需求进行修改和完善。"
    ]
}

generation_records = []
record_id_counter = 1

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="无法验证凭证")
    except Exception:
        raise HTTPException(status_code=401, detail="无法验证凭证")
    
    user = users_db.get(username)
    if user is None:
        raise HTTPException(status_code=401, detail="用户不存在")
    return user

async def require_teacher(current_user = Depends(get_current_user)):
    if current_user["role"] not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="需要教师或管理员权限")
    return current_user

async def require_admin(current_user = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="需要管理员权限")
    return current_user

@app.get("/")
def root():
    return {"message": "AIGC 实训平台 API 服务已启动"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/auth/register", response_model=UserResponse)
def register(request: RegisterRequest):
    global user_id_counter
    
    if request.username in users_db:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    new_user = {
        "id": user_id_counter,
        "username": request.username,
        "email": request.email,
        "hashed_password": simple_hash(request.password),
        "role": "student",
        "full_name": request.full_name or request.username,
        "is_active": True
    }
    
    users_db[request.username] = new_user
    user_id_counter += 1
    
    return {k: v for k, v in new_user.items() if k != "hashed_password"}

@app.post("/api/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or not verify_simple_hash(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    if not user.get("is_active", True):
        raise HTTPException(status_code=403, detail="账户已被禁用")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"], "id": user["id"]},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/users/me", response_model=UserResponse)
def get_me(current_user = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "username": current_user["username"],
        "email": current_user["email"],
        "role": current_user["role"],
        "full_name": current_user["full_name"],
        "is_active": current_user.get("is_active", True)
    }

def generate_text_with_zhipu(prompt: str, style: str, tone: str, language: str) -> str:
    if not has_zhipu():
        return None

    style_map = {
        "story": "故事",
        "poem": "诗歌",
        "article": "文章",
        "neutral": "文本"
    }
    style_name = style_map.get(style.lower(), "文本")

    tone_map = {
        "formal": "正式",
        "casual": "轻松",
        "humorous": "幽默",
        "serious": "严肃",
        "neutral": "中性"
    }
    tone_name = tone_map.get(tone.lower(), "中性")

    lang_map = {
        "zh": "中文",
        "en": "英文",
        "mixed": "中英双语"
    }
    lang_name = lang_map.get(language.lower(), "中文")

    system_prompt = f"你是一位专业的AI助手，请根据用户要求生成内容。\n要求：\n- 内容类型：{style_name}\n- 语气：{tone_name}\n- 语言：{lang_name}\n请直接输出内容，不要加前后缀。"

    try:
        response = requests.post(
            ZHIPU_TEXT_API_URL,
            headers={
                "Authorization": f"Bearer {ZHIPU_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "glm-4",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.8,
                "max_tokens": 2000
            },
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            print(f"智谱文本 API 错误: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"智谱文本 API 异常: {e}")
        return None

@app.post("/api/text/generate", response_model=GenerationRecordResponse)
def generate_text(request: TextGenerationRequest, current_user = Depends(get_current_user)):
    global record_id_counter
    
    if not request.prompt or len(request.prompt.strip()) == 0:
        raise HTTPException(status_code=400, detail="提示词不能为空")
    
    params = json.dumps({
        "length": request.length,
        "style": request.style,
        "tone": request.tone,
        "language": request.language
    })
    
    result = generate_text_with_zhipu(
        request.prompt, request.style, request.tone, request.language)
    
    if result is None:
        category = request.style.lower()
        if category not in MOCK_TEXT_RESPONSES:
            category = "neutral"
        import random
        result = random.choice(MOCK_TEXT_RESPONSES[category])
    
    record = {
        "id": record_id_counter,
        "type": "text",
        "prompt": request.prompt,
        "params": params,
        "result_url": result,
        "status": "completed",
        "created_at": datetime.utcnow(),
        "completed_at": datetime.utcnow(),
        "user_id": current_user["id"]
    }
    
    generation_records.append(record)
    record_id_counter += 1
    
    return record

@app.get("/api/text/history", response_model=list[GenerationRecordResponse])
def get_text_history(skip: int = 0, limit: int = 50, current_user = Depends(get_current_user)):
    text_records = [r for r in generation_records if r["type"] == "text"]
    return text_records[skip:skip+limit]

def generate_image_with_zhipu(prompt: str, resolution: str, style: str, num_images: int) -> str:
    if not has_zhipu():
        print("智谱 AI API Key 未配置")
        return None
    
    style_map = {
        "realistic": "写实",
        "cartoon": "卡通",
        "oil-painting": "油画",
        "watercolor": "水彩",
        "anime": "动漫",
        "sci-fi": "科幻",
        "pixel": "像素风",
        "cyberpunk": "赛博朋克",
        "vintage": "复古"
    }
    style_name = style_map.get(style.lower(), "写实")
    
    headers = {
        "Authorization": f"Bearer {ZHIPU_API_KEY}",
        "Content-Type": "application/json"
    }

    full_prompt = f"{prompt}，{style_name}风格"

    data = {
        "model": "cogview-4",
        "prompt": full_prompt,
        "size": resolution
    }

    print(f"调用智谱 CogView-4 图像生成...")
    print(f"提示词: {full_prompt}")
    print(f"分辨率: {resolution}")

    try:
        response = requests.post(ZHIPU_IMAGE_API_URL, headers=headers, json=data, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            print(f"API 响应: {str(result)[:300]}")
            
            if "error" in result:
                print(f"API 返回错误: {result['error']}")
                return None
            
            if "data" in result and len(result["data"]) > 0:
                img_url = result["data"][0].get("url")
                if img_url:
                    print(f"获取到图片 URL: {img_url[:50]}...")
                    return img_url
                img_b64 = result["data"][0].get("b64_json")
                if img_b64:
                    print(f"获取到 base64 图片")
                    return img_b64
            return None
        else:
            print(f"智谱 API 错误: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"智谱 API 异常: {e}")
        return None

class ImageGenerationRequest(BaseModel):
    prompt: str
    resolution: str = "1024x1024"
    style: str = "realistic"
    num_images: int = 1

@app.post("/api/image/generate", response_model=GenerationRecordResponse)
def generate_image(request: ImageGenerationRequest, current_user = Depends(get_current_user)):
    global record_id_counter
    
    if not request.prompt or len(request.prompt.strip()) == 0:
        raise HTTPException(status_code=400, detail="提示词不能为空")
    
    params = json.dumps({
        "resolution": request.resolution,
        "style": request.style,
        "num_images": request.num_images
    })
    
    result = generate_image_with_zhipu(
        request.prompt, request.resolution, request.style, request.num_images)
    
    if result:
        if result.startswith("http"):
            result_url = result
        else:
            result_url = f"data:image/png;base64,{result}"
    else:
        result_url = f"https://picsum.photos/seed/{record_id_counter}/512/512"
    
    record = {
        "id": record_id_counter,
        "type": "image",
        "prompt": request.prompt,
        "params": params,
        "result_url": result_url,
        "status": "completed",
        "created_at": datetime.utcnow(),
        "completed_at": datetime.utcnow(),
        "user_id": current_user["id"]
    }
    
    generation_records.append(record)
    record_id_counter += 1
    
    return record

@app.get("/api/image/history", response_model=list[GenerationRecordResponse])
def get_image_history(skip: int = 0, limit: int = 50, current_user = Depends(get_current_user)):
    image_records = [r for r in generation_records if r["type"] == "image"]
    return image_records[skip:skip+limit]

class VideoGenerationRequest(BaseModel):
    prompt: str
    duration: int = 5
    resolution: str = "720p"
    style: str = "realistic"

@app.post("/api/video/generate", response_model=GenerationRecordResponse)
def generate_video(request: VideoGenerationRequest, current_user = Depends(get_current_user)):
    global record_id_counter
    
    if not request.prompt or len(request.prompt.strip()) == 0:
        raise HTTPException(status_code=400, detail="提示词不能为空")
    
    params = json.dumps({
        "duration": request.duration,
        "resolution": request.resolution,
        "style": request.style
    })
    
    mock_video_url = f"https://picsum.photos/seed/video{record_id_counter}/640/360"
    
    record = {
        "id": record_id_counter,
        "type": "video",
        "prompt": request.prompt,
        "params": params,
        "result_url": mock_video_url,
        "status": "completed",
        "created_at": datetime.utcnow(),
        "completed_at": datetime.utcnow(),
        "user_id": current_user["id"]
    }
    
    generation_records.append(record)
    record_id_counter += 1
    
    return record

@app.get("/api/video/history", response_model=list[GenerationRecordResponse])
def get_video_history(skip: int = 0, limit: int = 50, current_user = Depends(get_current_user)):
    video_records = [r for r in generation_records if r["type"] == "video"]
    return video_records[skip:skip+limit]

class AudioGenerationRequest(BaseModel):
    text: str
    voice: str = "female"
    speed: str = "medium"
    tone: str = "neutral"

@app.post("/api/audio/generate", response_model=GenerationRecordResponse)
def generate_audio(request: AudioGenerationRequest, current_user = Depends(get_current_user)):
    global record_id_counter
    
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="文本内容不能为空")
    
    params = json.dumps({
        "voice": request.voice,
        "speed": request.speed,
        "tone": request.tone
    })
    
    mock_audio_url = f"https://picsum.photos/seed/audio{record_id_counter}/100/50"
    
    record = {
        "id": record_id_counter,
        "type": "audio",
        "prompt": request.text,
        "params": params,
        "result_url": mock_audio_url,
        "status": "completed",
        "created_at": datetime.utcnow(),
        "completed_at": datetime.utcnow(),
        "user_id": current_user["id"]
    }
    
    generation_records.append(record)
    record_id_counter += 1
    
    return record

@app.get("/api/audio/history", response_model=list[GenerationRecordResponse])
def get_audio_history(skip: int = 0, limit: int = 50, current_user = Depends(get_current_user)):
    audio_records = [r for r in generation_records if r["type"] == "audio"]
    return audio_records[skip:skip+limit]

tasks = []
submissions = []
task_id_counter = 1
submission_id_counter = 1

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    type: str
    requirements: str | None = None
    deadline: str | None = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    type: str
    requirements: str | None
    deadline: str | None
    teacher_id: int
    teacher_name: str
    created_at: datetime
    is_active: bool

class SubmissionCreate(BaseModel):
    task_id: int
    file_path: str | None = None
    generated_content: str | None = None

class SubmissionUpdate(BaseModel):
    score: float | None = None
    comment: str | None = None

class SubmissionResponse(BaseModel):
    id: int
    task_id: int
    task_title: str
    student_id: int
    student_name: str
    file_path: str | None
    generated_content: str | None
    status: str
    score: float | None
    comment: str | None
    submitted_at: datetime
    graded_at: datetime | None

@app.post("/api/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, current_user = Depends(require_teacher)):
    global task_id_counter
    
    new_task = {
        "id": task_id_counter,
        "title": task.title,
        "description": task.description,
        "type": task.type,
        "requirements": task.requirements,
        "deadline": task.deadline,
        "teacher_id": current_user["id"],
        "teacher_name": current_user["full_name"] or current_user["username"],
        "created_at": datetime.utcnow(),
        "is_active": True
    }
    
    tasks.append(new_task)
    task_id_counter += 1
    
    return new_task

@app.get("/api/tasks", response_model=list[TaskResponse])
def list_tasks(skip: int = 0, limit: int = 100, current_user = Depends(get_current_user)):
    filtered_tasks = [t for t in tasks if t["is_active"]]
    
    if current_user["role"] in ["teacher", "admin"]:
        filtered_tasks = [t for t in filtered_tasks if t["teacher_id"] == current_user["id"]]
    
    return filtered_tasks[skip:skip+limit]

@app.get("/api/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, current_user = Depends(get_current_user)):
    task = next((t for t in tasks if t["id"] == task_id and t["is_active"]), None)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task

@app.put("/api/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskCreate, current_user = Depends(require_teacher)):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    if task["teacher_id"] != current_user["id"] and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="只能修改自己创建的任务")
    
    if task_update.title:
        task["title"] = task_update.title
    if task_update.description is not None:
        task["description"] = task_update.description
    if task_update.type:
        task["type"] = task_update.type
    if task_update.requirements is not None:
        task["requirements"] = task_update.requirements
    if task_update.deadline:
        task["deadline"] = task_update.deadline
    
    return task

@app.delete("/api/tasks/{task_id}", response_model=TaskResponse)
def delete_task(task_id: int, current_user = Depends(require_teacher)):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    if task["teacher_id"] != current_user["id"] and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="只能删除自己创建的任务")
    
    task["is_active"] = False
    return task

@app.post("/api/submissions", response_model=SubmissionResponse, status_code=201)
def create_submission(submission: SubmissionCreate, current_user = Depends(get_current_user)):
    global submission_id_counter
    
    if current_user["role"] in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="学生才能提交作业")
    
    task = next((t for t in tasks if t["id"] == submission.task_id and t["is_active"]), None)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    existing_submission = next((s for s in submissions if s["task_id"] == submission.task_id and s["student_id"] == current_user["id"]), None)
    if existing_submission:
        raise HTTPException(status_code=400, detail="已提交过该作业")
    
    new_submission = {
        "id": submission_id_counter,
        "task_id": submission.task_id,
        "task_title": task["title"],
        "student_id": current_user["id"],
        "student_name": current_user["full_name"] or current_user["username"],
        "file_path": submission.file_path,
        "generated_content": submission.generated_content,
        "status": "pending",
        "score": None,
        "comment": None,
        "submitted_at": datetime.utcnow(),
        "graded_at": None
    }
    
    submissions.append(new_submission)
    submission_id_counter += 1
    
    return new_submission

@app.get("/api/submissions/my", response_model=list[SubmissionResponse])
def get_my_submissions(skip: int = 0, limit: int = 100, current_user = Depends(get_current_user)):
    if current_user["role"] not in ["student"]:
        raise HTTPException(status_code=403, detail="学生才能查看自己的作业")
    
    student_submissions = [s for s in submissions if s["student_id"] == current_user["id"]]
    return student_submissions[skip:skip+limit]

@app.get("/api/tasks/{task_id}/submissions", response_model=list[SubmissionResponse])
def get_task_submissions(task_id: int, skip: int = 0, limit: int = 100, current_user = Depends(require_teacher)):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    if task["teacher_id"] != current_user["id"] and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="只能查看自己任务的提交")
    
    task_submissions = [s for s in submissions if s["task_id"] == task_id]
    return task_submissions[skip:skip+limit]

@app.post("/api/submissions/{submission_id}/grade", response_model=SubmissionResponse)
def grade_submission(submission_id: int, update: SubmissionUpdate, current_user = Depends(require_teacher)):
    submission = next((s for s in submissions if s["id"] == submission_id), None)
    if not submission:
        raise HTTPException(status_code=404, detail="作业不存在")
    
    task = next((t for t in tasks if t["id"] == submission["task_id"]), None)
    if task and task["teacher_id"] != current_user["id"] and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="只能批改自己任务的作业")
    
    if update.score is not None:
        submission["score"] = update.score
    if update.comment is not None:
        submission["comment"] = update.comment
    
    if update.score is not None:
        submission["status"] = "completed"
        submission["graded_at"] = datetime.utcnow()
    
    return submission

@app.put("/api/submissions/{submission_id}/grade", response_model=SubmissionResponse)
def update_grade(submission_id: int, update: SubmissionUpdate, current_user = Depends(require_teacher)):
    return grade_submission(submission_id, update, current_user)

class ExportTextRequest(BaseModel):
    text: str
    title: str = "Generated Content"

class ExportImagesRequest(BaseModel):
    urls: list[str]

def generate_filename(prefix: str, ext: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{ext}"

def mock_pdf_content(title: str, text: str) -> bytes:
    pdf_content = f"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj
4 0 obj
<< /Length 44 >>
stream
BT
/F1 12 Tf
100 700 Td
({title}) Tj
ET
endstream
endobj
5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 6
0000000000 65535 f 
0000000010 00000 n 
0000000060 00000 n 
0000000115 00000 n 
0000000210 00000 n 
0000000280 00000 n 
trailer
<< /Size 6 /Root 1 0 R >>
startxref
340
%%EOF
"""
    return pdf_content.encode('utf-8')

@app.post("/api/export/text-to-pdf")
def export_text_to_pdf(
    request: ExportTextRequest,
    current_user = Depends(get_current_user)
):
    from fastapi.responses import Response
    
    pdf_content = mock_pdf_content(request.title, request.text)
    filename = generate_filename("text", "pdf")
    
    return Response(
        content=pdf_content,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.post("/api/export/text-to-word")
def export_text_to_word(
    request: ExportTextRequest,
    current_user = Depends(get_current_user)
):
    from fastapi.responses import Response
    
    doc_content = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:body>
<w:p><w:r><w:t>{request.title}</w:t></w:r></w:p>
<w:p><w:r><w:t>{request.text}</w:t></w:r></w:p>
</w:body>
</w:document>"""
    
    filename = generate_filename("text", "docx")
    
    return Response(
        content=doc_content.encode('utf-8'),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.post("/api/export/images-to-zip")
def export_images_to_zip(
    request: ExportImagesRequest,
    current_user = Depends(get_current_user)
):
    from fastapi.responses import Response
    import zipfile
    
    if not request.urls or len(request.urls) == 0:
        raise HTTPException(status_code=400, detail="请提供图片URL")
    
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zf:
        for i, url in enumerate(request.urls):
            zf.writestr(f"image_{i+1}.txt", f"Image URL: {url}")
    
    buffer.seek(0)
    zip_content = buffer.read()
    
    filename = generate_filename("images", "zip")
    
    return Response(
        content=zip_content,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

resources = []
resource_id_counter = 1

resource_categories = [
    {"id": "tutorial", "name": "教程"},
    {"id": "case", "name": "案例"},
    {"id": "document", "name": "文档"},
    {"id": "video", "name": "视频"}
]

class ResourceCreate(BaseModel):
    title: str
    description: str | None = None
    category: str = "document"
    file_url: str | None = None
    cover_url: str | None = None

class ResourceResponse(BaseModel):
    id: int
    title: str
    description: str | None
    category: str
    category_name: str
    file_url: str | None
    cover_url: str | None
    uploader_id: int
    uploader_name: str
    view_count: int
    created_at: datetime

@app.post("/api/resources", response_model=ResourceResponse, status_code=201)
def create_resource(
    resource: ResourceCreate,
    current_user = Depends(require_teacher)
):
    global resource_id_counter
    
    category_name = next((c["name"] for c in resource_categories if c["id"] == resource.category), resource.category)
    
    new_resource = {
        "id": resource_id_counter,
        "title": resource.title,
        "description": resource.description,
        "category": resource.category,
        "category_name": category_name,
        "file_url": resource.file_url,
        "cover_url": resource.cover_url or f"https://picsum.photos/seed/resource{resource_id_counter}/400/300",
        "uploader_id": current_user["id"],
        "uploader_name": current_user["full_name"] or current_user["username"],
        "view_count": 0,
        "created_at": datetime.utcnow()
    }
    
    resources.append(new_resource)
    resource_id_counter += 1
    
    return new_resource

@app.get("/api/resources", response_model=list[ResourceResponse])
def list_resources(
    category: str | None = None,
    skip: int = 0,
    limit: int = 50,
    current_user = Depends(get_current_user)
):
    filtered = resources
    
    if category:
        filtered = [r for r in filtered if r["category"] == category]
    
    return filtered[skip:skip+limit]

@app.get("/api/resources/{resource_id}", response_model=ResourceResponse)
def get_resource(
    resource_id: int,
    current_user = Depends(get_current_user)
):
    resource = next((r for r in resources if r["id"] == resource_id), None)
    if not resource:
        raise HTTPException(status_code=404, detail="资源不存在")
    
    resource["view_count"] += 1
    
    return resource

@app.delete("/api/resources/{resource_id}", response_model=ResourceResponse)
def delete_resource(
    resource_id: int,
    current_user = Depends(require_teacher)
):
    resource = next((r for r in resources if r["id"] == resource_id), None)
    if not resource:
        raise HTTPException(status_code=404, detail="资源不存在")
    
    resources.remove(resource)
    return resource

@app.get("/api/resources/categories")
def get_resource_categories(current_user = Depends(get_current_user)):
    return resource_categories

creation_logs = []
log_id_counter = 1

class CreationLogCreate(BaseModel):
    module: str
    content: str | None = None

class CreationLogResponse(BaseModel):
    id: int
    user_id: int
    user_name: str
    module: str
    content: str | None
    created_at: datetime

@app.post("/api/creation-logs", response_model=CreationLogResponse, status_code=201)
def create_creation_log(
    log: CreationLogCreate,
    current_user = Depends(get_current_user)
):
    global log_id_counter
    
    new_log = {
        "id": log_id_counter,
        "user_id": current_user["id"],
        "user_name": current_user["full_name"] or current_user["username"],
        "module": log.module,
        "content": log.content,
        "created_at": datetime.utcnow()
    }
    
    creation_logs.insert(0, new_log)
    log_id_counter += 1
    
    return new_log

@app.get("/api/creation-logs", response_model=list[CreationLogResponse])
def list_creation_logs(
    skip: int = 0,
    limit: int = 50,
    current_user = Depends(get_current_user)
):
    return creation_logs[skip:skip+limit]

@app.get("/api/statistics/overview")
def get_statistics_overview(current_user = Depends(require_teacher)):
    students = [u for u in users_db.values() if u.get("role") == "student"]
    total_students = len(students)
    total_tasks_count = len(tasks)
    total_submissions_count = len(submissions)
    
    submission_rate = (total_submissions_count / (total_students * max(total_tasks_count, 1)) * 100) if total_students > 0 else 0
    
    graded_submissions = [s for s in submissions if s.get("score") is not None]
    average_score = sum(s.get("score", 0) for s in graded_submissions) / len(graded_submissions) if graded_submissions else 0
    
    recent_submissions = sorted(submissions, key=lambda x: x.get("submitted_at", datetime.min), reverse=True)[:10]
    
    return {
        "total_students": total_students,
        "total_tasks": total_tasks_count,
        "total_submissions": total_submissions_count,
        "submission_rate": round(submission_rate, 2),
        "average_score": round(average_score, 2),
        "pending_grades": len([s for s in submissions if s.get("score") is None]),
        "recent_submissions": recent_submissions
    }

@app.get("/api/statistics/grade-distribution")
def get_grade_distribution(
    period: str = "all",
    current_user = Depends(require_teacher)
):
    graded = [s for s in submissions if s.get("score") is not None]
    
    distribution = {
        "0-59": 0,
        "60-69": 0,
        "70-79": 0,
        "80-89": 0,
        "90-100": 0
    }
    
    for s in graded:
        grade = s.get("score", 0)
        if grade < 60:
            distribution["0-59"] += 1
        elif grade < 70:
            distribution["60-69"] += 1
        elif grade < 80:
            distribution["70-79"] += 1
        elif grade < 90:
            distribution["80-89"] += 1
        else:
            distribution["90-100"] += 1
    
    return distribution

@app.get("/api/statistics/task-completion")
def get_task_completion(current_user = Depends(require_teacher)):
    students = [u for u in users_db.values() if u.get("role") == "student"]
    total_students = len(students)
    
    completion_data = []
    for task in tasks:
        task_id = task["id"]
        submitted_count = len([s for s in submissions if s.get("task_id") == task_id])
        completion_rate = (submitted_count / total_students * 100) if total_students > 0 else 0
        
        completion_data.append({
            "task_id": task_id,
            "title": task["title"],
            "total_students": total_students,
            "submitted_count": submitted_count,
            "completion_rate": round(completion_rate, 2)
        })
    
    return completion_data

@app.get("/api/statistics/module-usage")
def get_module_usage(
    period: str = "week",
    current_user = Depends(require_teacher)
):
    now = datetime.utcnow()
    if period == "week":
        start_date = now - timedelta(days=7)
    elif period == "month":
        start_date = now - timedelta(days=30)
    else:
        start_date = now - timedelta(days=90)
    
    recent_logs = [log for log in creation_logs if log.get("created_at", datetime.min) >= start_date]
    
    usage = {
        "text": 0,
        "image": 0,
        "video": 0,
        "audio": 0
    }
    
    for log in recent_logs:
        module = log.get("module", "").lower()
        if module in usage:
            usage[module] += 1
    
    return usage

@app.get("/api/statistics/student-progress/{student_id}")
def get_student_progress(
    student_id: int,
    current_user = Depends(require_teacher)
):
    student = next((u for u in users_db.values() if u.get("id") == student_id and u.get("role") == "student"), None)
    if not student:
        raise HTTPException(status_code=404, detail="学生不存在")
    
    student_submissions = [s for s in submissions if s.get("student_id") == student_id]
    completed_tasks = len(set(s.get("task_id") for s in student_submissions))
    total_tasks_count = len(tasks)
    
    graded_submissions = [s for s in student_submissions if s.get("score") is not None]
    average_score = sum(s.get("score", 0) for s in graded_submissions) / len(graded_submissions) if graded_submissions else 0
    
    module_usage = {"text": 0, "image": 0, "video": 0, "audio": 0}
    student_logs = [log for log in creation_logs if log.get("user_id") == student_id]
    for log in student_logs:
        module = log.get("module", "").lower()
        if module in module_usage:
            module_usage[module] += 1
    
    return {
        "student_id": student_id,
        "student_name": student.get("full_name", student.get("username")),
        "completed_tasks": completed_tasks,
        "total_tasks": total_tasks_count,
        "completion_rate": round((completed_tasks / total_tasks_count * 100), 2) if total_tasks_count > 0 else 0,
        "average_score": round(average_score, 2),
        "total_submissions": len(student_submissions),
        "module_usage": module_usage
    }

@app.get("/api/statistics/export-report")
def export_report(current_user = Depends(require_teacher)):
    try:
        from fastapi.responses import Response
        
        xlsx_content = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<sheetData>
<row>
<cell><v>学号</v></cell>
<cell><v>姓名</v></cell>
<cell><v>任务</v></cell>
<cell><v>成绩</v></cell>
<cell><v>评语</v></cell>
</row>
"""
        
        for submission in submissions:
            student = next((u for u in users_db.values() if u.get("id") == submission.get("student_id")), None)
            task = next((t for t in tasks if t.get("id") == submission.get("task_id")), None)
            
            if student and task:
                xlsx_content += f"""<row>
<cell><v>{student.get('id', '')}</v></cell>
<cell><v>{student.get('full_name', student.get('username', ''))}</v></cell>
<cell><v>{task.get('title', '')}</v></cell>
<cell><v>{submission.get('score', '未评分')}</v></cell>
<cell><v>{submission.get('comment', '')}</v></cell>
</row>
"""
        
        xlsx_content += """</sheetData>
</worksheet>"""
        
        return Response(
            content=xlsx_content.encode('utf-8'),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=grade_report.xlsx"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")

def get_system_config_dict():
    return {
        "api_key_status": {
            "zhipu": has_zhipu()
        },
        "rate_limit": {
            "text_per_hour": 100,
            "image_per_hour": 50,
            "video_per_hour": 20,
            "audio_per_hour": 20
        },
        "file_limit": {
            "max_file_size_mb": 10,
            "allowed_extensions": [".txt", ".pdf", ".docx", ".png", ".jpg", ".mp4", ".mp3"]
        }
    }

system_config = get_system_config_dict()

operation_logs = []
admin_log_id_counter = 1

pending_contents = []
content_id_counter = 1

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "student"
    full_name: Optional[str] = None

class UserUpdate(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

class ContentReview(BaseModel):
    approved: bool
    reason: Optional[str] = None

class ConfigUpdate(BaseModel):
    rate_limit: Optional[dict] = None
    file_limit: Optional[dict] = None

@app.get("/api/admin/users")
def list_users(
    skip: int = 0,
    limit: int = 20,
    role: Optional[str] = None,
    search: Optional[str] = None,
    current_user = Depends(require_admin)
):
    all_users = [v for v in users_db.values()]
    
    if role:
        all_users = [u for u in all_users if u.get("role") == role]
    
    if search:
        search_lower = search.lower()
        all_users = [u for u in all_users if search_lower in u.get("username", "").lower() or search_lower in u.get("full_name", "").lower()]
    
    result = []
    for u in all_users[skip:skip+limit]:
        result.append({k: v for k, v in u.items() if k != "hashed_password"})
    
    return result

@app.post("/api/admin/users", status_code=201)
def create_user(
    user_data: UserCreate,
    current_user = Depends(require_admin)
):
    global user_id_counter
    
    if user_data.username in users_db:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    new_user = {
        "id": user_id_counter,
        "username": user_data.username,
        "email": user_data.email,
        "hashed_password": simple_hash(user_data.password),
        "role": user_data.role,
        "full_name": user_data.full_name or user_data.username,
        "is_active": True,
        "created_at": datetime.utcnow()
    }
    
    users_db[user_data.username] = new_user
    user_id_counter += 1
    
    return {k: v for k, v in new_user.items() if k != "hashed_password"}

@app.put("/api/admin/users/{user_id}")
def update_user(
    user_id: int,
    update: UserUpdate,
    current_user = Depends(require_admin)
):
    user = next((u for u in users_db.values() if u.get("id") == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    if update.email is not None:
        user["email"] = update.email
    if update.role is not None:
        user["role"] = update.role
    if update.full_name is not None:
        user["full_name"] = update.full_name
    if update.is_active is not None:
        user["is_active"] = update.is_active
    
    return {k: v for k, v in user.items() if k != "hashed_password"}

@app.delete("/api/admin/users/{user_id}")
def delete_user(
    user_id: int,
    current_user = Depends(require_admin)
):
    user = next((u for u in users_db.values() if u.get("id") == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    user["is_active"] = False
    return {"message": "用户已禁用"}

@app.post("/api/admin/users/{user_id}/reset-password")
def reset_password(
    user_id: int,
    current_user = Depends(require_admin)
):
    user = next((u for u in users_db.values() if u.get("id") == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    new_password = "password123"
    user["hashed_password"] = simple_hash(new_password)
    
    return {"message": "密码已重置为: password123"}

@app.get("/api/admin/system/config")
def get_system_config(current_user = Depends(require_admin)):
    current_config = get_system_config_dict()
    current_config["rate_limit"] = system_config["rate_limit"]
    current_config["file_limit"] = system_config["file_limit"]
    return current_config

@app.put("/api/admin/system/config")
def update_system_config(
    config: ConfigUpdate,
    current_user = Depends(require_admin)
):
    global system_config
    
    if config.rate_limit is not None:
        system_config["rate_limit"].update(config.rate_limit)
    if config.file_limit is not None:
        system_config["file_limit"].update(config.file_limit)
    
    return system_config

@app.get("/api/admin/logs")
def list_logs(
    skip: int = 0,
    limit: int = 50,
    user_id: Optional[int] = None,
    current_user = Depends(require_admin)
):
    filtered = operation_logs
    
    if user_id:
        filtered = [log for log in filtered if log.get("user_id") == user_id]
    
    return filtered[skip:skip+limit]

@app.get("/api/admin/contents/pending")
def list_pending_contents(
    skip: int = 0,
    limit: int = 20,
    current_user = Depends(require_admin)
):
    pending = [c for c in pending_contents if c.get("status") == "pending"]
    return pending[skip:skip+limit]

@app.post("/api/admin/contents/{content_id}/review")
def review_content(
    content_id: int,
    review: ContentReview,
    current_user = Depends(require_admin)
):
    content = next((c for c in pending_contents if c.get("id") == content_id), None)
    if not content:
        raise HTTPException(status_code=404, detail="内容不存在")
    
    content["status"] = "approved" if review.approved else "rejected"
    content["review_reason"] = review.reason
    content["reviewed_at"] = datetime.utcnow()
    content["reviewed_by"] = current_user.get("username")
    
    return content

@app.post("/api/admin/contents")
def submit_for_review(
    type: str,
    content: str,
    current_user = Depends(get_current_user)
):
    global content_id_counter
    
    new_content = {
        "id": content_id_counter,
        "type": type,
        "content": content,
        "user_id": current_user.get("id"),
        "status": "pending",
        "created_at": datetime.utcnow()
    }
    
    pending_contents.append(new_content)
    content_id_counter += 1
    
    return new_content

@app.get("/api/admin/statistics")
def admin_statistics(current_user = Depends(require_admin)):
    all_users = list(users_db.values())
    return {
        "total_users": len(all_users),
        "total_students": len([u for u in all_users if u.get("role") == "student"]),
        "total_teachers": len([u for u in all_users if u.get("role") == "teacher"]),
        "total_admins": len([u for u in all_users if u.get("role") == "admin"]),
        "pending_contents": len([c for c in pending_contents if c.get("status") == "pending"]),
        "active_users": len([u for u in all_users if u.get("is_active", True)]),
        "total_tasks": len(tasks),
        "total_submissions": len(submissions)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_simple:app", host="0.0.0.0", port=8000, reload=True)
