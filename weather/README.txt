本脚本主要用于自动生成符合特定要求的html页面，供进一步处理
结果保存为html/index.html
（经过ubuntu server 10.04.1 i386 版本测试）

安装环境:　
python 2.6 版本以上

安装指南：

1、进入用户home 目录,从git服务器git源代码， 保证weather目录下有logs，
    没有则建立一个。

    cd ~
    git clone git://github.com/bailiangcn/github-example.git www
    mkdir ~/www/weather/logs

2、确认时区正确，如果错误
    ubuntu　下面手动设置时区的命令
    dpkg-reconfigure tzdata
    还需要执行下面的操作 ：
    ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
    这样的操作，可以避免系统重启后，时 间又变了的状况。

3、定义自动运行
    crontab -e 
    进入crontab设置文本,输入
    0 3 * * * cd /home/bl/www/weather/ && python /home/bl/www/weather/autowea.py

4、查看日志
    脚本会在weather/logs/目录下生成两个日志文件
    running.log  记录的是正常运行的脚本时间及进度
    weatherlog.txt 记录的是错误信息

5、主调用程序
    autowea.py
