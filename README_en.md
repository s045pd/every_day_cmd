<p align="center">
<img src="media/bashs.png" />
    <p align="center">One words commond , one note per day.</p>
        <p align="center">
    <a target="_blank" href="https://www.python.org/downloads/" title="Python version"><img src="https://img.shields.io/badge/python-%3E=_3.7.4-green.svg"></a>
    <a target="_blank" href="LICENSE" title="License: MIT"><img src="https://img.shields.io/badge/License-MIT-blue.svg"></a>
    <a target="_blank" href="Sanic" title="Sanic"><img src="https://img.shields.io/badge/power_by-Sanic-Green.svg"></a></p>
</p>

> Use a tldr library of cmd to generate a random command usage.

## Requirement

- Sanic_Cors >= 0.9.9.post1
- GitPython >= 3.0.3
- sanic >= 19.9.0
- ua_parser >= 0.8.0

## Install

```sh
git clone https://github.com/aoii103/every_day_cmd.git

cd every_day_code

python3 -m pip install -r requirements.txt
```

## Useage

```sh
python3 server.py

```

then we open the page ```http://127.0.0.1:8000/api/random_code``` it will identify your os name based on your user-agent and push the relevant commands.

<img src="media/every_day_cmd.gif">

and you can specific the os like ```?os=linux,osx,common,window,sunos``` or use ```?os=all``` to all.

## 📝 License

This project is [MIT](https://github.com/kefranabg/readme-md-generator/blob/master/LICENSE) licensed.

***

If you think this script is useful to you, don't forget star ~ 🐶.