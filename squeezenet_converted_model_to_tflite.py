import tensorflow as tf
print(tensorflow.__version__)
# converter = tf.lite.TFLiteConverter.from_keras_model('model_squeeze.h5') 
# # tflite_model = converter.convert()

# # with open('model.tflite' , 'wb') as f:
# #     f.write(tflite_model)




# # model = create_empty_model() #your model definition from keras that you create when you train
# # model.load_weights(".../model.h5",compile=False)
# # converter = tf.lite.TFLiteConverter.from_keras_model(tflite_model)
# # tflite_save = converter.convert()
# # open("short-train.tflite", "wb").write(tflite_save)

# converter.experimental_new_converter = True
# tflite_model = converter.convert()

# #salva o modelo em memória.
# with open('model.tflite', 'wb') as f:
#   f.write(tflite_model)