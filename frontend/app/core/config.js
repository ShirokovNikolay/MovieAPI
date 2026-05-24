/**
 * Базовый URL API без завершающего слэша.
 * Пустая строка: запросы идут на тот же origin (например, через nginx в Docker).
 * Для отладки с другого порта можно задать window.__API_BASE__ = 'http://localhost:8000'
 * до подключения остальных скриптов (потребуется CORS на бэкенде).
 */
window.__API_BASE__ = typeof window.__API_BASE__ !== "undefined" ? window.__API_BASE__ : "";
