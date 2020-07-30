Crie uma pasta chamada 'dataset' no mesma pasta dos arquivos encode_faces.py e pi_face_recognition.py 
contendo pastas com os nomes das pessoas e fotos dentro das respectivas pastas.


Para realizar o processamento das imagens e gerar o arquivo de encodings:

	python encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method hog


Para reconhecer os rostos:

	python pi_face_recognition.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle


Passo a passo para preparar sistema:

	Recomendados:
		1. conda create --name "nome_de_sua_escolha" python=3.6
		2. conda activate "nome_de_sua_escolha"

	Obrigatórios:
		3. pip install opencv-contrib-python
		4. pip install dlib -vvv
		5. pip install face_recognition -vvv
		6. pip install imutils
