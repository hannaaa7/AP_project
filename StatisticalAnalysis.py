import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sbn

# خواندن فایل CSV
housing = pd.read_csv('housing_data.csv', encoding='gbk', low_memory=False)

# چاپ اطلاعات اولیه از داده‌ها
# print(housing.shape)
# print(housing.head())

# حذف ستون‌های مشخص
housing_dropped = housing.drop(columns=['Unnamed: 0', 'url', 'id', 'Cid'])

# نمایش تعداد داده‌های گمشده در هر ستون
housing_null = pd.DataFrame(housing_dropped.isna().sum())
# print(housing_null)

# نمایش نمودار جعبه‌ای
housing_dropped.DOM.plot(kind='box')
#plt.show()  # افزودن این خط برای نمایش نمودار

# ایجاد نسخه‌ای از داده‌ها بدون مقادیر گمشده
housing_no_missing = housing_dropped.copy()
housing_no_missing['DOM'] = housing_no_missing['DOM'].fillna(housing_no_missing['DOM'].mode()[0])
housing_no_missing = housing_no_missing.dropna(subset=['subway', 'elevator'])

# چاپ اطلاعات کلی از داده‌های بدون مقادیر گمشده
# print(housing_no_missing.info())

# ذخیره داده‌های بدون مقادیر گمشده به فایل CSV
housing_no_missing.to_csv('housing_no_missing.csv', encoding='gbk', index=False)

# print(dict(housing.iloc[:,:5]))
