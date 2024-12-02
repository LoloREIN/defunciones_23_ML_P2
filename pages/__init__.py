import unicodedata

def quitar_acentos(texto):
    """
    Elimina los acentos y diacríticos de un texto.
    
    Args:
        texto: String o cualquier otro tipo de dato que se convertirá a string
        
    Returns:
        String sin acentos ni diacríticos
    """
    if isinstance(texto, str):
        return ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
        )
    return texto

def procesar_datos(df):
    """
    Aplica el procesamiento de datos necesario para el modelo.
    
    Args:
        df: DataFrame con los datos a procesar
        
    Returns:
        DataFrame procesado
    """
    return df.applymap(quitar_acentos)