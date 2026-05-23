"""
Convertidor: Notación Excel (ABCDEFGHIJ) ↔ Bits (1111111111)
"""

def excel_a_bits(notacion_excel, n_nodos):
    """
    Convierte notación Excel a bits binarios.
    
    Ejemplo:
        excel_a_bits("ABCDEFGHIJ", 10) → "1111111111"
        excel_a_bits("ACE", 10) → "1010100000"
    """
    bits = ['0'] * n_nodos
    
    if notacion_excel is None or notacion_excel == "":
        return ''.join(bits)
    
    for char in str(notacion_excel):
        pos = ord(char.upper()) - ord('A')
        if 0 <= pos < n_nodos:
            bits[pos] = '1'
    
    return ''.join(bits)


def bits_a_excel(bits):
    """
    Convierte bits binarios a notación Excel.
    
    Ejemplo:
        bits_a_excel("1111111111") → "ABCDEFGHIJ"
        bits_a_excel("1010100000") → "ACE"
    """
    resultado = []
    for i, bit in enumerate(str(bits)):
        if bit == '1':
            resultado.append(chr(ord('A') + i))
    
    return ''.join(resultado) if resultado else "∅"


# Tests
if __name__ == "__main__":
    print("Test 1:", excel_a_bits("ABCDEFGHIJ", 10))  # 1111111111
    print("Test 2:", excel_a_bits("ACE", 10))  # 1010100000
    print("Test 3:", bits_a_excel("1111111111"))  # ABCDEFGHIJ
    print("Test 4:", bits_a_excel("1010100000"))  # ACE
