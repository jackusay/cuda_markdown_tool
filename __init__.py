from cudatext import *

from cudax_lib import get_translation
_ = get_translation(__file__)  # I18N
PRE = '[Markdown Tool] '

class Command:
    def level_down(self):   return down()
    def level_up(self):     return up()

#level down;  text =>   text;  # => ##; ## => ###; ... when select
#             text => # text; # => ##; ## => ###; ...  when no select
#
# if select text, only heading will level down.
# if not select text, it will generate prefix # anyway.
def down():
    if ed.get_text_sel(): #for multiple lines, but also works on one line
        start_line_index, end_line_index = ed.get_sel_lines() #line index
        for index in range(start_line_index, end_line_index+1):
            line = ed.get_text_line(index)
            if line.startswith("#"):
                ed.set_text_line(index, "#" + line)
    else: #for one line
        carets = ed.get_carets()
        PosX, PosY, EndX, EndY = carets[0]
            #PosY is caret's line (0-base).
        line = ed.get_text_line(PosY)
        if line.startswith("#"):
            ed.set_text_line(PosY, "#" + line)
        else:
            ed.set_text_line(PosY, "# " + line.lstrip())
          
#level up; 
#do nothing      when selecting contains heading level 1

#mode1: all do nothing  if you select # heading
#mode2: do seperate     # => #; ## => #; ### => ##; ...       xxxxxxxxxx no implement
#mode3: all do anyway   # =>  ; ## => #; ### => ##; ...       xxxxxxxxxx no implement
def up():
    if ed.get_text_sel(): #for multiple lines, but also works on one line
        start_line_index, end_line_index = ed.get_sel_lines() #line index
        
        ###Check whether the user has selected a line that contains a heading level 1. If true, the 'up()' will do nothing. ###
        for index in range(start_line_index, end_line_index+1):
            line = ed.get_text_line(index)
            
            # line is heading level 1
            if line.startswith("#") and not line.startswith("#", 1):
                print("Select line that contains heading level 1 #. Do nothing.")
                msg_status(PRE + _('Select line that contains heading level 1 #. Do nothing.'))
                return
                
        #do level up work
        for index in range(start_line_index, end_line_index+1):
            line = ed.get_text_line(index)
            if line.startswith("#"):
                ed.set_text_line(index, line[1:])
    else: #for one line
        carets = ed.get_carets()
        PosX, PosY, EndX, EndY = carets[0]
            #PosY is caret's line (0-base).
        line = ed.get_text_line(PosY)
        if line.startswith("#") and not line.startswith("#", 1): # line is heading level 1
            ed.set_text_line(PosY, line[1:].lstrip())
        elif line.startswith("#"):                               # line is heading but not level 1 
            ed.set_text_line(PosY, line[1:])