import time


def exec_summary():
    start_time = time.time()
    time.sleep(2.1)  # 延时2.1s
    end_time = time.time()

    time.sleep(1.1)  # 延时2.1s
    end_time_again = time.time()

    exec_time = end_time - start_time
    exec_time_again = end_time_again - end_time

    print("程序运行时间：%.2f s，程序再次执行时间：%.2f s" % (exec_time, exec_time_again))  # 显示到微秒


for i in range(5):
    exec_summary()
