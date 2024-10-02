# 项目来源
这是给广州一家外贸企业制作的，轮换切换浏览器指纹，并点击链接以提高产品点击率的脚本，虽然也不清楚是否真的有用。。。
# 使用
- 本环境依赖于python3.11.9，先使用pyenv安装，并指定py版本
- 执行`pdm init`
- 执行`pdm add` 安装依赖
- 打包`pdm run pyinstaller -F testsel.py`

# 文件介绍
testsel.py 是入口文件
up_ads.bat 是启动文件
关键字.txt  配置了要搜索的关键字，匹配的网址，循环的次数
goto.py    是跳出while循环的goto
unuse目录   是以前的一些模块，后来没用上，不知道以后是否有用就没删掉