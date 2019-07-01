# -*- coding:utf-8 -*-

class ReadFileInList(object):
    """
    将文件每行的内容按列表返回
    """

    def __init__(self):
        pass

    def read_file(self, file_path):
        file = open(file_path, encoding='utf-8')
        file_list = []
        for line in file.readlines():
            line = line.strip('\n')
            file_list.append(line)
        return file_list
        pass
