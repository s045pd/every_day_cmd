from datetime import datetime
from itertools import chain
from pathlib import Path
from random import choice
from time import time
from typing import Optional

from apscheduler.schedulers.background import BackgroundScheduler
from git import Repo
from ua_parser import user_agent_parser

from conf import config
from fastapi import FastAPI, Header, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from imgkit import from_string
import pytz
from tzlocal import get_localzone

current_timezone = pytz.timezone( get_localzone().zone)

template = """<html><head><style>a{text-decoration:none}.every_day_cmd{display:inline-block;height:30px;line-height:30px;padding:0 20px;color:rgb(73,80,87);font-size:13px;font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica Neue,Arial,Noto Sans,sans-serif,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol,Noto Color Emoji}.every_day_cmd code{color:rgb(232,62,140);background:none;border:none}</style></head><body><a href="https://github.com/aoii103/every_day_cmd"><div id="every_day_cmd"class="every_day_cmd"title="字字珠玑，每日一记。">$codes$</div></a><div class="divider"></div></body></html>"""

app = FastAPI()
origins = ("*",)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=("*",),
    allow_headers=("*",),
)

root_path = Path(config.root_git_path)


def update_repo(init=False) -> None:
    if not root_path.exists():
        print("start clone!")
        Repo.clone_from(config.root_git_url, root_path)
    elif not init:
        print("start pull!")
        Repo(root_path).git().pull()


def check_os(user_agent_str: str) -> list:
    result = config.types_by_ua[-1:]
    family = user_agent_parser.ParseOS(user_agent_str)["family"].lower()
    os_names = dict(
        zip(["mac os x", "window", "solaris", "linux"], config.types_by_ua[:-1])
    )
    if family in os_names:
        result.append(os_names[family])
    return result


def get_random_code(types: list) -> dict:
    files = [Path(config.root_file).glob(f"{item}/*.md") for item in set(types)]
    target = choice(list(chain(*files)))
    with target.open("r") as md:
        data = md.read().split("- ")[1:]
        description, code = choice(data).strip().split("\n\n")
        return dict(
            zip(
                ("system", "type", "description", "code"),
                (target.parent.name, target.name, description[:-1], code[1:-1]),
            )
        )


def check_with_browser(user_agent: str, os: str) -> list:
    types_by_user = [config.types_by_user.get(key, "common") for key in os.split(",")]
    return types_by_user if types_by_user else check_os(user_agent)


@app.get("/")
async def random_code(user_agent: Optional[str] = Header(None), os: str = ""):
    return get_random_code(check_with_browser(user_agent, os))


@app.get("/html", response_class=HTMLResponse)
async def get_html(user_agent: Optional[str] = Header(None), os: str = ""):
    data = await random_code(user_agent, os)
    return template.replace(
        "$codes$", "🍺 {description}: <code>{code}</code>".format(**data)
    )


@app.get("/png")
async def get_png(user_agent: Optional[str] = Header(None), os: str = ""):
    from_string(await get_html(user_agent, os), config.out_file)
    return FileResponse(
        config.out_file,
        headers={
            "cache-control": "no-cache,max-age=0,no-store,s-maxage=0,proxy-revalidate",
            "expires": datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"),
        },
    )


@app.get("/flush")
async def get_flush(user_agent: Optional[str] = Header(None), os: str = ""):
    return RedirectResponse("png?code={}".format(int(time())), status_code=302)


scheduler = BackgroundScheduler()
scheduler.add_job(
    update_repo,
    trigger="interval",
    hours=24,
    timezone=current_timezone,
    id="updateTLDR",
)
scheduler.start()
update_repo(True)
