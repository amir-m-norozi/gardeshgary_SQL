from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base, Category, Place, Image, Video  # وارد کردن مدل‌ها
from database import engine  # فایل database برای تنظیمات دیتابیس
from pydantic import BaseModel
from typing import List

# ایجاد اپلیکیشن FastAPI
app = FastAPI()

# تنظیمات دیتابیس (اتصال به دیتابیس PostgreSQL)
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:opsg8113@localhost/postgres"  # باید اینجا اطلاعات دیتابیس خود را وارد کنید

# ایجاد موتور دیتابیس
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# ساخت Session برای ارتباط با دیتابیس
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# تابع برای گرفتن session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# مدل‌های Pydantic برای تایید داده‌ها
class CategoryCreate(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True

class PlaceCreate(BaseModel):
    name: str
    location: str

    class Config:
        orm_mode = True

class ImageCreate(BaseModel):
    filename: str
    url: str

    class Config:
        orm_mode = True

class VideoCreate(BaseModel):
    filename: str
    url: str

    class Config:
        orm_mode = True

# API‌ها برای Category
@app.post("/categories", response_model=CategoryCreate)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = Category(name=category.name, description=category.description)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.get("/categories", response_model=List[CategoryCreate])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories

@app.get("/categories/{category_id}", response_model=CategoryCreate)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@app.put("/categories/{category_id}", response_model=CategoryCreate)
def update_category(category_id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db_category.name = category.name
    db_category.description = category.description
    db.commit()
    db.refresh(db_category)
    return db_category

@app.delete("/categories/{category_id}", response_model=CategoryCreate)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return db_category

# API‌ها برای Place
@app.post("/places", response_model=PlaceCreate)
def create_place(place: PlaceCreate, db: Session = Depends(get_db)):
    db_place = Place(name=place.name, location=place.location)
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place

@app.get("/places", response_model=List[PlaceCreate])
def get_places(db: Session = Depends(get_db)):
    places = db.query(Place).all()
    return places

@app.get("/places{place_id}", response_model=PlaceCreate)
def get_place(place_id: int, db: Session = Depends(get_db)):
    place = db.query(Place).filter(Place.id == place_id).first()
    if place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    return place

@app.put("/places{place_id}", response_model=PlaceCreate)
def update_place(place_id: int, place: PlaceCreate, db: Session = Depends(get_db)):
    db_place = db.query(Place).filter(Place.id == place_id).first()
    if db_place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    db_place.name = place.name
    db_place.location = place.location
    db.commit()
    db.refresh(db_place)
    return db_place

@app.delete("/places{place_id}", response_model=PlaceCreate)
def delete_place(place_id: int, db: Session = Depends(get_db)):
    db_place = db.query(Place).filter(Place.id == place_id).first()
    if db_place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    db.delete(db_place)
    db.commit()
    return db_place

# API‌ها برای Image
@app.post("/images", response_model=ImageCreate)
def create_image(image: ImageCreate, db: Session = Depends(get_db)):
    db_image = Image(filename=image.filename, url=image.url)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

@app.get("/images", response_model=List[ImageCreate])
def get_images(db: Session = Depends(get_db)):
    images = db.query(Image).all()
    return images

@app.get("/images{image_id}", response_model=ImageCreate)
def get_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(Image).filter(Image.id == image_id).first()
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return image

@app.put("/images{image_id}", response_model=ImageCreate)
def update_image(image_id: int, image: ImageCreate, db: Session = Depends(get_db)):
    db_image = db.query(Image).filter(Image.id == image_id).first()
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    db_image.filename = image.filename
    db_image.url = image.url
    db.commit()
    db.refresh(db_image)
    return db_image

@app.delete("/images{image_id}", response_model=ImageCreate)
def delete_image(image_id: int, db: Session = Depends(get_db)):
    db_image = db.query(Image).filter(Image.id == image_id).first()
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    db.delete(db_image)
    db.commit()
    return db_image

# API‌ها برای Video
@app.post("/videos", response_model=VideoCreate)
def create_video(video: VideoCreate, db: Session = Depends(get_db)):
    db_video = Video(filename=video.filename, url=video.url)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video

@app.get("/videos", response_model=List[VideoCreate])
def get_videos(db: Session = Depends(get_db)):
    videos = db.query(Video).all()
    return videos

@app.get("/videos{video_id}", response_model=VideoCreate)
def get_video(video_id: int, db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id).first()
    if video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return video

@app.put("/videos{video_id}", response_model=VideoCreate)
def update_video(video_id: int, video: VideoCreate, db: Session = Depends(get_db)):
    db_video = db.query(Video).filter(Video.id == video_id).first()
    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    db_video.filename = video.filename
    db_video.url = video.url
    db.commit()
    db.refresh(db_video)
    return db_video

@app.delete("/videos{video_id}", response_model=VideoCreate)
def delete_video(video_id: int, db: Session = Depends(get_db)):
    db_video = db.query(Video).filter(Video.id == video_id).first()
    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    db.delete(db_video)
    db.commit()
    return db_video

import logging
logging.basicConfig(level=logging.DEBUG)

