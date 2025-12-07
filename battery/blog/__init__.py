from typing import TYPE_CHECKING
from illumine.db import Base, engine, SessionLocal
from sqlalchemy import Column, Integer, String, Text

if TYPE_CHECKING:
    from illumine.core import Illumine

# --- Models ---
class BlogPost(Base):
    __tablename__ = "blog_posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)

# Ensure tables exist
Base.metadata.create_all(bind=engine)

# --- Battery Init ---
def init_battery(app: 'Illumine'):
    """
    Initialize the Blog battery.
    """
    print("Initializing Blog Battery...")
    
    @app.route("/blog")
    def blog_index():
        db = SessionLocal()
        posts = db.query(BlogPost).all()
        db.close()
        
        return app.theme_manager.render("blog/index.html", posts=posts)

    from flask import request, redirect
    
    @app.route("/blog/create", methods=["POST"])
    def create_post():
        title = request.form.get("title")
        content = request.form.get("content")
        
        if title and content:
            db = SessionLocal()
            new_post = BlogPost(title=title, content=content)
            db.add(new_post)
            db.commit()
            db.close()
            
        return redirect("/blog")

    @app.route("/blog/<int:post_id>")
    def blog_detail(post_id):
        db = SessionLocal()
        post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
        db.close()
        
        if post:
            # Dispatch hook for plugins (like comments)
            extra_content_list = app.hooks.dispatch("post_render_content", content_id=post_id, content_type="blog_post")
            extra_content = "".join(extra_content_list)
            
            return app.theme_manager.render(
                "blog/detail.html", 
                post=post, 
                extra_content=extra_content
            )
        return "Post not found", 404
