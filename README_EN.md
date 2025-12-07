# Illumine

A general-purpose website framework.

[中文文档](README.md)

## Project Structure

- **/illumine**: Core library containing the main application logic, engine adapters (Flask/FastAPI), plugin manager, and database utilities.
- **/plugin**: Directory for extension plugins.
- **/admin**: Admin interface logic.
- **/battery**: "Batteries included" - pre-built components like Blog, Forum, etc.
- **/website**: Site core code and content management.
- **/theme**: Theme assets and templates.

## Getting Started

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Application**:
    ```bash
    python app.py
    ```

3.  **Access the Site**:
    - Home: http://127.0.0.1:8000/
    - Blog: http://127.0.0.1:8000/blog
    - Admin: http://127.0.0.1:8000/admin
    - Plugin Demo: http://127.0.0.1:8000/plugin/hello

## Features

- **Multi-Engine Support**: Switch between Flask and FastAPI by changing `engine_type` in `app.py`.
- **Plugin System**: Drop plugins into the `plugin/` directory.
- **Batteries**: Modular feature sets (e.g., Blog) that can be loaded on demand.
- **Theming**: Jinja2-based theme support.
- **Database**: SQLAlchemy integration built-in.
