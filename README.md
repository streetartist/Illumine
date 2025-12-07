# Illumine

一个通用的现代化网站框架。

[English README](README_EN.md)

## 项目结构

Illumine 采用了模块化的设计，旨在让开发者能够快速构建功能丰富的网站。

- **/illumine**: 核心库。包含应用程序主逻辑、引擎适配器（支持 Flask/FastAPI）、插件管理器、数据库工具、主题管理以及钩子系统。
- **/plugin**: 插件目录。用于存放扩展功能的插件（例如评论系统）。
- **/admin**: 管理后台逻辑（已集成在核心库中）。
- **/battery**: "Batteries included"（开箱即用）组件。预置了 Blog（博客）、Forum（论坛）等功能模块。
- **/website**: 网站核心代码。包含您的业务逻辑、数据模型、自定义视图以及网站专属的静态资源和模板。
- **/theme**: 主题资源。包含模板 (`templates`) 和静态文件 (`static`)。

## 快速开始

1.  **安装依赖**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **运行应用**:
    ```bash
    python app.py
    ```

3.  **访问网站**:
    - 首页: http://127.0.0.1:8000/
    - 博客 (Battery): http://127.0.0.1:8000/blog
    - 论坛 (Battery): http://127.0.0.1:8000/forum
    - 管理后台: http://127.0.0.1:8000/admin
    - 自定义页面示例: http://127.0.0.1:8000/custom

## 核心特性

### 1. 多引擎支持
Illumine 支持无缝切换底层 Web 框架。您可以在 `app.py` 初始化时指定：
```python
# 使用 Flask (默认)
app = Illumine(engine_type="flask")

# 使用 FastAPI
app = Illumine(engine_type="fastapi")
```

### 2. 强大的模块化系统 (Batteries & Plugins)
- **Batteries**: 独立的功能模块（如博客、论坛）。每个 Battery 可以拥有自己的路由、数据库模型、模板 (`templates`) 和静态文件 (`static`)。
- **Plugins**: 跨模块的扩展。插件可以监听系统钩子（Hooks），从而在不修改 Battery 代码的情况下增强功能。
    - *示例*: `plugin/comments` 插件通过监听 `post_render_content` 钩子，同时为博客和论坛添加了评论区。

### 3. 资源管理 (Static & Templates)
Illumine 自动管理和路由各模块的资源：
- **Theme**:
    - 模板: `theme/<active_theme>/templates/`
    - 静态资源: `theme/<active_theme>/static/` (自动映射到 `/static/theme`)
- **Website**:
    - 模板: `website/templates/`
    - 静态资源: `website/static/` (自动映射到 `/static/website`)
- **Battery**:
    - 静态资源映射到 `/static/battery/<name>`
- **Plugin**:
    - 静态资源映射到 `/static/plugin/<name>`

### 4. 钩子系统 (Hooks)
核心内置了 `HookManager`，允许模块间解耦交互。
```python
# 注册钩子
app.hooks.register("event_name", callback_function)

# 触发钩子
app.hooks.dispatch("event_name", data)
```

### 5. 主题与模板
基于 Jinja2 的强大模板系统。`ThemeManager` 支持多级模板查找路径，允许主主题覆盖 Battery 或 Plugin 的默认模板。

## 开发指南

### 添加新页面
在 `website/views.py` 中定义路由，并在 `app.py` 中通过 `init_website_routes(app)` 注册。

### 创建自定义 Battery
1. 在 `battery/` 下创建目录（例如 `shop`）。
2. 创建 `__init__.py` 并定义 `init_battery(app)` 函数。
3. 可选：添加 `templates` 和 `static` 目录，框架会自动加载。

### 编写插件
1. 在 `plugin/` 下创建目录。
2. 创建 `__init__.py` 并定义 `init_plugin(app)` 函数。
3. 使用 `app.hooks.register` 监听感兴趣的事件。
