import socket
import sys
if len(sys.argv) < 3 or len(sys.argv) > 4:#根据题目要求把host port path加进去，然后如果参数大于4就拦截
    print("用法: python webget.py <host> <path> [port]")
    print("例如: python webget.py www.bjfu.edu.cn / 80")
    sys.exit()#根据要求把参数host path 和port变成可选的，然后依照要求完成“参数不足时打印用法并退出”
host = sys.argv[1]#拿到第一个参数
path = sys.argv[2]#拿到第二个参数
port = int(sys.argv[3]) if len(sys.argv) == 4 else 80 #如果传了第四个参数就是port，不然就是默认的80
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)#根据要求设置settimeout为10
s.connect((host, port))#把写死的换成变量（host，port）
request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"#把写死的请求报文改成f-string进行动态拼接
s.sendall(request.encode())#加上.encode把字符串变成字节串

total_data = b"" #初始化一个空的字节串来把recv接受的的每一小块结合起来
recv_count = 0#用来记录recv一共调用了多少次
while True:#开启循环
    chunk = s.recv(4096)#从TCP缓冲区里面读数据，最多读4096个字节，然后赋值给chunk
    if not chunk: 
        print("\n[TCP 连接已由服务器关闭，接收结束]")
        break#如果chunk为空，也就是服务器把所有数据都发完了然后执行完了TCP挥手，recv此时就会收到空的字节串b""，然后就会打印提示并且跳出循环
    recv_count += 1
    total_data += chunk#把这次循环接收到的一小块chunk，全部拼接到total_data后面，也就是在还原TCP的字节流
    print(f"第 {recv_count} 次 recv，收到 {len(chunk)} 字节")
s.close() #关闭套接字，释放端口
print(f"总长度: {len(total_data)} 字节")#满足要求，打印完整的响应
header_data, _, body_data = total_data.partition(b'\r\n\r\n')#用\r\n\r\n把网页切割成头部和身体
header_text = header_data.decode('utf-8', errors='ignore')#把头部转换成文字格式便于打印

status_line = header_text.split('\r\n')[0]
print(f"\n--- 状态行 ---\n{status_line}")#提取状态行，然后打印
print(f"\n--- 全部响应头 ---\n{header_text}")#打印响应头
with open("output.html", "wb") as f:
    f.write(body_data)
print("\n网页正文已保存到 output.html 文件中！")#把身体保存成二进制模式的文件