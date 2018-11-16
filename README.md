# MyBlog
### --基于Python Flask与BootStrap搭建的博客
------Python版本：3.6.3
## 使用方法：
### 1、安装集成Virtualenv的pipenv 
pip install pipenv 
### 2、进入文件夹
cd Myblog
### 3、为当前项目创建虚拟环境
pipenv install --dev
### 4、激活虚拟环境
pipenv shell
### 5、为当前项目创建一些虚拟数据
flask forge
### 6、运行
flask run
## 默认生成的虚拟数据的虚拟管理员
管理员账号：super 密码：123456
## 当不需要虚拟数据测试时，可以直接生成干净的博客界面
### 1、激活虚拟环境
pipenv shell
### 2、清空当前数据库
flask initdb --drop
### 3、创建管理员账号
flask init
### 运行
flask run
