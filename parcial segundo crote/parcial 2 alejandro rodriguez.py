"""Sistema de Compra de Boletas — Cine Metro"""

GENEROS = ("Acción", "Comedia", "Drama", "Terror", "Animación", "Ciencia Ficción")

PELICULAS = {
    1: {"titulo": "Guardianes del Cosmos", "genero": GENEROS[5], "duracion_min": 148, "sala": "A", "horarios": ("14:00", "17:30", "21:00"), "precio_base": 14_000, "asientos_disponibles": 60},
    2: {"titulo": "La Última Risa",        "genero": GENEROS[1], "duracion_min": 105, "sala": "B", "horarios": ("15:00", "18:00", "20:30"), "precio_base": 12_000, "asientos_disponibles": 45},
    3: {"titulo": "Sombras del Pasado",    "genero": GENEROS[2], "duracion_min": 132, "sala": "C", "horarios": ("13:30", "16:30", "19:30"), "precio_base": 13_000, "asientos_disponibles": 50},
    4: {"titulo": "El Grito Eterno",       "genero": GENEROS[3], "duracion_min":  98, "sala": "D", "horarios": ("16:00", "19:00", "22:00"), "precio_base": 13_500, "asientos_disponibles": 40},
    5: {"titulo": "Mundo Peludo",          "genero": GENEROS[4], "duracion_min":  90, "sala": "E", "horarios": ("11:00", "14:00", "16:30"), "precio_base": 11_000, "asientos_disponibles": 80},
}

CUPONES = {"CINE20": 0.20, "ESTUDIANTE": 0.15, "CINEFAN": 0.10}
historial_compras = []

fmt = lambda v: f"${v:,.0f} COP"
sep = lambda c="─", n=55: print(c * n)


def mostrar_cartelera():
    print("\n" + "═"*55)
    print("          🎬  CARTELERA — CINE METRO  🎬")
    print("═"*55)
    print(f"{'ID':<4} {'TÍTULO':<28} {'GÉNERO':<16} {'PRECIO'}")
    sep()
    for id_p, p in PELICULAS.items():
        d = "✔" if p["asientos_disponibles"] > 0 else "✘"
        print(f" {id_p}   {p['titulo']:<28} {p['genero']:<16} {fmt(p['precio_base'])}  {d}")
    sep()
    print("  ✔ = con disponibilidad   ✘ = agotado\n")


def mostrar_detalle(p):
    sep()
    print(f"  🎞  {p['titulo'].upper()}")
    sep()
    print(f"  Género   : {p['genero']}   |  Duración: {p['duracion_min']} min")
    print(f"  Sala     : {p['sala']}   |  Precio  : {fmt(p['precio_base'])}")
    print(f"  Asientos : {p['asientos_disponibles']} disponibles")
    print(f"  Horarios : {' | '.join(p['horarios'])}")
    sep()


def pedir_int(prompt, valido, error="Opción inválida."):
    while True:
        try:
            v = int(input(prompt))
            if valido(v): return v
            raise ValueError(error)
        except ValueError as e:
            print(f"  ⚠  {e}  Intenta de nuevo.")


def seleccionar_pelicula():
    mostrar_cartelera()
    while True:
        try:
            id_p = int(input("  Ingresa el ID de la película: "))
            if id_p not in PELICULAS: raise ValueError(f"ID '{id_p}' no existe.")
            p = PELICULAS[id_p]
            if p["asientos_disponibles"] == 0: raise ValueError(f"'{p['titulo']}' está agotada.")
            return id_p, p
        except ValueError as e:
            print(f"  ⚠  {e}  Intenta de nuevo.\n")


def seleccionar_horario(horarios):
    print("\n  Horarios disponibles:")
    for i, h in enumerate(horarios, 1): print(f"    {i}. {h}")
    return horarios[pedir_int("  Elige el número de horario: ", lambda v: 1 <= v <= len(horarios), "Fuera de rango.") - 1]


def pedir_cantidad(disponibles):
    return pedir_int(
        f"  ¿Cuántas boletas? (máx. {disponibles}): ",
        lambda v: 0 < v <= min(disponibles, 10),
        f"Ingresa entre 1 y {min(disponibles, 10)}."
    )


def aplicar_cupon(subtotal):
    codigo = input("\n  ¿Tienes cupón? (Enter para omitir): ").strip().upper()
    if not codigo: return subtotal, 0, None
    if codigo in CUPONES:
        desc = int(subtotal * CUPONES[codigo])
        print(f"  ✅  Cupón '{codigo}': -{CUPONES[codigo]*100:.0f}% = -{fmt(desc)}")
        return subtotal - desc, desc, codigo
    print("  ⚠  Cupón no válido.")
    return subtotal, 0, None


def procesar_pago(total):
    print(f"\n  💳  Total: {fmt(total)}")
    metodo = pedir_int("  Método (1) Efectivo  (2) Tarjeta: ", lambda v: v in (1, 2))
    if metodo == 1:
        while True:
            try:
                pago = int(input("  Monto en efectivo: $"))
                if pago < total: raise Exception(f"Faltan {fmt(total - pago)}.")
                print(f"  ✅  Cambio: {fmt(pago - total)}")
                return True
            except Exception as e:
                print(f"  ⚠  {e}")
    print("  ✅  Tarjeta procesada.")
    return True


def generar_recibo(c):
    print("\n" + "═"*55)
    print("         🎟  RECIBO DE COMPRA — CINE METRO")
    print("═"*55)
    print(f"  Película : {c['pelicula']}  |  Sala: {c['sala']}")
    print(f"  Horario  : {c['horario']}  |  Boletas: {c['cantidad']}")
    print(f"  Precio   : {fmt(c['precio_unitario'])} c/u")
    if c["cupon"]: print(f"  Cupón    : {c['cupon']} (-{fmt(c['descuento'])})")
    print(f"  TOTAL    : {fmt(c['total'])}")
    sep("─"); print("  ¡Disfruta la función! 🍿"); print("═"*55)


def ver_historial():
    if not historial_compras:
        print("\n  📭  No hay compras en esta sesión."); return
    print("\n" + "═"*55 + "\n        📋  HISTORIAL — SESIÓN\n" + "═"*55)
    total = 0
    for i, c in enumerate(historial_compras, 1):
        print(f"  {i}. {c['pelicula']} | {c['horario']} | {c['cantidad']} boleta(s) | {fmt(c['total'])}")
        total += c["total"]
    sep("─"); print(f"  Total sesión: {fmt(total)}"); print("═"*55)


def realizar_compra():
    print("\n" + "═"*55 + "\n   🎬  BIENVENIDO AL SISTEMA DE BOLETAS CINE METRO\n" + "═"*55)
    id_p, p = seleccionar_pelicula()
    mostrar_detalle(p)
    horario  = seleccionar_horario(p["horarios"])
    cantidad = pedir_cantidad(p["asientos_disponibles"])
    subtotal = p["precio_base"] * cantidad
    print(f"\n  Subtotal ({cantidad} × {fmt(p['precio_base'])}): {fmt(subtotal)}")
    total, desc, cupon = aplicar_cupon(subtotal)
    if procesar_pago(total):
        PELICULAS[id_p]["asientos_disponibles"] -= cantidad
        compra = {"pelicula": p["titulo"], "sala": p["sala"], "horario": horario,
                  "cantidad": cantidad, "precio_unitario": p["precio_base"],
                  "descuento": desc, "cupon": cupon, "total": total}
        historial_compras.append(compra)
        generar_recibo(compra)


def menu_principal():
    opciones = {"1": ("Comprar boletas", realizar_compra),
                "2": ("Ver cartelera", mostrar_cartelera),
                "3": ("Ver historial", ver_historial),
                "4": ("Salir", None)}
    while True:
        print("\n" + "─"*40 + "\n  MENÚ PRINCIPAL\n" + "─"*40)
        for k, (n, _) in opciones.items(): print(f"  {k}. {n}")
        print("─"*40)
        op = input("  Selecciona una opción: ").strip()
        if op not in opciones: print("  ⚠  Opción no válida."); continue
        nombre, fn = opciones[op]
        if fn is None: print("\n  👋  ¡Hasta pronto!"); break
        try: fn()
        except KeyboardInterrupt: print("\n\n  ⚠  Operación cancelada.")


if __name__ == "__main__":
    menu_principal()