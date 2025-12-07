def init_plugin(app):
    print("Comments Plugin Initialized!")
    
    # Define a callback to render comments
    def render_comments(content_id, content_type):
        # We can now link to static files provided by this plugin!
        # /static/plugin/comments/comments.css
        
        return f"""
        <link rel="stylesheet" href="/static/plugin/comments/comments.css">
        <div class="comment-box" style="padding: 10px; margin-top: 20px;">
            <h4>Comments for {content_type} #{content_id}</h4>
            <ul>
                <li>User1: Great post!</li>
                <li>User2: Thanks for sharing.</li>
            </ul>
            <form>
                <input type="text" placeholder="Add a comment...">
                <button>Post</button>
            </form>
        </div>
        """
        
    # Register the hook
    app.hooks.register("post_render_content", render_comments)
