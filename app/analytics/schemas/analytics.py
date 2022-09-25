from typing import List, Union
from pydantic import BaseModel, Field

class BaseClass(BaseModel):
    class Config:
        orm_mode = True

class ResponseBaseModel(BaseClass):
    success: bool = Field(..., description="success")
    message: Union[str, dict, list] = Field(..., description="message")

class FeaturesUsedCount(BaseClass):
    featureName: str = Field(..., description="featureName")
    featureUsedCount: int = Field(..., description="featureUsedCount")\

class CompanyFeatures(BaseClass):
    companyName: str = Field(..., description="companyName")
    features: List[FeaturesUsedCount] = Field(..., description="features")

class UserFeatures(BaseClass):
    userName: str = Field(..., description="userName")
    features: List[FeaturesUsedCount] = Field(..., description="features")

class CompanyUserFeaturesCount(BaseClass):
	companyName: str = Field(..., description="companyName")
	users: List[UserFeatures] = Field(..., description="users")

class GetCompanyListResponseSchema(ResponseBaseModel):
    message: List[CompanyFeatures] = Field(..., description="message")

class GetCompanyUserListResponseSchema(ResponseBaseModel):
    message: List[CompanyUserFeaturesCount] = Field(..., description="message")

