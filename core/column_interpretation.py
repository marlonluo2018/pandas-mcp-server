import os
import pandas as pd
import logging
from chardet import detect
from .config import MAX_FILE_SIZE
from .data_types import get_descriptive_type

# Get metadata logger
logger = logging.getLogger('metadata')

def interpret_column_values(file_path: str, column_names: list) -> dict:
    """Interpret column values in a data file and return their unique values.
    
    Args:
        file_path: Path to the data file
        column_names: List of column names to interpret
        
    Returns:
        dict: Interpretation results including:
            - status: SUCCESS/ERROR
            - file_info: File metadata
            - columns_analysis: List of column interpretations
    """
    try:
        logger.info(f"Starting column value analysis for file: {file_path}")
        logger.debug(f"Columns to interpret: {column_names}")
        
        # Validate file existence and size
        if not os.path.exists(file_path):
            return {"status": "ERROR", "error": "FILE_NOT_FOUND", "path": file_path}

        file_size = os.path.getsize(file_path)
        if file_size > MAX_FILE_SIZE:
            return {
                "status": "ERROR",
                "error": "FILE_TOO_LARGE",
                "max_size": f"{MAX_FILE_SIZE / 1024 / 1024}MB",
                "actual_size": f"{file_size / 1024 / 1024:.1f}MB"
            }

        # Detect file type
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.csv':
            # Read CSV file
            logger.info("Processing CSV file for column analysis")
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)  # Only read first 10KB for encoding detection
                encoding = detect(raw_data)['encoding']
            logger.debug(f"Detected encoding: {encoding}")
            
            # Read the entire CSV file for accurate analysis
            df = pd.read_csv(file_path, encoding=encoding)
            
            # Interpret each requested column
            columns_interpretation = []
            for col_name in column_names:
                if col_name not in df.columns:
                    columns_interpretation.append({
                        "column_name": col_name,
                        "error": f"Column '{col_name}' not found in file"
                    })
                    continue
                
                col_interpretation = _interpret_single_column(df[col_name])
                col_interpretation["column_name"] = col_name
                columns_interpretation.append(col_interpretation)
            
            return {
                "status": "SUCCESS",
                "file_info": {
                    "type": "csv",
                    "size": f"{file_size / 1024:.1f}KB",
                    "encoding": encoding,
                    "total_rows": len(df),
                    "total_columns": len(df.columns)
                },
                "columns_interpretation": columns_interpretation
            }
        else:
            return {
                "status": "ERROR",
                "error": "UNSUPPORTED_FILE_TYPE",
                "message": f"Only CSV files are supported. File type {file_ext} is not supported."
            }
            
    except Exception as e:
        logger.error(f"Column value analysis failed: {str(e)}")
        return {
            "status": "ERROR",
            "error_type": type(e).__name__,
            "message": str(e)
        }

def _interpret_single_column(series: pd.Series) -> dict:
    """Interpret a single pandas Series and return its unique values and statistics."""
    # Get basic statistics
    total_values = len(series)
    null_count = series.isnull().sum()
    unique_count = series.nunique()
    
    # Get unique values and their counts
    value_counts = series.dropna().value_counts().to_dict()
    
    # Convert to list of tuples (value, count) and sort by count descending
    unique_values_with_counts = sorted(value_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Determine data type
    data_type = get_descriptive_type(series)
    
    return {
        "data_type": data_type,
        "total_values": total_values,
        "null_count": null_count,
        "unique_count": unique_count,
        "unique_values_with_counts": unique_values_with_counts
    }

def _generate_column_interpretation(column_name: str, data_type: str, unique_values: list, sample_values: list, value_count: int = None) -> str:
    """Generate an interpretation of what the column represents based on its values."""
    if not unique_values:
        return "This column appears to be empty or contains only null values."
    
    # Start with basic information
    interpretation = f"Column '{column_name}' contains {data_type} data. "
    
    # Check column name for hints about the data type
    column_name_lower = column_name.lower()
    
    # Add specific interpretations based on data type and values
    if data_type == 'bool':
        # Boolean data interpretation
        true_count = sum(1 for v in unique_values if v is True)
        false_count = sum(1 for v in unique_values if v is False)
        interpretation += f"This appears to be a boolean column with {true_count} true and {false_count} false values. "
        
        # Check for column name hints about the boolean meaning
        if any(keyword in column_name_lower for keyword in ['active', 'enabled', 'valid']):
            interpretation += "The values likely indicate active/inactive or enabled/disabled status. "
        elif any(keyword in column_name_lower for keyword in ['has', 'contains', 'is']):
            interpretation += "The values likely indicate the presence or absence of a characteristic. "
        else:
            interpretation += "The values represent binary true/false conditions. "
    elif data_type in ['int64', 'float64']:
        # Numeric data interpretation with enhanced logic
        # Ensure sample_values doesn't contain boolean values
        numeric_sample_values = [v for v in sample_values if not isinstance(v, bool)]
        if not numeric_sample_values:
            interpretation += "This appears to be a boolean column. "
        else:
            min_val = min(numeric_sample_values)
            max_val = max(numeric_sample_values)
        
        # Check for specific numeric patterns based on column name
        if any(keyword in column_name_lower for keyword in ['id', 'code', 'num']):
            interpretation += f"This appears to be an identifier or code column with unique numeric values ranging from {min_val} to {max_val}. "
        elif any(keyword in column_name_lower for keyword in ['age', 'year', 'duration', 'time']):
            interpretation += f"This appears to be a time-related measurement with values ranging from {min_val} to {max_val}. "
        elif any(keyword in column_name_lower for keyword in ['salary', 'income', 'price', 'cost', 'amount', 'revenue']):
            interpretation += f"This appears to be a monetary value with amounts ranging from {min_val} to {max_val}. "
        elif any(keyword in column_name_lower for keyword in ['score', 'rating', 'grade', 'performance']):
            interpretation += f"This appears to be a performance score or rating with values from {min_val} to {max_val}. "
        else:
            # Check if values are integers within a small range (likely categorical)
            if all(isinstance(v, int) or (isinstance(v, float) and v.is_integer()) for v in numeric_sample_values):
                if max_val - min_val < 100:
                    interpretation += f"The values are integers ranging from {min_val} to {max_val}, suggesting this might be a categorical or rating scale. "
                else:
                    interpretation += f"The values are integers ranging from {min_val} to {max_val}. "
            
            # Check if values are all positive (might be counts or measurements)
            if all(v >= 0 for v in numeric_sample_values):
                interpretation += "All values are non-negative, suggesting this might represent counts, measurements, or ratings. "
            
            # Check for common patterns
            if all(v in [0, 1] for v in numeric_sample_values):
                interpretation += "This appears to be a binary/boolean column with values 0 and 1. "
            elif all(v in range(1, 6) for v in numeric_sample_values):
                interpretation += "Values range from 1 to 5, suggesting this might be a rating scale. "
        
    else:
        # Categorical/string data interpretation
        # Check for common patterns
        if all(v.lower() in ['male', 'female', 'm', 'f'] for v in sample_values if isinstance(v, str)):
            interpretation += "This appears to be a gender column with values representing male/female categories. "
        elif all(v.lower() in ['yes', 'no', 'y', 'n', 'true', 'false', 't', 'f'] for v in sample_values if isinstance(v, str)):
            interpretation += "This appears to be a boolean column with yes/no or true/false values. "
        elif all(v.lower() in ['active', 'inactive', 'enabled', 'disabled'] for v in sample_values if isinstance(v, str)):
            interpretation += "This appears to be a status column indicating active/inactive states. "
        elif any('date' in str(v).lower() or 'time' in str(v).lower() for v in sample_values[:5] if isinstance(v, str)):
            interpretation += "This column appears to contain date or time information. "
        elif any('@' in str(v) for v in sample_values[:5] if isinstance(v, str)):
            interpretation += "This column appears to contain email addresses. "
        elif any(v.replace('.', '').replace('-', '').replace(' ', '').isdigit() for v in sample_values[:5] if isinstance(v, str) and not isinstance(v, bool)):
            interpretation += "This column appears to contain phone numbers or other numeric identifiers. "
        else:
            # General categorical interpretation - simplified to avoid redundancy
            unique_count = len(unique_values)
            interpretation += f"This appears to be a categorical column with {unique_count} distinct "
            
            if unique_count == 1:
                interpretation += "value. "
            elif unique_count == 2:
                interpretation += "values. "
            else:
                interpretation += "values. "
            
            # For columns with few values, provide a brief description instead of listing all values
            if unique_count <= 5:
                # Try to infer the nature of the categories
                if any('level' in str(v).lower() for v in sample_values if isinstance(v, str)):
                    interpretation += "The values appear to represent different levels or tiers. "
                elif 'status' in column_name_lower or 'state' in column_name_lower:
                    interpretation += "The values appear to represent different statuses or states. "
                elif 'type' in column_name_lower or 'category' in column_name_lower:
                    interpretation += "The values appear to represent different types or categories. "
                else:
                    interpretation += "The values represent different categories. "
            elif unique_count <= 20:
                interpretation += "The values represent various categories. "
            else:
                interpretation += "The values represent a wide range of categories. "
    
    # Add data quality observations
    if len(unique_values) == 1:
        interpretation += "Note: This column has only one unique value, which might indicate limited variability or data quality issues. "
    
    return interpretation