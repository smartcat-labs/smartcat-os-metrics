#!/usr/bin/env python

import ftools
import resource
import os
import stat


def matrix_to_string(matrix, header):
    """
Note: this function is from: http://mybravenewworld.wordpress.com/2010/09/19/print-tabular-data-nicely-using-python/
i modified it a bit. ;-)

 Return a pretty, aligned string representation
 of a nxm matrix.

 This representation can be used to print any
 tabular data, such as database results. It
 works by scanning the lengths of each element
 in each column, and determining the format
 string dynamically.

 @param matrix: Matrix representation (list with n rows
  of m elements).
 @param header: Optional tuple with header elements to be
  displayed.
    """
    lengths = []
    matrix = [header] + matrix
    for row in matrix:
        for column in row:
            i = row.index(column)
            cl = len(str(column))
            try:
                ml = lengths[i]
                if cl > ml:
                    lengths[i] = cl
            except IndexError:
                lengths.append(cl)

    lengths = tuple(lengths)
    format_string = ""
    for length in lengths:
        format_string += "%-" + str(length) + "s    "
    format_string += "\n"

    matrix_str = ""
    for row in matrix:
        matrix_str += format_string % tuple(row)

    return matrix_str


def execute(target, directory):
    page_size = resource.getpagesize()
    rows = []

    if directory:
        for (path, dirs, files) in os.walk(target):
            for myfile in files:
                f = os.path.join(path, myfile)
                fd = file(f,'r')
                file_size = os.fstat(fd.fileno())[stat.ST_SIZE]
                if file_size == 0:
                    fd.close()
                    continue
                pages_cached, pages_total = ftools.fincore_ratio(fd.fileno())
                fd.close()
                rows.append([f, file_size, pages_total, pages_cached, (pages_cached * page_size), (float(pages_cached) / float(pages_total)) * 100.0])
    else:
        fd = file(target, 'r')
        file_size = os.fstat(fd.fileno())[stat.ST_SIZE]
        if file_size == 0:
            fd.close()
            return None
        else:
            pages_cached, pages_total = ftools.fincore_ratio(fd.fileno())
            fd.close()
            rows.append([target, file_size, pages_total, pages_cached, (pages_cached * page_size), (float(pages_cached) / float(pages_total)) * 100.0])

    rows = sorted(rows, key=lambda t: t[5], reverse=True)
    return rows

