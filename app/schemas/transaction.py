from pydantic import BaseModel

class CreateTransactionDTO(BaseModel):
    account: str
    link: str
    date_from: str
    date_to: str
    save_data: bool = True