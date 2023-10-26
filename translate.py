column = ['building', 'room_number', 'capacity']

data = [
('Packard', '101', '500'),
('Painter', '514', '10'),
('Taylor', '3128', '70'),
('Watson', '100', '30'),
('Watson', '120', '50')
]

print('[')
for i in range(len(data)):
    print("{")
    for j in range(len(column)):
        print(" "+column[j]+': '+'"'+data[i][j]+'"'+',')
    print("},")
print(']')
