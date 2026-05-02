.PHONY: all help test-q1 test-q2 test-q3 test-q4 test-q5 test-q6 test-q7 test-q8 test-q9 test-q10 clean

help:
	@echo "make test-q1 - test question 1 "
	@echo "make test-q2 - test question 2 "
	@echo "make test-q3 - test question 3 "
	@echo "make test-q4 - test question 4 "
	@echo "make test-q5 - test question 5 "
	@echo "make test-q6 - test question 6 "
	@echo "make test-q7 - test question 7 "
	@echo "make test-q8 - test question 8 "
	@echo "make test-q9 - test question 9 "
	@echo "make test-q10 - test question 10 "	
	@echo "make test - execution de tous les tests"
	@echo "make clean - Nettoie"

all : test-q1 test-q2 test-q3 test-q4 test-q5 test-q6 test-q7 test-q8 test-q9 test-q10

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

test-q7: 
	@echo "question 7 : \n"
	python -m unittest tests_projet.TestQ7 -v

test-q8 :
	@echo "question 8 : \n"
	python -m unittest tests_projet.TestQ8 -v

test-q9 :
	@echo "question 9 : \n"
	python -m unittest tests_projet.TestQ9 -v

test-q10 : 
	@echo "question 10 : \n"
	python -m unittest tests_projet.TestQ10 -v

clean:
	rm -rf __pycache__