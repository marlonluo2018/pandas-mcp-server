from core.metadata import read_metadata
import pprint

# Test with a sample file - replace with actual file path
#file_path = r"C:\Users\MengNingLuo\Desktop\DO288_21 Apr 2025 (1).xlsx"
file_path = r"C:\Users\MengNingLuo\Downloads\Credential T2G Report with Population Updated on 2025-06-20(2).csv"
result = read_metadata(file_path)

print("\nRaw metadata output:")
pprint.pprint(result, width=120)

print("\nType:", type(result))
print("Keys:", result.keys() if isinstance(result, dict) else "N/A")