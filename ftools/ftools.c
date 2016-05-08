#include <Python.h>

#include <unistd.h>
#include <sys/mman.h>
#include <sys/syscall.h>

static PyObject *ftools_fincore(PyObject *self, PyObject *args) {
    PyObject *ret;
    int fd;
    void *file_mmap;
    unsigned char *mincore_vec;
    struct stat file_stat;
    ssize_t page_size = getpagesize();
    ssize_t vec_size;

    if(!PyArg_ParseTuple(args, "i", &fd)) {
        return NULL;
    }

    if(fstat(fd, &file_stat) < 0) {
        PyErr_SetString(PyExc_IOError, "Could not fstat file");
        return NULL;
    }

    if ( file_stat.st_size == 0 ) {
        PyErr_SetString(PyExc_IOError, "Cannot mmap zero size file");
        return NULL;
    }

    file_mmap = mmap((void *)0, file_stat.st_size, PROT_NONE, MAP_SHARED, fd, 0);

    if(file_mmap == MAP_FAILED) {
        PyErr_SetString(PyExc_IOError, "Could not mmap file");
        return NULL;
    }

    vec_size = (file_stat.st_size + page_size - 1) / page_size;
    mincore_vec = calloc(1, vec_size);

    if(mincore_vec == NULL) {
        return PyErr_NoMemory();
    }

    if(mincore(file_mmap, file_stat.st_size, mincore_vec) != 0) {
        PyErr_SetFromErrno(PyExc_OSError);
        PyErr_SetString(PyExc_OSError, "Could not call mincore for file");
        return NULL;
    }

    ret = Py_BuildValue("s#", mincore_vec, vec_size);
    free(mincore_vec);
    munmap(file_mmap, file_stat.st_size);
    return ret;
}

static PyObject *ftools_fincore_ratio(PyObject *self, PyObject *args) {
    int fd;
    void *file_mmap;
    unsigned char *mincore_vec;
    struct stat file_stat;
    ssize_t page_size = getpagesize();
    size_t page_index;
    ssize_t vec_size;

    if(!PyArg_ParseTuple(args, "i", &fd)) {
        return NULL;
    }

    if(fstat(fd, &file_stat) < 0) {
        PyErr_SetString(PyExc_IOError, "Could not fstat file");
        return NULL;
    }

    if ( file_stat.st_size == 0 ) {
        PyErr_SetString(PyExc_IOError, "Cannot mmap zero size file");
        return NULL;
    }

    file_mmap = mmap((void *)0, file_stat.st_size, PROT_NONE, MAP_SHARED, fd, 0);

    if(file_mmap == MAP_FAILED) {
        PyErr_SetString(PyExc_IOError, "Could not mmap file");
        return NULL;
    }

    vec_size = (file_stat.st_size + page_size - 1) / page_size;
    mincore_vec = calloc(1, vec_size);

    if(mincore_vec == NULL) {
        return PyErr_NoMemory();
    }

    if(mincore(file_mmap, file_stat.st_size, mincore_vec) != 0) {
        PyErr_SetString(PyExc_OSError, "Could not call mincore for file");
        return NULL;
    }

    int cached = 0;
    for (page_index = 0; page_index <= file_stat.st_size/page_size; page_index++) {
        if (mincore_vec[page_index]&1) {
            ++cached;
        }
    }

    free(mincore_vec);
    munmap(file_mmap, file_stat.st_size);

    int total_pages = (int)ceil( (double)file_stat.st_size / (double)page_size );
    return Py_BuildValue("(ii)", cached, total_pages);
}

static PyMethodDef FtoolsMethods[] = {
    {"fincore", ftools_fincore, METH_VARARGS, "Return the mincore structure for the given file."},
    {"fincore_ratio", ftools_fincore_ratio, METH_VARARGS, "Return a int two tuple indicating file in page cache ratio."},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initftools(void) {
    (void)Py_InitModule("ftools", FtoolsMethods);

}
