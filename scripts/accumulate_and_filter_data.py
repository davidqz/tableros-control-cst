# -*- coding: utf-8 -*-
import pandas
import glob
import matplotlib.pyplot as plt

# Global constants
YEAR_LABEL = 'Periodo'
YEARS = ['2016', '2017', '2018']
IMPORTANT_FIELDS = {
    'Articulos': ['Adscripción', 'Categoría', 'Circulación de la revista'],
    'Conferencias Tecnicas': ['Adscripción', 'Alcance', 'Naturaleza de la conferencia'],
    'Consultoria': ['Adscripción', 'Área responsable', 'Sector'],
    'Cursos': ['Adscripción', 'Área responsable', 'Sector'],
    'Proyectos': ['Adscripción', 'Área responsable', 'Sector'],
    'OtrasActividades': ['Adscripción', ],
}
AREA_MAPPING = {
    'MY': 'Monterrey',
    'AG': 'Aguascalientes',
    'ZC': 'Zacatecas',
    'GAD': 'Actualización Docente',
    'CST': 'Servicios Tecnológicos',
    'ST': 'Servicios Tecnológicos',
    'GDS': 'Desarrollo de Software',
    'DS': 'Desarrollo de Software',
    'GS': 'Desarrollo de Software',
    'GMI': 'Matemáticas Industriales',
    'CE': 'Consultoría Estadística',
    'GCE': 'Consultoría Estadística',
    'GE': 'Consultoría Estadística',
}
TABLE_INDEX = 0  # Articulos
# TABLE_INDEX = 1  # Conferencias Tecnicas
# TABLE_INDEX = 2  # Consultoria
# TABLE_INDEX = 3  # Cursos
# TABLE_INDEX = 4  # Otras Actividades
# TABLE_INDEX = 5  # Proyectos

FIELD_INDEX = 0

# Read data 2016-2018
file_paths = glob.glob('../data/2016-2018/*.xls*')
file_paths.sort()
file_titles = [title.split('/')[3].split('.')[0].strip() for title in file_paths]

# Add a DataFrame (table) for each file into a dictionary with file_titles as keys
data_frames = {file_titles[i]: pandas.read_excel(path) for i, path in enumerate(file_paths)}

# Read data from 2019
extra_data_frame = pandas.read_excel('../data/2019_S2/1. Publicaciones.xlsx')

# Data Cleaning reformatting
for file_title, df in data_frames.items():
    # Remove semester suffix ('1_', '2_') from all YEAR_LABEL columns (leaving just the year)
    df[YEAR_LABEL] = df[YEAR_LABEL].str.slice_replace(stop=2)
    # Map 'Adscripción' codes to areas from AREA_MAPPING
    df[IMPORTANT_FIELDS[file_title][0]] = df[IMPORTANT_FIELDS[file_title][0]].apply(
        lambda s: AREA_MAPPING[s.split(' ')[1]]
    )
    # print(df[IMPORTANT_FIELDS[file_title][0]])


def add_count_columns(field_label, table, output_dic, output_column_labels):
    # Get all different values for field_label and their counts
    field_values_count = table[field_label].value_counts()
    field_values = list(field_values_count.index)
    field_values.sort()

    # Separate rows from table by year in a dictionary with years as keys
    rows_by_year = {year: table.loc[table[YEAR_LABEL] == year] for year in YEARS}

    # Add to output_column_labels concatenating the field with each unique value
    output_column_labels.extend(f'{field_label}.{value}' for value in field_values)

    if field_label == 'Adscripción' or field_label == 'Depa218':
        for f in field_values:
            adscripciones[f] = 0

    # For every year (row) in output_dic add the counts of each field value of that year
    for year in YEARS:
        counts_by_year = rows_by_year[year][field_label].value_counts()
        for field_value in field_values:
            if field_value in list(counts_by_year.index):
                output_dic[year].append(counts_by_year[field_value])
            else:
                output_dic[year].append(0)


def create_count_table(file_title):
    table = data_frames[file_title]
    fields = IMPORTANT_FIELDS[file_title]

    # Get total entries per year
    rows_by_year_count = table[YEAR_LABEL].value_counts()

    # Initialize output dictionary with format {year: total entries from that year}
    output_dic = {}
    for year in YEARS:
        if year in rows_by_year_count.index:
            output_dic[year] = [rows_by_year_count[year]]
        else:
            output_dic[year] = [0]

    output_column_labels = ['Total']

    for field in fields:
        add_count_columns(field_label=field, table=table, output_dic=output_dic,
                          output_column_labels=output_column_labels)

    output_table = pandas.DataFrame.from_dict(output_dic, orient='index', columns=output_column_labels)
    output_table.to_csv(f'../data/output/{file_title}.csv', index_label=YEAR_LABEL)
    return output_table


adscripciones = {}

count_tables = [create_count_table(file) for file in file_titles]

# print(len(adscripciones.keys()))
# print(adscripciones.keys())

# table_name = file_titles[TABLE_INDEX]
# count_table = count_tables[TABLE_INDEX]
#
# field = IMPORTANT_FIELDS[table_name][FIELD_INDEX]
# field_labels = count_table.columns[count_table.columns.str.startswith(field)]
# for y in YEARS:
#     plt.figure(f'{table_name} por {field} {y}', figsize=(8, 6))
#     pie_values = count_table.loc[y, field_labels]
#     pie_values = pie_values[pie_values > 0]
#     total_values = sum(pie_values)
#     # format_labels = pie_values.index.str.split('.')
#     # print(format_labels)
#     plt.pie(pie_values.values, labels=pie_values.index,
#             autopct=lambda p: f'{int(p * total_values / 100)}')
#
# plt.figure(table_name, figsize=(8, 6))
# plt.bar(count_table.index, count_table['Total'])

# plt.show()
