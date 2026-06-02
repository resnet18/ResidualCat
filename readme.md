# ResidualCat

> 开发代号：rescat  
> 一个轻量多模态验证原型，以桌宠形式实现。

rescat/
├── frontend/                    # Astro 前端
│   ├── src/
│   │   └── pages/
│   │       └── assignment4.astro   # 主页面
│   ├── public/                  # 静态资源
│   │   ├── rescat_idle.png
│   │   ├── rescat_process.png
│   │   ├── rescat_skip.png
│   │   ├── rescat_vanish.png
│   │   └── rescat_converge.png
│   ├── astro.config.mjs
│   └── package.json
│
├── backend/                     # FastAPI 后端
│   ├── main.py                  # 核心：ResCat Brain + API
│   ├── requirements.txt
│   └── Dockerfile               # 可选，Render 部署用
│
├── docs/                        # 作业文档
│   └── dev_log.md               # 开发日志（AI 交互记录）
│
└── README.md                    # 项目说明