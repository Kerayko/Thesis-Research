from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Recommendation
from rest_framework.decorators import api_view
from rest_framework.response import Response
import random

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
