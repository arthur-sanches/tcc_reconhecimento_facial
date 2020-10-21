# importa os pacotes necessários
from imutils import paths
import face_recognition
import pickle
import cv2
import os


def isEncoded(fileName):
    if(fileName.startswith('encoded-')):
        return True
    else:
        return False


dataset_path = "dataset"
detection_method = "hog"
encodings_path = "encodings.pickle"

# pega os caminhos das imagens de entrada da pasta dataset
print("[INFO] quantifying faces...")
imagePaths = [imagePath for imagePath in list(paths.list_images(
    dataset_path)) if not isEncoded(imagePath.split(os.path.sep)[-1])]

# inicializa a lista de codificações e nomes conhecidos
knownEncodings = []
knownNames = []

# passa pelos caminhos das imagens
for (i, imagePath) in enumerate(imagePaths):
    # extrai o nome da pessoa do caminho da imagem
    name = imagePath.split(os.path.sep)[-2]
    fileName = imagePath.split(os.path.sep)[-1]

    if(not isEncoded(fileName)):
        print("[INFO] processing image {}/{}".format(i + 1,
                                                     len(imagePaths)))

        # carrega a imagem de entrada e a converte de BGR (ordenação do OpenCV)
        # para RGB (ordenação do dlib)
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detecta as coordenadas (x, y) das caixas delimitadoras
        # correspondentes para cada face nas imagens de entrada
        boxes = face_recognition.face_locations(rgb,
                                                model=detection_method)

        # processa as incorporações (embedding) faciais para a face
        encodings = face_recognition.face_encodings(rgb, boxes)

        # passa pelas codificações (encodings)
        for encoding in encodings:
            # adiciona cada codificação + nome para nosso conjunto de
            # codificações e nomes conhecidos
            knownEncodings.append(encoding)
            knownNames.append(name)
            print(f"Name: {name}  -  Encoding: {encoding}")

        newFileName = 'encoded-' + fileName

        newImagePath = os.path.split(imagePath)[0] + '/' + newFileName

        os.rename(imagePath, newImagePath)

# grava as codificações faciais + nomes no disco
print("[INFO] serializing encodings...")

if(len(knownNames) > 0 and len(knownEncodings) > 0):
    if(os.path.exists(encodings_path)):
        with open("encodings.pickle", "rb") as f:
            data = pickle.loads(f.read())
            data['encodings'].extend(knownEncodings)
            data['names'].extend(knownNames)
    else:
        data = {"encodings": knownEncodings, "names": knownNames}

    with open("encodings.pickle", "wb") as f:
        f.write(pickle.dumps(data))
