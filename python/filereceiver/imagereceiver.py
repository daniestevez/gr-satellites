#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Daniel Estevez <daniel@destevez.net>.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

from ..feh import FehOpener
from .filereceiver import FileReceiver

class ImageReceiver(FileReceiver):
    """
    Class to reassemble images transmitted in chunks and display them
    in real-time using feh

    This implements the generic framework. Specific protocols should
    inherit from this class and implement some FileReceiver methods
    """
    def __init__(self, path, verbose = False, display = False, fullscreen = True):
        """
        Builds a new ImageReceiver

        Args:
            path: directory where files should be stored (str or pathlib.Path)
            verbose: verbose reporting of events (bool)
            display: display image in real-time using feh (bool)
            fullscreen: run feh in fullscreen (bool)
        """
        super().__init__(path, verbose)
        self._feh = FehOpener(fullscreen) if display else None
        self._name = 'ImageReceiver'

    def filename(self, fid):
        """
        Generates a filename based on the file id

        The default implementation uses the fid.jpg as filename
        
        Args:
           fid: file id (usually int)
        """
        return f'{fid}.jpg'

    def _new_file(self, fid):
        """
        Creates a new file

        Args:
            fid: file id of the new file (usually int)
        Returns:
            the new file
        """
        f = super()._new_file(fid)
        f.displaying = False
        return f

    def push_chunk(self, chunk):
        """
        Processes a new chunk

        The user should call this function whenever a new chunk
        is received.

        Args:
            chunk: the file chunk (bytes)
        """
        super().push_chunk(chunk)
        if self._current_file is None:
            return
        f = self._files[self._current_file]
        if f.write_pointer >= 10*64:
            # enough data to display
            if self._feh is not None and not f.displaying:
                f.displaying =  True
                self._feh.open(f.path)
