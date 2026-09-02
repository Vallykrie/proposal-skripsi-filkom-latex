.PHONY: preview official test check clean

preview:
	python3 scripts/build.py preview

official:
	python3 scripts/build.py official

test:
	python3 -m unittest discover -s tests -v

check: test preview
	python3 scripts/check_log.py build/proposal.log
	python3 scripts/check_pdf.py build/proposal.pdf --mode preview

clean:
	python3 scripts/build.py clean
