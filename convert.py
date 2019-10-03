import tensorflow as tf

graph_def_file = "retrained_graph.pb"
input_arrays = ["model_inputs"]
output_arrays = ["model_outputs"]

converter = tf.contrib.lite.TFLiteConverter.from_saved_model(graph_def_file)
tflite_model = converter.convert()
open("converted_model.tflite", "wb").write(tflite_model)

