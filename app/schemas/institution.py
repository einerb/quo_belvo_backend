from typing import List, Optional
from pydantic import BaseModel, Field, AnyHttpUrl

class FieldValueDTO(BaseModel):
    code: str
    label: str

class FormFieldDTO(BaseModel):
    name: str
    type: str
    validation: Optional[str] = None
    values: Optional[List[FieldValueDTO]] = None

class SimplifiedInstitutionDTO(BaseModel):
    id: int
    name: str
    display_name: str = Field(..., alias="display_name")
    logo: AnyHttpUrl
    icon_logo: AnyHttpUrl
    text_logo: AnyHttpUrl
    country: str = Field(..., alias="country_code")
    status: str
    form_fields: List[FormFieldDTO] = Field(default_factory=list)

class InstitutionListDTO(BaseModel):
    count: int
    institutions: List[SimplifiedInstitutionDTO]
