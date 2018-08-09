#!/usr/bin/env python3
import argparse
import os, re
import dlib
import numpy as np
import json

class NcFaceRecognition:
    def __init__(self, predictor, model):
        self.data = {}
        self.sp = dlib.shape_predictor(predictor)
        self.facerec = dlib.face_recognition_model_v1(model)
        self.detector = dlib.get_frontal_face_detector()
        self.data['status'] = []
        self.data['faces-locations'] = []

    def appendFace(self, filename, name, distance, top, right, bottom, left, encoding=None):
        self.data['faces-locations'].append({
                  'filename': filename,
                  'name': name,
                  'distance': distance,
                  'top': top,
                  'right': right,
                  'bottom': bottom,
                  'left': left,
                  'encoding': encoding.tolist() if encoding is not None else None
        })

    def appendStatus(self, message):
        self.data['status'].append({
                  'message': message
        })

    def findFaces(self, filename):
        try:
            img = dlib.load_rgb_image(filename)
        except:
            return

        dets = self.detector(img, 1)
        if len(dets) == 0:
            self.appendFace(filename, 'empty', 0.0, 0, 0, 0, 0)
            return

        for k, d in enumerate(dets):
            shape = self.sp(img, d)
            face_descriptor = np.array(self.facerec.compute_face_descriptor(img, shape))
            self.appendFace (filename, "unknown", 1.0, d.top(), d.right(), d.bottom(), d.left(), face_descriptor)

    def folderFind(self, path):
        if path.startswith('.'):
            return

        for filename in os.listdir(path):
            fullpath = os.path.join(path, filename)
            if os.path.isdir (fullpath):
                self.folderFind (fullpath)
            else:
                if fullpath.lower().endswith(('.png','.jpg','.jpeg')):
                    self.findFaces (fullpath)

    def analyze(self, filename):
        if os.path.isdir (filename):
            self.folderFind(filename)
        else:
            if filename.lower().endswith(('.png','.jpg','.jpeg')):
                self.findFaces (filename)

    def dump(self):
        print(json.dumps(self.data, ensure_ascii=False, indent=2))

# Main App.

def analyze_list (args):
    nc = NcFaceRecognition (args.predictor[0], args.model[0])
    for filename in args.search:
        nc.analyze(filename)
    nc.dump()
    return 0

def print_status (args):
    version = dlib.__version__
    data = {}
    data['dlib-version'] = version
    data['cuda-support'] = dlib.DLIB_USE_CUDA
    data['avx-support'] =  dlib.USE_AVX_INSTRUCTIONS
    data['neon-support'] = dlib.USE_NEON_INSTRUCTIONS

    print (json.dumps(data, ensure_ascii=False, indent=2))

    return 0

def main():
    parser = argparse.ArgumentParser(description='Analyze pictures in search of faces')
    parser.add_argument('operation', nargs='+', choices=['analyze', 'status'], help='Operation')
    parser.add_argument('--predictor', nargs='+', help='Predictor used to search faces')
    parser.add_argument('--model', nargs='+', help='Model used to search faces')
    parser.add_argument('--search', nargs='+', help='List of pictures or folders to search faces')

    args = parser.parse_args()
    op = {
        'analyze': analyze_list,
        'status': print_status,
    }[args.operation[0]]

    exit(op(args))

if __name__ == '__main__':
    main()
