from io import BytesIO
import os

from django.conf import settings
import numpy as np
import onnxruntime as ort
from PIL import Image

from .sources import RACKETS

TARGET_SIZE = (256, 256)


def preprocess_image(
    uploaded_file, target_size=TARGET_SIZE, scale="mobilenet_v2"
):
  img = Image.open(BytesIO(uploaded_file.read())).convert("RGB")
  img = img.resize(target_size, Image.Resampling.BILINEAR)
  arr = np.asarray(img, dtype=np.float32)

  if scale == "mobilenet_v2":
    arr = (arr / 127.5) - 1.0
  elif scale == "div255":
    arr = arr / 255.0

  return np.expand_dims(arr, axis=0)


def predict_racket(uploaded_file):
  model_path = os.path.join(
      settings.BASE_DIR,
      "prediction",
      "models",
      "racket_classifier_model.onnx",
  )

  opts = ort.SessionOptions()
  opts.intra_op_num_threads = 1
  opts.inter_op_num_threads = 1
  opts.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL

  session = ort.InferenceSession(
      model_path, sess_options=opts, providers=["CPUExecutionProvider"]
  )
  input_name = session.get_inputs()[0].name

  x = preprocess_image(uploaded_file)
  outputs = session.run(None, {input_name: x})
  probs = outputs[0][0]
  idx = int(np.argmax(probs))

  return RACKETS[idx] if idx < len(RACKETS) else "どれでもない"