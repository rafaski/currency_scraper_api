from pydantic import BaseModel


class Metadata(BaseModel):
    """Schema for nested metadata output"""
    time_of_conversion: str
    from_currency: str
    to_currency: str


class ConvertCurrency(BaseModel):
    """Schema for currency conversion output"""
    converted_amount: float
    mid_market_rate: float
    metadata: Metadata


class HistoricalRates(BaseModel):
    """Schema for historical rates output"""
    rate: float
    time: str


class AverageRate(BaseModel):
    """Schemas for average rate output"""
    average_rate: float
    duration_in_days: int
