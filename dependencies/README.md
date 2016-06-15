"Ordinary" dependencies
=======================

Those are dependencies used for debian packaging:

For python2.7
-------------

	seelablet-common,
	python-serial,  python-pyqtgraph,  python-qt5,
	python-pyqt5.qtwebkit,
	python-appindicator

For python3
-----------
	seelablet-common,
	python3-serial, python3-pyqtgraph, python3-pyqt5.qtopengl,
	python3-pyqt5.qtwebkit
	gir1.2-appindicator3-0.1

"Exceptional" dependencies
========================

as of May 2016, Qt4's WebKit removal will prevent the package seelablet
to work properly in Debian. See those annouces:

 * <https://wiki.debian.org/Qt4WebKitRemoval> in Debian's wiki
 * <https://lists.debian.org/debian-devel-announce/2015/05/msg00001.html> in the mailing list debian-devel-announce

The solution is to migrate seelablet to PyQt5, which is done in the present
branch of our GIT repository.

However, the packages python-pyqtgraph and python3-pyqtgraph only support
Qt4 currently. One contributor for pyqtgraph has developped a branch "develop"
in Github's official repository, which provides the support for Qt5 too;
thanks **mfitzp** at Github!

Please find in this directory the following packages:

 * [python-pyqtgraph\_0.9.10+develop-1\_all.deb](python-pyqtgraph\_0.9.10+develop-1\_all.deb)
 * [python3-pyqtgraph\_0.9.10+develop-1\_all.deb](python3-pyqtgraph\_0.9.10+develop-1\_all.deb)

both are "exceptional" dependencies for seelablet which uses Qt5, until this
new development will reach the Debian archive.
