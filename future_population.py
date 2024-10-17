from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from io import BytesIO
import pandas as pd

# Carregando os dados
pop = pd.read_csv('Censo 2022 - Crescimento Populacional - Brasil.csv', sep = ';')
pop.columns = ['Ano', 'População', 'Recorte', 'Extra1', 'Extra2']
pop = pop[['Ano', 'População']]
pop['População'] = pd.to_numeric(pop['População'], errors = 'coerce')

# Criando DataFrame (todos os anos)
years = pd.DataFrame({'Ano': range(pop['Ano'].min(), pop['Ano'].max() + 1)})
new_pop = pd.merge(years, pop, on = 'Ano', how = 'left')
new_pop['População'] = new_pop['População'].interpolate(method = 'linear')

# Adicionando o quadrado do ano
new_pop['Ano²'] = new_pop['Ano'] ** 2

# Calculo de média móvel (3 anos)
new_pop['Média_Móvel'] = new_pop['População'].rolling(window = 3).mean()

# Eixos para regressão polinomial
x = new_pop[['Ano', 'Ano²']]
y = new_pop['População']

# Separar treino e teste
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 42)

# Criando modelo de regressão polinomial
model_poly = LinearRegression()
model_poly.fit(x_train, y_train)


def gen_chart(year) -> BytesIO:
    # Usando o ano para prever a população
    predicted_population = estimate(year)

    plt.figure(figsize = (10, 6))
    plt.plot(new_pop['Ano'], new_pop['População'], label = 'População Interpolada', marker = 'o')
    plt.plot(new_pop['Ano'], new_pop['Média_Móvel'], label = 'Média Móvel', linestyle = '--')
    plt.scatter(year, predicted_population, color = 'red', label = f'Previsão {year} (Polinomial)')
    plt.title(f'Crescimento Populacional com Previsão para {year} ({int(predicted_population):,.0f})')
    plt.xlabel('Ano')
    plt.ylabel('População')
    plt.legend()
    plt.grid()

    img = BytesIO()
    plt.savefig(img, format = 'png')
    plt.close()
    img.seek(0)

    return img


def estimate(year) -> int:
    future_year_poly = pd.DataFrame({'Ano': [year], 'Ano²': [year ** 2]})
    predicted_pop_poly = model_poly.predict(future_year_poly)
    return int(predicted_pop_poly[0])
    

