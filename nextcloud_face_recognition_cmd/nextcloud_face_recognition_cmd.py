#!/usr/bin/env python3
import argparse
import os, re
import face_recognition
import json

data = {}

def response_append_face(filename, name, distance, top, right, bottom, left):
    data['faces-locations'].append({
         'filename': filename,
         'name': name,
         'distance': distance,
         'top': top,
         'right': right,
         'bottom': bottom,
         'left': left
    })

def response_append_status(message):
    data['status'].append({
         'message': message
    })

def scan_known_people(folder):
    known_names = []
    known_face_encodings = []

    for filename in os.listdir(folder):
        if filename.startswith('.'):
            continue
        fullpath = os.path.join(folder, filename)
        basename = os.path.splitext(os.path.basename(fullpath))[0]

        img = face_recognition.load_image_file(fullpath)
        encodings = face_recognition.face_encodings(img)

        if len(encodings) > 1:
            append_status_response("WARNING: More than one face found in {}. Only considering the first face.".format(filename))

        if len(encodings) == 0:
            append_status_response("WARNING: No faces found in {}. Ignoring file.".format(filename))
        else:
            known_names.append(basename)
            known_face_encodings.append(encodings[0])

    return known_names, known_face_encodings


def image_find_faces(filename, known_encodings, known_names):
    try:
        image = face_recognition.load_image_file(filename)
        face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="hog")
        face_encodings = face_recognition.face_encodings(image, face_locations)
    except:
        response_append_status("Fail to analyze: {}".format(filename))
        return

    if len(face_locations) == 0:
        response_append_face(filename, 'empty', 1.0, 0, 0, 0, 0)
        return

    for unknown_encoding, location in zip (face_encodings, face_locations):
        top, right, bottom, left = location
        distances = face_recognition.face_distance(known_encodings, unknown_encoding)
        result = list(distances <= 0.6)
        if True in result:
            for distance, name in zip(distances, known_names):
                if distance <= 0.6:
                    response_append_face(filename, name, distance, top, right, bottom, left)
        else:
            response_append_face(filename, 'Unknown', 1.0, top, right, bottom, left)

def folder_find_faces(path, known_encodings, known_names):
    if path.startswith('.'):
        return
    for filename in os.listdir(path):
        fullpath = os.path.join(path, filename)
        if os.path.isdir (fullpath):
            folder_find_faces (fullpath, known_encodings, known_names)
        else:
            if fullpath.lower().endswith(('.png','.jpg','.jpeg')):
                image_find_faces (fullpath, known_encodings, known_names)

def analyze_list (args):
    data['status'] = []
    data['faces-locations'] = []

    known_names, known_encodings = scan_known_people(args.known)

    for filename in args.search:
        if os.path.isdir (filename):
            folder_find_faces(filename, known_encodings, known_names)
        else:
            if filename.lower().endswith(('.png','.jpg','.jpeg')):
                image_find_faces (filename, known_encodings, known_names)
    if True:
        print (json.dumps(data, ensure_ascii=False, indent=2))
    else:
        with open('.faces.json', 'w') as f:
            json.dump(data, f, indent=2)
    return 0

def main():
    parser = argparse.ArgumentParser(description='Analyze pictures in search of faces')
    parser.add_argument('operation', nargs='+', choices=['analyze'], help='Operation')
    parser.add_argument('--search', nargs='+', help='List of pictures or folders to search faces')
    parser.add_argument('--known', type=str, help='Folder with knonw face pictures to compare')

    args = parser.parse_args()
    op = {
        'analyze': analyze_list,
    }[args.operation[0]]

    exit(op(args))

if __name__ == '__main__':
    main()
