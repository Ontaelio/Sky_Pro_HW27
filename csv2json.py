import csv
import json

'''
An app to convert CSVs into JSONs for automatic loading.
Use python manage.py loaddata ads.json
and python manage.py loaddata categories.json
to populate database after running this thingie.
'''


def csv_to_json(csv_file, json_file):

    json_list = []

    with open(csv_file, encoding='utf-8') as fin:
        csv_data = csv.DictReader(fin)

        for row in csv_data:
            result = {}
            if row.get('Id'):
                result['pk'] = row.pop('Id')
                result['model'] = 'ads.ad'
            if row.get('id'):
                result['pk'] = row.pop('id')
                result['model'] = 'ads.category'
            if row.get('price'):
                row['price'] = float(row['price'])
            if row.get('is_published'):
                row['is_published'] = True if row['is_published'] == 'TRUE' else False
            print(row)
            result['fields'] = row
            json_list.append(result)

    with open(json_file, 'w', encoding='utf-8') as fout:
        json_string = json.dumps(json_list, indent=4, ensure_ascii=False)
        fout.write(json_string)


if __name__ == "__main__":

    csv_to_json('datasets/ads.csv', 'ads/fixtures/ads.json')
    csv_to_json('datasets/categories.csv', 'ads/fixtures/categories.json')
