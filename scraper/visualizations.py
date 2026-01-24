"""
Visualizaciones del proyecto MercadoLibre Inmuebles

Genera 4 gráficos de análisis de propiedades:
- Precio promedio por zona (barras)
- Distribución de precios (histograma)
- Relación precio vs área (dispersión)
- Distribución de precios por zona (boxplot)
"""

import matplotlib.pyplot as plt
import pandas as pd


def cargar_datos():
    """
    Carga el dataset de las propiedades depuradas
    """
    return pd.read_csv("./propiedades_limpias.csv")


def box_plot(df):
    """
    Gráfico de caja:
        - Muestra un el promedio y un area de recurrencia, ademas de valores outliers
    """

    zonas = df.groupby("zone").apply(lambda x: x.name).to_list()
    precios = (
        df.groupby("zone")["price"].apply(lambda x: (x / 1000).to_list()).to_list()
    )

    fig_box, ax_box = plt.subplots(figsize=(10, 6))

    bp = ax_box.boxplot(precios, labels=zonas, patch_artist=True)

    for patch in bp["boxes"]:
        patch.set_facecolor("lightblue")

    ax_box.set_title("Distribución de Precios por Zona", fontsize=16, fontweight="bold")
    ax_box.set_ylabel("Precio (Miles de USD)", fontsize=12)

    # Grid
    ax_box.grid(axis="y", alpha=0.3)

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    try:
        plt.savefig("./plots/boxplot_zonas.png", dpi=300, bbox_inches="tight")
        print("Grafico de barra guardado correctamente en: plots/boxplot_zonas.png")

    except Exception as e:
        print("Error al guardar el gráfico de barras:", e)

    return


def bar_plot(df):
    """
    Gráfico de barras: Muestra la relación de promedio de precio por zona
    """
    promedios = df.groupby("zone")["price"].mean() / 1000

    X = promedios.index
    Y = promedios.values

    fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
    ax_bar.bar(X, Y, color="steelblue", width=0.6)

    ax_bar.set_title("Precio Promedio por Zona", fontsize=16, fontweight="bold")
    ax_bar.set_xlabel("Zona", fontsize=12)
    ax_bar.set_ylabel("Precio (Miles de USD)", fontsize=12)

    ax_bar.grid(axis="y", alpha=0.3, linestyle="--")

    plt.xticks(rotation=45, ha="right")  # ha = horizontal alignment

    plt.tight_layout()

    try:
        plt.savefig("./plots/precio_por_zona.png", dpi=300, bbox_inches="tight")
        print("Grafico de barra guardado correctamente en: plots/precio_por_zona.png")

    except Exception as e:
        print("Error al guardar el gráfico de barras:", e)

    return


def his_plot(df):
    """
    Gráfico histograma: Muestra la distribución de la variable precios
    """
    precios = df["price"] / 1000

    fig_his, ax_his = plt.subplots(figsize=(10, 6))
    ax_his.hist(precios, bins=30, color="coral", edgecolor="black", alpha=0.7)
    ax_his.set_title("Distribución de Precios", fontsize=16, fontweight="bold")
    ax_his.set_xlabel("Precio (Miles de USD)", fontsize=12)
    ax_his.set_ylabel("Cantidad de propiedades", fontsize=12)

    # Grid
    ax_his.grid(axis="y", alpha=0.3)

    plt.tight_layout()

    try:
        plt.savefig("./plots/distribucion_precios.png", dpi=300, bbox_inches="tight")
        print("Guardado correctamente en plots/distribucion_precios.png")

    except Exception as e:
        print("Error al guardar el histograma:", e)

    return


def scatter_plot(df):
    """
    Gráfico scatter: Muestra la relación entre dos variables: Area y Precios
    """
    area = df["area"]
    precio = df["price"] / 1000

    fig_scat, ax_scat = plt.subplots(figsize=(10, 6))

    ax_scat.scatter(area, precio, alpha=0.5, s=50, color="green", edgecolors="black")

    # Personalizar
    ax_scat.set_title("Relación Precio vs Área", fontsize=16, fontweight="bold")
    ax_scat.set_xlabel("Área (m²)", fontsize=12)
    ax_scat.set_ylabel("Precio (Miles de USD)", fontsize=12)

    # Grid
    ax_scat.grid(True, alpha=0.3)

    plt.tight_layout()

    try:
        plt.savefig("./plots/precio_vs_area.png", dpi=300, bbox_inches="tight")
        print("Guardado correctamente en plots/precio_vs_area.png")

    except Exception as e:
        print("Error al guardar el histograma:", e)

    return


def main():
    df = cargar_datos()
    print(f" Cargadas {df.shape[0]} propiedades")
    print("\n Generando visualizaciones...\n")

    bar_plot(df)
    his_plot(df)
    scatter_plot(df)
    box_plot(df)

    print("\n ¡Todas las visualizaciones generadas exitosamente!")
    print(" Revisa la carpeta 'plots/' para ver los gráficos")


if __name__ == "__main__":
    main()
