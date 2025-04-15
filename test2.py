import os
path = r"C:\Users\MengNingLuo\Desktop\DO280 21 April.csv"
print("存在性:", os.path.exists(path))
print("可读性:", os.access(path, os.R_OK))
print("绝对路径:", os.path.abspath(path))