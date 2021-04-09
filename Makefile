server:
	(cd wwwroot; python3 ../webserver.py)

# Re-do the compression of elements for the web server, to update them
reload:
	(cd wwwroot; python3 ../compress.py index.html)
	(cd wwwroot; python3 ../compress.py huffman.bmp)
	(cd wwwroot; python3 ../compress.py oval.png)
	(cd wwwroot; python3 ../compress.py favicon.ico)

# Simple before/after test of compress and decompress
#	These files are designed to compress better than huffman.bmp
test:
	make single FILE=test.1.txt
	make single FILE=arrow.png
	make single FILE=oval.png

single:
	python3 compress.py $(FILE)
	python3 decompress.py $(FILE).huf
	cmp $(FILE) $(FILE).huf.decomp
	cksum $(FILE) $(FILE).huf.decomp

h:
	python3 huffman.py

clean:
	-rm arrow.png.huf
	-rm arrow.png.huf.decomp
	-rm oval.png.huf
	-rm oval.png.huf.decomp
	-rm test.1.txt.huf
	-rm test.1.txt.huf.decomp
	-rm -r -f __pycache__
