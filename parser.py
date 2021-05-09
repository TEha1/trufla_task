import csv
import sys
import xmltodict
import json
from abc import ABC


class Parser(ABC):

    def exclude_data(self):
        """
        a property object of reshaped data
        :return: return dictionary object
        """
        with open(f'{self.out_path}/results.json', 'w', encoding='utf-8') as file:
            json.dump(self.data, file)


class CSVParser(Parser):

    def reshape_data(self, customers_data, vehicles_data, paths):
        """
        reshaping the loaded data to fit the json data that will be exported
        :param customers_data: a list of dictionary objects of customers data
        :param vehicles_data: a list of dictionary objects of vehicles data
        :param paths: list of the two imported files
        :return: return a list 0f dictionaries if data is fit or None otherwise
        """
        data = []
        if len(paths) > 1:

            file_name = f'{paths[0]}, {paths[1]}'

            for customer in customers_data:
                data.append({
                    'file_name': file_name,
                    'transaction': {
                        'date': customer.get('date'),
                        'customer': {
                            'id': customer.get('id'),
                            'name': customer.get('name'),
                            'address': customer.get('address'),
                            'phone': customer.get('phone')
                        },
                        'vehicles': [
                            {
                                'id': vehicle.get('id'),
                                'make': vehicle.get('make'),
                                'vin_number': vehicle.get('vin_number')
                            }
                            for vehicle in vehicles_data
                            if customer.get('id') == vehicle.get('owner_id')
                        ]
                    }
                })

        return data

    def __init__(self, out_path, paths):

        if len(paths) > 1:

            self.out_path = out_path

            try:
                paths = [filepath for filepath in paths if filepath.endswith('.csv')]
                if len(paths) > 1:

                    with open(paths[0], mode='r', newline='', encoding='utf-8', ) as customers_file, \
                            open(paths[1], mode='r', newline='', encoding='utf-8', ) as vehicles_file:

                        customers_data = list(csv.DictReader(customers_file))
                        vehicles_data = list(csv.DictReader(vehicles_file))
                        self.data = self.reshape_data(customers_data, vehicles_data, paths)

                else:
                    raise ValueError('Unsupported file type')

            except Exception:
                raise ValueError('Unsupported file type')

        else:
            raise ValueError('This operation require two csv files (customers.csv) and (vehicles.csv)')


class XMLParser(Parser):

    def reshape_data(self, data, filepath):
        """
        reshaping the loaded data to fit the json data that will be exported
        :param data: dictionary object of loaded data
        :param filepath: the path of the imported file
        :return: return dictionary object if data is fit or None otherwise
        """
        transaction = data.get('Transaction')
        if transaction:
            customer = transaction.get('Customer')
            if customer:
                vehicles = []
                units = customer.get('Units')

                if units:
                    for key, value in units.items():
                        """
                        iterating at units to extract vehicles data 
                        """
                        if isinstance(value, list):
                            """
                            if the current value is a list, then the vehicles list will be filled from this list then break the loop
                            """
                            vehicles = [
                                {
                                    'id': vehicle['@id'],
                                    'make': vehicle['Make'],
                                    'vin_number': vehicle['Make'],
                                }
                                for vehicle in value
                            ]
                            break
                        else:
                            vehicles.append(
                                {
                                    'id': value['@id'],
                                    'make': value['Make'],
                                    'vin_number': value['Make'],
                                }
                            )

                return {
                    'file_name': filepath,
                    'transaction': {
                        'date': transaction.get('Date'),
                        'customer': {
                            'id': customer.get('@id'),
                            'name': customer.get('Name'),
                            'address': customer.get('Address'),
                            'phone': customer.get('Phone'),
                        },
                        'vehicles': vehicles
                    }
                }

        return {}

    def __init__(self, out_path, paths):

        if len(paths) > 0:

            try:
                if paths[0].endswith('.xml'):
                    with open(paths[0], "r", encoding='utf-8') as xml_obj:
                        self.out_path = out_path
                        data = xmltodict.parse(xml_obj.read())
                        self.data = self.reshape_data(data=data, filepath=paths[0])
                else:
                    raise ValueError('Unsupported file type')

            except EnvironmentError:
                raise ValueError('Unsupported file type')

        else:
            raise ValueError('This operation require two csv files (customers.csv) and (vehicles.csv)')


def connection_factory(file_type, out_path, paths):
    try:

        if file_type == 'csv':
            connector = CSVParser
        elif file_type == 'xml':
            connector = XMLParser
        else:
            raise ValueError('Cannot connect to this file')

        return connector(out_path, paths)

    except Exception as error:
        print(error)


def main():

    args = sys.argv[1:]

    if len(args) > 1:

        factory = connection_factory(file_type=args[0], out_path='json', paths=args[1:])

        if factory:
            factory.exclude_data()
            print('Data excluded into json/results.json')

    else:
        print('failed, missing arguments')


if __name__ == '__main__':
    main()
