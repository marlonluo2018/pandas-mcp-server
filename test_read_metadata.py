from server import read_metadata

# Test file path
test_file = r"C:\Users\MengNingLuo\Desktop\DO288_21 Apr 2025 (1).xlsx"
#test_file = r"C:\Users\MengNingLuo\Desktop\DO280 21 April.csv"

# Run the function and print result
result = read_metadata(test_file)
print(result)
