import json
import os

def GenerateColorScheme(path: str) -> list[list[str]]:

    with open(path) as json_data:
          color_data = json.load(json_data)['colors']
          json_data.close()

    color_scheme = []
    for i in range(8):
        left_color = 'color'+str(i)
        right_color = 'color'+str(i+8)
        new_element = [color_data[left_color], color_data[right_color]]
        color_scheme.append(new_element)

    return color_scheme


file_location = os.path.expanduser('~') + '/.theming/colors.json'
print(GenerateColorScheme(file_location))

    
