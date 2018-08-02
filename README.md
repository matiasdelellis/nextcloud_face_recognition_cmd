# nextcloud_face_recognition_cmd
Yet another tool to analyze images to search for faces, which tries to be useful for nextcloud..

In principle the idea is only to detect the faces ... Later how to show it in the interface, it is debatable ..
How would it work?

> nextcloud-face-recognition-cmd analyze --search /media/datos/Services/nextcloud/data/matias/files/Photos/

When it finishes, it creates a json file with the position of the faces in the files:
```
[matias@delellis facerecognition]$ nextcloud-face-recognition-cmd analyze --search /media/datos/Services/nextcloud/data/matias/files/Photos/
{
  "status": [],
  "faces-locations": [
    {
      "filename": "/media/datos/Services/nextcloud/data/matias/files/Photos/IMG-20151008-WA0006.jpg",
      "name": "unknown",
      "distance": 1.0,
      "top": 174,
      "right": 273,
      "bottom": 353,
      "left": 94,
      "encoding": [
        0.06392085552215576,
        -0.08724345266819,
        -0.011156797409057617,
        -0.02944638580083847,
        .....................
      ]
    },
    {
      "filename": "/media/datos/Services/nextcloud/data/matias/files/Photos/IMG-20151008-WA0006.jpg",
      "name": "unknown",
      "distance": 1.0,
      "top": 228,
      "right": 559,
      "bottom": 377,
      "left": 410,
      "encoding": [
        -0.05560929328203201,
        0.10869283974170685,
        0.08669254183769226,
        -0.16590343415737152,
        .....................
      ]
    },
    {
      "filename": "/media/datos/Services/nextcloud/data/matias/files/Photos/IMG-20170922-WA0025.jpg",
      "name": "unknown",
      "distance": 1.0,
      "top": 336,
      "right": 714,
      "bottom": 646,
      "left": 405,
      "encoding": [
        -0.030378900468349457,
        0.09909146279096603,
        0.07931775599718094,
        -0.06877224147319794,
        .....................
      ]
    },
    {
      "filename": "/media/datos/Services/nextcloud/data/matias/files/Photos/IMG-20170922-WA0027.jpg",
      "name": "unknown",
      "distance": 1.0,
      "top": 156,
      "right": 527,
      "bottom": 527,
      "left": 156,
      "encoding": [
        0.051517583429813385,
        0.11508943140506744,
        0.05868631601333618,
        -0.0627085417509079,
        .....................
      ]
    },
    {
      "filename": "/media/datos/Services/nextcloud/data/matias/files/Photos/IMG-20170921-WA0002.jpeg",
      "name": "unknown",
      "distance": 1.0,
      "top": 701,
      "right": 938,
      "bottom": 1236,
      "left": 403,
      "encoding": [
        -0.05293906852602959,
        0.12819457054138184,
        0.06564678251743317,
        -0.018265023827552795,
        .....................
      ]
    }
  ]
}
```

**How to install?**

 * Just depend on https://github.com/ageitgey/face_recognition/
