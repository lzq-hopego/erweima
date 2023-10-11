作者: lizhanqi    
page: github.com/lzq-hopego
开源协议: 本项目遵循mit开源协议


使用python搭建的web服务

建议使用python3.7 及 以上    （以下的操作都是基于python3.7.12的环境进行的）
数据库版本无所谓

将本项目解压出后，在项目的根目录有一个requirements.txt文件，这里面声明了本项目使用的第三库，使用pip3.7进行安装     在根目录执行pip3.7 install -r requirements.txt   等待安装完成

在启动本项目之前需要您创建一个数据库,名字可以和本项目使用的一样test_demo，然后在本项目的erweima目录下有一个名为settings.py的文件，打开文件翻到最下面，找到下面的配置，并修改成你自己的
DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME':'test_demo',      #数据库名字
    'USER': 'root',                 #数据用户名
    'PASSWORD': 'lizhanqi0228',    #数据用户密码
    'HOST': '127.0.0.1',
    'PORT': '3306',
    }
}


接下来还需要修改qr目录下的utils目录下的settings.py中的
host="http://8.130.64.173:9000/"   #你需要将你不部署项目的域名写在这里包括端口号，如果使用了反向代理，则填写反向代理后的域名


现在我们需要对项目进行初始化，在根目录执行
python3.7 ./manage.py makemigrations     #检查代码的数据，并生成相应配置
python3.7 ./manage.py migrate	     #连接数据库增删改查数据库

使用下面命令启动本项目，0.0.0.0是谁都可以访问  9000是端口，对反向代理有很大用 
python3.7 ./manage.py runserver 0.0.0.0:9000 --insecure


如果访问流量很大则需要使用uwsgi方式+nginx反向代理的方案，项目到此结束
