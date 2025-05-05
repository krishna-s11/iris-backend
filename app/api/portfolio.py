from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.portfolio import Portfolio
from app.schemas.portfolio import PortfolioCreate, PortfolioOut
from app.core.security import get_current_user
from app.services.auth_service import get_user_by_email
from typing import List
import plotly.express as px
import json

router = APIRouter()

@router.post("/add", response_model=PortfolioOut)
def add_portfolio_entry(
    portfolio: PortfolioCreate,
    current_user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print(f"DEBUG: Adding portfolio for email: {current_user_email}")
    user = get_user_by_email(db, current_user_email)
    if not user:
        print("DEBUG: User not found")
        raise HTTPException(status_code=404, detail="User not found")
    print(f"DEBUG: User found - ID: {user.id}")
    db_portfolio = Portfolio(
        user_id=user.id,
        total_portfolio_value=portfolio.total_portfolio_value,
        roi=portfolio.roi,
        auto_trading_status=portfolio.auto_trading_status,
        market_confidence_index=portfolio.market_confidence_index,
        purchase_price=portfolio.purchase_price,
        total_assets_purchased=portfolio.total_assets_purchased
    )
    print(f"DEBUG: Portfolio object created: {db_portfolio.__dict__}")
    try:
        db.add(db_portfolio)
        db.commit()
        db.refresh(db_portfolio)
        print(f"DEBUG: Portfolio committed - ID: {db_portfolio.id}, Created At: {db_portfolio.created_at}")
        # Verify the new entry in the database
        new_entry = db.query(Portfolio).filter(Portfolio.id == db_portfolio.id).first()
        print(f"DEBUG: Verified new entry: {new_entry.__dict__}")
        return db_portfolio
    except Exception as e:
        db.rollback()
        print(f"DEBUG: Error committing portfolio: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/", response_model=List[PortfolioOut])
def get_portfolio(
    current_user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print(f"DEBUG: Fetching portfolio for email: {current_user_email}")
    user = get_user_by_email(db, current_user_email)
    if not user:
        print("DEBUG: User not found")
        raise HTTPException(status_code=404, detail="User not found")
    print(f"DEBUG: User found - ID: {user.id}")
    portfolios = db.query(Portfolio).filter(Portfolio.user_id == user.id).all()
    print(f"DEBUG: Portfolios fetched: {[p.__dict__ for p in portfolios]}")
    return portfolios

from app.schemas.portfolio import PortfolioOverview
from typing import List

@router.get("/graph")
def get_portfolio_graph(
    current_user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, current_user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    portfolios = db.query(Portfolio).filter(Portfolio.user_id == user.id).all()
    if not portfolios:
        raise HTTPException(status_code=404, detail="No portfolio data found")
    df = [(p.created_at, p.total_portfolio_value) for p in portfolios]
    fig = px.line(x=[x[0] for x in df], y=[x[1] for x in df], title=f"Portfolio for {user.email}")
    return json.loads(fig.to_json())

@router.get("/overview", response_model=List[PortfolioOverview])
def get_portfolio_overview(
    current_user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, current_user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    portfolios = db.query(Portfolio).filter(Portfolio.user_id == user.id).all()
    if not portfolios:
        raise HTTPException(status_code=404, detail="No portfolio data found")

    overview = []
    for p in portfolios:
        # TODO: Implement logic to fetch token name, quantity, value, entry price, market price, P&L, and status
        # This is placeholder data
        overview.append(PortfolioOverview(
            token="BTC",
            quantity=1.0,
            value=30000.0,
            entry_price=20000.0,
            market_price=30000.0,
            p_l=10000.0,
            status="Up"
        ))
    return overview
