
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import Base, engine, get_db
from backend import model as models
from backend.model import Report
from backend.schemas import ReportCreate, ReportResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables when the app starts
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="CivicSignal API",
    description="Evidence-aware civic issue reporting platform",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/")
def home():
    return {
        "message": "Welcome to CivicSignal API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post(
    "/api/reports",
    response_model=ReportResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_report(
    payload: ReportCreate,
    db: Session = Depends(get_db),
):
    # Prevent an existing report ID from being overwritten
    existing_report = (
        db.query(Report)
        .filter(Report.id == payload.id)
        .first()
    )

    if existing_report:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A report with this ID already exists.",
        )

    report = Report(**payload.model_dump())

    db.add(report)
    try:
        db.commit()
        db.refresh(report)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not save the report.",
        )

    return report


@app.get("/api/reports", response_model=list[ReportResponse])
def list_reports(db: Session = Depends(get_db)):
    return db.query(Report).order_by(Report.ingested_at.desc()).all()


@app.get("/api/reports/{report_id}", response_model=ReportResponse)
def get_report(
    report_id: str,
    db: Session = Depends(get_db),
):
    report = (
        db.query(Report)
        .filter(Report.id == report_id)
        .first()
    )

    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found.",
        )

    return report
