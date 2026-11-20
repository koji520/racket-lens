from django.shortcuts import render
from .forms import ImageUploadForm
from django.conf import settings
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from io import BytesIO
import numpy as np
import os

def predict(request):
    if request.method in ('GET', 'HEAD'):
        form = ImageUploadForm()
        return render(request, 'home.html', {'form': form})
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img_file = form.cleaned_data['image']
            img_file = BytesIO(img_file.read())
            img = load_img(img_file, target_size=(256, 256))
            img_array = img_to_array(img)
            img_array = img_array.reshape((1, 256, 256, 3))
            img_array = img_array/255
            model_path = os.path.join(settings.BASE_DIR, 'prediction', 'models', 'racket_classifier_model.keras')
            model = load_model(model_path)
            result = model.predict(img_array)
            max_result = np.argmax(result[0])

            match max_result:
                case 0:
                    prediction = 'Pure Aero'
                case 1:
                    prediction = 'Pure Drive'
                case 2:
                    prediction = 'Ezone'
                case 3:
                    prediction = 'Vcore'
                case _:
                    prediction = 'どれでもない'
            return render(request, 'home.html', {'form': form, 'prediction': prediction})
        else:
            form = ImageUploadForm()
            return render(request, 'home.html', {'form': form})
