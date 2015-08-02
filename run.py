# encoding=utf-8
from echo import EchoFactory
from Container import Container
from RFIDFactory import RFIDFactory
from RFIDProtocol import RFIDProtocol
from twisted.internet.serialport import SerialPort
from txsockjs.factory import SockJSResource
from twisted.internet import reactor

from flask import Flask, render_template
from echo import EchoProtocol

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


from flask.ext.twisted import Twisted

twisted = Twisted(app)

container = Container()  # 实例化一个工厂容器

container.buildFactory(RFIDFactory, 'RFID', RFIDProtocol)  # 创建一个名字是rfid的RFIDFactory工厂实例
container.buildFactory(EchoFactory, 'echo', EchoProtocol)  # 创建一个名字是echo的EchoFactory工厂实例

twisted.add_resource("echo", SockJSResource(container.servers['echo']))

SerialPort(RFIDProtocol(container.servers['RFID']), '/dev/ttyUSB0', reactor, baudrate=38400)  # '/dev/ttyUSB0'
# twisted老套路(端口号,工厂)
reactor.listenTCP(8001, container.servers['echo'])

if __name__ == '__main__':
    print 'reactor begin to run '
    app.run()
