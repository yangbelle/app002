import yaml, os


class GetData:

    def get_yml_data(self, name):
        """
        读取yaml文件数据
        :param name: 需要读取文件名字
        :return:
        """
        print('os.getcwd',os.getcwd())

        with open("./Data" + os.sep + name, "r") as f:
            return yaml.safe_load(f)
