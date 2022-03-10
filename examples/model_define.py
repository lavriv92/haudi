import sys
from pathlib import Path

BASE_PATH = Path(".").absolute()

sys.path.append(str(BASE_PATH / "src"))

from haudi import BaseModel, ValidationError


class Post(BaseModel):
    title: str
    content: str

    def __repr__(self):
        return f"Post(title={self.title!r}, content={self.content!r})"


def main():
    try:
        post = Post(title="Test post title", content="Test post content")
        post.title = 12

        print(post)
    except ValidationError as e:
        print(e.json)


if __name__ == "__main__":
    main()
