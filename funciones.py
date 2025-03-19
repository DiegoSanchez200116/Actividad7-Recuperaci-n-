#Función_1. Carga los archivos con extensiones .csv y .html y los convierte a dataframe, si es un  archivo con cualquier 
# otra extensión, emitirá el raise (“Hola, acabas de ingresar un documento que desconozco, con extensión: .formato”)

def cargar_dataset(archivo):  #La entrada es un archivo
    import pandas as pd
    import os
    #Si se desea agregar un input se coloca:
#   archivo=input("Por favor, ingresa el nombre del archivo: ")
    extension = os.path.splitext(archivo)[1].lower()
# Cargar el archivo según su extensión
    if extension == '.csv':
        df= pd.read_csv(archivo)
        return (df)
    elif extension == '.html':
        df= pd.read_html(archivo)
        return (df)
    else:
            raise ValueError(f"Hola, acabas de ingresar un documento que desconozco, con extensión: {extension}")

#Función_2. Sustituye los valores nulos de las variables de las columnas primas (0,1, 2, 3, 5, 7, 11, 13…etc.) 
# con la constante numérica  “1111111” y de las demás columnas numéricas con la constante “1000001”. 
# Las columnas que no sean de tipo numérico se sustituirán con el string “Valor Nulo”
def limpieza_nulos(df):
    import pandas as pd
    #Separo las columnas primas
    primas = df.iloc[:, [0,1,2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]]
    #Separo las columnas restantes
    no_primas = df.iloc[:, [4,6,8,9,10,12,14,15,16,18,20,21,22,24,25,26,27,28,30,32,33,34,35,36,38,39,40,42,44,45,46,48]]
    
    #Separo columnas cuantitativas primas del dataframe
    cuantitativas_primas= primas.select_dtypes(include=['float64', 'int64','float','int'])
    #Sustituir valores nulos por un valor numérico en  concreto 
    cuantitativas_primas= cuantitativas_primas.fillna(1111111) 
    
    #Separo columnas cuantitativas no primas del dataframe
    cuantitativas_no_primas= no_primas.select_dtypes(include=['float64', 'int64','float','int'])
    #Sustituir valores nulos por un valor numérico en  concreto
    cuantitativas_no_primas=cuantitativas_no_primas.fillna(1000001)
    
    #Separo columnas cualitativas primas del dataframe 
    cualitativas_primas= primas.select_dtypes(include=['object', 'datetime','category'])
    #Sustituir valores nulos por un string en  concreto
    cualitativas_primas =cualitativas_primas.fillna("Valor Nulo") 
        
    #Separo columnas cualitativas pares del dataframe 
    cualitativas_no_primas= no_primas.select_dtypes(include=['object', 'datetime','category'])
    #Sustituir valores nulos por un string en  concreto 
    cualitativas_no_primas =cualitativas_no_primas.fillna("Valor Nulo") 
    
    # Unimos el dataframe cuantitativo limpio con el dataframe cualitativo
    df = pd.concat([cuantitativas_primas, cuantitativas_no_primas, cualitativas_primas,
                    cualitativas_no_primas], axis=1)
    return(df)

#Función_3. Identifica los valores nulos “por columna” y “por dataframe”
def cuenta_nulos(df):
    #Valores nulos por columna
    valores_nulos_cols = df.isnull().sum()
    #Valores nulos por dataframe
    valores_nulos_df = df.isnull().sum().sum()
    
    return("Valores nulos por columna", valores_nulos_cols,
            "Valores nulos por dataframe", valores_nulos_df)

#Función_4. Identifica los valores atípicos de las columnas numéricas con el método de “Rango intercuartílico” 
# y los sustituye con la leyenda “Valor Atípico”
def sust_atipicos(df):
    import pandas as pd
    #Separamos las columnas con valores cuantitativos
    cuantitativas = df.select_dtypes(include=['float64', 'int64','float','int'])
    cualitativas = df.select_dtypes(include=['object', 'datetime','category'])

    #Método aplicando Cuartiles. Encuentro cuartiles 0.25 y 0.75
    y = cuantitativas
    
    percentile25=y.quantile(0.25) #Q1
    percentile75=y.quantile(0.75) #Q3
    iqr=percentile75-percentile25 
    
    Limite_Superior_iqr = percentile75 + 1.5*iqr
    Limite_Inferior_iqr = percentile25 - 1.5*iqr

    df_iqr = cuantitativas[(y<=Limite_Superior_iqr)&(y>=Limite_Inferior_iqr)]
    df_iqr

    df_iqr = df_iqr.fillna('Valor Atípico')
    df_iqr

    df_limpio = pd.concat([cualitativas, df_iqr], axis=1)
    df_limpio
    return(df_limpio)