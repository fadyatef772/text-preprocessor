from pydantic import BaseModel, Field
from typing import Optional 

class PreprocessingOptions(BaseModel):
    remove_stopwords: Optional[bool] = Field(default=False, description="Whether to remove stopwords from the text.")
    lemmatization: Optional[bool] = Field(default=False, description="Whether to apply lemmatization to the text.")
    stemming: Optional[bool] = Field(default=False, description="Whether to apply stemming to the text.")
    lowercase: Optional[bool] = Field(default=False, description="Whether to convert the text to lowercase.")
    
    
class PreprocessRequest(BaseModel):
        text: str = Field(..., description="The input text to be preprocessed.")
        language: str = Field(..., pattern="^(ar|en)$", description="Language code: 'ar' or 'en'")        
        options: PreprocessingOptions = Field(..., description="The preprocessing options to apply to the text.")
    

class PreprocessResponse(BaseModel):
        original_text: str = Field(..., description="The original input text.")
        processed_text: str = Field(..., description="The preprocessed text after applying the specified options.")
        language: str = Field(..., description="The detected language of the input text.")
        applied_steps: list[str] = Field(..., description="A list of preprocessing steps that were applied to the text.")
        
        