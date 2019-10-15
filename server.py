from sanic import Sanic
from sanic_cors import CORS, cross_origin
from sanic.response import json
import pathlib
import random
from conf import config
from git import Repo

root_path = pathlib.Path(config.root_git_path)

if not root_path.exists():
    Repo.clone_from(config.root_git_url, root_path)
else:
    Repo(root_path).git().pull()

app = Sanic(__name__)
CORS(app)


@app.route("api/random_code", methods=["GET", "OPTIONS"])
async def random_code(request):
    target = random.choice(list(pathlib.Path(config.root_file).glob("**/*.md")))
    with target.open("r") as md:
        data = md.read().split("- ")[1:]
        description, code = random.choice(data).strip().split("\n\n")
        return json(
            dict(
                zip(
                    ("system", "type", "description", "code"),
                    (target.parent.name, target.name, description[:-1], code[1:-1]),
                )
            )
        )


if __name__ == "__main__":
    app.run(host=config.ip, port=config.port)
