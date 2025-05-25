from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/savings/", response_model=schemas.Saving)
def create_saving(saving: schemas.SavingCreate, db: Session = Depends(get_db)):
    return crud.create_saving(db=db, saving=saving)

@router.get("/savings/", response_model=list[schemas.Saving])
def read_savings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_savings(db, skip=skip, limit=limit)

@router.get("/savings/{saving_id}", response_model=schemas.Saving, responses={404: {"model": schemas.ErrorResponse}})
def get_saving(saving_id: int, db: Session = Depends(get_db)):
    saving = crud.get_saving_by_id(db, saving_id)
    if not saving:
        raise HTTPException(status_code=404, detail="Saving not found")
    return saving

@router.delete("/savings/{saving_id}", responses={404: {"model": schemas.ErrorResponse}})
def delete_saving(saving_id: int, db: Session = Depends(get_db)):
    result = crud.delete_saving(db, saving_id)
    if result["ok"]:
        return {"message": f"Saving with ID {saving_id} deleted."}
    raise HTTPException(status_code=404, detail="Saving not found")

@router.put("/savings/{saving_id}", response_model=schemas.Saving, responses={404: {"model": schemas.ErrorResponse}})
def update_saving(saving_id: int, saving: schemas.SavingCreate, db: Session = Depends(get_db)):
    updated = crud.update_saving(db, saving_id, saving)
    if updated:
        return updated
    raise HTTPException(status_code=404, detail="Saving not found")


@router.get("/summary/")
def get_summary(db: Session = Depends(get_db)):
    return crud.get_summary(db)
