# JS-Secrets-Scraper
Python based Web Scraper which can discover javascript files and parse them for juicy information (API keys, IP's, Hidden Paths etc).

## Screenshots

![](https://raw.githubusercontent.com/computer-engineer/JS-Secrets-Scraper/master/screenshots/screen1.png) 
![](https://raw.githubusercontent.com/computer-engineer/JS-Secrets-Scraper/master/screenshots/screen2.png)

## Technologies Used
1. Flask
2. Scrapy


## Requirements
1. Python 3
2. Linux/Windows/MAC OSX


## Installation 
```python
pip3 install -r requirements.txt 
```

## Usage
```python
(+) usage: python3 ./web/main.py
```

## Example
```python
$ python3 ./web/main.py                                                                                            2 ⨯
 * Serving Flask app "main" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: XXX-XXX-XXX
```
Then, access the interface on ``http://127.0.0.1:5000/``


