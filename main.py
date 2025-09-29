from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime

from . import models, database

app = FastAPI(title="Smart Melt Management")
app.mount("/static", StaticFiles(directory="backend/static"), name="static")
templates = Jinja2Templates(directory="backend/templates")

models.Base.metadata.create_all(bind=database.engine)


# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    melts = db.query(models.Melt).all()
    total_melts = len(melts)
    total_weight = sum([m.weight_kg for m in melts]) if melts else 0
    total_scrap = sum([m.scrap_kg for m in melts]) if melts else 0
    scrap_percent = round((total_scrap / total_weight) * 100, 2) if total_weight > 0 else 0

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "total_melts": total_melts,
        "total_weight": total_weight,
        "scrap_percent": scrap_percent,
        "melts": melts
    })


@app.get("/melts", response_class=HTMLResponse)
def melts_list(request: Request, db: Session = Depends(get_db)):
    melts = db.query(models.Melt).order_by(models.Melt.date.desc()).all()
    return templates.TemplateResponse("melts.html", {"request": request, "melts": melts})


@app.post("/melts/add")
def add_melt(
    melt_number: str = Form(...),
    date: str = Form(...),
    shift: str = Form(...),
    weight_kg: float = Form(...),
    scrap_kg: float = Form(...),
    alloy: str = Form(...),
    notes: str = Form(""),
    db: Session = Depends(get_db)
):
    new_melt = models.Melt(
        melt_number=melt_number,
        date=datetime.fromisoformat(date),
        shift=shift,
        weight_kg=weight_kg,
        scrap_kg=scrap_kg,
        alloy=alloy,
        notes=notes
    )
    db.add(new_melt)
    db.commit()
    return RedirectResponse(url="/melts", status_code=303)
