# nextcloud_face_recognition_cmd
Yet another tool to analyze images to search for faces, which tries to be useful for nextcloud..

In principle the idea is only to detect the faces ... Later how to show it in the interface, it is debatable ..
How would it work?
> ./nextcloud-face-detect.py update --folder /media/datos/Services/nextcloud/data/matias/files/

When it finishes, it creates a json file with the position of the faces in the files:
```$ cat /media/datos/Services/nextcloud/data/matias/files/Imágenes/Android/.faces.json 
{
    "faces-locations": [
        {
            "filemame": "/media/datos/Services/nextcloud/data/matias/files/Im\u00e1genes/Android/IMG_20170122_123907941_HDR.jpg",
            "top": 577,
            "right": 955,
            "bottom": 886,
            "left": 646
        },
        {
            "filemame": "/media/datos/Services/nextcloud/data/matias/files/Im\u00e1genes/Android/IMG_20170122_123907941_HDR.jpg",
            "top": 280,
            "right": 1394,
            "bottom": 651,
            "left": 1023
        },
        {
            "filemame": "/media/datos/Services/nextcloud/data/matias/files/Im\u00e1genes/Android/IMG_20170122_123856291_TOP.jpg",
            "top": 651,
            "right": 734,
            "bottom": 1023,
            "left": 362
        },
```

**How to install?**

 * Just depend on https://github.com/ageitgey/face_recognition/
