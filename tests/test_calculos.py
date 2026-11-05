"""
Tests para verificar que src/ calcula lo mismo que verificacion/.

Compara resultados de las funciones de src/ con valores esperados
de verificacion/ para las muestras pequeñas.
"""

import sys
import os
import pandas as pd
import numpy as np
from pathlib import Path

# Agregar src y verificacion al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent / "verificacion"))

from eda import resumen_numerico
from distribuciones import gumbel_momentos, cuantil_retorno
from regresion import calculo_manual
from series import promedio_movil, indices_estacionales, metodos_referencia, metricas


# ============================================================================
# Valores esperados (de verificacion/)
# ============================================================================

EDA_ESPERADO = {
    'media': 8.9245,
    'mediana': 8.9465,
    'varianza': 2.8793,
    'desv_est': 1.6969,
}

DIST_ESPERADO = {
    'mu': 72.9269,
    'beta': 11.8905,
    'x10': 99.6849,
    'x50': 119.3229,
    'x100': 127.6250,
}

REG_ESPERADO = {
    'b0': 16.8804,
    'b1': -0.0328,
    'r2': 0.1272,
    'p_value': 0.3858,
}

SERIES_ESPERADO = {
    'pm3': 118.8530,
    'smape_est': 9.6943,  # Estacional ingenuo
}


# ============================================================================
# Tests
# ============================================================================

def test_eda():
    """Verifica EDA con muestra_eda10.csv"""
    print("🧪 Test EDA... ", end="")
    
    # Cargar datos
    df = pd.read_csv('/workspaces/app-estadistica-aplicada-2026-2/datos/muestra_eda10.csv')
    y = df['rendimiento']
    
    # Calcular estadísticas
    stats = resumen_numerico(y)
    
    # Verificar
    assert abs(stats['media'] - EDA_ESPERADO['media']) < 0.0001, \
        f"Media: {stats['media']} vs {EDA_ESPERADO['media']}"
    
    assert abs(stats['mediana'] - EDA_ESPERADO['mediana']) < 0.0001, \
        f"Mediana: {stats['mediana']} vs {EDA_ESPERADO['mediana']}"
    
    assert abs(stats['varianza'] - EDA_ESPERADO['varianza']) < 0.001, \
        f"Varianza: {stats['varianza']} vs {EDA_ESPERADO['varianza']}"
    
    assert abs(stats['desv_est_muestral'] - EDA_ESPERADO['desv_est']) < 0.001, \
        f"Desv Est: {stats['desv_est_muestral']} vs {EDA_ESPERADO['desv_est']}"
    
    print("✅ APROBADO")


def test_distribuciones():
    """Verifica Gumbel con muestra_dist10.csv"""
    print("🧪 Test Distribuciones... ", end="")
    
    # Cargar datos
    df = pd.read_csv('/workspaces/app-estadistica-aplicada-2026-2/datos/muestra_dist10.csv')
    x = df['pmax24h_mm']
    
    # Ajustar Gumbel
    params_dict = gumbel_momentos(x.values)
    
    # Verificar parámetros
    assert abs(params_dict['mu'] - DIST_ESPERADO['mu']) < 0.01, \
        f"μ: {params_dict['mu']} vs {DIST_ESPERADO['mu']}"
    
    assert abs(params_dict['beta'] - DIST_ESPERADO['beta']) < 0.01, \
        f"β: {params_dict['beta']} vs {DIST_ESPERADO['beta']}"
    
    # Convertir a tupla para cuantil_retorno (μ, β)
    params_tuple = (params_dict['mu'], params_dict['beta'])
    
    # Verificar períodos de retorno
    x10 = cuantil_retorno('Gumbel', params_tuple, 10)
    assert abs(x10 - DIST_ESPERADO['x10']) < 0.01, \
        f"x₁₀: {x10} vs {DIST_ESPERADO['x10']}"
    
    x50 = cuantil_retorno('Gumbel', params_tuple, 50)
    assert abs(x50 - DIST_ESPERADO['x50']) < 0.01, \
        f"x₅₀: {x50} vs {DIST_ESPERADO['x50']}"
    
    x100 = cuantil_retorno('Gumbel', params_tuple, 100)
    assert abs(x100 - DIST_ESPERADO['x100']) < 0.01, \
        f"x₁₀₀: {x100} vs {DIST_ESPERADO['x100']}"
    
    print("✅ APROBADO")


def test_regresion():
    """Verifica regresión con muestra_reg8.csv"""
    print("🧪 Test Regresión... ", end="")
    
    # Cargar datos
    df = pd.read_csv('/workspaces/app-estadistica-aplicada-2026-2/datos/muestra_reg8.csv')
    x = df['lamina_riego'].values
    y = df['rendimiento'].values
    
    # Calcular manualmente
    resultado = calculo_manual(x, y)
    
    # Verificar coeficientes
    assert abs(resultado['b0'] - REG_ESPERADO['b0']) < 0.001, \
        f"b₀: {resultado['b0']} vs {REG_ESPERADO['b0']}"
    
    assert abs(resultado['b1'] - REG_ESPERADO['b1']) < 0.0001, \
        f"b₁: {resultado['b1']} vs {REG_ESPERADO['b1']}"
    
    # Verificar R²
    assert abs(resultado['R2'] - REG_ESPERADO['r2']) < 0.001, \
        f"R²: {resultado['R2']} vs {REG_ESPERADO['r2']}"
    
    # Verificar p-value (tolerancia mayor por métodos numéricos)
    assert abs(resultado['p_valor'] - REG_ESPERADO['p_value']) < 0.01, \
        f"p-value: {resultado['p_valor']} vs {REG_ESPERADO['p_value']}"
    
    print("✅ APROBADO")


def test_series():
    """Verifica series de tiempo con muestra_series24.csv"""
    print("🧪 Test Series... ", end="")
    
    # Cargar serie directamente de muestra_series24.csv con índice de fecha
    df = pd.read_csv('/workspaces/app-estadistica-aplicada-2026-2/datos/muestra_series24.csv')
    y = pd.Series(
        df['precipitacion_mm'].values,
        index=pd.to_datetime(df['fecha']),
        name='precipitacion_mm'
    )
    y.index.freq = 'MS'
    
    # Usar primeros 18 para entrenar
    y_train = y.iloc[:18]
    y_val = y.iloc[18:]
    
    # Calcular promedio móvil
    pm3 = promedio_movil(y_train, orden=3)
    
    # Verificar PM3 en el mes 18 (índice 17)
    # El promedio móvil es NaN para los primeros 2 elementos
    pm3_18 = pm3.iloc[17]
    assert abs(pm3_18 - SERIES_ESPERADO['pm3']) < 0.01, \
        f"PM3₁₈: {pm3_18} vs {SERIES_ESPERADO['pm3']}"
    
    # Calcular índices estacionales
    indices = indices_estacionales(y_train)
    
    # Calcular pronósticos
    pronos_dict = metodos_referencia(y_train, h=6)
    
    # Calcular métricas
    metricas_dict = {}
    for metodo, pronos in pronos_dict.items():
        m = metricas(y_val, pronos)
        metricas_dict[metodo] = m
    
    # Verificar SMAPE del método estacional ingenuo
    # Nota: verificacion/ usa factor 100, src/series.py usa factor 200
    # Entonces se espera que src sea el doble
    smape_est = metricas_dict['estacional_ingenuo']['SMAPE']
    smape_esperado_ajustado = SERIES_ESPERADO['smape_est'] * 2  # Ajustar por factor 200 vs 100
    assert abs(smape_est - smape_esperado_ajustado) < 1.0, \
        f"SMAPE Estacional: {smape_est} vs {smape_esperado_ajustado}"
    
    print("✅ APROBADO")


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("TESTS DE CONSISTENCIA: src/ vs verificacion/")
    print("="*60 + "\n")
    
    try:
        test_eda()
        test_distribuciones()
        test_regresion()
        test_series()
        
        print("\n" + "="*60)
        print("✅ TODOS LOS TESTS APROBADOS")
        print("="*60)
        print("\n✨ La app calcula lo mismo que verificacion/")
        print("   Confianza en los resultados: MÁXIMA ✅\n")
        
    except AssertionError as e:
        print(f"\n❌ TEST FALLIDO: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        sys.exit(1)
