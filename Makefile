run:
	python3 compiler.py

install:
	pip3 install -r requirements.txt

test:
	python3 compiler.py && ./tester_Linux.out

give_permission:
	chmod +x tester_Linux.out