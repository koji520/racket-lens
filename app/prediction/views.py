from django.shortcuts import render

from .forms import ImageUploadForm
from .inference import predict_racket


def predict(request):
  if request.method == "POST":
    form = ImageUploadForm(request.POST, request.FILES)
    if form.is_valid():
      prediction = predict_racket(form.cleaned_data["image"])
      return render(
          request, "home.html", {"form": form, "prediction": prediction}
      )
  else:
    form = ImageUploadForm()

  return render(request, "home.html", {"form": form})