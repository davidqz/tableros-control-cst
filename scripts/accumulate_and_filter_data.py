# -*- coding: utf-8 -*-
import pandas
import glob
import matplotlib.pyplot as plt

# Global constants
YEAR_LABEL = 'Periodo'
YEARS = ['2016', '2017', '2018', '2019', '2020']
IMPORTANT_FIELDS = {
    'Articulos': ['Adscripción', 'Categoría', 'Circulación de la revista'],
    'Conferencias Tecnicas': ['Adscripción', 'Alcance', 'Naturaleza de la conferencia'],
    'Consultoria': ['Adscripción', 'Sector'],
    'Cursos': ['Adscripción', 'Sector'],
    'Proyectos': ['Adscripción', 'Sector'],
    'OtrasActividades': ['Adscripción', ],
}
EXTRA_FILES = {
    'Articulos': ['2019_S1/1. Publicaciones.xlsx', '2019_S2/1. Publicaciones.xlsx',
                  '2020_S1/01. Publicaciones realizadas.xls'],
    'Conferencias Tecnicas': ['2019_S1/7. Conferencias.xlsx', '2019_S2/7. Conferencias.xlsx',
                              '2020_S1/18. Conferencias impartidas.xls'],
    'Consultoria': ['2019_S1/4. Asesorías y consultorías.xlsx', '2019_S2/4. Asesorias y consultorias.xlsx',
                    '2020_S1/04. Asesorías y consultorías realizadas.xls'],
    'Cursos': ['2019_S1/5. Cursos.xlsx', '2019_S2/5. Cursos.xlsx',
               '2020_S1/05. Cursos y capacitaciones impartidas.xls'],
    'Proyectos': ['2019_S1/3. Proyectos de desarrollo tecnológico.xlsx',
                  '2019_S2/3. Proyectos de desarrollo tecnologico.xlsx',
                  '2020_S1/03. Proyectos de desarrollo tecnológico realizados.xls'],
    'OtrasActividades': ['2019_S1/18. Otras actividades relevantes.xlsx',
                         '2019_S2/18. Otras actividades relevantes.xlsx',
                         '2020_S1/21. Otras actividades relevantes.xls'],
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
# TABLE_INDEX = 0  # Articulos
# TABLE_INDEX = 1  # Conferencias Tecnicas
# TABLE_INDEX = 2  # Consultoria
# TABLE_INDEX = 3  # Cursos
# TABLE_INDEX = 4  # Otras Actividades
TABLE_INDEX = 5  # Proyectos

FIELD_INDEX = 1

# Read data 2016-2018
file_paths = glob.glob('../data/2016-2018/*.xls*')
file_paths.sort()
file_titles = [title.split('/')[3].split('.')[0].strip() for title in file_paths]

# Add a DataFrame (table) for each file into a dictionary with file_titles as keys
data_frames = {file_titles[i]: pandas.read_excel(path) for i, path in enumerate(file_paths)}

# Read extra data from 2019-2020
data_frames_19 = {}
data_frames_20 = {}
for name, path in EXTRA_FILES.items():
    s1 = pandas.read_excel(f'../data/{path[0]}')  # 2019_S1
    s2 = pandas.read_excel(f'../data/{path[1]}')  # 2019_S2
    data_frames_19[name] = pandas.concat([s1, s2])
    data_frames_20[name] = pandas.read_excel(f'../data/{path[2]}')  # 2020_S1

# Data Cleaning reformatting
for file, df in data_frames.items():
    # Remove semester suffix ('1_', '2_') from all YEAR_LABEL columns (leaving just the year)
    df[YEAR_LABEL] = df[YEAR_LABEL].str.slice_replace(stop=2)
    # Map 'Adscripción' codes to areas from AREA_MAPPING
    df[IMPORTANT_FIELDS[file][0]] = df[IMPORTANT_FIELDS[file][0]].apply(
        lambda s: AREA_MAPPING[s.split(' ')[1]]
    )


# Remove U or Unidad and correct Monterrrey
def format_adscripcion(name):
    split_name = name.split(' ')
    if len(split_name) > 1:
        new_name = split_name[1]
    else:
        new_name = name
    if new_name == 'Monterrrey':
        return 'Monterrey'
    if new_name in AREA_MAPPING.keys():
        return AREA_MAPPING[new_name]
    else:
        return new_name


for file, df in data_frames_19.items():
    df[IMPORTANT_FIELDS[file][0]] = df[IMPORTANT_FIELDS[file][0]].apply(format_adscripcion)

for file, df in data_frames_20.items():
    # Rename columns 'Área de adscripción' and 'Area adscripción' to 'Adscripción'
    df.rename(columns={'Área de adscripción': 'Adscripción', 'Area adscripción': 'Adscripción'}, inplace=True)
    df[IMPORTANT_FIELDS[file][0]] = df[IMPORTANT_FIELDS[file][0]].apply(format_adscripcion)


def add_count_columns_multiyear(field_label, table, table_19, table_20, output_dic, output_column_labels):
    # Get all different values for field_label and their counts
    field_values_count = table[field_label].value_counts()
    field_values = list(field_values_count.index)

    # Add the missing columns from 2019
    table_19_field_values_count = table_19[field_label].value_counts()
    table_19_field_values = list(table_19_field_values_count.index)
    for f in table_19_field_values:
        if f not in field_values:
            field_values.append(f)

    # Add the missing columns from 2020
    table_20_field_values_count = table_20[field_label].value_counts()
    table_20_field_values = list(table_20_field_values_count.index)
    for f in table_20_field_values:
        if f not in field_values:
            field_values.append(f)

    field_values.sort()

    # Separate rows from table by year in a dictionary with years as keys
    rows_by_year = {year: table.loc[table[YEAR_LABEL] == year] for year in YEARS}

    # Add to output_column_labels concatenating the field with each unique value
    output_column_labels.extend(f'{field_label}.{value}' for value in field_values)
    # output_column_labels.extend(field_values)

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
    table_19 = data_frames_19[file_title]
    table_20 = data_frames_20[file_title]
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
        add_count_columns_multiyear(table=table, table_19=table_19, table_20=table_20, field_label=field,
                                    output_dic=output_dic, output_column_labels=output_column_labels)

    # Add 2019-2020 data
    for label in output_column_labels:
        if label == 'Total':
            output_dic['2019'] = [len(table_19.index)]
            output_dic['2020'] = [len(table_20.index)]
        else:
            if label.startswith('Adscripción'):
                area = label.split('.')[1]
                counts_by_area_19 = len(table_19[table_19['Adscripción'] == area].index)
                counts_by_area_20 = len(table_20[table_20['Adscripción'] == area].index)
                output_dic['2019'].append(counts_by_area_19)
                output_dic['2020'].append(counts_by_area_20)
            else:
                output_dic['2019'].append(0)
                output_dic['2020'].append(0)

    output_table = pandas.DataFrame.from_dict(output_dic, orient='index', columns=output_column_labels)
    output_table.to_csv(f'../data/output/{file_title}.csv', index_label=YEAR_LABEL)
    return output_table


adscripciones = {}

count_tables = [create_count_table(file) for file in file_titles]

# print(len(adscripciones.keys()))
# print(adscripciones.keys())

table_name = file_titles[TABLE_INDEX]
count_table = count_tables[TABLE_INDEX]

field = IMPORTANT_FIELDS[table_name][FIELD_INDEX]
field_labels = count_table.columns[count_table.columns.str.startswith(field)]
for y in YEARS:
    plt.figure(f'{table_name} por {field} {y}', figsize=(8, 6))
    pie_values = count_table.loc[y, field_labels]
    pie_values = pie_values[pie_values > 0]
    total_values = sum(pie_values)
    # format_labels = pie_values.index.str.split('.')
    # print(format_labels)
    plt.pie(pie_values.values, labels=pie_values.index,
            autopct=lambda p: f'{int(p * total_values / 100)}')

plt.figure(table_name, figsize=(8, 6))
plt.bar(count_table.index, count_table['Total'])

plt.show()
