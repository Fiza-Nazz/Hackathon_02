from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from ..models import Tag, TagCreate, TagRead, User
from ..database.database import get_session
from ..api.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[TagRead])
def get_user_tags(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all tags for current user."""
    query = select(Tag).where(Tag.user_id == current_user.id).order_by(Tag.usage_count.desc())
    tags = session.exec(query).all()
    return tags

@router.post("/", response_model=TagRead)
def create_tag(
    tag: TagCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new tag."""
    # Check if tag already exists
    existing = session.exec(
        select(Tag).where(Tag.name == tag.name, Tag.user_id == current_user.id)
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Tag already exists")
    
    db_tag = Tag(
        name=tag.name,
        color=tag.color,
        user_id=current_user.id
    )
    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)
    return db_tag

@router.delete("/{tag_id}")
def delete_tag(
    tag_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a tag."""
    tag = session.exec(
        select(Tag).where(Tag.id == tag_id, Tag.user_id == current_user.id)
    ).first()
    
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    session.delete(tag)
    session.commit()
    return {"message": "Tag deleted successfully"}