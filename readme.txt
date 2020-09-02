Crie uma pasta chamada 'dataset' na mesma pasta dos arquivos encode_faces.py e pi_face_recognition.py 
contendo pastas com os nomes das pessoas e fotos dentro das respectivas pastas.


Para realizar o processamento das imagens e gerar o arquivo de encodings:

	python encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method hog


Para reconhecer os rostos:

	python pi_face_recognition.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle


Passo a passo para preparar sistema:
	-A versão necessária do Python é a 3.6.x-

	Recomendados:
		1. sudo apt-get update
		2. conda create --name "nome_de_sua_escolha" python=3.6
		3. conda activate "nome_de_sua_escolha"

	Obrigatórios:
		4. sudo apt-get install build-essential cmake
		5. sudo apt-get install libopenblas-dev liblapack-dev
		6. sudo apt-get install libx11-dev libgtk-3-dev
		7. pip install opencv-contrib-python
		8. pip install dlib -vvv
		9. pip install face_recognition -vvv
	   10. pip install imutils
