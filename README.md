## Set-Up

### Dev
copy the .env.ini file and rename it .env
```bash
cp .env.ini .env
```

then change the TOKEN value in it by your discord bot token
```python
# .env
TOKEN=INSERT_TOKEN # put your discord bot's token here
```

then create a virtual env and install the dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

then you can run it
```bash
python3 main.py
```


### Docker
get/make the image
```bash
docker build -t discord_birthday_bot .
```

then create a volume and run it
```bash
# create a directory data to store the data
mkdir data
# don't forget to change the token
docker run -d -e DATABASE=db/database.db -e TOKEN=INSERT_YOUR_TOKEN_HERE -v ./data:/app/db discord_birthday_bot
```
