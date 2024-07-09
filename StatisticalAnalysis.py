import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionStyle
import matplotlib.image as mpimg
import seaborn as sns
from math import radians

# خواندن فایل CSV
housing = pd.read_csv('housing_data.csv', encoding='gbk', low_memory=False)

# حذف ستون‌های مشخص
housing_dropped = housing.drop(columns=['Unnamed: 0', 'url', 'id', 'Cid'])

# نمایش تعداد داده‌های گمشده در هر ستون
housing_null = pd.DataFrame(housing_dropped.isna().sum())
# print(housing_null)

# ایجاد نسخه‌ای از داده‌ها بدون مقادیر گمشده
housing_no_missing = housing_dropped.copy()
housing_no_missing['DOM'] = housing_no_missing['DOM'].fillna(housing_no_missing['DOM'].mode()[0])
housing_no_missing = housing_no_missing.dropna(subset=['subway', 'elevator'])

# ذخیره داده‌های بدون مقادیر گمشده به فایل CSV
housing_no_missing.to_csv('housing_no_missing.csv', encoding='gbk', index=False)

#-------------------------------------------------------------------------------------#
housing_categorical = pd.read_csv('housing_no_missing.csv', encoding='gbk')

housing_categorical["elevator"] = housing_categorical["elevator"].map({1: "has elevator",
                                                                       0:"no elevator"})

housing_categorical["subway"] = housing_categorical["subway"].map({1: "has subway",
                                                                   0:"no subway"})

housing_categorical["renovationCondition"] = housing_categorical["renovationCondition"].map({1: "other",
                                                                                             2: "rough",
                                                                                             3: "Simplicity",
                                                                                             4:"hardcover"})

housing_construction = housing_categorical.copy()

housing_construction = housing_construction[housing_construction.constructionTime != '未知']
housing_construction.constructionTime = housing_construction.constructionTime.astype(int)

housing_floor = housing_construction.copy()

housing_floor['floor'] = housing_floor['floor'].str.split(" ", n = 1, expand = True)[1]
housing_floor.floor = housing_floor.floor.astype(int)

Q1 = housing_floor.totalPrice.quantile(0.25)
Q3 = housing_floor.totalPrice.quantile(0.75)
IQR = Q3 - Q1

housing_no_outlier = housing_floor.drop(housing_floor[(housing_floor.totalPrice.values < Q1-1.5*IQR) | (housing_floor.totalPrice.values > Q3+1.5*IQR)].index)

housing_no_outlier.to_csv('housing_no_outlier.csv', encoding='gbk', index=False)
#--------------------------------------------------------------------------------------#

capital_Lng = radians(116.4074)
capital_Lat = radians(39.9042)

housing_capital = housing_no_outlier.copy()

Lat = housing_capital['Lat'].apply(lambda x: radians(x))
Lng = housing_capital['Lng'].apply(lambda x: radians(x))

x = np.arccos(np.sin(Lat)*np.sin(capital_Lat) + np.cos(Lat)*np.cos(capital_Lat)*np.cos(capital_Lng-Lng))

housing_capital['distanceToCapital'] = x*6371.0088

housing_PPS = housing_capital.copy()

housing_PPS['pricePerSquare'] = (housing_PPS['totalPrice'] / housing_PPS['square']) * 1000







# نمودار هیستوگرام
fig, ax = plt.subplots(figsize=(15, 15))
housing_PPS.hist(ax=ax, bins=20)
# plt.show()  # نمایش نمودار

# نمودار رگرسیون
fig, ax = plt.subplots(figsize=(8, 8))
sns.regplot(ax=ax, data=housing_PPS, x='distanceToCapital', y='pricePerSquare',
            line_kws={'color': 'red'}, scatter_kws={'alpha': 0.1})
# plt.show()  # نمایش نمودار

# نمودار KDE برای اثر آسانسور
fig, ax = plt.subplots(figsize=(6, 6))
housing_PPS[housing_PPS.elevator == 'no elevator']['totalPrice'].plot(kind='kde', ax=ax, label='no elevator', color='blue')
housing_PPS[housing_PPS.elevator == 'has elevator']['totalPrice'].plot(kind='kde', ax=ax, label='has elevator', color='orange')
ax.legend()
ax.set_title('effect of elevator on price', color='red')
ax.set_facecolor('#ffffcc')
fig.set_facecolor('khaki')
ax.set_xlabel('pricePerSquare')
# plt.show()  # نمایش نمودار

housing_PPS.to_csv('housing_extended.csv', encoding='gbk', index=False)

# نمونه‌گیری از داده‌ها
housing_extended = housing_PPS.copy()
housing_sample = housing_extended.iloc[:-100:100]

# نمودار پراکندگی
fig, ax = plt.subplots(figsize=(10, 7))
housing_sample.plot(x='Lng', y='Lat', ax=ax, kind='scatter', alpha=0.2)
ax.axis('equal')
ax.set_title('scatter plot')
# plt.show()

# نمودار پراکندگی با رنگبندی قیمت
fig, ax = plt.subplots(figsize=(10, 7))
housing_sample.plot(x='Lng', y='Lat', ax=ax, kind='scatter', alpha=0.4,
                    c='pricePerSquare', cmap=plt.get_cmap("jet"), colorbar=True)
ax.axis('equal')

connectionstyle = ConnectionStyle("Arc3", rad=0.3)
ax.annotate('center of beijing', xy=(39.90, 116.40), xytext=(39.65, 116.6),
            arrowprops=dict(arrowstyle='fancy', connectionstyle=connectionstyle))

print(ax.texts)

# نمودار پراکندگی با اندازه متناسب با فاصله از پایتخت
fig, ax = plt.subplots(figsize=(10, 7))
housing_sample.plot(x='Lng', y='Lat', ax=ax, kind='scatter', alpha=0.2,
                    s=housing_sample['distanceToCapital'] * 4)
ax.axis('equal')

beijing_img = mpimg.imread('map1.jpg')
ax.imshow(beijing_img, extent=[115.89777890444654, 116.90711309555346, 39.5957436, 40.2840444])

# نمودار پراکندگی با نقشه
fig, ax = plt.subplots(figsize=(12.5, 7))
ax.axis("equal")
housing_sample.plot(x='Lng', y='Lat', c='district', kind='scatter',
                    s=(housing_sample['square'] / 20), cmap=plt.get_cmap('nipy_spectral'), ax=ax, alpha=0.6)
ax.imshow(beijing_img, extent=[ax.get_xlim()[0], ax.get_xlim()[1], ax.get_ylim()[0], ax.get_ylim()[1]])

# نمودار پراکندگی با فیلتر فاصله از پایتخت و نقشه
fig, ax = plt.subplots(figsize=(12.5, 7))
ax.axis("equal")
housing_sample = housing_sample[(housing_sample['distanceToCapital'] > 10) & (housing_sample['distanceToCapital'] < 30)]
beijing_img2 = mpimg.imread('map2.jpg')
housing_sample.plot(x='Lng', y='Lat', c='district', kind='scatter', ax=ax,
                    s=(housing_sample['square'] / 20), cmap=plt.get_cmap('nipy_spectral'), alpha=0.6)
ax.imshow(beijing_img2, extent=[ax.get_xlim()[0], ax.get_xlim()[1], ax.get_ylim()[0], ax.get_ylim()[1]])

plt.show()
