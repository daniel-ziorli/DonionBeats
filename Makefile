PYTHON = python3

setup:
	pip install -r requirements.txt
	sudo apt-get install ffmpeg
run:
	${PYTHON} main.py
