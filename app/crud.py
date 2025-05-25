from sqlalchemy.orm import Session
from app import models, schemas
from collections import defaultdict
from datetime import datetime

def create_saving(db: Session, saving: schemas.SavingCreate):
    db_saving = models.Saving(**saving.model_dump())
    db.add(db_saving)
    db.commit()
    db.refresh(db_saving)
    return db_saving

def get_savings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Saving).offset(skip).limit(limit).all()

def get_saving_by_id(db: Session, saving_id: int):
    return db.query(models.Saving).filter(models.Saving.id == saving_id).first()

def delete_saving(db: Session, saving_id: int):
    saving = db.query(models.Saving).filter(models.Saving.id == saving_id).first()
    if saving:
        db.delete(saving)
        db.commit()
        return {"ok": True}
    return {"ok": False}

def update_saving(db: Session, saving_id: int, new_data: schemas.SavingCreate):
    saving = db.query(models.Saving).filter(models.Saving.id == saving_id).first()
    if saving:
        for field, value in new_data.model_dump().items():
            setattr(saving, field, value)
        db.commit()
        db.refresh(saving)
    return saving

def get_summary(db: Session):
    savings = db.query(models.Saving).all()
    
    total = sum(s.amount for s in savings)

    monthly = defaultdict(float)
    category_totals = defaultdict(float)
    category_counts = defaultdict(int)

    for s in savings:
        month_key = s.date.strftime("%Y-%m")
        monthly[month_key] += s.amount

        category_key = s.category or "Unknown"
        category_totals[category_key] += s.amount
        category_counts[category_key] += 1

    average = round(total / len(monthly), 2) if monthly else 0.0
    highest_month = max(monthly.items(), key=lambda x: x[1], default=(None, 0))

    return {
        "total_savings": round(total, 2),
        "average_monthly": average,
        "monthly_breakdown": dict(monthly),
        "category_breakdown": {
            "amounts": {k: round(v, 2) for k, v in category_totals.items()},
            "counts": dict(category_counts)
        },
        "highest_month": {
            "month": highest_month[0],
            "amount": round(highest_month[1], 2)
        }
    }
