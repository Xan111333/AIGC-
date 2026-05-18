#!/bin/bash

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="$PROJECT_DIR/docker-compose.prod.yml"
ENV_FILE="$PROJECT_DIR/.env.prod"
BACKUP_DIR="$PROJECT_DIR/backups/$(date +%Y%m%d_%H%M%S)"

echo "=================================="
echo "AIGC实训平台 - 一键部署脚本"
echo "=================================="

check_requirements() {
    echo "[1/6] 检查部署环境..."

    if ! command -v docker &> /dev/null; then
        echo "❌ 错误: Docker 未安装，请先安装 Docker"
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        echo "❌ 错误: Docker Compose 未安装，请先安装 Docker Compose"
        exit 1
    fi

    if [ ! -f "$ENV_FILE" ]; then
        echo "⚠️  警告: $ENV_FILE 不存在"
        echo "   正在从 .env.prod.example 创建..."
        cp "$PROJECT_DIR/.env.prod.example" "$ENV_FILE"
        echo "   请编辑 $ENV_FILE 配置必要参数后重新运行脚本"
        exit 1
    fi

    echo "✅ 环境检查通过"
}

backup() {
    echo "[2/6] 创建备份..."

    mkdir -p "$BACKUP_DIR"

    if [ -f "$ENV_FILE" ]; then
        cp "$ENV_FILE" "$BACKUP_DIR/.env.prod"
        echo "✅ 环境变量已备份"
    fi

    echo "✅ 备份完成: $BACKUP_DIR"
}

pull_images() {
    echo "[3/6] 拉取基础镜像..."

    if command -v docker-compose &> /dev/null; then
        docker-compose -f "$COMPOSE_FILE" pull
    else
        docker compose -f "$COMPOSE_FILE" pull
    fi

    echo "✅ 基础镜像拉取完成"
}

build_images() {
    echo "[4/6] 构建服务镜像..."

    if command -v docker-compose &> /dev/null; then
        docker-compose -f "$COMPOSE_FILE" build
    else
        docker compose -f "$COMPOSE_FILE" build
    fi

    echo "✅ 服务镜像构建完成"
}

start_services() {
    echo "[5/6] 启动服务..."

    if command -v docker-compose &> /dev/null; then
        docker-compose -f "$COMPOSE_FILE" up -d
    else
        docker compose -f "$COMPOSE_FILE" up -d
    fi

    echo "✅ 服务启动中..."
}

health_check() {
    echo "[6/6] 健康检查..."

    echo "等待服务启动 (30秒)..."
    sleep 30

    if command -v docker-compose &> /dev/null; then
        SERVICES=$(docker-compose -f "$COMPOSE_FILE" ps --services)
    else
        SERVICES=$(docker compose -f "$COMPOSE_FILE" ps --services)
    fi

    for service in $SERVICES; do
        if command -v docker-compose &> /dev/null; then
            STATUS=$(docker-compose -f "$COMPOSE_FILE" ps --filter "name=$service" --format "{{.Status}}")
        else
            STATUS=$(docker compose -f "$COMPOSE_FILE" ps --filter "name=$service" --format "{{.Status}}")
        fi

        if echo "$STATUS" | grep -q "Up"; then
            echo "✅ $service: 运行中"
        else
            echo "❌ $service: 异常"
        fi
    done

    echo ""
    echo "=================================="
    echo "🎉 部署完成！"
    echo "=================================="
    echo ""
    echo "服务地址:"
    echo "  - 前端: http://localhost"
    echo "  - 后端: http://localhost:8000"
    echo "  - API文档: http://localhost:8000/docs"
    echo ""
    echo "测试账户:"
    echo "  - 管理员: admin / admin123"
    echo "  - 教师:   teacher / teacher123"
    echo "  - 学生:   student / student123"
    echo ""
    echo "常用命令:"
    echo "  - 查看日志: docker-compose -f $COMPOSE_FILE logs -f [service]"
    echo "  - 重启服务: docker-compose -f $COMPOSE_FILE restart"
    echo "  - 停止服务: docker-compose -f $COMPOSE_FILE down"
    echo "  - 查看状态: docker-compose -f $COMPOSE_FILE ps"
}

case "${1:-deploy}" in
    deploy)
        check_requirements
        backup
        pull_images
        build_images
        start_services
        health_check
        ;;
    backup)
        backup
        ;;
    restart)
        echo "重启服务..."
        if command -v docker-compose &> /dev/null; then
            docker-compose -f "$COMPOSE_FILE" restart
        else
            docker compose -f "$COMPOSE_FILE" restart
        fi
        health_check
        ;;
    stop)
        echo "停止服务..."
        if command -v docker-compose &> /dev/null; then
            docker-compose -f "$COMPOSE_FILE" down
        else
            docker compose -f "$COMPOSE_FILE" down
        fi
        ;;
    start)
        echo "启动服务..."
        if command -v docker-compose &> /dev/null; then
            docker-compose -f "$COMPOSE_FILE" up -d
        else
            docker compose -f "$COMPOSE_FILE" up -d
        fi
        health_check
        ;;
    *)
        echo "用法: $0 [command]"
        echo "命令:"
        echo "  deploy   - 完整部署（默认）"
        echo "  backup   - 仅创建备份"
        echo "  start    - 启动服务"
        echo "  stop     - 停止服务"
        echo "  restart  - 重启服务"
        exit 1
        ;;
esac
