import sys
from pathlib import Path

BASE_PATH = Path(".").absolute()

sys.path.append(str(BASE_PATH / "src"))

from haudi import BaseModel, validator, ValidationError


class Post(BaseModel):
    title: str
    content: str

    __constrants__ = {"title": []}

    @validator("title")
    def validate_start(self, value: str, **kwargs):
        if not value.startswith("b"):
            raise ValueError("Title sholud be started from b")

    @validator("title")
    def validate_title(self, value, **kwargs):
        if len(value) < 6:
            raise ValueError(f"Length of title shold be at least then 5")

    def __repr__(self):
        return f"Post(title={self.title!r}, content={self.content!r})"


def main():
    try:
        post = Post(title="bTest post title", content="Test post content")
        post.title = "bTest post"

        post.save()

        print("Saved post: ", post.dict)
    except ValidationError as e:
        print(e.json)


if __name__ == "__main__":
    main()
