#!/bin/bash

set -e

echo "========================================="
echo "  AIGC实训平台回滚脚本"
echo "========================================="
echo ""

BACKUP_DIR="./backups"

list_backups() {
    echo "可用的备份:"
    if [ -d "$BACKUP_DIR" ]; then
        ls -1 "$BACKUP_DIR" | nl
    else
        echo "没有找到备份目录"
        exit 1
    fi
    echo ""
}

restore_backup() {
    local backup_name=$1
    
    echo "正在回滚到: $backup_name"
    echo ""
    
    echo "[1/4] 停止服务..."
    docker-compose -f docker-compose.prod.yml down
    echo "✓ 服务已停止"
    echo ""
    
    echo "[2/4] 恢复环境变量..."
    if [ -f "$BACKUP_DIR/$backup_name/.env.prod.backup" ]; then
        cp "$BACKUP_DIR/$backup_name/.env.prod.backup" .env.prod
        echo "✓ 环境变量已恢复"
    else
        echo "警告: 未找到环境变量备份"
    fi
    echo ""
    
    echo "[3/4] 清理旧数据..."
    docker volume rm aigc_platform_mysql_data 2>/dev/null || true
    docker volume rm aigc_platform_redis_data 2>/dev/null || true
    echo "✓ 数据卷已清理"
    echo ""
    
    echo "[4/4] 重新启动服务..."
    docker-compose -f docker-compose.prod.yml up -d
    echo "✓ 服务已启动"
    echo ""
}

show_status() {
    echo "========================================="
    echo "  回滚完成！"
    echo "========================================="
    echo ""
    echo "服务状态:"
    docker-compose -f docker-compose.prod.yml ps
    echo ""
}

if [ "$1" == "latest" ]; then
    latest_backup=$(ls -1t "$BACKUP_DIR" | head -1)
    if [ -z "$latest_backup" ]; then
        echo "错误: 没有可用的备份"
        exit 1
    fi
    restore_backup "$latest_backup"
    show_status
elif [ "$1" == "list" ]; then
    list_backups
elif [ -n "$1" ]; then
    restore_backup "$1"
    show_status
else
    echo "用法:"
    echo "  $0 list              - 列出所有备份"
    echo "  $0 latest            - 回滚到最新备份"
    echo "  $0 <backup_name>     - 回滚到指定备份"
    echo ""
    list_backups
fi