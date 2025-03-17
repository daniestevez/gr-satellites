/*
 * Copyright 2025 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

/***********************************************************************************/
/* This file is automatically generated using bindtool and can be manually edited  */
/* The following lines can be configured to regenerate this file during cmake      */
/* If manual edits are made, the following tags should be modified accordingly.    */
/* BINDTOOL_GEN_AUTOMATIC(0)                                                       */
/* BINDTOOL_USE_PYGCCXML(0)                                                        */
/* BINDTOOL_HEADER_FILE(frame_counter.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(d031b6796e0ad5976f4778383f534ca8)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <satellites/frame_counter.h>
// pydoc.h is automatically generated in the build directory
#include <frame_counter_pydoc.h>

void bind_frame_counter(py::module& m)
{

    using frame_counter = ::gr::satellites::frame_counter;


    py::class_<frame_counter,
               gr::sync_block,
               gr::block,
               gr::basic_block,
               std::shared_ptr<frame_counter>>(m, "frame_counter", D(frame_counter))

        .def(py::init(&frame_counter::make),
             py::arg("itemsize"),
             py::arg("frame_size"),
             D(frame_counter, make))


        ;
}
