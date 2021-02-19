/*
 * Copyright 2021 Free Software Foundation, Inc.
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
/* BINDTOOL_HEADER_FILE(descrambler308.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(bff741b093f515cd5bfbefff15efc533)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <satellites/descrambler308.h>
// pydoc.h is automatically generated in the build directory
#include <descrambler308_pydoc.h>

void bind_descrambler308(py::module& m)
{

    using descrambler308 = ::gr::satellites::descrambler308;


    py::class_<descrambler308,
               gr::sync_block,
               gr::block,
               gr::basic_block,
               std::shared_ptr<descrambler308>>(m, "descrambler308", D(descrambler308))

        .def(py::init(&descrambler308::make), D(descrambler308, make))


        ;
}