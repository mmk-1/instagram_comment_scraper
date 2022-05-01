class Post:
    def __init__(self, url) -> None:
        self.comments = {}
        self.url = url
    
    def addComment(self, user, content):
        self.comments[user] = content
    