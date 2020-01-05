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

import pathlib

class File:
    """
    Class to hold housekeeping data about a file being received
    """
    def __init__(self, path):
        """
        Builds a new file, initializing housekeeping data

        Args:
            path: path of the file (pathlib.Path)
        """
        self.path = path
        self.f = open(path, 'wb')
        self.broken = False
        self.expected_seq = 0
        self.write_pointer = 0
        self.size = None
        self.chunks = None

class FileReceiver:
    """
    Class to reassemble files transmitted in chunks

    This implements the generic framework. Specific protocols should
    inherit from this class and implement some functions
    """
    def __init__(self, path, verbose = False):
        """
        Builds a new FileReceiver

        Args:
            path: directory where files should be stored (str or pathlib.Path)
            verbose: verbose reporting of events (bool)
        """
        self._files = dict()
        self._current_file = None
        self._next_fid = 0
        self._path = pathlib.Path(path)
        self._verbose = verbose
        self._name = 'FileReceiver'

    def file_id(self, chunk):
        """
        Returns the file ID of a given chunk

        If the file cannot be identified from a chunk, it should
        return None.

        The default implementation returns chunk.file_id if available
        else None
        
        Args:
            chunk: a file chunk (parsed by parse_chunk())
        """
        return getattr(chunk, 'file_id', None)

    def chunk_sequence(self, chunk):
        """
        Returns the sequence number of a given chunk
        
        The sequence number should increase from 0. If the chunk number
        cannot be identified from a chunk, or if chunk_offset is used
        instead, it should return None.

        The default implementation returns chunk.sequence if available
        else None

        Args:
            chunk: a file chunk (parsed by parse_chunk())
        """
        return getattr(chunk, 'sequence', None)

    def chunk_size(self):
        """
        Returns the size of a chunk if all chunks (except possibly
        the last one) have the same fixed size, None if not
        """
        return None

    def chunk_offset(self, chunk):
        """
        Returns the offset in bytes of a given chunk within the file

        This should return None if it is not possible to determine
        the chunk offset from the chunk.

        The default implementation first returns chunk.offset if available.
        If not, it tries to use chunk_sequence() and chunk_size() to
        determine the offset.

        Args:
            chunk: a file chunk (parsed by parse_chunk())
        """
        off = getattr(chunk, 'offset', None)
        if off is not None:
            return off
        s = self.chunk_size()
        i = self.chunk_sequence(chunk)
        if s is not None and i is not None:
            return s * i
        else:
            return None

    def chunk_data(self, chunk):
        """
        Returns the file data in a given chunk

        The default implementation returns chunk.data.

        Args:
            chunk: a file chunk (parsed by parse_chunk())
        Returns:
            bytes
        """
        return chunk.data

    def file_chunks(self, chunk):
        """
        Returns the total number of chunks in the file

        The default implementation returns chunk.chunks if available
        else None

        Args:
            chunk: a file chunk (parsed by parse_chunk())
        """
        return getattr(chunk, 'chunks', None)

    def file_size(self, chunk):
        """
        Returns the total number of bytes in the file

        The default implementation returns chunk.filesize if available
        else None

        Args:
            chunk: a file chunk (parsed by parse_chunk())
        """
        return getattr(chunk, 'filesize', None)

    def is_last_chunk(self, chunk):
        """
        Returns whether this is the last chunk in the file

        The default implementation returns None

        Args:
            chunk: a file chunk (parsed by parse_chunk())
        Returns:
            True if this is is the last chunk, False if this is not
            the last chunk, None if it is unknown whether this is the
            last chunk.
        """
        return None
    
    def parse_chunk(self, chunk):
        """
        Parses the chunk into an object which is easier to handle

        The default implementation does nothing.
        A return of None means the chunk is invalid and should not
        be processed.

        Args:
            chunk: a file chunk (bytes)
        """
        return chunk

    def filename(self, fid):
        """
        Generates a filename based on the file id

        The default implementation uses the file id as filename
        
        Args:
           fid: file id (usually int)
        """
        return str(fid)

    def on_completion(self, f):
        """
        Function to be called on file completion

        The user should overload this function if some action
        needs to be done after a file is complete

        Args:
            f: the file just completed (File)
        """
    
    def _new_file(self, fid):
        """
        Creates a new file

        Args:
            fid: file id of the new file (usually int)
        Returns:
            the new file
        """
        f = File(self._path / self.filename(fid))
        self._files[fid] = f
        return f

    def _fill_file_data(self, f, chunk):
        """
        Tries to fill some file data from the chunk

        Args:
            f: a File
            chunk: a file chunk (parsed by parse_chunk())
        """
        if f.size is None:
            f.size = self.file_size(chunk)
        if f.chunks is None:
            f.chunks = self.file_chunks(chunk)

    def log(self, message):
        if self._verbose:
            print(f'{self._name}: {message}')
            
    def push_chunk(self, chunk):
        """
        Processes a new chunk

        The user should call this function whenever a new chunk
        is received.

        Args:
            chunk: the file chunk (bytes)
        """
        chunk = self.parse_chunk(chunk)
        if chunk is None:
            return
        
        # find file
        # TODO: logic about new file when file_id == None
        fid = self.file_id(chunk)
        if fid is None:
            fid = self._current_file
        if fid is None:
            fid = self._next_fid
            self._next_fid += 1
        try:
            f = self._files[fid]
        except KeyError:
            self.log(f'new file {fid}')
            f = self._new_file(fid)

        seq = self.chunk_sequence(chunk)

        # detect a new file if sequence has decreased
        if self.file_id(chunk) is None and seq is not None and seq < f.expected_seq:
            # f is finished
            self.log(f'file {fid} is finished')
            fid = self._next_fid
            self._next_fid += 1
            f = self._new_file(fid)
            self.log(f'receiving new file {fid}')
        self._current_file = fid

        self._fill_file_data(f, chunk)

        if seq is not None:
            self.log(f'received sequence {seq} for file {fid}')

        if f.broken:
            # file is broken, nothing can be done with the chunk
            return

        # try to determine offset
        offset = self.chunk_offset(chunk)
        if seq is None and offset is not None:
            self.log(f'received offset {offset} for file {fid}')
        if offset is None:
            # check sequence continuity
            if seq is None:
                raise Exception('FileReceiver unable to compute chunk_offset() nor chunk_sequence()')
            if seq != f.expected_seq:
                self.log(f'received sequence {seq} != expected sequence {f.expected_seq}. File reception is broken.')
                f.broken = True
                return
            offset = f.write_pointer
            
        data = self.chunk_data(chunk)
        new_write_pointer = offset + len(data)

        # check offset within size
        if f.size is not None and new_write_pointer > f.size:
            self.log(f'invalid offset {offset} (chunk size is {len(data)}, file size is {f.size})')
            return

        # write chunk at offset
        f.f.seek(offset)
        f.f.write(data)
        f.f.flush()

        # update pointers
        f.write_pointer = new_write_pointer
        f.expected_seq = seq + 1 if seq is not None else None

        # check if file is complete
        if (f.size is not None and f.write_pointer >= f.size) or \
          (f.chunks is not None and f.expected_seq >= f.chunks) or \
          self.is_last_chunk(chunk) is True:
          self.log(f'file {fid} complete')
          self.on_completion(f)
          self._current_file = None
