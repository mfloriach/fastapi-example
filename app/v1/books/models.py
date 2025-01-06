
from datetime import datetime
from enum import IntEnum
from typing import Optional

from pydantic import field_validator
from sqlmodel import Field, SQLModel


class Language(IntEnum):
    ENGLISH = 1
    JAPANESE = 2
    SPANISH = 3


class _BookBase(SQLModel):
    """ Book Model representation """

    title: str = Field(nullable=False, index=True)
    num_pages: int = Field(nullable=False) 
    language: Language = Field(nullable=False) 
    prize: int = Field(nullable=False) 

    created_at: datetime = Field(  
        default=datetime.now(),  
        nullable=False,  
    )  
    updated_at: datetime = Field(  
        default_factory=datetime.now,  
        nullable=False,  
    )

    @field_validator("prize", "num_pages")
    def prize_higher_than_zero(cls, v):
        if v <= 0 or v >= 999999 :
            raise ValueError("must be higher than 0 and lower 999999")
        
        return v
        
    @field_validator("language")
    def language_in_enum(cls, v):
        if v <= 0 or v >= 999999 :
            raise ValueError("must be higher than 0 and lower 999999")
        
        for item in Language:
            if item == v:
                return v
        
        raise ValueError("not valid value")
    
class BookCreate(_BookBase):
    pass

class BookUpdate(_BookBase):
    pass

class Book(_BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
