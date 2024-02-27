import pandas as pd
from matplotlib import pyplot as plt

# ### Завдання 1
# Відкрити та зчитати файл з даними.

print("Завдання 1")
print("Відкрити та зчитати файл з даними.")
df = pd.read_csv('Weather.csv')

print(df)

# ### Додатковий підпункт
# Обріжемо зайві пробіли в назвах полів (колонок)

print("\n\nДодатковий підпункт")
print("Обріжемо зайві пробіли в назвах полів (колонок)")

print(df.columns)

df.columns = pd.Series(df.columns).apply(lambda x: str(x).strip())
print(df.columns)

# ### Завдання 2
# Визначити та вивести кількість записів та кількість полів у кожному записі.

print("\n\nЗавдання 2")
print("Визначити та вивести кількість записів та кількість полів у кожному записі.")

print(f'Кількість записів: {len(df)}')

print(f'Кількість полів: {len(df.columns)}')

# ### Завдання 3
# Вивести 5 записів, починаючи з *M-ого* (число *M* - місяць народження студента, має бути визначено як змінна), та кожен *N-тий* запис, де число *N* визначається як 500 * M для місяця з першого півріччя та 300 * M для місяця з другого півріччя.

print("\n\nЗавдання 3")
print("""Вивести 5 записів, починаючи з *M-ого* (число *M* - місяць народження студента, 
має бути визначено як змінна), та кожен *N-тий* запис, де число *N* визначається як 500 * M 
для місяця з першого півріччя та 300 * M для місяця з другого півріччя.""")

M = '17-07-2004'

M = pd.to_datetime(M, format='%d-%m-%Y')
M = M.month
print(f'Місяць - {M}-ий')

print(df[M:].head())

N = 500 * M if M <= 6 else 300 * M

print(N)

print(df[::N][1:])

# ### Завдання 4
# Визначити та вивести тип полів кожного запису.

print("\n\nЗавдання 4")
print("Визначити та вивести тип полів кожного запису.")

print(df.dtypes)

# ### Завдання 5
# Замість поля *CET* ввести нові текстові поля, що відповідають числу, місяцю та року. Місяць та число повинні бути записані у двоцифровому форматі.

print("\n\nЗавдання 5")
print("""Замість поля *CET* ввести нові текстові поля, що відповідають числу, 
місяцю та року. Місяць та число повинні бути записані у двоцифровому форматі.""")

df['CET'] = pd.to_datetime(df['CET'])

df['CET_year'] = df['CET'].dt.year
df['CET_month'] = df['CET'].dt.month.map("{:02d}".format)
df['CET_day'] = df['CET'].dt.day.map("{:02d}".format)
del df['CET']

df = df[list(df.columns[-3:]) + list(df.columns[:-3])]

print(df)

# ### Завдання 6
# Визначити та вивести:

print("\n\nЗавдання 6")
print("Визначити та вивести:")

# > а. Кількість днів із порожнім значенням поля *Events*

print("а. Кількість днів із порожнім значенням поля *Events*")

len(df[df['Events'].isna() == True])

# >b. День, у який середня вологість була мінімальною, а також швидкість вітру в цей день.

print("b. День, у який середня вологість була мінімальною, а також швидкість вітру в цей день.")

row = df.iloc[[df['Mean Humidity'].idxmin()]]
print(row[['CET_year', 'CET_month', 'CET_day', 'Mean Humidity', 'Mean Wind SpeedKm/h']])

# > c. Місяці, коли середня температура від нуля до п'яти градусів.

print("c. Місяці, коли середня температура від нуля до п'яти градусів.")

mask = df[(df['Mean TemperatureC'] >= 0) & (df['Mean TemperatureC'] <= 5)]

print(mask[['CET_year', 'CET_month', 'Mean TemperatureC']])

# ### Завдання 7
# Визначити та вивести:

print("\n\nЗавдання 7")
print("Визначити та вивести:")

# >a. Середню максимальну температуру по кожному дню за всі роки.

print("a. Середню максимальну температуру по кожному дню за всі роки.")

print(df.groupby(['CET_day']).mean(numeric_only=True)[['Max TemperatureC']])

# >b. Кількість днів у кожному році з туманом

print("b. Кількість днів у кожному році з туманом")

fog_df = df[df['Events'] == 'Fog'].groupby(['CET_year', 'CET_day']).sum(numeric_only=True)

days_by_year = fog_df.index.get_level_values(1).groupby(fog_df.index.get_level_values(0))

for k, v in days_by_year.items():
    print(f'Рік - {k}, кількість туманних днів - {len(v)}')

# ### Завдання 8
# Побудувати стовпчикову діаграму кількості *Events*.

print("\n\nЗавдання 8")
print("Побудувати стовпчикову діаграму кількості *Events*.")

figure, (bar_ax, pie_ax, graph_ax) = plt.subplots(1, 3, figsize=(45,12))

var = df['Events'].value_counts()

bar = bar_ax.bar(var.index, var.values)
bar_ax.set_xticklabels(var.index, rotation=40)
bar_ax.set_title("Стовпчикова діаграма кількості Events")

# ### Завдання 9
# Побудувати кругову діаграму напрямків вітру (сектор на діаграмі має відповідати одному з восьми напрямків - північний, південний, східний, західний та проміжні).

print("\n\nЗавдання 9")
print("""Побудувати кругову діаграму напрямків вітру (сектор на діаграмі 
має відповідати одному з восьми напрямків - північний, південний, східний, 
західний та проміжні).""")

directions = ["Північий", "Північно-східний", "Східний", "Південно-східний", "Південний", "Південно-західий",
              "Західний", "Північно-західий"]


def get_direction(x):
    x = x if x >= 0 else 360 + x
    n = x // 22.5
    part = n // 2 + n % 2
    return directions[int(part) % 8]


df_for_pie = df['WindDirDegrees'].apply(get_direction).value_counts()
idx, vals = df_for_pie.index, df_for_pie.values

pie_ax.pie(vals, labels=idx, autopct='%1.1f%%')
pie_ax.set_title("Кругова діаграма напрямків вітру")

# ### Завдання 10
# Побудувати на одному графіку (тип графіка обрати самостійно!):

# > а. Середню по кожному місяцю кожного року максимальну температуру;

# > b. Середню по кожному місяцю кожного року мінімальну точку роси.

print("\n\nЗавдання 10")
print("Побудувати на одному графіку (тип графіка обрати самостійно!):")
print("а. Середню по кожному місяцю кожного року максимальну температуру;")
print("b. Середню по кожному місяцю кожного року мінімальну точку роси.")

graph_data = df.groupby(['CET_year', 'CET_month'], as_index=False).mean(numeric_only=True)[['CET_year', 'CET_month', 'Max TemperatureC', 'Min DewpointC']]

graph_ax.stackplot(graph_data.index, graph_data[['Max TemperatureC']].values.flatten(), labels=['Max TemperatureC', 'Min DewpointC'], colors="green", alpha=0.25)
graph_ax.stackplot(graph_data.index, graph_data[['Min DewpointC']].values.flatten(), labels=['Max TemperatureC', 'Min DewpointC'], colors="red", alpha=0.25)

xticklabels = [f"({year}, {month})" for year, month in zip(graph_data['CET_year'], graph_data['CET_month'])]
x_0 = xticklabels[0]
rest = xticklabels[::50]
xticklabels = [str(x_0)] + rest

graph_ax.set_xlabel('CET_year,CET_month')
graph_ax.set_ylabel('Температура')
graph_ax.set_xticklabels(xticklabels)
graph_ax.set_title("Середня по кожному місяцю кожного року максимальна температура і мінімальна точка роси")
graph_ax.legend()

mng = plt.get_current_fig_manager()
mng.resize(2800, 1000)

plt.show()