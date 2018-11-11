# MyBlog
###基于Python Flask与BootStrap搭建的博客
## 使用方法：
### 1、安装集成Virtualenv的pipenv 
pip install pipenv 
### 2、进入文件夹
cd myblog
### 3、为当前项目创建虚拟环境
pipenv install --dev
### 4、激活虚拟环境
pipenv shell
### 5、为当前项目创建一些虚拟数据
flask forge
### 6、运行
flask run
## 默认数据
管理员账号：super 密码：123456
## 更改管理员
flask init 后修改账号密码
