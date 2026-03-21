from pydantic import BaseModel, Field, EmailStr, model_validator
from typing import Optional

"""
Here I created a new models.py file inorder to NOT to write everything in main.py and increase code Modularity
"""

# 6. Enroll Request Model
class EnrollRequest(BaseModel):
    student_name: str = Field(..., min_length=2)
    course_id: int = Field(..., gt=0)
    email: EmailStr
    payment_method: str = Field(default='card', min_length=2)
    coupon_code: Optional[str] = ""

    gift_enrollment: bool = False
    recipient_name: str = ""

    @model_validator(mode="after")
    def validate_gift(cls, values):
        if values.gift_enrollment and not values.recipient_name.strip():
            raise ValueError("Recipient name is required for gift enrollment")
        return values


# 11. New Course Model
class NewCourse(BaseModel):
    title: str = Field(..., min_length=2)
    instructor: str = Field(..., min_length=2)
    category: str = Field(..., min_length=2)
    level: str = Field(..., min_length=2)
    price: int = Field(..., ge=0)
    seats_left: int = Field(default=10, ge=0)