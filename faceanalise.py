from traceback import print_tb
import boto3
import json

client = boto3.client('rekognition',region_name='us-east-1')
s3 = boto3.resource('s3')

def detecta_faces():
    faces_detectadas = client.index_faces(
        CollectionId='faces',
        DetectionAttributes=['DEFAULT'],
        ExternalImageId='TEMPORARIA',
        Image={
            'S3Object' : {
                'Bucket' : 'vlcp',
                'Name' : 'analise.jpg',
            },
        },
    )
    # print(json.dumps(faces_detectadas, indent=4))
    return faces_detectadas

def cria_lista_faceId_detectadas(faces_detectadas):
    faceId_detectadas = []
    for imagens in range(len(faces_detectadas['FaceRecords'])):
        faceId_detectadas.append(faces_detectadas['FaceRecords'][imagens]['Face']['FaceId'])
    return faceId_detectadas
        
        
def compara_imagens(faceId_detectadas):
    resultado_comparacao = []
    for ids in faceId_detectadas:
        resultado_comparacao.append(
            client.search_faces(
                CollectionId='faces',
                FaceId=ids,
                FaceMatchThreshold=80,
                MaxFaces=10,
            )
        )
    return resultado_comparacao
    
def gera_dados_json(resultado_comparacao):
    dados_json = []
    for face_matches in resultado_comparacao:
        if(len(face_matches.get('FaceMatches'))) >= 1:
            perfil = dict(nome=face_matches['FaceMatches'][0]['Face']['ExternalImageId'],
                          faceMatch=round(face_matches['FaceMatches'][0]['Similarity'],2))
            dados_json.append(perfil)
    return dados_json

faces_detectadas = detecta_faces() 
faceId_detectadas = cria_lista_faceId_detectadas(faces_detectadas)
resultado_comparacao = compara_imagens(faceId_detectadas)
dados_json = gera_dados_json(resultado_comparacao)
print(json.dumps(dados_json, indent=4))