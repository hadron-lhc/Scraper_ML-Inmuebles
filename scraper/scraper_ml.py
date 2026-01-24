import requests
from bs4 import BeautifulSoup
from config import CIUDADES_POR_ZONA, generar_url
from processing import procesar_caracteristicas
import time
import pandas as pd

headers = {
    "User-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36"
}


def conectar_a_web(url):
    try:
        time.sleep(2)  # Esperar antes de hacer el request
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            print("Te has conectado a la web!!!")
            return response.text
        else:
            print(f"Error: Status code {response.status_code}")
            exit()

    except requests.exceptions.RequestException as e:
        print("Ocurrió un error al conectarte a la web: ", e)
        exit()


def extraer_precio(element):
    # Obteniendo precio
    try:
        contenedor_precio = element.find("div", class_="poly-price__current")
        if contenedor_precio:
            link = contenedor_precio.find("span", class_="andes-money-amount__fraction")
            if link:
                return link.get_text()
        return None
    except Exception as e:
        print(f"Error extrayendo precio: {e}")
        return None


def extraer_caracteristicas(element):
    # Obteniendo ambientes, baños y area
    try:
        contenedor_caracteristicas = element.find("ul", class_="poly-attributes_list")
        caracteristicas = contenedor_caracteristicas.find_all("li")
        array_caracteristicas = []
        for item in caracteristicas:
            array_caracteristicas.append(item.get_text())
        return array_caracteristicas

    except Exception as e:
        print(f"Error extrayendo caracteristicas: {e}")
        return None


def extraer_data(html, zona, ciudad):
    soup = BeautifulSoup(html, "html.parser")
    df_data = []
    try:
        # Bloque de casas
        casas_individuales = soup.find_all("div", class_="poly-card__content")

    except Exception as e:
        print(f"Error al procesar el bloque de casas: {e}")
        exit()

    for element in casas_individuales:
        precio = extraer_precio(element)
        caracteristicas_raw = extraer_caracteristicas(element)
        caracteristicas = procesar_caracteristicas(caracteristicas_raw)
        # Verificar que hay al menos 3 características
        if caracteristicas and len(caracteristicas) >= 3:
            df_data.append(
                {
                    "zona": zona,
                    "ciudad": ciudad,
                    "precio": precio,
                    "ambientes": caracteristicas["amb"],
                    "bathrooms": caracteristicas["banos"],
                    "area": caracteristicas["m2"],
                }
            )
        else:
            # Manejar caso donde faltan datos
            df_data.append(
                {
                    "precio": precio,
                    "ambientes": None,
                    "bathrooms": None,
                    "area": None,
                }
            )
    return df_data


def guardar_en_csv(df):
    df_raw = pd.DataFrame(df)
    df_raw.to_csv("data.csv", index=False)
    print("DataFrame guardado correctamente en: data.csv")


def main():
    todas_las_propiedades = []  # Acumular TODAS las propiedades

    # Loop por cada zona
    for zona, ciudades in CIUDADES_POR_ZONA.items():
        print(f"\n=== Procesando zona: {zona} ===")

        # Loop por cada ciudad de la zona
        for ciudad in ciudades:
            print(f"  → Ciudad: {ciudad}")

            # Generar URL
            url = generar_url(zona, ciudad)

            # Scrapear
            html = conectar_a_web(url)
            propiedades = extraer_data(html, zona, ciudad)  # ← Pasamos zona y ciudad

            # Acumular
            todas_las_propiedades.extend(propiedades)

            print(f"    Propiedades encontradas: {len(propiedades)}")

    print(f"\n=== TOTAL: {len(todas_las_propiedades)} propiedades ===")

    # Guardar todo en CSV
    guardar_en_csv(todas_las_propiedades)


if __name__ == "__main__":
    main()
