import json

location_camera = []
# data = {"Location": "", "Floor": 0, "Cluster": ""}

while True:
    data = {"Location": input('Nama Lokasi: '),
            "Floor": int(input('Lantai: ')),
            "Camera": input('Camera: ')}

    print(data)
    location_camera.append(data)

    nextCamera = input('Lanjut? [y/n] ')
    if nextCamera == 'y':
        continue
    else:
        break

print(location_camera)

with open('Location-Camera.json', 'w') as f:
    json.dump(location_camera, f)
