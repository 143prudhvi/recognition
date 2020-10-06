from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import cv2
import os
from django.core.paginator import Paginator
import face_recognition
from .models import Person
from .form import PersonForm
from django.contrib import messages
import numpy as np
# Create your views here.


# def index(request):
#     return render(request, 'face/known_upload.html')

def face(request):
    return render(request, 'face/index.html')

def detect(request):
    myfile = request.FILES['image']
    fs = FileSystemStorage()
    filename = fs.save('unknown/'+myfile.name, myfile)
    uploaded_file_url = fs.url(filename)
    encodes = []
    names = []
    files = []

    person = Person.objects.all()
    for i in person:
        encodes.append(i.name + '_face_encoding')
        files.append(i.picture.url[1:])   # /media/known/filename.jpg
        names.append(i.name)

    for i in range(0, len(encodes)):
        image = face_recognition.load_image_file(files[i])
        encodes[i] = face_recognition.face_encodings(image)[0]
    uploadedimg = cv2.imread(uploaded_file_url[1:])
    width = uploadedimg.shape[1]
    height = uploadedimg.shape[0]
    if width >= 1000 and height >= 1000:
        uploadedimg = cv2.resize(uploadedimg, (0, 0), fx=0.1, fy=0.1)
    upload_locations = face_recognition.face_locations(uploadedimg)
    upload_encoding = face_recognition.face_encodings(uploadedimg, upload_locations)
    for (t, r, b, l), encode in zip(upload_locations, upload_encoding):
        result = face_recognition.compare_faces(encodes, encode)
        name = 'Unknown'
        face_distances = face_recognition.face_distance(encodes, encode)
        best_match_index = np.argmin(face_distances)
        if result[best_match_index]:
            name = names[best_match_index]
        cv2.rectangle(uploadedimg, (l, t), (r, b), (0, 255, 255), 3)
        cv2.putText(uploadedimg, name, (l+2, t-20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 2)
    cv2.imwrite('media/output.jpg', uploadedimg)
    return render(request, 'face/output.html')

def upload(request):
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('display')
    else:
        form = PersonForm()
    return render(request, 'face/known_upload.html', {'form': form})

def display(request):
    persons = Person.objects.all()
    paginator = Paginator(persons, 2)
    page = request.GET.get('page')
    persons = paginator.get_page(page)
    return render(request, 'face/display.html', {'persons': persons})
