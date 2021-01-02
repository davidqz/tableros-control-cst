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
EXTRA_FILES = {
    'Articulos': ['2019_S1/1. Publicaciones.xlsx', '2019_S2/1. Publicaciones.xlsx', '2020_S1/01. Publicaciones realizadas.xls'],
    'Conferencias Tecnicas': ['2019_S1/7. Conferencias.xlsx', '2019_S2/7. Conferencias.xlsx', ],
    'Consultoria': ['2019_S1/4. Asesorías y consultorías.xlsx', '2019_S2/4. Asesorias y consultorias.xlsx', ],
    'Cursos': ['2019_S1/5. Cursos.xlsx', '2019_S2/5. Cursos.xlsx', ],
    'Proyectos': ['2019_S1/3. Proyectos de desarrollo tecnológico.xlsx', '2019_S2/3. Proyectos de desarrollo tecnologico.xlsx', ],
    'OtrasActividades': ['2019_S1/18. Otras actividades relevantes.xlsx', '2019_S2/18. Otras actividades relevantes.xlsx', ],
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

# Read extra data from 2019_S1
# extra_data_frames = {name: pandas.read_excel(f'data/{path[0]}') for name, path in EXTRA_FILES.items()}
extra_data_frames = {}
for name, path in EXTRA_FILES.items():
    s1 = pandas.read_excel(f'../data/{path[0]}')
    s2 = pandas.read_excel(f'../data/{path[1]}')
    extra_data_frames[name] = pandas.concat([s1, s2])

# Data Cleaning reformatting
for file, df in data_frames.items():
    # Remove semester suffix ('1_', '2_') from all YEAR_LABEL columns (leaving just the year)
    df[YEAR_LABEL] = df[YEAR_LABEL].str.slice_replace(stop=2)
    # Map 'Adscripción' codes to areas from AREA_MAPPING
    df[IMPORTANT_FIELDS[file][0]] = df[IMPORTANT_FIELDS[file][0]].apply(
        lambda s: AREA_MAPPING[s.split(' ')[1]]
    )
    # print(df[IMPORTANT_FIELDS[file_title][0]])

# Remove U or Unidad and correct Monterrrey
def format_adscripcion(name):
    split_name = name.split(' ')
    if len(split_name) > 1:
        if split_name[1] == 'Monterrrey':
            return 'Monterrey'
        else:
            return split_name[1]
    else:
        if name in AREA_MAPPING.keys():
            return AREA_MAPPING[name]
        else:
            return name

for file, df in extra_data_frames.items():
    df[IMPORTANT_FIELDS[file][0]] = df[IMPORTANT_FIELDS[file][0]].apply(format_adscripcion)


def add_count_columns_multiyear(field_label, table, extra_table, output_dic, output_column_labels):
    # Get all different values for field_label and their counts
    field_values_count = table[field_label].value_counts()
    field_values = list(field_values_count.index)
    # Add the extra columns from 2019-2020
    extra_field_values_count = extra_table[field_label].value_counts()
    extra_field_values = list(extra_field_values_count.index)
    for f in extra_field_values:
        if f not in field_values:
            field_values.append(f)

    field_values.sort()

    # Separate rows from table by year in a dictionary with years as keys
    rows_by_year = {year: table.loc[table[YEAR_LABEL] == year] for year in YEARS}

    # Add to output_column_labels concatenating the field with each unique value
    output_column_labels.extend(f'{field_label}.{value}' for value in field_values)

    if field_label == 'Adscripción':
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
    extra_table = extra_data_frames[file_title]
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
        add_count_columns_multiyear(table=table, extra_table=extra_table, field_label=field, output_dic=output_dic,
                                    output_column_labels=output_column_labels)

    # Add 2019_S1 data
    for label in output_column_labels:
        if label == 'Total':
            output_dic['2019'] = [len(extra_table.index)]
        else:
            if label.startswith('Adscripción'):
                area = label.split('.')[1]
                counts_by_area = len(extra_table[extra_table['Adscripción'] == area].index)
                output_dic['2019'].append(counts_by_area)
            else:
                output_dic['2019'].append(0)

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
