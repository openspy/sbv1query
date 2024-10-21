# python version of c code from https://aluigi.altervista.org/papers.htm#gsmsalg
# Copyright 2004,2005,2006,2007,2008 Luigi Auriemma

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA

# http://www.gnu.org/licenses/gpl.txt

def gsvalfunc(reg):
    if reg < 26:
        return chr(reg + ord('A'))
    if reg < 52:
        return chr(reg + ord('G'))
    if reg < 62:
        return chr(reg - 4)
    if reg == 62:
        return '+'
    if reg == 63:
        return '/'
    return chr(0)

def gsseckey(src, key):
    keysz = len(key)
    enctmp = list(range(256))
    a = 0
    
    #init state
    for i in range(256):
        a += enctmp[i] + ord(key[i % keysz])
        enctmp[a % 256], enctmp[i] = enctmp[i], enctmp[a % 256]

    a = 0
    b = 0
    tmp = [0] * 66
    i = 0

    while i < len(src):
        a += ord(src[i]) + 1
        x = enctmp[a % 256]
        b += x
        y = enctmp[b % 256]
        enctmp[b % 256], enctmp[a % 256] = x, y
        tmp[i] = ord(src[i]) ^ enctmp[(x + y) % 256]
        i += 1
    
    size = i
    while size % 3:
        tmp[size] = 0
        size += 1

    p = []

    #generate key
    for i in range(0, size, 3):
        x = tmp[i]
        y = tmp[i + 1]
        z = tmp[i + 2]
        p.append(gsvalfunc(x >> 2))
        p.append(gsvalfunc(((x & 3) << 4) | (y >> 4)))
        p.append(gsvalfunc(((y & 15) << 2) | (z >> 6)))
        p.append(gsvalfunc(z & 63))
    
    return ''.join(p)