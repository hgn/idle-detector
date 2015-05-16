

install:
	install -m 0755 idle-detector.py /usr/local/bin/
	ln -s /usr/local/idle-detector.py /usr/local/bin/idle-detector
	cp idle-detector.service /etc/systemd/system/
	@echo "Now you can call:"
	@echo "  systemctl enable /etc/systemd/system/idle-detector.service"
	@echo "  systemctl start idle-detector.service"
	@echo "  systemctl status idle-detector.service"

uninstall:
	rm -rf /usr/local/bin/idle-detector
	rm -rf /usr/local/bin/idle-detector.py
	rm -rf /etc/systemd/system/idle-detector.service

.PHONY: install uninstall
