from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class Portfolio(Base):
    __tablename__ = "portfolio"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_portfolio_value = Column(Float, nullable=True)
    roi = Column(Float, nullable=True)
    auto_trading_status = Column(Boolean, nullable=True)
    market_confidence_index = Column(Integer, nullable=True)
    purchase_price = Column(Float, nullable=True)
    total_assets_purchased = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
