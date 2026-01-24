import pandas as pd


def show_menu():
    print()
    print("=========================================")
    print("Menu de opciones: ")
    print("a - Valor promedio por zona")
    print("b - Valor promedio por ciudad")
    print("c - Valor promedio por metro cuadrado")
    print("d - Top ciudades mas caras")
    print("e - Top ciudades mas baratas")
    print("s - Salir")
    print("=========================================")
    print()


def promedio_por_zona(df):
    return df.groupby("zone")["price"].mean()


def promedio_por_ciudad(df):
    return df.groupby("city")["price"].mean()


def promedio_por_m2(df):
    # Crear columna nueva: precio / área
    df["price_per_m2"] = df["price"] / df["area"]
    # Agrupar por zona y calcular promedio
    return df.groupby("zone")["price_per_m2"].mean()


def top_ciudades_caras(df):
    # Ordenar todo el DataFrame por precio
    df_ordenado = df.sort_values("price", ascending=False)
    # Retornar solo ciudad y precio (primeras 10)
    return df_ordenado[["city", "price"]].head(10)


def top_ciudades_baratas(df):
    df_ordenado = df.sort_values("price", ascending=True)
    return df_ordenado[["city", "price"]].head(10)


def main():
    df = pd.read_csv("./propiedades_limpias.csv")
    while True:
        show_menu()
        char = input("Ingrese una opcion: ")
        match char.upper():
            case "A":
                print(promedio_por_zona(df))
            case "B":
                print(promedio_por_ciudad(df))
            case "C":
                print(promedio_por_m2(df))
            case "D":
                print(top_ciudades_caras(df))
            case "E":
                print(top_ciudades_baratas(df))
            case "S":
                break
            case _:
                print("Opcion invalida")


if __name__ == "__main__":
    main()
