from django.shortcuts import render
import numpy as np
from django.core.files.storage import FileSystemStorage
from tensorflow.keras.models import load_model
from PIL import Image
import json
import tensorflow.compat.v1 as tf
from tensorflow.keras.utils import load_img, img_to_array
from django.http import HttpResponseBadRequest

tf.disable_eager_execution()

img_height, img_width = 128, 128

from roboflow import Roboflow
rf = Roboflow(api_key="uehKBYOpQocYQ5eFQZ0K")
project = rf.workspace().project("bone-fracture-7fylg")
model = project.version(1).model
                    
# Create the graph and session outside the view functions
model_graph = tf.Graph()
with model_graph.as_default():
    tf_session = tf.Session()
    with tf_session.as_default():
        # Load the models
        model1 = load_model('./models/Model.h5')
        model2 = load_model('./models/model_lung.h5')
        model3 = load_model('./models/model_eye.h5')
        model4 = load_model('./models/bonemodel.h5')
        model5 = load_model('./models/kneeModel.h5')
        model6 = load_model('./models/recModel.h5')


def index(request):
    context = {'a': 1}
    return render(request, 'home.html', context)

def firstHome(request):
    context = {'a': 1}
    return render(request, 'firstHome.html', context)

def uploadBrain(request):
    context = {'a': 1}
    return render(request, 'uploadBrain.html', context)


def uploadLung(request):
    context = {'a': 1}
    return render(request, 'uploadLung.html', context)


def uploadEye(request):
    context = {'a': 1}
    return render(request, 'uploadEye.html', context)

def uploadBone(request):
    context = {'a': 1}
    return render(request, 'uploadBone.html', context)

def uploadKnee(request):
    context = {'a': 1}
    return render(request, 'uploadKnee.html', context)


def helpPage(request):
    context = {'a': 1}
    return render(request, 'helpPage.html', context)


def firstHelpPage(request):
    context = {'a': 1}
    return render(request, 'firstHelpPage.html', context)


def login(request):
    context = {'a': 1}
    return render(request, 'login.html', context)

def modelRec(request):
    context = {'a': 1}
    return render(request, 'modelRec.html', context)


def predictImageBrain(request):
    global model1, model_graph, tf_session

    fileObj = request.FILES['filePath']
    fs = FileSystemStorage()
    filePathName = fs.save(fileObj.name, fileObj)
    filePathName = fs.url(filePathName)
    testimage = '.' + filePathName
    img = Image.open(testimage).resize((img_height, img_width))
    x = np.array(img)
    x = x / 255
    x = x.reshape((1, x.shape[0], x.shape[1], x.shape[2]))

    with model_graph.as_default():
        with tf_session.as_default():
            predi = model1.predict(x)
            print(predi, '\n')
            predict_index = np.argmax(predi)
            print(predict_index)
            if predict_index == 2:
                predictedLabel = "No tumor"
            else:
                if predict_index != 2:
                    if predict_index == 0:
                        predictedLabel = "The tumor is: GLIOMA"
                    elif predict_index == 1:
                        predictedLabel = "The tumor is: MENINGIOMA"
                    else:
                        if predict_index == 3:
                            predictedLabel = "The tumor is: PITUITARY"

    print(predictedLabel)
    context = {'filePathName': filePathName, 'predictedLabel': predictedLabel}
    return render(request, 'braintumor.html', context)


def predictImageLung(request):
    global model2, model_graph, tf_session

    img_size = 150
    fileObj = request.FILES['filePath']
    fs = FileSystemStorage()
    filePathName = fs.save(fileObj.name, fileObj)
    filePathName = fs.url(filePathName)
    testimage = '.' + filePathName
    img = Image.open(testimage).resize((img_size, img_size))
    img = img.convert('RGB')

    with model_graph.as_default():
        with tf_session.as_default():
            x = img_to_array(img)
            x /= 255
            x = np.expand_dims(x, axis=0)

            classes = model2.predict(x, batch_size=10)
            print(classes)
            if classes > 0.5:
                predictedLabel = " the presence of pneumonia in the scanned images. It is recommended to consult with a healthcare professional for further evaluation and treatment."
            else:
                predictedLabel = " that you are in a healthy and normal condition!"

    print(predictedLabel)
    context = {'filePathName': filePathName, 'predictedLabel': predictedLabel}
    return render(request, 'lungdesease.html', context)


def predictImageEye(request):
    global model3, model_graph, tf_session

    img_size = 224
    fileObj = request.FILES['filePath']
    fs = FileSystemStorage()
    filePathName = fs.save(fileObj.name, fileObj)
    filePathName = fs.url(filePathName)

    testimage = '.' + filePathName
    img = Image.open(testimage).resize((img_size, img_size))
    img = img.convert('RGB')

    with model_graph.as_default():
        with tf_session.as_default():
            x = img_to_array(img)
            x /= 255
            x = np.expand_dims(x, axis=0)

            classe = np.argmax(model3.predict(x), axis=1)
            print(classe)
            if classe == 3:
                predictedLabel = "there is no eye condition, it's a normal case !"
            else:
                if classe != 3:
                    if classe == 0:
                        predictedLabel = "the eye condition is cataract !"
                    elif classe == 1:
                        predictedLabel = "the eye condition is diabetic_retinopathy !"
                    else:
                        if classe == 2:
                            predictedLabel = "the eye condition is glaucoma !"

    print(predictedLabel)
    context = {'filePathName': filePathName, 'predictedLabel': predictedLabel}
    return render(request, 'eyedesease.html', context)


def predictImageBone(request):
    global model4, model_graph, tf_session

    img_size = 150

    if 'filePath' in request.FILES:
        # File uploaded through the file input field
        fileObj = request.FILES['filePath']
    elif 'filePath' in request.POST:
        # File uploaded through drag-and-drop
        fileObj = request.FILES.get('filePath')
    else:
        # Handle the case when no file is provided
        # Return an appropriate response or redirect to an error page
        # Example: return HttpResponseBadRequest("No file provided")
        return HttpResponseBadRequest("No file provided")

    if fileObj is not None and hasattr(fileObj, 'name'):
        fs = FileSystemStorage()
        filePathName = fs.save(fileObj.name, fileObj)
        filePathName = fs.url(filePathName)
        testimage = '.' + filePathName
        img = Image.open(testimage).resize((img_size, img_size))
        img = img.convert('RGB')

        with model_graph.as_default():
            with tf_session.as_default():
                x = img_to_array(img)
                x /= 255
                x = np.expand_dims(x, axis=0)

                images = np.vstack([x])
                classe = model4.predict(images, batch_size=10)
                if classe > 0.5:
                    predictedLabel = "Not Fractured"
                else:
                    predictedLabel = "Fractured"
                 
                    # visualize your prediction
                    model.predict(testimage, confidence=40, overlap=30).save("media\\bonedetect.jpg")
                    filePathName = "media\\bonedetect.jpg"
            print(predictedLabel)

        context = {'filePathName': filePathName, 'predictedLabel': predictedLabel}
        return render(request, 'boneFracture.html', context)
    else:
        # Handle the case when fileObj is None or has no name attribute
        # Return an appropriate response or redirect to an error page
        # Example: return HttpResponseBadRequest("Invalid file provided")
        return HttpResponseBadRequest("Invalid file provided")



def predictImageKnee(request):
    global model5, model_graph, tf_session

    img_size = 150

    if 'filePath' in request.FILES:
        # File uploaded through the file input field
        fileObj = request.FILES['filePath']
    elif 'filePath' in request.POST:
        # File uploaded through drag-and-drop
        fileObj = request.FILES.get('filePath')
    else:
        # Handle the case when no file is provided
        # Return an appropriate response or redirect to an error page
        # Example: return HttpResponseBadRequest("No file provided")
        return HttpResponseBadRequest("No file provided")

    if fileObj is not None and hasattr(fileObj, 'name'):
        fs = FileSystemStorage()
        filePathName = fs.save(fileObj.name, fileObj)
        filePathName = fs.url(filePathName)
        testimage = '.' + filePathName
        img = Image.open(testimage).resize((img_size, img_size))
        img = img.convert('RGB')

        with model_graph.as_default():
            with tf_session.as_default():
                x = img_to_array(img)
                x /= 255
                x = np.expand_dims(x, axis=0)

                images = np.vstack([x])
                classe = model5.predict(images, batch_size=10)
                if classe <= 0.5:
                    predictedLabel = "there is no Osteoarthritis it's a normal knee scan"
                else:
                    predictedLabel = "there is an Osteoarthritis in the knee scan! It is recommended to consult with a healthcare professional for further evaluation and treatment"
                    
            print(predictedLabel)

        context = {'filePathName': filePathName, 'predictedLabel': predictedLabel}
        return render(request, 'KneeOsteoarthritis.html', context)
    else:
        # Handle the case when fileObj is None or has no name attribute
        # Return an appropriate response or redirect to an error page
        # Example: return HttpResponseBadRequest("Invalid file provided")
        return HttpResponseBadRequest("Invalid file provided")
    
    
def predictImageRec(request):
    global model6, model_graph, tf_session

    img_size = 128
    fileObj = request.FILES['filePath']
    fs = FileSystemStorage()
    filePathName = fs.save(fileObj.name, fileObj)
    filePathName = fs.url(filePathName)

    testimage = '.' + filePathName
    img = Image.open(testimage).resize((img_size, img_size))
    img = img.convert('RGB')

    with model_graph.as_default():
        with tf_session.as_default():
            x = img_to_array(img)
            x /= 255
            x = np.expand_dims(x, axis=0)

            classe = np.argmax(model6.predict(x), axis=1)
            print(classe)
            if classe == 0:
                predictedLabel = "Bone Fracture !"
            else:
                if classe != 0:
                    if classe == 1:
                        predictedLabel = "Brain Tumor !"
                    elif classe == 2:
                        predictedLabel = "Eye Diseases !"
                    else:
                        if classe == 3:
                            predictedLabel = "Knee Osteoarthritis !"
                        else:
                            predictedLabel = "Lung Diseases !"


    print(predictedLabel)
    context = {'filePathName': filePathName, 'predictedLabel': predictedLabel}
    return render(request, 'recResult.html', context)

    
# VIEW ALL IMAGES
def viewDataBase(request):
    import os
    listOfImages = os.listdir('./media/')
    listOfImagesPath = ['./media/' + i for i in listOfImages]
    context = {'listOfImagesPath': listOfImagesPath}
    return render(request, 'viewDB.html', context)

