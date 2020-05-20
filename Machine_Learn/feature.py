from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.feature_selection import VarianceThreshold
from sklearn.decomposition import PCA
import jieba
import numpy as np

"""
特征处理方式
1,归一化. 2,标准化 3,缺失值处理 4,one-hot编码 5,时间排序
fit输入数据(同时计算平均值及标准差等数据)transform转化数据(使用上一个fit输入数据的平均值标准差) 
"""
# 特征抽取
#
# 导入包
# from sklearn.feature_extraction.text import CountVectorizer
#
# # 实例化CountVectorizer
#
# vector = CountVectorizer()
#
# # 调用fit_transform输入并转换数据
#
# res = vector.fit_transform(["life is short,i like python","life is too long,i dislike python"])
#
# # 打印结果
# print(vector.get_feature_names())
#
# print(res.toarray())

def dictvec():
    """
    字典数据抽取
    :return: None
    """
    # 实例化
    dict = DictVectorizer(sparse=False)#实例化字典特征抽取类默认sparse=True,表示转化为sparse矩阵,否则转化为数组
    # sparse 稀疏矩阵(有值的项比无值多的矩阵),将矩阵中有值的位置用坐标表示出来.例如:  (0,1) 100 第零行第一列的值为100
    # 调用fit_transform,将字典数据返回为sparse矩阵
    data = dict.fit_transform([{'city': '北京','temperature': 100}, {'city': '上海','temperature':60}, {'city': '深圳','temperature': 30}])

    print(dict.get_feature_names())#把字典中类别的数据分别转换为特征

    print(dict.inverse_transform(data))#逆转化,返回fit.transform转化之前的数据

    print(data)

    return None

def countvec():
    """
    对文本进行特征值化
    :return: None
    """
    cv = CountVectorizer()

    data = cv.fit_transform(["人生 苦短，我 喜欢 python", "人生漫长，不用 python"])

    print(cv.get_feature_names())#统计以上文章中出现的所有词汇,重复的只看作一次,并用列表展示(单个字母不统计)

    print(data.toarray())#功能类似于sparse=false
    #返回数组,显示get_feature_names()函数获得的词汇列表中各个词汇的出现次数
    return None

def cutword():
    #返回字符串
    con1 = jieba.cut("今天很残酷，明天更残酷，后天很美好，但绝对大部分是死在明天晚上，所以每个人不要放弃今天。")

    con2 = jieba.cut("我们看到的从很远星系来的光是在几百万年之前发出的，这样当我们看到宇宙时，我们是在看它的过去。")

    con3 = jieba.cut("如果只用一种方式了解某样事物，你就不会真正了解它。了解事物真正含义的秘密取决于如何将其与我们所了解的事物相联系。")

    # 转换成列表
    content1 = list(con1)
    content2 = list(con2)
    content3 = list(con3)
    print(content1)
    # 吧列表转换成字符串,并添加空格
    c1 = ' '.join(content1)
    c2 = ' '.join(content2)
    c3 = ' '.join(content3)

    return c1, c2, c3



def hanzivec():
    """
    中文特征值化,和英文基本相同
    :return: None
    """
    c1, c2, c3 = cutword()

    print(c1, c2, c3)

    cv = CountVectorizer()

    data = cv.fit_transform([c1, c2, c3])

    print(cv.get_feature_names())

    print(data.toarray())

    return None


#朴素贝叶斯tf-idf,tf:词的频率,idf:逆文档频率 log(总文档数量/该词出现的文档数量)人话:该词出现的文档数量越多,频率趋近于零,越少越趋近于1
#tf乘以idf,得出该词的重要性
def tfidfvec():
    """
    中文特征值化(使用朴素贝叶斯算法)
    :return: None
    """
    c1, c2, c3 = cutword()

    print(c1, c2, c3)

    tf = TfidfVectorizer()#实例化tfidf算法对象

    data = tf.fit_transform([c1, c2, c3])

    print(tf.get_feature_names())#得出所有不重复词的列表

    print(data.toarray())#得出词汇重要性的计算结果

    return None

#归一化容易受到异常点的影响,使这种算法的鲁棒性(稳定性)较差,只适合传统的精确小数据场景
def mm():
    """
    归一化处理,将数据缩小到零到1之间,计算时每列单独计算为一组特征值,每列最大值计算为1,最小值计算为0
    :return: NOne
    """
    mm = MinMaxScaler(feature_range=(2, 3))#默认参数feature_range=(0,1)缩放范围为(0,1)

    data = mm.fit_transform([[90,2,10,40],[60,4,15,45],[75,3,13,46]])

    print(data)

    return None

#标准化算法:(x-平均值)/标准差,标准差:方差开根号,方差:每个数据-平均值结果的平方除以样本数,
#数据越集中,方差越小,数据越分散,方差越大
#同样作用于每一列
def stand():
    """
    标准化缩放
    :return:
    """
    std = StandardScaler()

    data = std.fit_transform([[ 1., -1., 3.],[ 2., 4., 2.],[ 4., 6., -1.]])

    print(data)

    return None


def im():
    """
    缺失值处理 1,删除 2,插补
    :return:NOne
    """
    # NaN, nan
    im = SimpleImputer(missing_values=np.nan, strategy='mean', axis=0)#指定缺失值的位置NaN,填补策略平均值,按列填补平均值
    #缺失数据必须为np.nan格式(flaot),可以使用np.replace(?,nan)替换
    data = im.fit_transform([[1, 2], [np.nan, 3], [7, 6]])

    print(data)

    return None

#数据降维
def var():
    """
    特征选择-删除低方差的特征..
    :return: None
    """
    var = VarianceThreshold(threshold=1.0)#参数指定方差的大小,默认为0

    data = var.fit_transform([[0, 2, 0, 3], [0, 1, 4, 3], [0, 1, 1, 3]])

    print(data)
    #会把第一列和第四列相同的列删除
    return None


def pca():
    """
    主成分分析进行特征降维,类似于矩阵中秩的概念
    :return: None
    """
    pca = PCA(n_components=0.9)#至少保存90%数据

    data = pca.fit_transform([[2,8,4,5],[6,3,0,8],[5,4,9,1]])

    print(data)

    return None


if __name__ == "__main__":
    #pca()
    cutword()