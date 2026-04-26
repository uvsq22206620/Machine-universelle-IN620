.PHONY: all help test test-q1 test-q2 test-q3 test-q4 test-q5 test-q6 run clean

help:
    @echo "  make test-q1    - test de la question 1 "
    @echo "  make test-q2    - test de la question 2 "
    @echo "  make test-q3    - test de la question 3 "
    @echo "  make test-q4    - test de la question 4 "
    @echo "  make test-q5    - test de la question 5 "
    @echo "  make test-q6    - test de la question 6 "
    @echo "  make test       - execution de tous les tests"
    @echo "  make run        - execution du code"
    @echo "  make clean      - Nettoie"

test-q1:
    @echo "question 1 : \n"
    python -m unittest tests_projet.TestQ1 -v

test-q2:
    @echo "question 2 : \n"
    python -m unittest tests_projet.TestQ2 -v

test-q3:
    @echo "question 3 : \n"
    python -m unittest tests_projet.TestQ3 -v

test-q4:
    @echo "question 4 : \n"
    python -m unittest tests_projet.TestQ4 -v

test-q5:
    @echo "question 5 : \n"
    python -m unittest tests_projet.TestQ5 -v

test-q6:
    @echo "question 6 : \n"
    python -m unittest tests_projet.TestQ6 -v

test: test-q1 test-q2 test-q3 test-q4 test-q5 test-q6
    @echo "\n✓ Tous les tests sont terminés !"

all: test
    python code.py

run:
    python code.py

clean:
    rm -rf __pycache__
    find . -name "*.pyc" -delete