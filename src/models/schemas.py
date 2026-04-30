from pydantic import BaseModel, Field
from typing import Optional 

class PreprocessingOptions(BaseModel):
    normalize: Optional[bool] = Field(default=False, description="Lowercase and normalize the text.")
    remove_urls: Optional[bool] = Field(default=False, description="Remove URLs from text.")
    remove_emojis: Optional[bool] = Field(default=False, description="Remove emojis and special Unicode symbols.")
    remove_punctuation: Optional[bool] = Field(default=False, description="Remove punctuation characters.")
    remove_numbers: Optional[bool] = Field(default=False, description="Remove numeric characters.")
    remove_stopwords: Optional[bool] = Field(default=False, description="Remove stopwords.")
    stemming: Optional[bool] = Field(default=False, description="Apply stemming.")
    lemmatize: Optional[bool] = Field(default=False, description="Apply lemmatization.")
    
    
class PreprocessRequest(BaseModel):
        text: str = Field(..., description="The input text to be preprocessed.")
        language: str = Field(..., pattern="^(ar|en)$", description="Language code: 'ar' or 'en'")        
        options: PreprocessingOptions = Field(..., description="The preprocessing options to apply to the text.")
    

class PreprocessResponse(BaseModel):
        original_text: str = Field(..., description="The original input text.")
        processed_text: str = Field(..., description="The preprocessed text after applying the specified options.")
        language: str = Field(..., description="The detected language of the input text.")
        applied_steps: list[str] = Field(..., description="A list of preprocessing steps that were applied to the text.")
        
        