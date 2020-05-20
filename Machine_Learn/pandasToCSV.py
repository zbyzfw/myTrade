import pandas as pd


class SaveCsv:

    def __init__(self):
        self.clist = [[1,2,3], [4,5,6], [7,8,9]]

    def savefile(self, my_list):
        """
        把文件存成csv格式的文件，header 写出列名，index写入行名称
        :param my_list: 要存储的一条列表数据
        :return:
        """
        df = pd.DataFrame(data=[my_list])
        df.to_csv("./Test.csv", encoding="utf-8-sig", mode="a", header=False, index=False)

    def saveAll(self):
        """
        一次性存储完
        :return:
        """
        pf = pd.DataFrame(data=self.clist)
        pf.to_csv("./Test_1.csv", encoding="utf-8-sig", header=False, index=False)


    def main(self):
        nameList = ["beijing", "shanghai", "guangzhou", "shenzhen", "xiongan", "zhengzhou"]
        # start表示循环从1开始计数
        for num, data in enumerate(nameList, start=1):
            if num % 2 == 0:
                self.savefile(["成功", data, num])
            else:
                self.savefile(["失败", data, num])
        return 0

if __name__ == '__main__':
    sc = SaveCsv()
    sc.main()
    sc.saveAll()