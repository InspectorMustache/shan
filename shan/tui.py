import curses
from collections import namedtuple
from time import sleep

import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG)

# $value represents what is returned when hitting enter, $str_ represents the
# menu entry as it appears to the user
MenuEntry = namedtuple('MenuEntry', ['value', 'str_'])

# $first is the number of the first entry, $last the number of the final entry
# + 1 (for use with range())
MenuPage = namedtuple('MenuPage', ['first', 'last'])


class Menu():
    """Menu class with navigation methods. Each menu entry must be an
    MenuEntry. Constructing requires a list of MenuEntry objects and a stdscr
    object from curses.wrapper."""

    def __init__(self, stdscr, entry_list):
        self.stdscr = stdscr
        self.entry_dict = self._get_entry_dict(entry_list)
        self.current_pos = 0
        self.current_page = 0
        # the following method assigns:
        # self.base_win
        # self.sub_win
        self._init_windows(self.stdscr)
        self.pages_dict = self._get_pages_dict()

    def _init_windows(self, stdscr):
        """Draw initial interface."""
        stdscr.clear()
        curses.curs_set(0)

        base_win = curses.newwin(curses.LINES - 2,
                                 curses.COLS - 2,
                                 1, 1)
        base_win.box()

        base_win_height, base_win_width = base_win.getmaxyx()
        sub_win = base_win.derwin(base_win_height - 2,
                                  base_win_width - 2,
                                  1, 1)

        # make windows available to all methods
        self.base_win = base_win
        self.sub_win = sub_win

        # create the menulist
        for pos, entry in self.entry_dict.items():
            sub_win.addstr(pos, 0, entry.str_)

        self.mark_current_position()
        self.update_screen()

        sleep(3)  # for debugging only

    # def draw_page(self, page_num):
    #     """Draw page $page_num."""
    #     entry_dict_slice = {}
    #     for entry

    def _get_entry_dict(self, entry_list):
        positions = len(entry_list)
        entry_dict = {pos: entry_list[pos] for pos in range(positions)}
        return entry_dict

    def _get_pages_dict(self):
        """Return a dictionary of pages and their containing entries by
        position reference."""
        entry_count = len(self.entry_dict)
        page_size, _ = self.sub_win.getmaxyx()
        # page_breaks = those positions at which a page ends and a new one
        # begins
        page_breaks = list(range(entry_count))[::page_size]

        pages_dict = {}
        for iter_, page in enumerate(page_breaks):
            first_page = page_breaks[iter_]
            try:
                last_page = page_breaks[iter_ + 1]
            except IndexError:
                last_page = entry_count

            pages_dict[iter_] = MenuPage(first=first_page, last=last_page)

        logging.debug(pages_dict)
        return pages_dict

    def mark_current_position(self):
        """Mark line at position $pos."""
        y_pos, x_pos = self.sub_win.getyx()
        self.sub_win.move(self.current_pos, 0)
        self.sub_win.chgat(curses.A_REVERSE)
        # reset cursor position
        self.sub_win.move(y_pos, x_pos)

    def update_screen(self):
        """Refresh all windows and redraw screen."""
        self.stdscr.noutrefresh()
        self.base_win.noutrefresh()
        self.sub_win.noutrefresh()
        curses.doupdate()


entries = [MenuEntry(value='bla', str_='miau'), MenuEntry(value='bla', str_='wuff')]
curses.wrapper(Menu, entries)
