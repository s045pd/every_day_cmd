<p align="center">
<img src="media/bashs.png" />
    <p align="center">One words commond , one note per day.</p>
        <p align="center">
    <a target="_blank" href="https://www.python.org/downloads/" title="Python version"><img src="https://img.shields.io/badge/python-%3E=_3.7.4-green.svg"></a>
    <a target="_blank" href="LICENSE" title="License: MIT"><img src="https://img.shields.io/badge/License-MIT-blue.svg"></a>
    <a target="_blank" href="FastAPI" title="FastAPI"><img src="https://img.shields.io/badge/power_by-FastAPI-Green.svg"></a></p>
</p>

> Use a tldr library of cmd to generate a random command usage.

## Requirement

- wkhtmltopdf
- requirements.txt

## Install

```sh
git clone https://github.com/s045pd/every_day_cmd.git

cd every_day_cmd

chmod +x run.sh && ./run.sh
```

## Useage

```sh
python3 server.py

```

then we open the page ```http://x.x.x.x:12308``` it will identify your os name based on your user-agent and push the relevant commands.


And we provide the `\html` and '\png' path as generate interface , how to use it is up to you.

<img src="media/every_day_cmd.gif">

and you can specific the os like ```?os=linux,osx,common,window,sunos``` or use ```?os=all``` to all.

## 📝 License

This project is [MIT](https://github.com/kefranabg/readme-md-generator/blob/master/LICENSE) licensed.

***

If you think this script is useful to you, don't forget star ~ 🐶.