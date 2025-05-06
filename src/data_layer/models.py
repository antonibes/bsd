import datetime

from pydantic import BaseModel, ConfigDict, Field


class TransactionModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    date: datetime.date = Field(alias="Date", description="Transaction date")
    description: str = Field(alias="Description", description="Transaction title or description")
    amount: float = Field(alias="Amount", description="Transaction amount (negative for expenses, positive for income)")
    transaction_type: str = Field(alias="Type", description="Income or Expense")
    balance: float | None = Field(default=None, alias="Balance", description="Account balance after transaction")

    @property
    def is_expense(self) -> bool:
        return self.amount < 0

    @property
    def is_income(self) -> bool:
        return self.amount > 0
