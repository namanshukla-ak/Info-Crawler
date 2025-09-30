"""
Utility functions for data processing and formatting
"""
import pandas as pd
from typing import List, Dict, Any
from datetime import datetime
import io


def format_bio_data(bios: List[Dict]) -> pd.DataFrame:
    """
    Format bio data for display
    
    Args:
        bios: List of bio dictionaries
        
    Returns:
        Formatted DataFrame
    """
    if not bios:
        return pd.DataFrame()
    
    df = pd.DataFrame(bios)
    
    # Ensure expected columns exist
    expected_columns = ["name", "title", "organization", "bio_short", "bio_long", "headshot", "tenure"]
    for col in expected_columns:
        if col not in df.columns:
            df[col] = ""
    
    # Reorder columns
    column_order = ["name", "title", "organization", "tenure", "bio_short", "bio_long", "headshot"]
    df = df[[col for col in column_order if col in df.columns]]
    
    return df


def format_job_data(jobs: List[Dict]) -> pd.DataFrame:
    """
    Format job posting data for display
    
    Args:
        jobs: List of job dictionaries
        
    Returns:
        Formatted DataFrame
    """
    if not jobs:
        return pd.DataFrame()
    
    df = pd.DataFrame(jobs)
    
    # Ensure expected columns exist
    expected_columns = [
        "title", "organization", "location", "posted_date", 
        "salary_range", "job_board", "url", "description"
    ]
    for col in expected_columns:
        if col not in df.columns:
            df[col] = ""
    
    # Format dates
    if "posted_date" in df.columns:
        df["posted_date"] = pd.to_datetime(df["posted_date"], errors="coerce")
    
    return df


def format_news_data(news: List[Dict]) -> pd.DataFrame:
    """
    Format news article data for display
    
    Args:
        news: List of news dictionaries
        
    Returns:
        Formatted DataFrame
    """
    if not news:
        return pd.DataFrame()
    
    df = pd.DataFrame(news)
    
    # Ensure expected columns exist
    expected_columns = [
        "title", "source", "published_date", "url", 
        "summary", "category", "tags"
    ]
    for col in expected_columns:
        if col not in df.columns:
            df[col] = "" if col != "tags" else []
    
    # Format dates
    if "published_date" in df.columns:
        df["published_date"] = pd.to_datetime(df["published_date"], errors="coerce")
    
    # Format tags as strings for display
    if "tags" in df.columns:
        df["tags"] = df["tags"].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)
    
    return df


def create_csv_download(df: pd.DataFrame, filename_prefix: str) -> bytes:
    """
    Create CSV file for download
    
    Args:
        df: DataFrame to export
        filename_prefix: Prefix for filename
        
    Returns:
        CSV file as bytes
    """
    return df.to_csv(index=False).encode('utf-8')


def generate_filename(prefix: str, extension: str = "csv") -> str:
    """
    Generate filename with timestamp
    
    Args:
        prefix: Filename prefix
        extension: File extension (default: csv)
        
    Returns:
        Formatted filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"


def calculate_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate basic statistics from DataFrame
    
    Args:
        df: Input DataFrame
        
    Returns:
        Dictionary of statistics
    """
    if df.empty:
        return {"total_rows": 0, "total_columns": 0}
    
    stats = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "columns": list(df.columns)
    }
    
    return stats


def validate_required_fields(data: Dict, required_fields: List[str]) -> bool:
    """
    Validate that required fields are present and non-empty
    
    Args:
        data: Data dictionary to validate
        required_fields: List of required field names
        
    Returns:
        True if all required fields are present and non-empty
    """
    for field in required_fields:
        if field not in data or not data[field]:
            return False
    return True


def sanitize_for_csv(text: str) -> str:
    """
    Sanitize text for CSV export
    
    Args:
        text: Input text
        
    Returns:
        Sanitized text
    """
    if not isinstance(text, str):
        return str(text)
    
    # Remove problematic characters
    text = text.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
    text = text.replace('"', '""')  # Escape quotes
    
    return text.strip()
