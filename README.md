## flask restful风格的开发框架

>基于flask的restful风格的web服务端开发框架，一种用于mobile端（jwt方式）应用的开发；
>另一种用于pc端后台管理系统（session的方式）的开发。  
>可用于服务端开发的脚手架工程。


项目的基本结构如下：
```
flask-demo  
├── common -- 通用类包
├── config -- 配置类包  
├── jobs -- 定时任务类包  
├── service -- service类包   
├── models -- po类包
├── validators -- 表单验证处理包
├── web -- web包
|     ├── controllers  --controllers包
|     └── api --api接口
├── application.py --封装flask全局变量，包括app、数据库等，是项目的核心类
├── manager.py -- 项目入口文件
├── www.py -- 蓝图注册统一管理
└── docs --文档包

```