import threading

import itchat

import comsumer


def loginCallback():
    print("***登录成功***")


def exitCallback():
    print("***已退出***")

def login():
    itchat.auto_login(hotReload=True, enableCmdQR=2, loginCallback=loginCallback,
                      exitCallback=exitCallback)  # 首次扫描登录后后续自动登录


def callback(ch, method, properties, body):
    itchat.auto_login(hotReload=True, enableCmdQR=2)  # 首次扫描登录后后续自动登录
    users = itchat.search_friends(name='徐武强')  # 使用备注名来查找实际用户名
    # 获取好友全部信息,返回一个列表,列表内是一个字典
    print(users)
    # 获取`UserName`,用于发送消息
    userName = users[0]['UserName']
    data = body.decode("utf-8")
    itchat.send(data, toUserName=userName)

def loop():
    print('thread %s is running...' % threading.current_thread().name)
    comsumer.comsume()
    print('thread %s ended.' % threading.current_thread().name)


def start():
    login()
    print('thread %s is running...' % threading.current_thread().name)
    t = threading.Thread(target=loop, name='wechat_sender')
    t.start()
    print('thread %s ended.' % threading.current_thread().name)


if __name__ == '__main__':
    start()
