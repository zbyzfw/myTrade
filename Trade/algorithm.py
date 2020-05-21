from sklearn.datasets import load_iris, fetch_20newsgroups, load_boston#sklearn中自带的数据集
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

def datasetDemo():
    li = load_iris()#直接实例化数据集,返回一个字典格式

    print("获取特征值")
    print(li.data)
    # print("目标值")
    print(li.target)
    print(li.DESCR)
    #li.DESCR,li.feature_names,li.target_names描述,特征名,标签名
    # 注意返回值, 训练集 train  特征值x_train, 目标值y_train        测试集  test   特征值x_test, 目标值y_test
    x_train, x_test, y_train, y_test = train_test_split(li.data, li.target, test_size=0.25)#返回数据顺序不能错
    #test_size参数测试集所占大小.代表25%
    print("训练集特征值和目标值：", x_train, y_train)
    print("测试集特征值和目标值：", x_test, y_test)
    fit(x_train, y_train)#输入训练集
    y_predict = predict(x_test)#获得特征值x_test的目标值
    score(x_test,y_test)#得到预测的准确率

    news = fetch_20newsgroups(subset='all')
    #
    print(news.data)
    print(news.target)
    #
    lb = load_boston()
    #
    print("获取特征值")
        # print(lb.data)
    print("目标值")
    print(lb.target)
    print(lb.DESCR)
    return None


def knncls():
    """
    K-近邻算法 预测用户签到位置,算法:(a-b)^2+(c-d)^2开根号
    :return:None
    """
    # 读取数据
    data = pd.read_csv("./data/FBlocation/train.csv")

    # print(data.head(10))

    # 处理数据
    # 1、缩小数据,按x,y坐标位置缩小,使用pd中的query函数
    data = data.query("x > 1.0 &  x < 1.25 & y > 2.5 & y < 2.75")

    # 处理时间戳(python中的时间戳:import time ; time.time())
    time_value = pd.to_datetime(data['time'], unit='s')

    print(time_value)

    # 把日期格式转换成 字典格式
    time_value = pd.DatetimeIndex(time_value)

    # 构造一些特征
    data['day'] = time_value.day
    #data.loc(:,day) = time_value.day
    data['hour'] = time_value.hour
    data['weekday'] = time_value.weekday

    # 把时间戳特征删除
    data = data.drop(['time'], axis=1)#pandas中0表示列,sklearn中1表示列

    print(data)

    # 把签到数量少于n个目标位置删除
    place_count = data.groupby('place_id').count()#返回索引列为place_id,其他列统计次数的表

    tf = place_count[place_count.row_id > 3].reset_index()#reset_index()将行索引按1,2,3,4,5重设

    data = data[data['place_id'].isin(tf.place_id)]#将data中的place_id与tf中的取交集

    # 取出数据当中的特征值和目标值
    y = data['place_id']#place_id列为目标值

    x = data.drop(['place_id'], axis=1)#其他列为特征值

    # 进行数据的分割训练集合测试集
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

    # 特征工程（标准化）
    std = StandardScaler()

    # 对测试集和训练集的特征值进行标准化
    x_train = std.fit_transform(x_train)

    x_test = std.transform(x_test)

    # 进行算法流程 # 超参数
    knn = KNeighborsClassifier()#参数n_neighbor= 去邻居的个数,越小越容易收到异常点的影响

    # # fit， predict,score
    # knn.fit(x_train, y_train)
    #
    # # 得出预测结果
    # y_predict = knn.predict(x_test)
    #
    # print("预测的目标签到位置为：", y_predict)
    #
    # # 得出准确率
    # print("预测的准确率:", knn.score(x_test, y_test))#结果为百分之二,预测失败

    # 构造一些参数的值进行搜索,算法的调参
    param = {"n_neighbors": [3, 5, 10]}

    # 进行网格搜索
    gc = GridSearchCV(knn, param_grid=param, cv=2)

    gc.fit(x_train, y_train)

    # 预测准确率
    print("在测试集上准确率：", gc.score(x_test, y_test))

    print("在交叉验证当中最好的结果：", gc.best_score_)

    print("选择最好的模型是：", gc.best_estimator_)

    print("每个超参数每次交叉验证的结果：", gc.cv_results_)

    return None


def naviebayes():
    """
    朴素贝叶斯进行文本分类,不需要调参,算法固定,缺点:训练集误差大效果不好,
    :return: None
    """
    news = fetch_20newsgroups(subset='all')

    # 进行数据分割
    x_train, x_test, y_train, y_test = train_test_split(news.data, news.target, test_size=0.25)

    # 对数据集进行特征抽取
    tf = TfidfVectorizer()

    # 以训练集当中的词的列表进行每篇文章重要性统计['a','b','c','d']
    x_train = tf.fit_transform(x_train)

    print(tf.get_feature_names())

    x_test = tf.transform(x_test)#统计测试集中的词汇

    # 进行朴素贝叶斯算法的预测
    mlt = MultinomialNB(alpha=1.0)#alpha拉普拉斯平滑系数

    print(x_train.toarray())

    mlt.fit(x_train, y_train)

    y_predict = mlt.predict(x_test)

    print("预测的文章类别为：", y_predict)

    # 得出准确率
    print("准确率为：", mlt.score(x_test, y_test))

    print("每个类别的精确率和召回率：", classification_report(y_test, y_predict, target_names=news.target_names))

    return None


def decision():
    """
    决策树对泰坦尼克号进行预测生死
    :return: None
    """
    # 获取数据
    titan = pd.read_csv("http://biostat.mc.vanderbilt.edu/wiki/pub/Main/DataSets/titanic.txt")

    # 处理数据，找出特征值和目标值
    x = titan[['pclass', 'age', 'sex']]

    y = titan['survived']

    print(x)
    # 缺失值处理
    x['age'].fillna(x['age'].mean(), inplace=True)

    # 分割数据集到训练集合测试集
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

    # 进行处理（特征工程）特征-》类别-》one_hot编码
    dict = DictVectorizer(sparse=False)

    x_train = dict.fit_transform(x_train.to_dict(orient="records"))

    print(dict.get_feature_names())

    x_test = dict.transform(x_test.to_dict(orient="records"))

    # print(x_train)
    # 用决策树进行预测
    # dec = DecisionTreeClassifier()
    #
    # dec.fit(x_train, y_train)
    #
    # # 预测准确率
    # print("预测的准确率：", dec.score(x_test, y_test))
    #
    # # 导出决策树的结构
    # export_graphviz(dec, out_file="./tree.dot", feature_names=['年龄', 'pclass=1st', 'pclass=2nd', 'pclass=3rd', '女性', '男性'])

    # 随机森林进行预测 （超参数调优）
    rf = RandomForestClassifier()

    param = {"n_estimators": [120, 200, 300, 500, 800, 1200], "max_depth": [5, 8, 15, 25, 30]}

    # 网格搜索与交叉验证
    gc = GridSearchCV(rf, param_grid=param, cv=2)

    gc.fit(x_train, y_train)

    print("准确率：", gc.score(x_test, y_test))

    print("查看选择的参数模型：", gc.best_params_)

    return None


if __name__ == "__main__":
    decision()

