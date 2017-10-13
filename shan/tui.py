import curses

def main(stdscr):
    """Main curses function to be run from wrapper."""
    stdscr.clear()
    curses.curs_set(0)

    base_win = curses.newwin(curses.LINES - 2, curses.COLS - 2, 1, 1)
    base_win.border()
    base_win_height, base_win_width = base_win.getmaxyx()
    sub_win = base_win.derwin(base_win_height - 3, base_win_width - 5, 2, 3)

    for line in range(15):
        sub_win.addstr(line + 1, 2, 'miau')

    stdscr.noutrefresh()
    base_win.noutrefresh()
    curses.doupdate()
    while True:
        key = stdscr.getkey()

        if key == 'q':
            break

curses.wrapper(main)
