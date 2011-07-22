from fractions import Fraction
from tablature import chord, bar, tablature
import curses # KEY_*

# a
def append(ed, num):
	ed.tab.get_cursor_bar().chords.insert(ed.tab.cursor_chord,
			chord(ed.insert_duration))
	ed.move_cursor(new_chord = ed.tab.cursor_chord + 1)
	ed.redraw_view()
	ed.insert_mode()

# s - this one should delete under cursor
def set_chord(ed, num):
	ed.insert_mode()

# x
def delete_chord(ed, num):
	t = ed.tab
	del t.get_cursor_bar().chords[t.cursor_chord-1]
	if not t.bars[t.cursor_bar-1].chords:
		del t.bars[t.cursor_bar-1]
	if not t.bars:
		# empty tab
		t.bars = [bar()]
	if t.cursor_bar > len(t.bars):
		t.cursor_bar = len(t.bars)
		t.cursor_chord = len(t.bars[t.cursor_bar-1].chords)
	elif t.cursor_chord > len(t.bars[t.cursor_bar-1].chords):
		t.cursor_chord = len(t.bars[t.cursor_bar-1].chords)
	ed.move_cursor()
	ed.redraw_view()

# q
def set_duration(ed, num_arg):
	curch = ed.tab.get_cursor_chord()
	if num_arg:
		curch.duration = Fraction(1, num_arg)
	else:
		curch.duration = curch.duration * Fraction('1/2')
	ed.move_cursor()
	ed.redraw_view()

# Q
def increase_duration(ed, num):
	curch = ed.tab.get_cursor_chord()
	curch.duration = curch.duration * 2
	ed.move_cursor()
	ed.redraw_view()

# o
def append_bar(ed, num):
	curb = ed.tab.get_cursor_bar()
	ed.tab.bars.insert(ed.tab.cursor_bar, bar(curb.sig_num, curb.sig_den))
	ed.move_cursor(ed.tab.cursor_bar + 1, 1)
	ed.redraw_view()
	ed.insert_mode()

# G
def go_end(ed, num):
	if num:
		ed.move_cursor(min(len(ed.tab.bars), num), 1)
	else:
		ed.move_cursor(len(ed.tab.bars), 1)

# 0
def go_bar_beg(ed, num):
	if not num:
		ed.move_cursor(new_chord = 1)

# $
def go_bar_end(ed, num):
	ed.move_cursor(new_chord = len(ed.tab.get_cursor_bar().chords))

# TODO: I, A, O, gg

def set_bar_meter(ed, params):
	try:
		curb = ed.tab.get_cursor_bar()
		curb.sig_num, curb.sig_den = int(params[1]), int(params[2])
		ed.redraw_view()
	except:
		ed.st = 'Invalid argument'

def set_insert_duration(ed, params):
	try:
		ed.insert_duration = Fraction(int(params[1]), int(params[2]))
	except:
		ed.st = 'Invalid argument'

def edit_file(ed, params):
	try:
		ed.load_tablature(params[1])
		ed.move_cursor()
		ed.redraw_view()
	except IndexError:
		ed.st = 'File name not specified'

def write_file(ed, params):
	try:
		ed.save_tablature(params[1])
	except IndexError:
		if ed.file_name:
			ed.save_tablature(ed.file_name)
		else:
			ed.st = 'File name not specified'

def quit(ed, params):
	ed.terminate = True

def map_commands(ed):
	ed.nmap[ord('a')] = append
	ed.nmap[ord('x')] = delete_chord
	ed.nmap[ord('q')] = set_duration
	ed.nmap[ord('Q')] = increase_duration
	ed.nmap[ord('o')] = append_bar
	ed.nmap[ord('G')] = go_end
	ed.nmap[ord('0')] = go_bar_beg
	ed.nmap[ord('$')] = go_bar_end
	ed.nmap[ord('s')] = set_chord
	ed.nmap[ord('h')] = ed.nmap[curses.KEY_LEFT] = \
			lambda ed, num: ed.move_cursor_left()
	ed.nmap[ord('l')] = ed.nmap[curses.KEY_RIGHT] = \
			lambda ed, num: ed.move_cursor_right()
	ed.nmap[ord(':')] = lambda ed, num: ed.command_mode()
	
	ed.commands['meter'] = set_bar_meter
	ed.commands['ilen'] = set_insert_duration

	ed.commands['e'] = edit_file
	ed.commands['w'] = write_file
	ed.commands['q'] = quit
