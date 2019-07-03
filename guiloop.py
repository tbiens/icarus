import curses

def guiloop():
    while True:
        keysbox = curses.newwin(50, 100, 0, 51)
        keysbox.addstr(0, 1, "Icarus.config")
        keysbox.addstr(1, 1, "Virustotal:")
        keysbox.addstr(2, 1, "Enabled: " + virustotal)
        keysbox.addstr(3, 1, "APIKEY: " + vtapikey)
        keysbox.addstr(5, 1, "AbuseIPDB:")
        keysbox.addstr(6, 1, "Enabled: " + abuseip)
        keysbox.addstr(7, 1, "APIKEY: " + abuseapikey)
        keysbox.addstr(9, 1, "Syslog:")
        keysbox.addstr(10, 1, "Enabled: " + syslogenable)
        keysbox.addstr(11, 1, "Syslog Server: " + syslogip + ":" + syslogport)
        keysbox.addstr(13, 1, "Press P to change values.", curses.color_pair(2))
        keysbox.refresh()

        window.refresh()
        window.addstr(0, 0, "Listening on: " + IP)
        window.addstr(1, 0, "Server started. Press Q to quit.", curses.color_pair(1))
        # It always shows IP address it's listening on and showing you can hit Q to quit.

        key = w.getch()
        if key == ord('q'):
            break
        elif key == ord('p'):
            editor()  # from editor.py, opens your system editor.
            window.erase()
            window.refresh()
            # window.addstr(2,0,"You pressed P\n") # Just a place holder for new commands in the future.

        sleep(1)  # So that the screen isn't refreshing at crazy rates unnecessarily.