import tensorflow as tf

num_gpu_available = len(tf.config.experimental.list_physical_devices("GPU"))
print("Num GPUs Available:", num_gpu_available)
assert num_gpu_available == 1
