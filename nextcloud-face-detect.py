#!/usr/bin/env python3
import argparse
import os, re
import face_recognition
import json

data = {}

def scan_known_people(folder):
    known_names = []
    known_face_encodings = []

    for filename in os.listdir(folder):
        fullpath = os.path.join(folder, filename)
        basename = os.path.splitext(os.path.basename(fullpath))[0]
        img = face_recognition.load_image_file(fullpath)
        encodings = face_recognition.face_encodings(img)

        if len(encodings) > 1:
            print ("WARNING: More than one face found in {}. Only considering the first face.".format(filename))

        if len(encodings) == 0:
            print("WARNING: No faces found in {}. Ignoring file.".format(filename))
        else:
            known_names.append(basename)
            known_face_encodings.append(encodings[0])

    return known_names, known_face_encodings

def image_find_faces(filename, known_encodings, known_names):
    print("Searching faces on: {}".format(filename))
    try:
        image = face_recognition.load_image_file(filename)
        face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="hog")
        face_encodings = face_recognition.face_encodings(image, face_locations)
    except:
        print("Fail to analyze: {}".format(filename))
        return

    for unknown_encoding, location in zip (face_encodings, face_locations):
        distances = face_recognition.face_distance(known_encodings, unknown_encoding)
        result = list(distances <= 0.6)
        if True in result:
            for distance, name in zip(distances, known_names):
                if distance > 0.6:
                    continue
                top, right, bottom, left = location
                print("{},{},{},{},{},{},{}".format(filename, name, distance, top, right, bottom, left))
                data['faces-locations'].append({
                     'filemame': filename,
                     'name': name,
                     'distance': distance,
                     'top': top,
                     'right': right,
                     'bottom': bottom,
                     'left': left
                })
        else:
            name = 'Unknown'
            top, right, bottom, left = location
            distance = 1.0
            print("{},{},{},{},{},{},{}".format(filename, name, distance, top, right, bottom, left))
            data['faces-locations'].append({
                'filemame': filename,
                'name': name,
                'distance': distance,
                'top': top,
                'right': right,
                'bottom': bottom,
                'left': left
            })

def folder_detect_faces (path, known_encodings, known_names):
    for filename in os.listdir(path):
        fullpath = os.path.join(path, filename)
        if os.path.isdir (fullpath):
            folder_detect_faces (fullpath, known_encodings, known_names)
        else:
            if fullpath.lower().endswith(('.png','.jpg','.jpeg')):
                image_find_faces (fullpath, known_encodings, known_names)

def analyze_list (args):
    data['faces-locations'] = []
    known_names, known_encodings = scan_known_people(args.known)

    for filename in args.search:
        if os.path.isdir (filename):
            folder_detect_faces(filename, known_encodings, known_names)
        else:
            if filename.lower().endswith(('.png','.jpg','.jpeg')):
                image_find_faces (filename, known_encodings, known_names)
    if True:
        print (json.dumps(data, ensure_ascii=False, indent=2))
    else:
        #jsonfile = os.path.join(a.folder, '.faces.json')
        print('Saving the .faces.json file with the information')
        with open('.faces.json', 'w') as f:
            json.dump(data, f, indent=2)
    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyze pictures in search of faces')
    parser.add_argument('operation', nargs='+', choices=['analyze'], help='Operation')
    parser.add_argument('--search', nargs='+', help='List of pictures or folder to search faces')
    parser.add_argument('--known', type=str, help='Folder know face to compare')

    args = parser.parse_args()
    op = {
        'analyze': analyze_list,
    }[args.operation[0]]

    exit(op(args))