PYTHON = python3

setup:
	pip install -r requirements.txt
	sudo apt-get install ffmpeg
	@echo ""
	@echo "Go to https://discord.com/developers/applications select your bot and get your token"
	@echo "Use export command to set the TOKEN enviroment variable"
	@echo "Example: export TOKEN=MY-DISCORD-BOT-TOKEN"

run:
	${PYTHON} main.py
