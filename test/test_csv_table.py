from unittest import TestCase

from utils.csv_table import CsvTable


class TestCsvTable(TestCase):
    def test_values(self):
        path = "../data/data_test/sequences.csv"
        accession = ["MT292569", "MT292570", "MT292571", "MT292572", "MT292574",
                     "MT292575", "MT292576", "MT292573", "MT292577", "MT292578",
                     "MT292579", "MT292580", "MT292581", "MT292582", "MT256917",
                     "MT256918", "MT281577", "MT291826", "MT291827", "MT291828",
                     "MT291829", "MT291830", "MT291831", "MT291832", "MT291833",
                     "MT291834", "MT291835", "MT291836", "MT259226", "MT259227",
                     "MT259228", "MT259229", "MT259230", "MT259231"]
        csv_table = CsvTable(path)
        self.assertTrue(all([x in accession for x in csv_table.values("Accession")]))

    def test_group_countries_by_median_length(self):
        path = "../data/data_test/sequences.csv"
        row_china = {"Accession": "MT259228",
                     "Release_Date": "2020-03-30T00:00:00Z",
                     "Species": "Severe acute respiratory syndrome-related coronavirus",
                     "Length": "29861",
                     "Geo_Location": "China",
                     "Host": "Homo sapiens",
                     "Isolation_Source": "oronasopharynx",
                     "Collection_Date": "2020-01-26"}
        row_spain = {"Accession": "MT292577",
                     "Release_Date": "2020-04-06T00:00:00Z",
                     "Species": "Severe acute respiratory syndrome-related coronavirus",
                     "Length": "29788",
                     "Geo_Location": "Spain",
                     "Host": "Homo sapiens",
                     "Isolation_Source": "",
                     "Collection_Date": "2020-03-08"}

        list_cases = [row_spain, row_china]
        list_cases_test = CsvTable(list_cases)
        csv_table = CsvTable(path)
        list_csv = csv_table.group_countries_by_median_length()
        self.assertTrue(all(x in list_csv._table for x in list_cases_test._table))

