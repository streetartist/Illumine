# Illumine

[英文](https://github.com/streetartist/Illumine/Readme.md)

## Use Illumine to build any website.

# 文档
https://github.com/streetartist/Illumine/wiki

# 我们的想法
Python中一直没有像Wordpress这样的网站框架，所以我DIY了一个

目标是让用户在不修改内核代码的情况下，通过编写插件、电池、主题，来编写网站

创意：电池是事先编写好的网页框架（框架中的框架），加快编写速度

欢迎大家为Illumine编写插件电池主题！

# 项目结构

/illumine Illumine核心库

/plugin 插件

/admin 管理

/battery 电池

/engine 网页框架驱动（Flask、FastApi）

/site 站点核心代码

/theme 主题

conf.ini 配置文件

index.py 主程序

flush.py 缓存刷新

# 版本
- v 0.4.0
