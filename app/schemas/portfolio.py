from pydantic import BaseModel, Field
from datetime import datetime

class PortfolioCreate(BaseModel):
    total_portfolio_value: float | None = None
    roi: float | None = None
    auto_trading_status: bool | None = None
    market_confidence_index: int | None = None
    purchase_price: float | None = None
    total_assets_purchased: float | None = None

class PortfolioOut(BaseModel):
    id: int
    user_id: int
    total_portfolio_value: float | None = None
    roi: float | None = None
    auto_trading_status: bool | None = None
    market_confidence_index: int | None = None
    purchase_price: float | None = None
    total_assets_purchased: float | None = None
    created_at: datetime = Field(default=None)  # Accept datetime object

    class Config:
        from_attributes = True


class PortfolioOverview(BaseModel):
    token: str
    quantity: float
    value: float
    entry_price: float
    market_price: float
    p_l: float
    status: str
