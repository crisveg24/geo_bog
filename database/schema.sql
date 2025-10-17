-- Schema para la base de datos geo_bog

-- Tabla de ejemplo para datos geográficos
CREATE TABLE IF NOT EXISTS geographic_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    latitude REAL,
    longitude REAL,
    category VARCHAR(100),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de ejemplo para estadísticas
CREATE TABLE IF NOT EXISTS statistics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric_name VARCHAR(255) NOT NULL,
    metric_value REAL,
    metric_date DATE,
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_geographic_category ON geographic_data(category);
CREATE INDEX IF NOT EXISTS idx_statistics_date ON statistics(metric_date);
CREATE INDEX IF NOT EXISTS idx_statistics_category ON statistics(category);
