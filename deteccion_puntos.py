import numpy as np


def get_puntos_rostro():
    
    lista_detecciones = leer_puntos()
   
    # separa los tipos de detecciones 
    
    face_detections = [det for det in lista_detecciones if det[0] == 'Face']
    eye_detections = [det for det in lista_detecciones if det[0] == 'Eye']
    nose_detections = [det for det in lista_detecciones if det[0] == 'Nose']
    mouth_detections = [det for det in lista_detecciones if det[0] == 'Mouth']

    
    filtered_faces = non_max_suppression(face_detections)
    filtered_eyes = non_max_suppression(eye_detections)
    filtered_noses = non_max_suppression(nose_detections)
    filtered_mouths = non_max_suppression(mouth_detections)

    
    best_face = filtered_faces
    best_eyes = filtered_eyes
    best_nose = filtered_noses
    best_mouths = filtered_mouths

    puntos_rostro = [best_face, best_eyes, best_nose, best_mouths]

    # Display the results
    # print("Best Face:", best_face[0])
    # print("Best Eyes:", best_eyes[0])
    # print("Best Nose:", best_nose[0])
    # print("Best Mouths:", best_mouths[0])

    return puntos_rostro


def leer_puntos():
    with open('./static/Images/datos_1.txt', 'r') as file:
        detections = file.read()

    # obtener lista de detecciones
    detection_list = []
    for line in detections.strip().split('\n'):
        parts = line.split(': ')
        label = parts[0]
        coords = list(map(int, parts[1].split(', ')))
        detection_list.append((label, coords))

    return detection_list


def non_max_suppression(detections, overlap_thresh=0.3):
    if len(detections) == 0:
        return []

    # Convert detections to array
    boxes = np.array([det[1] for det in detections])
    labels = [det[0] for det in detections]
    
    # Initialize the list of picked indexes
    pick = []

    # Calculate the coordinates of the bounding boxes
    x1 = boxes[:,0]
    y1 = boxes[:,1]
    x2 = boxes[:,0] + boxes[:,2]
    y2 = boxes[:,1] + boxes[:,3]

    # Compute the area of the bounding boxes and sort by the bottom-right y-coordinate
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)

    while len(idxs) > 0:
        # Grab the last index in the indexes list and add the index value to the list of picked indexes
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        # Find the largest (x, y) coordinates for the start of the bounding box
        # and the smallest (x, y) coordinates for the end of the bounding box
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        # Compute the width and height of the bounding box
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        # Compute the ratio of overlap
        overlap = (w * h) / area[idxs[:last]]

        # Delete all indexes from the index list that have overlap greater than the provided overlap threshold
        idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlap_thresh)[0])))

    # Return only the picked detections
    return [(labels[i], boxes[i].tolist()) for i in pick]

print("mejores puntos")
get_puntos_rostro()

