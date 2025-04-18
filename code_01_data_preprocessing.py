import pandas as pd
import json
from pandas import json_normalize

df=pd.read_excel(r'C:\Users\VINOTH\Documents\Sharmila_Projects\GUVI_Project_03_Old_Car_Price_Prediction\input_data\bangalore_cars.xlsx',header=[0])
df
s=df['new_car_detail'].iloc[0]
print(s)
df['new_car_detail'].iloc[0].strip('"')
s = s.replace("'", '"').replace("None", "null")
data = json.loads(s)
df_1 = pd.json_normalize(data)
print(df_1)
df_1.shape