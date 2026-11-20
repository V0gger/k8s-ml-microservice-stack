# 🚀 K8s ML Microservice Stack

Учебный, но production-ready стенд, демонстрирующий лучшие практики развертывания микросервисной архитектуры. Проект разделяет Stateful (базы данных) и Stateless (приложение) нагрузки, использует Kubernetes для оркестрации и Prometheus/Grafana для мониторинга.

## 🏗 Архитектура

- **Stateless-слой**: Python (FastAPI) микросервис, упакованный в оптимизированный Docker-образ и развернутый в Kubernetes (k3s) с обеспечением отказоустойчивости (2+ реплики).
- **Stateful-слой**: PostgreSQL и Redis, развернутые через Docker Compose с жесткими лимитами ресурсов и персистентными томами.
- **Observability**: Стек Prometheus + Grafana + Node Exporter для сбора и визуализации метрик хоста и контейнеров в реальном времени.

## ⚙️ Ключевые DevOps практики (Highlights)

1. **Безопасность и оптимизация Docker**: 
   - Использование Multi-stage build для минимизации размера финального образа.
   - Запуск приложения от непривилегированного пользователя (appuser), а не от root.
   - Настроенный .dockerignore для исключения мусора из контекста сборки.
   - Встроенный HEALTHCHECK для мониторинга состояния контейнера.
2. **Управление конфигурацией в K8s**: 
   - Полное отсутствие хардкода. Настройки (APP_ENV, APP_VERSION) и секреты (DB_PASSWORD) вынесены в ConfigMap и Secret и инжектятся через envFrom.
3. **Отказоустойчивость и самовосстановление**:
   - Настроены livenessProbe и readinessProbe для автоматического перезапуска зависших подов.
   - Поддержка бесшовных обновлений (Zero Downtime Rolling Update) и мгновенного отката (rollout undo).

## 🛠 Как развернуть с нуля

### 1. Предварительные требования
- Виртуальная машина с Ubuntu 20.04/22.04 и установленным Docker + k3s.

### 2. Запуск Stateful-баз и Мониторинга (Опционально)
cd stateful-db && docker compose up -d
cd ../monitoring && docker compose up -d
# Grafana будет доступна на порту 3000 (логин/пароль: admin/admin)

### 3. Деплой приложения в Kubernetes
cd ../k8s

# 1. Применяем конфигурации и секреты
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml

# 2. Деплоим приложение и сервис
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# 3. Проверяем статус подов (должны быть 1/1 Running)
kubectl get pods -w

# 4. Тестируем работу сервиса
curl http://localhost:30080/health
curl http://localhost:30080/predict?text="hello_kubernetes"

## 🔍 Troubleshooting (Шпаргалка)

- **ImagePullBackOff**: kubectl describe pod <pod_name> (проверьте раздел Events).
- **CrashLoopBackOff**: kubectl logs <pod_name> или kubectl logs <pod_name> --previous.
- **Постоянные перезапуски при статусе Running**: Проверьте kubectl describe pod <pod_name> на наличие Liveness probe failed.

---
*Проект создан в рамках интенсивной практики по Kubernetes и Docker. Автор: Мухаметзянов Булат.*
