x = [
    {
        "name": "Marek",
        "age": "25",
        "animals": [
            {
                "type": "dog",
                "name": "Azor"
            },
            {
                "type": "cat",
                "name": "Filemon"
            }
        ]
    },
    {
        "name": "Kuba",
        "age": "27",
        "animals": [
            {
                "type": "hamster",
                "name": "Speedy"
            },
            {
                "type": "squirrel",
                "name": "Sonia"
            }
        ]
    }
]

for i, j in enumerate(x):
    print("i: ", i)
    print("j: ", j)
