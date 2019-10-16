class conf:
    ip = "0.0.0.0"
    port = 8000

    root_git_path = "./tldr"
    root_file = "./tldr/pages"
    root_git_url = "https://github.com/tldr-pages/tldr.git"

    types_by_ua = ["osx", "window", "sunos", "linux", "common"]
    types_by_user = {"osx": "osx",
                     "window": "window",
                     "sunos": "sunos",
                     "linux": "linux",
                     "common": "common",
                     "all":"**"}


config = conf
