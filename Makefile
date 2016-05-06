DESTDIR =
all:
	#make -C docs html
	#make -C docs/misc all
	python setup.py build
	python3 setup.py build

clean:
	rm -rf SEEL_Apps.egg-info build
	find . -name "*~" -o -name "*.pyc" -o -name "__pycache__" | xargs rm -rf
	#make -C docs clean
	#make -C docs/misc clean
	rm -rf /usr/lib/python2.7/dist-packages/SEEL_Apps*
	sudo rm /usr/bin/Experiments

IMAGEDIR=$(DESTDIR)/usr/share/doc/seelablet-common/images

install:
	# install documents
	install -d $(DESTDIR)/usr/share/doc/seelablet
	cp -r GUI $(DESTDIR)/usr/share/seelablet/seel_res/
	cp -r ICONS $(DESTDIR)/usr/share/seelablet/seel_res/
	cp -r HTML $(DESTDIR)/usr/share/seelablet/seel_res/
	#cp docs/misc/build/*.html $(DESTDIR)/usr/share/doc/seelablet/html
	# create ditributions for Python2 and Python3
	python setup.py install --install-layout=deb \
	         --root=$(DESTDIR)/ --prefix=/usr
	python3 setup.py install --install-layout=deb \
	         --root=$(DESTDIR)/ --prefix=/usr
	# move png files from dist-package dirs to /usr/share
	for d in apps miscellaneous; do \
	  mkdir -p $(IMAGEDIR)/$$d; \
	  mv $(DESTDIR)/usr/lib/python2.7/dist-packages/SEEL_Apps/$$d/*.png $(IMAGEDIR)/$$d; \
	  rm -f $(DESTDIR)/usr/lib/python3/dist-packages/SEEL_Apps/$$d/*.png; \
	  for f in $(IMAGEDIR)/$$d/*.png; do \
	    ln -rs $$f $(DESTDIR)/usr/lib/python2.7/dist-packages/SEEL_Apps/$$d/ ; \
	    ln -rs $$f $(DESTDIR)/usr/lib/python3/dist-packages/SEEL_Apps/$$d/ ; \
	  done; \
	done

