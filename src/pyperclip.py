# Pyperclip v1.3
# A cross-platform clipboard module for Python.
# By Al Sweigart <al@coffeeghost.net>
# Modified for 1337 Translator by Vinny Diehl <gbchaosmaster926@gmail.com>

# Usage:
#   import pyperclip
#   pyperclip.copy('The text to be copied to the clipboard.')
#   spam = pyperclip.paste()

# On Mac, this module makes use of the pbcopy and pbpaste commands,
# which should come with the os.
# On Linux, this module makes use of the xclip command, which should
# come with the os. Otherwise run "sudo apt-get install xclip"

# Copyright (c) 2010, Albert Sweigart
# All rights reserved.

# BSD-style license:

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the pyperclip nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY Albert Sweigart "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Albert Sweigart BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Change Log:
# 1.2 Use the platform module to help determine OS.
# 1.3 Changed ctypes.windll.user32.OpenClipboard(None) to
#     ctypes.windll.user32.OpenClipboard(0), after some people ran
#     into some TypeError

# 2012-05-31 gbchaosmaster - Making this support UTF-8. Adds Django dependency.

import platform, os
from django.utils.encoding import smart_str

def winGetClipboard():
    ctypes.windll.user32.OpenClipboard(0)
    pcontents = ctypes.windll.user32.GetClipboardData(1) # 1 is CF_TEXT
    data = ctypes.c_char_p(pcontents).value
    ctypes.windll.user32.CloseClipboard()
    return data

def winSetClipboard(text):
    GMEM_DDESHARE = 0x2000
    ctypes.windll.user32.OpenClipboard(0)
    ctypes.windll.user32.EmptyClipboard()
    try:
        # Works on Python 2 (bytes() only takes one argument)
        hCd = ctypes.windll.kernel32.GlobalAlloc(GMEM_DDESHARE,
                                                 len(bytes(smart_str(text)))+1)
    except TypeError:
        # Works on Python 3 (bytes() requires an encoding)
        hCd = ctypes.windll.kernel32.GlobalAlloc(GMEM_DDESHARE,
                                                 len(bytes(smart_str(text),
                                                           'ascii')) + 1)

    pchData = ctypes.windll.kernel32.GlobalLock(hCd)
    try:
        # Works on Python 2 (bytes() only takes one argument)
        ctypes.cdll.msvcrt.strcpy(ctypes.c_char_p(pchData),
                                  bytes(smart_str(text)))
    except TypeError:
        # Works on Python 3 (bytes() requires an encoding)
        ctypes.cdll.msvcrt.strcpy(ctypes.c_char_p(pchData),
                                  bytes(smart_str(text), 'ascii'))
    ctypes.windll.kernel32.GlobalUnlock(hCd)
    ctypes.windll.user32.SetClipboardData(1,hCd)
    ctypes.windll.user32.CloseClipboard()

def macSetClipboard(text):
    outf = os.popen('pbcopy', 'w')
    outf.write(smart_str(text))
    outf.close()

def macGetClipboard():
    outf = os.popen('pbpaste', 'r')
    content = outf.read()
    outf.close()
    return content

def gtkGetClipboard():
    return gtk.Clipboard().wait_for_text()

def gtkSetClipboard(text):
    cb = gtk.Clipboard()
    cb.set_text(smart_str(text))
    cb.store()

def qtGetClipboard():
    return str(cb.text())

def qtSetClipboard(text):
    cb.setText(smart_str(text))

def xclipSetClipboard(text):
    outf = os.popen('xclip -selection c', 'w')
    outf.write(smart_str(text))
    outf.close()

def xclipGetClipboard():
    outf = os.popen('xclip -selection c -o', 'r')
    content = outf.read()
    outf.close()
    return content

def xselSetClipboard(text):
    outf = os.popen('xsel -i', 'w')
    outf.write(smart_str(text))
    outf.close()

def xselGetClipboard():
    outf = os.popen('xsel -o', 'r')
    content = outf.read()
    outf.close()
    return content

if os.name == 'nt' or platform.system() == 'Windows':
    import ctypes
    getcb = winGetClipboard
    setcb = winSetClipboard
elif os.name == 'mac' or platform.system() == 'Darwin':
    getcb = macGetClipboard
    setcb = macSetClipboard
elif os.name == 'posix' or platform.system() == 'Linux':
    xclipExists = os.system('which xclip') == 0
    if xclipExists:
        getcb = xclipGetClipboard
        setcb = xclipSetClipboard
    else:
        xselExists = os.system('which xsel') == 0
        if xselExists:
            getcb = xselGetClipboard
            setcb = xselSetClipboard
        try:
            import gtk
            getcb = gtkGetClipboard
            setcb = gtkSetClipboard
        except:
            try:
                import PyQt4.QtCore
                import PyQt4.QtGui
                app = QApplication([])
                cb = PyQt4.QtGui.QApplication.clipboard()
                getcb = qtGetClipboard
                setcb = qtSetClipboard
            except:
                raise Exception(
'Pyperclip requires the gtk or PyQt4 module installed, or the xclip command.'
                )

copy = setcb
paste = getcb
