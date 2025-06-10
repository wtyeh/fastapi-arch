"""
Data analysis routes module.
"""
import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlmodel.ext.asyncio.session import AsyncSession as Session

from app.db.postgres import get_async_session
from app.utils.data_processing import process_dataframe

router = APIRouter()


@router.post("/upload-csv/", status_code=status.HTTP_200_OK)
async def upload_csv_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_async_session),
):
    """
    Upload and process CSV file.
    
    Args:
        file (UploadFile): CSV file
        db (Session): Database session
        
    Returns:
        dict: Processing results
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV files are allowed",
        )
    
    try:
        # Read CSV file into pandas DataFrame
        contents = await file.read()
        df = pd.read_csv(pd.io.common.BytesIO(contents))
        
        # Process DataFrame
        processed_df = process_dataframe(df)
        
        # Return statistics
        stats = {
            "row_count": len(processed_df),
            "column_count": len(processed_df.columns),
            "columns": list(processed_df.columns),
            "data_types": {col: str(processed_df[col].dtype) for col in processed_df.columns},
            "sample_data": processed_df.head(5).to_dict(orient="records"),
            "summary_stats": processed_df.describe().to_dict(),
        }
        
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}",
        )
