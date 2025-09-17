from pydantic import BaseModel, Field
from datetime import date

class FixedCost(BaseModel):
    """
    Representa um custo fixo com validação utilizado Pydantic.
    """
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=0)
    value: float = Field(..., gt=0)
    date: date

    def __str__(self) -> str:
        return f"Fixed Cost: {self.description}, Value: {self.value}, Date: {self.date.strftime('%Y-%m-%d')}"
