# Enhanced Metadata Format for Query Generation

## Common Structure
```json
{
  "status": "SUCCESS|ERROR",
  "file_info": {
    "size": "102.4KB",
    "type": "excel|csv",
    // Additional type-specific info
  },
  "data": {
    // Format-specific data with enhanced stats
  }
}
```

## Enhanced Column Metadata
```json
{
  "name": "ColumnName",
  "type": "number|string|date|boolean",
  "examples": ["sample1", "sample2"],
  "stats": {
    "null_count": 5,
    "unique_count": 10,
    
    // Numeric columns
    "min": 0,
    "max": 100,
    "mean": 42.5,
    "std_dev": 12.3,
    
    // String columns
    "max_length": 255,
    "distinct_values": ["A","B","C"],
    
    // Date columns
    "min_date": "2023-01-01",
    "max_date": "2023-12-31",
    
    // Type-specific flags
    "is_numeric": true,
    "is_temporal": false,
    "is_categorical": true
  },
  "warnings": [
    "High null count",
    "Low cardinality"
  ],
  "suggested_operations": [
    "normalize",
    "one_hot_encode"
  ]
}
```

## Key Additions for Query Generation:
1. **Extended Statistics**:
   - Numeric ranges (min/max)
   - Date ranges
   - String length limits
   - Distinct value samples

2. **Type Flags**:
   - Clear indicators of column type
   - Helps prevent type-related query errors

3. **Quality Indicators**:
   - Null percentages
   - Cardinality warnings
   - Value distribution hints

4. **Operation Suggestions**:
   - Recommended transformations
   - Compatible operations