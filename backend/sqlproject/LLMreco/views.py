from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Recommendation
from rest_framework.decorators import api_view
from rest_framework.response import Response
import random
import mysql.connector
import os

# MySQL 连接配置
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'guozhihan123',
    'database': 'test_db',
    'raise_on_warnings': True,
    'auth_plugin': 'mysql_native_password',
    'port': 3308,
    'connect_timeout': 10,  # 添加连接超时
    'allow_local_infile': True,
    'charset': 'utf8mb4',
    'use_pure': True  # 使用纯 Python 实现
}

def connect_mysql():
    """
    连接 MySQL 数据库
    """
    try:
        print("尝试连接 MySQL...")
        # 先尝试不指定数据库连接
        temp_config = MYSQL_CONFIG.copy()
        del temp_config['database']
        
        connection = mysql.connector.connect(**temp_config)
        print("基础连接成功，尝试选择数据库...")
        
        cursor = connection.cursor()
        
        # 先检查数据库是否存在
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        
        if 'test_db' not in databases:
            print("数据库不存在，创建新数据库...")
            cursor.execute("CREATE DATABASE test_db")
            print("数据库创建成功")
        
        # 使用数据库
        cursor.execute("USE test_db")
        cursor.close()
        
        print("MySQL 连接和数据库选择成功！")
        return connection
        
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("用户名或密码错误")
            print(f"当前配置: user={MYSQL_CONFIG['user']}, password={'*' * len(MYSQL_CONFIG['password'])}")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("数据库不存在")
        else:
            print(f"MySQL 连接错误: {err}")
            print(f"错误代码: {err.errno}")
        return None
    except Exception as e:
        print(f"发生未知错误: {type(e).__name__} - {str(e)}")
        return None

@api_view(['POST'])
@csrf_exempt
def mysql_operations(request):
    """
    处理 MySQL 相关操作的 API 接口
    """
    if request.method == 'POST':
        try:
            operation = request.data.get('operation')
            print(f"收到操作请求: {operation}")
            
            if operation == 'test_connection':
                # 测试数据库连接
                conn = connect_mysql()
                if conn:
                    conn.close()
                    return Response({
                        'status': 'success',
                        'message': '数据库连接成功'
                    })
                else:
                    return Response({
                        'status': 'error',
                        'message': '数据库连接失败，请检查配置'
                    }, status=500)
            
            elif operation == 'get_databases':
                conn = connect_mysql()
                if not conn:
                    return Response({
                        'status': 'error',
                        'message': '数据库连接失败'
                    }, status=500)
                
                cursor = conn.cursor()
                cursor.execute("SHOW DATABASES")
                databases = [db[0] for db in cursor.fetchall()]
                cursor.close()
                conn.close()
                
                return Response({
                    'status': 'success',
                    'databases': databases
                })
                
            elif operation == 'get_tables':
                database = request.data.get('database')
                if not database:
                    return Response({
                        'status': 'error',
                        'message': '未指定数据库'
                    }, status=400)
                
                conn = connect_mysql()
                if not conn:
                    return Response({
                        'status': 'error',
                        'message': '数据库连接失败'
                    }, status=500)
                
                cursor = conn.cursor()
                cursor.execute(f"USE {database}")
                cursor.execute("SHOW TABLES")
                tables = [table[0] for table in cursor.fetchall()]
                cursor.close()
                conn.close()
                
                return Response({
                    'status': 'success',
                    'tables': tables
                })
                
            elif operation == 'get_table_data':
                database = request.data.get('database')
                table = request.data.get('table')
                if not database or not table:
                    return Response({
                        'status': 'error',
                        'message': '未指定数据库或表'
                    }, status=400)
                
                conn = connect_mysql()
                if not conn:
                    return Response({
                        'status': 'error',
                        'message': '数据库连接失败'
                    }, status=500)
                
                cursor = conn.cursor(dictionary=True)
                cursor.execute(f"USE {database}")
                cursor.execute(f"SELECT * FROM {table} LIMIT 100")
                rows = cursor.fetchall()
                
                # 获取列名
                cursor.execute(f"SHOW COLUMNS FROM {table}")
                columns = [column['Field'] for column in cursor.fetchall()]
                
                cursor.close()
                conn.close()
                
                return Response({
                    'status': 'success',
                    'columns': columns,
                    'rows': rows
                })
            
            else:
                return Response({
                    'status': 'error',
                    'message': '不支持的操作类型'
                }, status=400)
                
        except Exception as e:
            print(f"操作出错: {str(e)}")
            return Response({
                'status': 'error',
                'message': f'操作失败: {str(e)}'
            }, status=500)
    
    return Response({
        'status': 'error',
        'message': '仅支持 POST 请求'
    }, status=405)

def get_completion_suggestion(input_text):
    """
    根据用户输入生成补全建议
    后续可以替换为实际的LLM逻辑
    """
    # 示例补全逻辑
    if not input_text:
        return ""
        
    # 简单的补全规则示例
    if "查询" in input_text:
        return "所有用户的基本信息"
    elif "删除" in input_text:
        return "指定ID的记录"
    elif "更新" in input_text:
        return "用户的密码信息"
    elif "添加" in input_text:
        return "新的用户记录"
    elif "如何" in input_text:
        return "使用SQL语句实现"
    else:
        return "使用SQL语句完成操作"

# Create your views here.
# 推荐问题动态获取，可添加LLM输出
def get_recommendations(request):
    base_recommendations = [
        '如何查询所有用户信息？',
        '如何添加新用户？',
        '如何删除指定记录？',
        '如何更新用户密码？',
    ]
    return JsonResponse(base_recommendations, safe=False)

@csrf_exempt
def process_input(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('input', '')
            print(f"收到用户输入: {user_input}")
            
            # 获取补全建议
            suggestion = get_completion_suggestion(user_input)
            
            # 将用户输入作为第一条推荐
            recommendations = [user_input] if user_input.strip() else []
            recommendations.extend([
                '如何查询所有用户信息？',
                '如何添加新用户？',
                '如何删除指定记录？',
                '如何更新用户密码？',
            ])
            
            return JsonResponse({
                'status': 'success',
                'message': '输入已接收',
                'recommendations': recommendations,
                'suggestion': suggestion
            })
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': '无效的JSON数据'
            }, status=400)
    return JsonResponse({
        'status': 'error',
        'message': '仅支持POST请求'
    }, status=405)

@csrf_exempt
def get_realtime_completion(request):
    """
    专门用于处理实时补全请求的接口
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('input', '')
            
            suggestion = get_completion_suggestion(user_input)
            
            return JsonResponse({
                'status': 'success',
                'suggestion': suggestion
            })
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': '无效的JSON数据'
            }, status=400)
    return JsonResponse({
        'status': 'error',
        'message': '仅支持POST请求'
    }, status=405)

@api_view(['POST'])
def chat_response(request):
    """
    处理聊天请求并返回固定回复
    """
    try:
        message = request.data.get('message', '')
        if not message:
            return Response({'error': 'Message is required'}, status=400)
            
        # 返回固定的三条消息
        response = "1.哪吒魔童闹海\n2.封神2\n3.唐探1900"
        
        return Response({
            'response': response,
            'status': 'success'
        })
        
    except Exception as e:
        return Response({
            'error': str(e),
            'status': 'error'
        }, status=500)

def retrievaldb():
    """
    存储数据库表数据信息
    """
    db_data = {
        'MySQL_Demo': {
            'tables': {
                'users': {
                    'columns': ['id', 'username', 'email', 'created_at'],
                    'rows': [
                        {'id': 1, 'username': 'johnn_doe', 'email': 'john@example.com', 'created_at': '2023-01-01'},
                        {'id': 2, 'username': 'jane_smith', 'email': 'jane@example.com', 'created_at': '2023-01-02'},
                        {'id': 3, 'username': 'bob_wilson', 'email': 'bob@example.com', 'created_at': '2023-01-03'}
                    ]
                },
                'orders': {
                    'columns': ['order_id', 'customer_id', 'total_amount', 'status'],
                    'rows': [
                        {'order_id': 101, 'customer_id': 1, 'total_amount': 299.99, 'status': 'completed'},
                        {'order_id': 102, 'customer_id': 2, 'total_amount': 199.50, 'status': 'pending'},
                        {'order_id': 103, 'customer_id': 1, 'total_amount': 499.99, 'status': 'processing'}
                    ]
                }
            }
        },
        'PostgreSQL_Test': {
            'tables': {
                'employees': {
                    'columns': ['emp_id', 'name', 'department', 'salary'],
                    'rows': [
                        {'emp_id': 'E001', 'name': 'Alice Brown', 'department': 'IT', 'salary': 75000},
                        {'emp_id': 'E002', 'name': 'Charlie Davis', 'department': 'HR', 'salary': 65000},
                        {'emp_id': 'E003', 'name': 'Eva Green', 'department': 'IT', 'salary': 78000}
                    ]
                },
                'departments': {
                    'columns': ['dept_id', 'name', 'location', 'budget'],
                    'rows': [
                        {'dept_id': 'D1', 'name': 'IT', 'location': 'Floor 1', 'budget': 500000},
                        {'dept_id': 'D2', 'name': 'HR', 'location': 'Floor 2', 'budget': 300000},
                        {'dept_id': 'D3', 'name': 'Finance', 'location': 'Floor 3', 'budget': 400000}
                    ]
                }
            }
        },
        'SQLite_Sample': {
            'tables': {
                'customers': {
                    'columns': ['customer_id', 'name', 'country', 'credit_limit'],
                    'rows': [
                        {'customer_id': 'C1', 'name': 'Tech Corp', 'country': 'USA', 'credit_limit': 50000},
                        {'customer_id': 'C2', 'name': 'Global Ltd', 'country': 'UK', 'credit_limit': 75000},
                        {'customer_id': 'C3', 'name': 'Local Shop', 'country': 'Canada', 'credit_limit': 25000}
                    ]
                },
                'inventory': {
                    'columns': ['item_id', 'name', 'quantity', 'price'],
                    'rows': [
                        {'item_id': 'I1', 'name': 'Laptop', 'quantity': 50, 'price': 999.99},
                        {'item_id': 'I2', 'name': 'Mouse', 'quantity': 100, 'price': 29.99},
                        {'item_id': 'I3', 'name': 'Keyboard', 'quantity': 75, 'price': 59.99}
                    ]
                }
            }
        }
    }
    
    return db_data

@api_view(['GET'])
def get_db_structure(request):
    """
    获取数据库表数据的API接口
    """
    try:
        db_data = retrievaldb()
        return Response({
            'status': 'success',
            'data': db_data
        })
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=500)
