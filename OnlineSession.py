# encoding=utf-8
'''这个类中的get_online_session()方法在当前的所有程序中并没有用到
全是通过self.online_session的字典取值来使用了,所以这个属性要进行封装使得外界通过接口进行获取'''


class OnlineSession(object):
    def __init__(self):
        self.online_session = {}  # 在线设备列表字典,其中存储的是各个protocol的实例名+端口号

    def get_online_session(self, divName):
        '''从在线设备列表中获取实例是divName设备对象'''
        # print self.online_session
        if self.online_session.get(divName) is None:
            print "没有找到您的设备!"
            return None
        else:
            print "您得到的设备是:" + divName
            return self.online_session.get(divName)

    def add_client(self, divname, transport):
        '''将设备的端口号存到在线设备列表中,因为是用端口号来区分不同的端口设备的'''
        self.online_session[divname] = transport
        print "您现在正在使用的设备有: "
        print self.online_session
        print '\n'

    def del_client(self, name):
        '''从在线设备列表里面删除这个设备'''
        if self.online_session.get(name):
            print "您要删除的设备是:" + name
            del self.online_session[name]
        else:
            print "您要删除的设备不存在"
        print "您现在正在的设备有: "
        print self.online_session
        print '\n'
