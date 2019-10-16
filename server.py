import pathlib
import random

from git import Repo
from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS, cross_origin
from ua_parser import user_agent_parser

from conf import config
from itertools import chain

root_path = pathlib.Path(config.root_git_path)

if not root_path.exists():
    Repo.clone_from(config.root_git_url, root_path)
else:
    Repo(root_path).git().pull()

app = Sanic(__name__)
CORS(app)


def check_os(user_agent_str):
    result = config.types_by_ua[-1:]
    family = user_agent_parser.ParseOS(user_agent_str)["family"].lower()
    os_names = dict(
        zip(["mac os x", "window", "solaris", "linux"], config.types_by_ua[:-1])
    )
    if family in os_names:
        result.append(os_names[family])
    return result


@app.route("api/random_code", methods=["GET", "OPTIONS"])
async def random_code(request):
    types_by_user = [
        config.types_by_user.get(key, "common")
        for key in request.args.get("os", "").split(",")
    ]
    types = types_by_user if types_by_user else check_os(request.headers["user-agent"])
    files = [pathlib.Path(config.root_file).glob(f"{item}/*.md") for item in set(types)]
    target = random.choice(list(chain(*files)))
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
