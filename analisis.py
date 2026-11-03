import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)


def analizar(df):
    print("\nInfo general:")
    df.info()
    print("\nEstadísticas numéricas:")
    print(df.describe())

    ingresos_por_categoria(df)
    canal_que_mas_vende(df)
    clientes_vip_vs_regular(df)
    metodo_pago_mas_usado(df)
    top5_clientes(df)


def ingresos_por_categoria(df):
    """Pregunta 1: ¿Qué categoría genera más ingresos?

    Pista: df.groupby("categoria")["total"].sum().sort_values(ascending=False)
    """
    # TODO 8: calcular e imprimir los ingresos por categoría y la categoría que más ingresa.
    ingresos = df.groupby("categoria")["total"].sum().sort_values(ascending=False)
    print("\nIngresos por categoría:")
    print(ingresos)
    print(f"Categoría con más ingresos: {ingresos.index[0]} (${ingresos.iloc[0]:,.0f})")


def canal_que_mas_vende(df):
    """Pregunta 2: ¿Qué canal vende más?

    Pista: agrupar por "canal" y usar .agg(ventas=("id_venta", "count"), ingresos=("total", "sum")).
    """
    # TODO 9: calcular e imprimir ventas e ingresos por canal.
    canales = df.groupby("canal").agg(
        ventas=("id_venta", "count"),
        ingresos=("total", "sum"),
    ).sort_values("ventas", ascending=False)
    print("\nVentas e ingresos por canal:")
    print(canales)
    print(
        "Canal que más vende (criterio: número de ventas): "
        f"{canales.index[0]} con {canales.iloc[0]['ventas']} ventas."
    )


def clientes_vip_vs_regular(df):
    """Pregunta 3: ¿Los clientes VIP compran más que los Regulares?

    Pista: como hay más clientes Regular que VIP, compare promedios por cliente, no totales.
    Calcular: número de clientes (nunique), compras y gasto total por segmento,
    y luego dividir compras y gasto entre el número de clientes.
    """
    # TODO 10: calcular e imprimir compras y gasto promedio por cliente según segmento_cliente.
    segmentos = df.groupby("segmento_cliente").agg(
        clientes=("id_cliente", "nunique"),
        compras=("id_venta", "count"),
        gasto_total=("total", "sum"),
    )
    segmentos["compras_por_cliente"] = segmentos["compras"] / segmentos["clientes"]
    segmentos["gasto_por_cliente"] = segmentos["gasto_total"] / segmentos["clientes"]

    print("\nCompras y gasto promedio por cliente según segmento:")
    print(segmentos)
    if segmentos.loc["VIP", "compras_por_cliente"] > segmentos.loc["Regular", "compras_por_cliente"]:
        print("VIP tiene más compras por cliente que Regular.")
    else:
        print("Regular tiene más compras por cliente que VIP.")
    if segmentos.loc["VIP", "gasto_por_cliente"] > segmentos.loc["Regular", "gasto_por_cliente"]:
        print("VIP tiene más gasto por cliente que Regular.")
    else:
        print("Regular tiene más gasto por cliente que VIP.")


def metodo_pago_mas_usado(df):
    """Pregunta 4: ¿Qué método de pago es más usado?

    Pista: df["metodo_pago"].value_counts()
    """
    # TODO 11: calcular e imprimir el conteo por método de pago y cuál es el más usado.
    conteos = df["metodo_pago"].value_counts()
    print("\nVentas por método de pago:")
    print(conteos)
    print(f"Método más usado: {conteos.index[0]} con {conteos.iloc[0]} ventas.")


def top5_clientes(df):
    """Pregunta 5: ¿Top 5 clientes con más compras?

    Pista: agrupar por ["id_cliente", "nombre_cliente"], contar compras y sumar total,
    ordenar por compras (y por gasto como desempate) y tomar las primeras 5 con .head(5).
    """
    # TODO 12: calcular e imprimir el top 5.
    clientes = df.groupby(["id_cliente", "nombre_cliente"]).agg(
        compras=("id_venta", "count"),
        gasto_total=("total", "sum"),
    )
    top = clientes.sort_values(
        ["compras", "gasto_total"], ascending=[False, False]
    ).head(5)
    print("\nTop 5 clientes por compras y gasto total:")
    print(top)

    # Separa abril y mayo y comprueba cuántas ventas reúne.
    abril = df[df["fecha_venta"].dt.month == 4]
    mayo = df[df["fecha_venta"].dt.month == 5]
    ventas_abril_mayo = pd.concat([abril, mayo], ignore_index=True)
    print(
        f"Ventas de abril y mayo: {len(ventas_abril_mayo)} "
        f"de {len(df)} ventas originales."
    )
