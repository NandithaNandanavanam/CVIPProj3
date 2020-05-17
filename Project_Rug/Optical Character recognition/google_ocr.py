import io
import sys
import os
import cv2
import json
import ner
from google.cloud import vision
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='glass-turbine-246812-60a2f3d98ecf.json'

def detect_text(path):
    """Detects text in the file."""
   
    client = vision.ImageAnnotatorClient()
    img = cv2.imread(path)
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print(texts)
    print('Texts:')
    with open('text_'+sys.argv[1].split('.')[0]+'.txt', 'a') as the_file:
        the_file.write(texts[0].description)
    results = ner.NLP(texts[0].description)
    with open('data.json', 'w') as fp:
        json.dump(results, fp)
    for text in texts[1:]:
        print('\n"{}"'.format(text.description))

        vertices = ([(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])
        print(vertices)
        cv2.line(img, vertices[0], vertices[1], (0, 255, 0))
        cv2.line(img, vertices[1], vertices[2], (0, 255, 0))
        cv2.line(img, vertices[2], vertices[3], (0, 255, 0))
        cv2.line(img, vertices[3], vertices[0], (0, 255, 0))

        print('bounds: ',vertices)
    cv2.imwrite('result_'+path, img)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

detect_text(sys.argv[1])
