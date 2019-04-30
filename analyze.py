import time
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import jieba
import wordcloud
import seaborn
import pandas as pd

local_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 获取时间
filename = '2019-04-28xm_fish.csv'

plt.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
plt.rcParams['font.size'] = 15

data = \
    pd.read_csv(
        filename,
        names=['房源名称', '租赁种类', '房源类型', '房源户型', '房源面积', '房源楼层', '房源朝向', '装修等级', '房源地址', '行政区划', '房源租金', '所在小区', '房源描述', '更新时间'],
        keep_default_na=False,
        index_col=False
    )
invalid_list = data.loc[data['房源面积'] == 0]
data = data.drop(index=invalid_list.index)

invalid_list2 = data.loc[data['房源租金'] > 20000]
data = data.drop(index=invalid_list2.index)

# print(data.drop(invalid_list))
# district_count = data['行政区划'].value_counts()
# plt.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
# asd, sdf = plt.subplots(1, 1, dpi=200)  # 设置画布
# # district.head(2500).plot(kind='bar', x='zone', y='size', title='房源数量分布', ax=sdf)
# district_count.plot()
# plt.legend(['数量（单位：套）'])

# house_type = data['房源类型'].value_counts()
# asd1, sdf1 = plt.subplots(1, 1, dpi=200)  # 设置画布
# house_type.head(2500).plot(kind='bar', x='zone', y='size', title='房源数量分布', ax=sdf1)  # 获取前10条数据
# plt.legend(['数量（单位：套）'])
# plt.plot(data['房源类型'], data['行政区划'])
# # plt.show()
#
# square = data['房源面积']
# rent = data['房源租金']
#
# fig = plt.figure(figsize=(25, 10))
# sns = pd.DataFrame(data, columns=['房源面积', '房源租金'])
# seaborn.regplot('房源面积', '房源租金', data=sns)
# plt.xlabel('房屋面积')
# plt.ylabel('房屋租金')
# fig.autofmt_xdate()
# # plt.show()
#
# fig = plt.figure(figsize=(25, 10))
# sns = pd.DataFrame(data, columns=['房源租金', '房源楼层'])
# seaborn.regplot('房源租金', '房源楼层', data=sns)
# plt.xlabel('房源租金')
# plt.ylabel('房源楼层')
# fig.autofmt_xdate()
#
# # title,price,size,block,type
# fig = plt.figure(figsize=(30, 10))
# plt.subplot(1, 2, 1)  # 一行两列第一个图
# square = data['房源面积']
# price = data['房源租金']
# plt.scatter(square, price)
# plt.xlabel('房屋面积')
# plt.ylabel('价格')
#
# plt.subplot(1, 2, 2)  # 一行两列第一个图
# plt.title('面积统计', fontsize=20, )
# plt.hist(square, bins=15)  # bins指定有几条柱状
# plt.xlabel('房屋面积')
# fig.autofmt_xdate()

# 房屋类型和价格的分析
# fig = plt.figure(figsize=(30, 10))
# plt.subplot(1, 2, 1)  # 一行两列第一个图
# layout = data['房源户型']
# # type = list(type)
# rent = data['房源租金']
# plt.scatter(layout, rent)
# plt.xlabel('房屋类型')
# plt.ylabel('价格')

# plt.subplot(1, 2, 2)  # 一行两列第一个图
# plt.title('类型统计', fontsize=20, )
# layout.value_counts().plot(kind='bar', )  # 绘制条形图
# plt.xlabel('房屋类型')
# fig.autofmt_xdate()
# plt.show()

# 生成一个三维坐标图 租金 面积以及所处于的行政区划
# 观察这个坐标图是否能够运用于KMeans聚类算法


# fig = plt.figure()
# ax = Axes3D(fig)
# rent = data['房源租金']
# square = data['房源面积']
# district = data['行政区划']
# ax.scatter(rent, square)
# fig.autofmt_xdate()

# 生成词云
#
# name = data['房源名称']
# desc = data['房源描述']
#
# # color_mask = imread("123.jpg")  # 读取背景图片，
#
# name = str(name)
# desc = str(desc)
# for ch in "'\n'' '！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜>｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.":
#     name = name.replace(ch, "")
#     desc = desc.replace(ch, "")
#
# ls = jieba.lcut(name) + jieba.lcut(desc)
# txt = " ".join(ls)
# a = wordcloud.WordCloud(font_path="simkai.ttf", width=1000, height=700, background_color="black")
# a.generate(txt)
# a.to_file("title.png")

# plt.scatter(data['房源楼层'], data['房源租金'])
# direction = data['房源朝向']
# plt.scatter(direction, data['房源租金'])
# plt.show()
#
# district_count = data['行政区划'].value_counts()
# top_3_district_count = district_count[:3]
# seaborn.barplot(x=top_3_district_count.index, y=top_3_district_count.value)
# plt.show()
# plt.scatter(data['装修等级'], data['房源租金'])
# plt.show()
# plt.scatter(data['所在小区'], data['房源租金'])
# plt.show()
# plt.scatter(data['房源面积'], data['房源租金'])
# plt.show()


# print(data['房源租金'].loc[data['行政区划'] == '集美'].mean())
# print(data['房源租金'].loc[data['行政区划'] == '集美'].max())
# print(data['房源租金'].loc[data['行政区划'] == '集美'].min())

# print(data.corr())
# print(data.describe())

print(data['所在小区'].value_counts())
print(type(data['所在小区'].value_counts().index))
# print(data['所在小区'].value_counts().value)

# print(data['房源租金'].loc[data['行政区划'] == '湖里'].mean())
# print(data['房源租金'].loc[data['行政区划'] == '湖里'].loc[data['租赁种类'] == '整租'].mean())
# print(data['房源租金'].loc[data['行政区划'] == '湖里'].loc[data['租赁种类'] == '合租'].mean())
# print(data['房源租金'].loc[data['行政区划'] == '湖里'].loc[data['房源类型'] == '普通住宅'].mean())
# print(data['房源租金'].loc[data['行政区划'] == '湖里'].loc[data['房源类型'] == '公寓'].mean())
# print(data['房源租金'].loc[data['行政区划'] == '湖里'].max())
# print(data['房源租金'].loc[data['行政区划'] == '湖里'].min())

# print(data['房源租金'].loc[data['行政区划'] == '思明'].mean())
# print(data['房源租金'].loc[data['行政区划'] == '思明'].max())
# print(data['房源租金'].loc[data['行政区划'] == '思明'].min())
