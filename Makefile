PYTHON = python3
setup:
	pip install -r requirements.txt
	sudo apt-get install ffmpeg
	@echo ""
	@echo "Go to https://discord.com/developers/applications select your bot and get your token"
	@read -p "Discord Bot Token: " token \
	&& echo "{ \"TOKEN\" : \"$${token}\" }" > config.json

run:
	${PYTHON} main.py
