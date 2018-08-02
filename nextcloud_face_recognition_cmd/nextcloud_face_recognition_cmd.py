#!/usr/bin/env python3
import argparse
import os, re
import face_recognition
import json

data = {}

def response_append_face(filename, name, distance, top, right, bottom, left, encoding=None):
    data['faces-locations'].append({
         'filename': filename,
         'name': name,
         'distance': distance,
         'top': top,
         'right': right,
         'bottom': bottom,
         'left': left,
         'encoding': encoding.tolist() if encoding is not None else None
    })

def response_append_status(message):
    data['status'].append({
         'message': message
    })

def image_find_faces(filename):
    try:
        image = face_recognition.load_image_file(filename)
        face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="hog")
        face_encodings = face_recognition.face_encodings(image, face_locations)
    except:
        response_append_status("Fail to analyze: {}".format(filename))
        return

    if len(face_locations) == 0:
        response_append_face(filename, 'empty', 0.0, 0, 0, 0, 0)
        return

    for unknown_encoding, location in zip (face_encodings, face_locations):
        top, right, bottom, left = location
        response_append_face(filename, 'unknown', 1.0, top, right, bottom, left, unknown_encoding)

def folder_find_faces(path):
    if path.startswith('.'):
        return
    for filename in os.listdir(path):
        fullpath = os.path.join(path, filename)
        if os.path.isdir (fullpath):
            folder_find_faces (fullpath)
        else:
            if fullpath.lower().endswith(('.png','.jpg','.jpeg')):
                image_find_faces (fullpath)

def analyze_list (args):
    data['status'] = []
    data['faces-locations'] = []

    for filename in args.search:
        if os.path.isdir (filename):
            folder_find_faces(filename)
        else:
            if filename.lower().endswith(('.png','.jpg','.jpeg')):
                image_find_faces (filename)
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

    args = parser.parse_args()
    op = {
        'analyze': analyze_list,
    }[args.operation[0]]

    exit(op(args))

if __name__ == '__main__':
    main()
