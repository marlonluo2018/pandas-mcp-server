from server import run_pandas_code, load_csv_tool

def test_load_csv_tool():
    file_path = "C:\\Users\\MengNingLuo\\Desktop\\DO280 21 April.csv"
    
    result = load_csv_tool(file_path)
    print("load_csv_tool result:", result)

test_load_csv_tool()
