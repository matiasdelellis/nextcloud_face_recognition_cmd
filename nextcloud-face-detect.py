#!/usr/bin/env python3
import argparse
import os, re
import face_recognition
import json

data = {}

def image_find_faces(path):
    print("Searching faces on: {}".format(path))
    image = face_recognition.load_image_file(path)
    face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="hog")
    faces = len(face_locations)
    if faces > 0:
        print("  I found {} face(s) in this photograph.".format(faces))

    for face_location in face_locations:
        top, right, bottom, left = face_location
        data['faces-locations'].append({
            'filemame': path,
            'top': top,
            'right': right,
            'bottom': bottom,
            'left': left
        })

def folder_detect_faces (path):
    for filename in os.listdir(path):
        fullpath = os.path.join(path, filename)
        if os.path.isdir (fullpath):
            folder_detect_faces (fullpath)
        else:
            if fullpath.lower().endswith(('.png','.jpg','.jpeg')):
                image_find_faces (fullpath)

def update_folder(a):
    data['faces-locations'] = []
    folder_detect_faces(a.folder)
    jsonfile = os.path.join(a.folder, '.faces.json')
    with open(jsonfile, 'w') as f:
        json.dump(data, f, indent=4)

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Manage users for PraghaServer')
    parser.add_argument('operation', nargs='+', choices=['update'], help='Operation')
    parser.add_argument('--folder', type=str, help='Folder to search faces recursively')
    parser.add_argument('--to-known', type=str, help='Folder to add face to assign name')
    parser.add_argument('--known', type=str, help='Folder know face to compare')

    args = parser.parse_args()
    op = {
        'update': update_folder,
    }[args.operation[0]]

    exit(op(args))