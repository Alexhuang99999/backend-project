respuesta="y"

while respuesta=="y":
    print("-----------欢迎使用我们的程序-----------")
    print("查看自己的余额请拨号1")
    print("查看当前流量请拨号2")
    print("显示当前剩余通话请拨号3")
    print("退出程序请拨号0")
    choice=input("请输入号码:")
    if choice=="1":
        print("你的余额为200")
    elif choice=="2":
        print("你的流量为200g")
    elif choice=="3":
        print( "剩余童话为2002")
    elif choice=="0":
        print("退出程序中")
        break
    else:
        print("退出钟")
        break


