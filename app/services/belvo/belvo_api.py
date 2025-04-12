from sqlalchemy import select
from datetime import datetime, date, timedelta

from app.db.session import get_db
from app.schemas.institution import SimplifiedInstitutionDTO, InstitutionListDTO
from .client import belvo_get, belvo_post
from app.schemas.transaction import CreateTransactionDTO
from app.models.link_institution import LinkInstitution

async def get_institutions():
    response = await belvo_get("institutions/?page_size=100")
    simplified_institutions = []

    for inst in response["results"]:
        inst["form_fields"] = inst.get("form_fields", [])
        simplified_institutions.append(SimplifiedInstitutionDTO(**inst))

    return InstitutionListDTO(
        count=len(simplified_institutions),
        institutions=simplified_institutions
    )
    
async def get_link_institution(name: str) -> str:
    async with get_db() as session:
        result = await session.execute(
            select(LinkInstitution.link_id).where(LinkInstitution.name == name)
        )
        link_id = result.scalar()
        
        return link_id

async def save_link_institution(name: str, link_id: str, date_expiration: date):
    async with get_db() as session:
        try:
            async with session.begin():
                result = await session.execute(
                    select(LinkInstitution).where(LinkInstitution.name == name)
                )
                existing = result.scalars().first()

                if existing:
                    existing.link_id = link_id
                    existing.date_expiration = date_expiration
                    session.add(existing)
                else:
                    new_link = LinkInstitution(
                        name=name,
                        link_id=link_id,
                        date_expiration=date_expiration
                    )
                    session.add(new_link)

            return existing if existing else new_link

        except Exception as e:
            raise ValueError(f"Error saving link institution: {str(e)}")

async def create_link(
    institution: str,
    credentials: dict,
    access_mode: str = "single",
    link_type: str = "sandbox"
):
    payload = {
        "institution": institution,
        "access_mode": access_mode,
        "type": link_type,
        "stale_in": "10d",
        **credentials
    }

    return await belvo_post("links/", payload)

async def create_link_and_save(
    institution: str,
    credentials: dict,
    access_mode: str = "single",
    link_type: str = "sandbox"
):
    link_data = await create_link(
        institution=institution,
        credentials=credentials,
        access_mode=access_mode,
        link_type=link_type
    )

    date_expiration = (datetime.utcnow() + timedelta(days=10)).date()

    await save_link_institution(
        name=institution,
        link_id=link_data["id"],
        date_expiration=date_expiration
    )

    return link_data


async def get_accounts(link_id: str):
    payload = {
        "link": link_id,
        "save_data": True,
    }
    return await belvo_post("accounts", payload)

async def get_transactions(link_id: str, account_id: str, date_from: str, date_to: str):
    payload = {
        "link": link_id,
        "account": account_id,
        "date_from": date_from,
        "date_to": date_to,
        "save_data": True,
    }
    transactions = await belvo_post("transactions", payload)
    return transactions

async def calculate_balance(payload: CreateTransactionDTO):
    transactions = await get_transactions(payload.link, payload.account, payload.date_from, payload.date_to)

    if not transactions:
        return {
            "is_negative": False,
            "balance": 0,
            "income": 0,
            "expenses": 0,
            "currency": None,
            "transactions": []
        }

    currency = transactions[0].get("currency") if transactions else None
    income = sum(float(t["amount"]) for t in transactions if t["type"] == "INFLOW")
    expenses = sum(float(t["amount"]) for t in transactions if t["type"] == "OUTFLOW")
    
    return {
        "is_negative": (income - expenses) < 0,
        "balance": income - expenses,
        "income": income,
        "expenses": expenses,
        "transactions": transactions,
        "currency": currency
    }
