OPTIONSH_NAME = optionsh.py
INSTALL_NAME = optionsh
DESTDIR = /usr/local

install: $(OPTIONSH_NAME)
	mkdir -p $(DESTDIR)/bin
	cp $(OPTIONSH_NAME) $(DESTDIR)/bin/$(INSTALL_NAME)
