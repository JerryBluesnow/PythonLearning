import json
 
with open('data.json', 'r', encoding='utf-8') as f:
    app_data = json.load(f)
    print(type(app_data))
    print(app_data['Application Path'])
