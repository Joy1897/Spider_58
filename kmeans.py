import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt


def kmeans():
    data = \
        pd.read_csv(
            '2019-04-28xm_fish.csv',
            names=['房源名称', '租赁种类', '房源类型', '房源户型', '房源面积', '房源楼层', '房源朝向', '装修等级', '房源地址', '行政区划', '房源租金', '所在小区', '房源描述', '更新时间'],
            keep_default_na=False,
            index_col=False
        )
    invalid_list = data.loc[data['房源面积'] == 0]
    data = data.drop(index=invalid_list.index)

    invalid_list2 = data.loc[data['房源租金'] > 20000]
    data = data.drop(index=invalid_list2.index)
    data1 = data.iloc[:, [4, 10]]

    km = KMeans(n_clusters=2, max_iter=500)
    cluster_result = km.fit(data1)
    # print(cluster_result.inertia_)
    y_pred = cluster_result.labels_
    predict = km.predict(data1)

    color = ['red', 'green', 'blue', 'black', 'orange']

    predict = [color[i] for i in predict]

    plt.scatter(data1['房源面积'], data1['房源租金'], c=predict)
    silhouette = silhouette_score(data1, y_pred)
    print(silhouette)
    plt.show()

    # # 尝试归纳户型与租金的关系
    # data2 = data.iloc[:, [3, 10]]
    # km_ = KMeans(n_clusters=2, max_iter=500)
    # cluster_result_ = km_.fit(data2)
    # # print(cluster_result.inertia_)
    # y_pred_ = cluster_result.labels_
    # predict_ = km.predict(data2)
    #
    # predict_ = [color[i] for i in predict_]
    #
    # plt.scatter(data2['房源面积'], data2['房源租金'], c=predict_)
    # silhouette = silhouette_score(data2, y_pred_)
    # print(silhouette)
    # plt.show()


if __name__ == '__main__':
    kmeans()

# kmeans对初始值的稳定性较差
# input_file = 'a.csv'
# output_file = 'out.csv'
#
# k = 3
# iteration = 500
# data = pd.read_csv(input_file, index_col='Id')
# data_zs = 1.0 * (data - data.mean()) / data.std()
#
# model = KMeans(n_clusters=k, n_jobs=2, max_iter=iteration)
# model.fit(data_zs)
#
# r1 = pd.Series(model.labels_).value_counts()
# r2 = pd.DataFrame(model.cluster_centers_)
# r = pd.concat([r2, r1], axis=1)
# r.columns = list(data.columns) + [u'类别数目']
# print(r)
#
# r = pd.concat([data, pd.Series(model.labels_, index=data.index)], axis=1)
# r.columns = list(data.columns) + [u'聚类类别']
# r.to_csv(output_file)
