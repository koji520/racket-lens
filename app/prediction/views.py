import gc
from io import BytesIO
import os

from django.conf import settings
from django.shortcuts import render
import numpy as np

from .forms import ImageUploadForm


def predict(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # POST時のみTensorFlowを読み込む
            from tensorflow.keras.models import load_model
            from tensorflow.keras.preprocessing.image import img_to_array, load_img

            model = None
            try:
                img_file = form.cleaned_data["image"]
                img_stream = BytesIO(img_file.read())

                img = load_img(img_stream, target_size=(256, 256))
                img_array = img_to_array(img).reshape((1, 256, 256, 3)) / 255.0

                model_path = os.path.join(
                    settings.BASE_DIR,
                    "prediction",
                    "models",
                    "racket_classifier_model.keras",
                )
                model = load_model(model_path, compile=False)
                result = model(img_array, training=False).numpy()
                max_result = int(np.argmax(result[0]))

                match max_result:
                    case 0:
                        prediction = "Pure Aero"
                    case 1:
                        prediction = "Pure Drive"
                    case 2:
                        prediction = "Ezone"
                    case 3:
                        prediction = "Vcore"
                    case _:
                        prediction = "どれでもない"

                return render(
                    request, "home.html", {"form": form, "prediction": prediction}
                )
            finally:
                del model
                gc.collect()
    else:
        form = ImageUploadForm()

    return render(request, "home.html", {"form": form})