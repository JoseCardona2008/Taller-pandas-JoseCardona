from pathlib import Path

PROCESSED = Path(__file__).parent / "Data" / "processed"


def validar_premerge(clientes, ventas):
    """Revisa que el merge se pueda hacer. Devuelve True si todo está bien, False si no.

    Revisar:
    - Que exista la columna "id_cliente" en los dos dataframes.
    - Que "id_cliente" no esté repetido en clientes.
    - Que "id_cliente" tenga el mismo tipo en los dos dataframes.
    - Cuántas ventas no tienen cliente asociado (esto solo se informa, no falla).
    """
    # TODO 6: escribir las validaciones y devolver True o False.
    valido = True

    if "id_cliente" not in clientes.columns or "id_cliente" not in ventas.columns:
        print("Error: falta la columna id_cliente en una de las tablas.")
        return False

    if clientes["id_cliente"].duplicated().any():
        print("Error: id_cliente está repetido en clientes.")
        valido = False

    if clientes["id_cliente"].dtype != ventas["id_cliente"].dtype:
        print("Error: id_cliente tiene tipos diferentes en las tablas.")
        valido = False

    ventas_sin_cliente = ventas[~ventas["id_cliente"].isin(clientes["id_cliente"])]
    print(f"Ventas sin cliente asociado: {len(ventas_sin_cliente)}")

    return valido


def unir(clientes, ventas):
    """Une ventas con clientes usando "id_cliente" y guarda el resultado en Data/processed/merge.csv.

    Pistas:
    - Usar pd.merge(...) o ventas.merge(...).
    - Usar how="left" para no perder ventas.
    - Usar validate="m:1" para confirmar que cada venta tiene un solo cliente.
    - Guardar con df.to_csv(...) en PROCESSED / "merge.csv".
    """
    # TODO 7: validar con validar_premerge(), hacer el merge, guardar el CSV y devolver el dataframe.
    if not validar_premerge(clientes, ventas):
        return None

    df_merge = ventas.merge(
        clientes, on="id_cliente", how="left", validate="m:1"
    )
    PROCESSED.mkdir(parents=True, exist_ok=True)
    df_merge.to_csv(PROCESSED / "merge.csv", index=False)
    print(f"Merge guardado en: {PROCESSED / 'merge.csv'}")
    return df_merge
