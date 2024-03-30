from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import onnxruntime
import numpy as np
from PIL import Image

imageClassList = {'0': 'Коттедж', '1': 'Таунхаус', '2': 'Хрущёвка'}  # Сюда указать классы


def scoreImagePage(request):
    return render(request, 'scorepage.html')


def predictImage(request):
    fileObj = request.FILES['filePath']
    fs = FileSystemStorage()
    filePathName = fs.save(('images/' + fileObj.name).replace(' ', '_'), fileObj)
    filePathName = fs.url(filePathName)
    modelName = request.POST.get('modelName')
    scorePrediction = predictImageData(modelName, '.' + filePathName)
    image = filePathName
    description = "Не один из классов"
    fitches = []
    if scorePrediction == imageClassList['0']:
        description = "Коттедж - это жилой дом, обычно одно- или двухэтажный, расположенный на отдельном участке земли. Коттеджи часто имеют просторную планировку и обширную территорию вокруг себя. Они обычно предназначены для проживания одной семьи и обладают большей приватностью и комфортом по сравнению с многоквартирными зданиями."
        fitches = ["1) Этажность: 2 этажей в среднем",
                   "2) Прямоугольная крыша",
                   "3) Один вход"
                   ]
    elif scorePrediction == imageClassList['1']:
        description = "Таунхаус - это тип жилого здания, которое обычно характеризуется узкой и высокой структурой и часто имеет общие стены с соседними единицами. Таунхаусы обычно являются частью более крупного комплекса или застройки и предназначены для максимального использования жилой площади в городских или пригородных районах. "
        fitches = ["1) Этажность: 2 этажа в среднем",
                   "2) Много повторямых элементов в форме крыши здания, соединённые между собой"
                   ]
    elif scorePrediction == imageClassList['2']:
        description = "Хрущёвка - это тип жилого здания, которое было построено во время правления Никиты Хрущева в Советском Союзе. Эти здания обычно представляют собой пятиэтажные квартирные блоки, состоящие из сборных панелей. "
        fitches = ["1) Этажность: 5 этажей в среднем",
                   "2) Прямоугольная форма",
                   "3) Большое количество подъездов"
                   ]
    context = {'scorePrediction': scorePrediction, "image": image, "description": description, "fitches": fitches}
    return render(request, 'scorepage.html', context)


def predictImageData(modelName, filePath):
    img = Image.open(filePath).convert("RGB")
    img = np.asarray(img.resize((32, 32), Image.LANCZOS))
    sess = onnxruntime.InferenceSession(
        r'C:\Users\Kolya\Desktop\Учёба\РНС\Дз 1\media\models\cifar100.onnx')  # <-Здесь требуется указать свой путь к модели
    outputOFModel = np.argmax(sess.run(None, {'input': np.asarray([img]).astype(np.float32)}))
    score = imageClassList[str(outputOFModel)]
    return score
