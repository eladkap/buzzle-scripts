import json


def write_to_json(key: str, array: list, json_file: str):
    if len(array) == 0:
        return
    with open(json_file, 'w') as fp:
        json.dump({key: array}, fp)


def write_to_csv(array: list, csv_file):
    if len(array) == 0:
        return
    with open(csv_file, 'w') as writer:
        fields = list(array[0].keys())
        column_names = ','.join(fields)
        writer.write(f'{column_names}\n')

        for record in array:
            row = ','.join(["\"" + record[field] + "\"" for field in fields])
            writer.write(f'{row}\n')
