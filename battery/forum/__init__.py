from typing import TYPE_CHECKING
from illumine.db import Base, engine, SessionLocal
from sqlalchemy import Column, Integer, String, Text

if TYPE_CHECKING:
    from illumine.core import Illumine

# --- Models ---
class ForumTopic(Base):
    __tablename__ = "forum_topics"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)

# Ensure tables exist
Base.metadata.create_all(bind=engine)

# --- Battery Init ---
def init_battery(app: 'Illumine'):
    """
    Initialize the Forum battery.
    """
    print("Initializing Forum Battery...")
    
    @app.route("/forum")
    def forum_index():
        db = SessionLocal()
        topics = db.query(ForumTopic).all()
        db.close()
        
        # Dispatch 'pre_render_topic_list' hook (if we wanted to modify topics)
        
        return app.theme_manager.render("forum/index.html", topics=topics)

    from flask import request, redirect
    
    @app.route("/forum/create", methods=["POST"])
    def create_topic():
        title = request.form.get("title")
        content = request.form.get("content")
        
        if title and content:
            db = SessionLocal()
            new_topic = ForumTopic(title=title, content=content)
            db.add(new_topic)
            db.commit()
            db.close()
            
        return redirect("/forum")

    @app.route("/forum/<int:topic_id>")
    def topic_detail(topic_id):
        db = SessionLocal()
        topic = db.query(ForumTopic).filter(ForumTopic.id == topic_id).first()
        db.close()
        
        if topic:
            # Dispatch 'post_render_content' hook
            # Plugins can return extra HTML to append
            extra_content_list = app.hooks.dispatch("post_render_content", content_id=topic_id, content_type="forum_topic")
            extra_content = "".join(extra_content_list)
            
            return app.theme_manager.render(
                "forum/detail.html", 
                topic=topic,
                extra_content=extra_content
            )
        return "Topic not found", 404
