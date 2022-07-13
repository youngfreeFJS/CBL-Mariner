# Mariner's Python RPM macros

This is the set of RPM macros needed to support 

Most files are directly derived from Fedora's RPM macros (license: MIT).
Specifically, the current set in this folder were derived from [version 3.11-1](https://src.fedoraproject.org/rpms/python-rpm-macros/c/b8b5cb92da8974aad9bd231f16b8eb31db7ab14c).

Files `python.attr`, 

We heavily modify these in a few different ways to better fit Mariner:
- All references to Python 2 are out. Fedora seems to be keeping at least some SRPM macros in for Python 2, but we've already removed them from all of our specs.
- Most unversioned macros are out. The only one that remains is 
- With this set of macros, going forward, we cut out support for Python < 3.9. In Mariner 2.0 and beyond, even if we support multiple versions of Python, we shouldn't support anything older than 3.9.
