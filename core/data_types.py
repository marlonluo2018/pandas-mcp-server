import pandas as pd
from pandas.api.types import infer_dtype

def get_descriptive_type(series: pd.Series) -> str:
    """Convert pandas dtype to more descriptive type name.
    
    Args:
        series: Pandas Series to analyze
        
    Returns:
        str: Descriptive type name like 'string', 'date', 'number', etc.
    """
    # Get detailed type information
    dtype = infer_dtype(series)
    
    # Map to more descriptive names
    type_map = {
        'string': 'string',
        'unicode': 'string',
        'bytes': 'string',
        'mixed-integer': 'number',
        'mixed-integer-float': 'number',
        'floating': 'number',
        'integer': 'number',
        'mixed': 'mixed',
        'categorical': 'category',
        'boolean': 'boolean',
        'datetime64': 'date',
        'datetime': 'date',
        'date': 'date',
        'timedelta64': 'duration',
        'timedelta': 'duration',
        'time': 'time',
        'period': 'period',
        'empty': 'empty',
        'unknown': 'unknown'
    }
    
    # Check for datetime types explicitly
    # Debug input type
    print(f"Input type: {type(series)}")
    if hasattr(series, 'shape'):
        print(f"Input shape: {series.shape}")
    
    # Handle case where input is actually a DataFrame
    if isinstance(series, pd.DataFrame):
        print(f"DataFrame with columns: {series.columns}")
        if len(series.columns) == 1:
            series = series.iloc[:, 0]
            print(f"Converted to Series: {type(series)}")
        else:
            return 'mixed'
    
    # Check for datetime types
    if pd.api.types.is_datetime64_any_dtype(series):
        return 'date'
    
    # Check for string types explicitly
    if pd.api.types.is_string_dtype(series):
        return 'string'
    
    # Return mapped type or fall back to original dtype
    return type_map.get(str(series.dtype), str(series.dtype))