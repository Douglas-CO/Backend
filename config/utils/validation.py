def validar_cedula_ecuador(cedula: str) -> bool:
    if not cedula.isdigit() or len(cedula) != 10:
        return False

    region = int(cedula[:2])
    if not ((1 <= region <= 24) or region == 30):
        return False

    tercer = int(cedula[2])
    if not (0 <= tercer <= 5):
        return False

    def multiplicar_impar(n: int) -> int:
        r = n * 2
        return r - 9 if r > 9 else r

    suma = 0
    for i in range(9):
        dig = int(cedula[i])
        if i % 2 == 0:
            suma += multiplicar_impar(dig)
        else:
            suma += dig

    verificador_esperado = (10 - (suma % 10)) % 10
    verificador_real = int(cedula[9])

    return verificador_esperado == verificador_real
