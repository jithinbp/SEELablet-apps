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
	mkdir -p $(DESTDIR)/usr/share/seelablet/seel_res
	cp -r seel_res/* $(DESTDIR)/usr/share/seelablet/seel_res/
	
	#cp docs/misc/build/*.html $(DESTDIR)/usr/share/doc/seelablet/html
	# create ditributions for Python2 and Python3
	python setup.py install --install-layout=deb \
	         --root=$(DESTDIR)/ --prefix=/usr
	#python3 setup.py install --install-layout=deb \
	#         --root=$(DESTDIR)/ --prefix=/usr
	# move png files from dist-package dirs to /usr/share

