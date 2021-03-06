# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
r"""Removes unneeded nodes from a GraphDef file.

This script is designed to help streamline models, by taking the input and
output nodes that will be used by an application and figuring out the smallest
set of operations that are required to run for those arguments. The resulting
minimal graph is then saved out.

The advantages of running this script are:
 - You may be able to shrink the file size.
 - Operations that are unsupported on your platform but still present can be
   safely removed.
The resulting graph may not be as flexible as the original though, since any
input nodes that weren't explicitly mentioned may not be accessible any more.

An example of command-line usage is:
bazel build tensorflow/python/tools:strip_unused && \
bazel-bin/tensorflow/python/tools/strip_unused \
--input_graph=some_graph_def.pb \
--output_graph=/tmp/stripped_graph.pb \
--input_node_names=input0
--output_node_names=softmax

You can also look at strip_unused_test.py for an example of how to use it.

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

from tensorflow.python.tools import strip_unused_lib


FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_string("input_graph", "",
                           """TensorFlow 'GraphDef' file to load.""")
tf.app.flags.DEFINE_boolean("input_binary", False,
                            """Whether the input files are in binary format.""")
tf.app.flags.DEFINE_string("output_graph", "",
                           """Output 'GraphDef' file name.""")
tf.app.flags.DEFINE_string("input_node_names", "",
                           """The name of the input nodes, comma separated.""")
tf.app.flags.DEFINE_string("output_node_names", "",
                           """The name of the output nodes, comma separated.""")
tf.app.flags.DEFINE_integer("placeholder_type_enum",
                            tf.float32.as_datatype_enum,
                            """The AttrValue enum to use for placeholders.""")


def main(unused_args):
  strip_unused_lib.strip_unused_from_files(FLAGS.input_graph,
                                           FLAGS.input_binary,
                                           FLAGS.output_graph,
                                           FLAGS.input_node_names,
                                           FLAGS.output_node_names,
                                           FLAGS.placeholder_type_enum)

if __name__ == "__main__":
  tf.app.run()
