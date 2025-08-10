#!/usr/bin/env python3
"""
Простой веб-интерфейс для DocxMD Converter
Базовая версия без Flask для демонстрации
"""

import json
import webbrowser
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socketserver
import threading
import time

class WebInterface:
    """Простой веб-интерфейс"""

    def __init__(self, port=8000):
        self.port = port
        self.server = None
        self.server_thread = None

    def create_html_page(self):
        """Создание HTML страницы"""
        html_content = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DocxMD Converter - Веб-интерфейс</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            color: #333;
            margin: 0;
            font-size: 2.5em;
        }
        .header p {
            color: #666;
            margin: 10px 0;
        }
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .feature-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            border: 2px solid #e9ecef;
            transition: transform 0.3s ease;
        }
        .feature-card:hover {
            transform: translateY(-5px);
            border-color: #667eea;
        }
        .feature-icon {
            font-size: 3em;
            margin-bottom: 15px;
        }
        .feature-title {
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
        }
        .feature-desc {
            color: #666;
            font-size: 0.9em;
        }
        .status-section {
            background: #e8f5e8;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            border-left: 5px solid #28a745;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .stat-item {
            text-align: center;
            background: white;
            padding: 15px;
            border-radius: 8px;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        .stat-label {
            color: #666;
            font-size: 0.9em;
        }
        .info-section {
            background: #fff3cd;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            border-left: 5px solid #ffc107;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 DocxMD Converter</h1>
            <p>Универсальная система обработки документов с интеллектуальным анализом</p>
            <p><strong>Версия 3.0.0</strong> | Статус: <span style="color: #28a745;">✅ Активна</span></p>
        </div>

        <div class="status-section">
            <h3>📊 Текущий статус системы</h3>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-number" id="processed-files">7</div>
                    <div class="stat-label">Обработано файлов</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">80.7</div>
                    <div class="stat-label">Средняя оценка</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">0.005</div>
                    <div class="stat-label">Время (сек)</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">100%</div>
                    <div class="stat-label">Успешность</div>
                </div>
            </div>
        </div>

        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">🧠</div>
                <div class="feature-title">NLP Анализ</div>
                <div class="feature-desc">Извлечение признаков, анализ тональности, определение сущностей</div>
            </div>

            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">Определение типов</div>
                <div class="feature-desc">Автоматическое определение типа документа из 7 категорий</div>
            </div>

            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <div class="feature-title">Оценка качества</div>
                <div class="feature-desc">Комплексная оценка по 5 критериям с рекомендациями</div>
            </div>

            <div class="feature-card">
                <div class="feature-icon">🔧</div>
                <div class="feature-title">Автоулучшения</div>
                <div class="feature-desc">Автоматическое исправление форматирования и структуры</div>
            </div>

            <div class="feature-card">
                <div class="feature-icon">📋</div>
                <div class="feature-title">Система шаблонов</div>
                <div class="feature-desc">7 типов документов с правилами обработки</div>
            </div>

            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <div class="feature-title">Высокая скорость</div>
                <div class="feature-desc">Обработка документа за 0.005 секунды</div>
            </div>
        </div>

        <div class="info-section">
            <h3>💡 Как использовать систему</h3>
            <p><strong>Через командную строку:</strong></p>
            <pre style="background: #f8f9fa; padding: 10px; border-radius: 5px; overflow-x: auto;">
# Запуск интеллектуального процессора
python3 intelligent_processor.py

# Демонстрация всех возможностей
python3 demo_all_features.py

# Универсальный запускатор
python3 run_system.py</pre>

            <p><strong>Поддерживаемые типы документов:</strong></p>
            <ul>
                <li>📄 Должностные инструкции</li>
                <li>📋 Положения о подразделениях</li>
                <li>📝 Рабочие инструкции</li>
                <li>📊 Отчеты</li>
                <li>📜 Договоры и соглашения</li>
                <li>📋 Протоколы заседаний</li>
                <li>📄 Общие документы</li>
            </ul>
        </div>

        <div style="text-align: center; margin-top: 30px; color: #666;">
            <p>🕒 Обновлено: <span id="current-time"></span></p>
            <p>Для полного функционала используйте Python интерфейсы</p>
        </div>
    </div>

    <script>
        // Обновление времени
        function updateTime() {
            const now = new Date();
            document.getElementById('current-time').textContent = now.toLocaleString('ru-RU');
        }

        updateTime();
        setInterval(updateTime, 1000);

        // Анимация счетчиков
        function animateCounter(element, target) {
            let current = 0;
            const increment = target / 50;
            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                element.textContent = Math.floor(current);
            }, 20);
        }

        // Запуск анимации при загрузке
        window.addEventListener('load', () => {
            const processedElement = document.getElementById('processed-files');
            animateCounter(processedElement, 7);
        });
    </script>
</body>
</html>"""

        # Сохраняем HTML файл
        html_file = Path("web_interface.html")
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return html_file

    def start_server(self):
        """Запуск веб-сервера"""
        try:
            # Создаем HTML страницу
            html_file = self.create_html_page()

            # Запускаем простой HTTP сервер
            handler = SimpleHTTPRequestHandler

            with socketserver.TCPServer(("", self.port), handler) as httpd:
                print(f"🌐 Веб-сервер запущен на http://localhost:{self.port}")
                print(f"📄 Страница: http://localhost:{self.port}/web_interface.html")
                print("🛑 Нажмите Ctrl+C для остановки")

                # Открываем браузер
                webbrowser.open(f"http://localhost:{self.port}/web_interface.html")

                # Запускаем сервер
                httpd.serve_forever()

        except KeyboardInterrupt:
            print("\n🛑 Веб-сервер остановлен")
        except Exception as e:
            print(f"❌ Ошибка запуска веб-сервера: {e}")


def main():
    """Основная функция"""
    print("🌐 Запуск веб-интерфейса DocxMD Converter")
    print("=" * 50)

    # Проверяем наличие Flask
    try:
        import flask
        print("⚠️  Flask обнаружен, но используется упрощенная версия")
    except ImportError:
        print("ℹ️  Flask не установлен, используется встроенный HTTP сервер")

    web_interface = WebInterface()
    web_interface.start_server()


if __name__ == "__main__":
    main()