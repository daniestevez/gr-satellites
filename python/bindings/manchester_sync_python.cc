/*
 * Copyright 2023 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <satellites/manchester_sync.h>
// pydoc.h is automatically generated in the build directory
#include <manchester_sync_pydoc.h>

template <class T>
void bind_manchester_sync_template(py::module& m, const char* classname)
{
    using manchester_sync = ::gr::satellites::manchester_sync<T>;

    py::class_<manchester_sync,
               gr::sync_decimator,
               gr::block,
               gr::basic_block,
               std::shared_ptr<manchester_sync>>(m, classname, D(manchester_sync))
        .def(py::init(&manchester_sync::make), py::arg("block_size"));
}

void bind_manchester_sync(py::module& m)
{
    bind_manchester_sync_template<gr_complex>(m, "manchester_sync_cc");
    bind_manchester_sync_template<float>(m, "manchester_sync_ff");
}
