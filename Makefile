all:
	$(MAKE) -C src all
	mv out/*.pdf .
	rm -rf out

build_only:
	$(MAKE) -C src all

clean:
	$(MAKE) -C src clean
