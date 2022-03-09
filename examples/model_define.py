import sys
from pathlib import Path

BASE_PATH = Path(".").absolute()

sys.path.append(str(BASE_PATH / "src"))

from haudi import BaseModel, ValidationError


def main():
    class Post(BaseModel):
        title: str
        content: str

        def __repr__(self):
            return f"Post(title={self.title!r}, content={self.content!r})"

    try:
        post = Post(title="Test post title", content="Test post content")
        post.title = "Hello world"
        
        print(post)
    except ValidationError as e:
        print(e.json)

if __name__ == '__main__':
    main()