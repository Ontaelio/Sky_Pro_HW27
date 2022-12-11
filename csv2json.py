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
            if row.get('id'):
                result['pk'] = row.pop('id')
            if row.get('price'):
                row['price'] = float(row['price'])
            if row.get('is_published'):
                row['is_published'] = True if row['is_published'] == 'TRUE' else False
            # if row.get('category_id'):
            #     row['category_id'] = int(row['category_id'])
            if row.get('lat'):
                row['lat'] = float(row['lat'])
            if row.get('lng'):
                row['lng'] = float(row['lng'])
            if row.get('age'):
                row['age'] = int(row['age'])
            # if row.get('location_id'):
            #     row['location'] = int(row['location_id'])
            # if row.get('author_id'):
            #     row['author'] = int(row['author_id'])
            # if row.get('category_id'):
            #     row['category'] = int(row['category_id'])


            print(row)

            result['model'] = 'ads.' + csv_file.split('/')[-1].split('.')[0]
            result['fields'] = row

            json_list.append(result)

    with open(json_file, 'w', encoding='utf-8') as fout:
        json_string = json.dumps(json_list, indent=4, ensure_ascii=False)
        fout.write(json_string)


if __name__ == "__main__":
    csv_to_json('datasets/ad.csv', 'ads/fixtures/ad.json')
    csv_to_json('datasets/category.csv', 'ads/fixtures/category.json')
    csv_to_json('datasets/user.csv', 'authentication/fixtures/user.json')
    csv_to_json('datasets/location.csv', 'authentication/fixtures/location.json')
