# encoding=utf-8
from OnlineSession import OnlineSession


class Container(object):  # 定义顶层容器,生产工厂,是工厂的工厂,仿照协议工厂来写
    def __init__(self):
        self.servers = {}  # 定义工厂名和工厂实例的映射(并非protocol的映射)
        self.onlineSession = OnlineSession()
        # 定义在线设备映射,在buildFactory里将这个属性赋值给每个工厂实例
        # 使得每个工厂实例都具有在线设备映射
        # 即实现各个protocol可以相互通信'''

    def buildFactory(self, factoryName, instanceName, protocol):
        # 用对应协议实例化一个工厂并添加此工厂实例到servers{}映射中(并非protocol实例)
        self.servers[instanceName] = factoryName(instanceName, protocol)

        self.servers[instanceName].onlineSession = self.onlineSession

    def getFactory(self, instanceName):
        pass

    def message_children(self, name, message):
        if name in self.servers.keys():
            self.servers[name].get_message(name, message)
