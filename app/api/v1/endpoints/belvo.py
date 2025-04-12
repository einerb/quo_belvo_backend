from fastapi import APIRouter, Body, Query, Request

from app.services.belvo.belvo_api import get_institutions, get_accounts, create_link_and_save, calculate_balance, get_link_institution
from app.utils.response import success_response, error_response
from app.schemas.link import CreateLinkDTO, LinkDTO
from app.schemas.transaction import CreateTransactionDTO
from app.core.rate_limiter import limiter

router = APIRouter(prefix="/belvo")

@router.get("/institutions")
@limiter.limit("30/minute")
async def list_institutions(request: Request):
    try:
        institutions = await get_institutions()

        return success_response(
            data=institutions,
            message="Institutions found!",
            status_code=200
        )
    except ValueError as e:
        return error_response(str(e), status_code=400)

    except Exception as e:
        return error_response(str(e), status_code=500)

@router.get("/link-institution")
@limiter.limit("50/minute")
async def list_institutions(request: Request, name: str = Query(...)):
    try:
        link_institution = await get_link_institution(name)

        return success_response(
            data={"link_id": link_institution},
            message="Link found!",
            status_code=200
        )
    except ValueError as e:
        return error_response(str(e), status_code=404)

    except Exception as e:
        return error_response(str(e), status_code=500)

@router.post("/create-link")
@limiter.limit("30/minute")
async def create_link_endpoint(request: Request, payload: CreateLinkDTO = Body(...)):
    try:
        link_data = await create_link_and_save(
            institution=payload.institution,
            credentials=payload.credentials,
            access_mode=payload.access_mode,
            link_type=payload.type
        )
        return success_response(
            data={"id": link_data["id"]},
            message="Link successfully created and saved!",
            status_code=201
        )
    except ValueError as e:
        return error_response(str(e), status_code=400)
    except Exception as e:
        return error_response("Unexpected error", status_code=500)


@router.post("/accounts")
@limiter.limit("50/minute")
async def list_accounts(request: Request, payload: LinkDTO = Body(...)):
    try:
        accounts = await get_accounts(payload.link)
        return success_response(
            data=accounts,
            message="Accounts found!",
            status_code=200
        )

    except ValueError as e:
        return error_response(str(e), status_code=400)

    except Exception as e:
        return error_response(str(e), status_code=500)

@router.post("/balance")
@limiter.limit("30/minute")
async def get_balance(request: Request, payload: CreateTransactionDTO = Body(...)):
    try:
        balance = await calculate_balance(payload)
        return success_response(
            data=balance,
            message="Balance found!",
            status_code=200
        )

    except ValueError as e:
        return error_response(str(e), status_code=400)

    except Exception as e:
        return error_response(str(e), status_code=500)