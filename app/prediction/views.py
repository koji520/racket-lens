from django.shortcuts import render

from .forms import ImageUploadForm
from .inference import predict_racket
from .sources import RACKETS

def predict(request):
  if request.method == "POST":
    form = ImageUploadForm(request.POST, request.FILES)
    if form.is_valid():
      prediction = predict_racket(form.cleaned_data["image"])
      img_data = request.POST.get('img_data')
      return render(
          request, "home.html", {"form": form, "prediction": prediction, "img_data": img_data}
      )
  else:
    form = ImageUploadForm()

  return render(request, "home.html", {"form": form})

def description(request):
  return render(request, "description.html", {"rackets": RACKETS})