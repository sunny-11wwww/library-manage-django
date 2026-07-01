import os

TEMPLATE_DIR = r"D:\Test_git\library_management\library_app\templates\library_app"

templates = {}

# base.html
templates["base.html"] = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}图书管理系统{% endblock %}</title>
    <link href="https://cdn.bootcdn.net/ajax/libs/bootstrap/5.3.3/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.bootcdn.net/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        body { background: #f4f6f9; }
        .navbar { background: linear-gradient(135deg, #1e3c72, #2a5298) !important; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .navbar-brand { font-weight: 700; font-size: 1.4rem; }
        .card { border-radius: 12px; border: none; box-shadow: 0 2px 12px rgba(0,0,0,0.08); transition: transform 0.2s; }
        .card:hover { transform: translateY(-2px); }
        .stat-card { text-align: center; padding: 1.5rem; }
        .stat-card .number { font-size: 2.2rem; font-weight: 700; color: #1e3c72; }
        .stat-card .label { color: #6c757d; font-size: 0.9rem; }
        .stat-card .icon { font-size: 2rem; margin-bottom: 0.5rem; }
        .btn-primary { background: #1e3c72; border-color: #1e3c72; }
        .btn-primary:hover { background: #2a5298; border-color: #2a5298; }
        .table th { background: #f8f9fa; border-bottom: 2px solid #dee2e6; }
        .badge-available { background: #28a745; }
        .badge-borrowed { background: #ffc107; color: #000; }
        .badge-overdue { background: #dc3545; }
        .badge-returned { background: #6c757d; }
        footer { text-align: center; padding: 1.5rem; color: #6c757d; font-size: 0.9rem; }
        .table td { vertical-align: middle; }
        .action-btn { padding: 0.25rem 0.5rem; font-size: 0.85rem; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand" href="/"><i class="fas fa-book-reader me-2"></i>图书管理系统</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    {% if user.is_authenticated %}
                        {% if user.is_staff %}
                            <li class="nav-item"><a class="nav-link" href="{% url 'admin_dashboard' %}"><i class="fas fa-tachometer-alt me-1"></i>管理首页</a></li>
                            <li class="nav-item"><a class="nav-link" href="{% url 'admin_books' %}"><i class="fas fa-book me-1"></i>图书管理</a></li>
                            <li class="nav-item"><a class="nav-link" href="{% url 'admin_borrow_records' %}"><i class="fas fa-list me-1"></i>借阅记录</a></li>
                            <li class="nav-item"><a class="nav-link" href="{% url 'admin_statistics' %}"><i class="fas fa-chart-bar me-1"></i>统计</a></li>
                        {% else %}
                            <li class="nav-item"><a class="nav-link" href="{% url 'student_books' %}"><i class="fas fa-book me-1"></i>图书列表</a></li>
                            <li class="nav-item"><a class="nav-link" href="{% url 'student_history' %}"><i class="fas fa-history me-1"></i>我的借阅</a></li>
                        {% endif %}
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                                <i class="fas fa-user me-1"></i>{{ user.username }}
                            </a>
                            <ul class="dropdown-menu dropdown-menu-end">
                                <li><a class="dropdown-item" href="{% url 'logout' %}"><i class="fas fa-sign-out-alt me-2"></i>退出登录</a></li>
                            </ul>
                        </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>
    <div class="container mt-4 mb-5">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        {% endif %}
        {% block content %}{% endblock %}
    </div>
    <footer class="text-center mt-5 py-3 text-muted">
        <p class="mb-0">&copy; 2026 图书管理系统 | Powered by Django</p>
    </footer>
    <script src="https://cdn.bootcdn.net/ajax/libs/bootstrap/5.3.3/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

# login.html
templates["login.html"] = """{% extends "library_app/base.html" %}
{% block title %}登录 - 图书管理系统{% endblock %}
{% block content %}
<div class="row justify-content-center mt-5">
    <div class="col-md-4">
        <div class="card p-4">
            <div class="text-center mb-4">
                <i class="fas fa-book-reader fa-3x" style="color:#1e3c72;"></i>
                <h3 class="mt-2">图书管理系统</h3>
                <p class="text-muted">请登录您的账户</p>
            </div>
            <form method="post">
                {% csrf_token %}
                <div class="mb-3">
                    <label class="form-label">用户名</label>
                    <input type="text" name="username" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">密码</label>
                    <input type="password" name="password" class="form-control" required>
                </div>
                <button type="submit" class="btn btn-primary w-100">登录</button>
            </form>
            <div class="text-center mt-3">
                <p class="mb-0">还没有账号？<a href="{% url 'register' %}">立即注册</a></p>
            </div>
            <hr>
            <div class="text-muted small">
                <p class="mb-1"><strong>管理员：</strong>admin / admin123</p>
                <p class="mb-0"><strong>学生：</strong>student / student123</p>
            </div>
        </div>
    </div>
</div>
{% endblock %}"""

# register.html
templates["register.html"] = """{% extends "library_app/base.html" %}
{% block title %}注册 - 图书管理系统{% endblock %}
{% block content %}
<div class="row justify-content-center mt-5">
    <div class="col-md-4">
        <div class="card p-4">
            <div class="text-center mb-4">
                <i class="fas fa-user-plus fa-3x" style="color:#1e3c72;"></i>
                <h3 class="mt-2">学生注册</h3>
            </div>
            <form method="post">
                {% csrf_token %}
                <div class="mb-3">
                    <label class="form-label">用户名</label>
                    <input type="text" name="username" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">姓名</label>
                    <input type="text" name="name" class="form-control">
                </div>
                <div class="mb-3">
                    <label class="form-label">邮箱</label>
                    <input type="email" name="email" class="form-control">
                </div>
                <div class="mb-3">
                    <label class="form-label">密码</label>
                    <input type="password" name="password" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">确认密码</label>
                    <input type="password" name="confirm_password" class="form-control" required>
                </div>
                <button type="submit" class="btn btn-primary w-100">注册</button>
            </form>
            <div class="text-center mt-3">
                <p class="mb-0">已有账号？<a href="{% url 'login' %}">去登录</a></p>
            </div>
        </div>
    </div>
</div>
{% endblock %}"""

# student_books.html
templates["student_books.html"] = """{% extends "library_app/base.html" %}
{% block title %}图书列表 - 图书管理系统{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h3><i class="fas fa-book me-2"></i>图书列表</h3>
    <span class="badge bg-primary fs-6">{{ books.count }} 本书</span>
</div>

<form class="mb-4" method="get">
    <div class="input-group">
        <input type="text" name="search" class="form-control" placeholder="搜索书名、作者或ISBN..." value="{{ search_query }}">
        <button class="btn btn-primary" type="submit"><i class="fas fa-search me-1"></i>搜索</button>
    </div>
</form>

<div class="row">
    {% for book in books %}
    <div class="col-md-4 mb-4">
        <div class="card h-100">
            <div class="card-body">
                <h5 class="card-title">{{ book.title }}</h5>
                <p class="card-text text-muted mb-1"><i class="fas fa-user me-1"></i>{{ book.author }}</p>
                {% if book.publisher %}<p class="card-text text-muted mb-1"><i class="fas fa-building me-1"></i>{{ book.publisher }}</p>{% endif %}
                <p class="card-text text-muted mb-1"><small>ISBN: {{ book.isbn }}</small></p>
                <hr>
                <div class="d-flex justify-content-between align-items-center">
                    <span class="badge {% if book.available_quantity > 0 %}bg-success{% else %}bg-danger{% endif %}">
                        可借 {{ book.available_quantity }}/{{ book.total_quantity }}
                    </span>
                    {% if book.available_quantity > 0 %}
                        <a href="{% url 'borrow_book' book.id %}" class="btn btn-sm btn-primary">借阅</a>
                    {% else %}
                        <button class="btn btn-sm btn-secondary" disabled>已借完</button>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
    {% empty %}
    <div class="col-12 text-center py-5">
        <i class="fas fa-book-open fa-4x text-muted mb-3"></i>
        <p class="text-muted">暂无图书</p>
    </div>
    {% endfor %}
</div>
{% endblock %}"""

# student_history.html
templates["student_history.html"] = """{% extends "library_app/base.html" %}
{% load tz %}
{% block title %}我的借阅 - 图书管理系统{% endblock %}
{% block content %}
<h3 class="mb-4"><i class="fas fa-history me-2"></i>我的借阅记录</h3>

<div class="card">
    <div class="card-body">
        <div class="table-responsive">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>图书</th>
                        <th>作者</th>
                        <th>借阅日期</th>
                        <th>应还日期</th>
                        <th>归还日期</th>
                        <th>状态</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                    {% for record in records %}
                    <tr>
                        <td>{{ record.book.title }}</td>
                        <td>{{ record.book.author }}</td>
                        <td>{{ record.borrow_date|date:"Y-m-d" }}</td>
                        <td>{{ record.due_date|date:"Y-m-d" }}</td>
                        <td>{{ record.return_date|date:"Y-m-d"|default:"-" }}</td>
                        <td>
                            {% if record.status == 'borrowed' %}
                                <span class="badge bg-warning text-dark">借阅中</span>
                            {% elif record.status == 'returned' %}
                                <span class="badge bg-secondary">已归还</span>
                            {% elif record.status == 'overdue' %}
                                <span class="badge bg-danger">逾期</span>
                            {% endif %}
                        </td>
                        <td>
                            {% if record.status == 'borrowed' %}
                                <a href="{% url 'return_book' record.id %}" class="btn btn-sm btn-success">归还</a>
                            {% elif record.status == 'overdue' %}
                                <a href="{% url 'return_book' record.id %}" class="btn btn-sm btn-danger">归还</a>
                            {% else %}
                                <span class="text-muted">-</span>
                            {% endif %}
                        </td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="7" class="text-center py-4 text-muted">暂无借阅记录</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}"""

# admin_dashboard.html
templates["admin_dashboard.html"] = """{% extends "library_app/base.html" %}
{% block title %}管理首页 - 图书管理系统{% endblock %}
{% block content %}
<h3 class="mb-4"><i class="fas fa-tachometer-alt me-2"></i>管理首页</h3>

<div class="row mb-4">
    <div class="col-md-3 mb-3">
        <div class="card stat-card">
            <div class="icon"><i class="fas fa-book" style="color:#1e3c72;"></i></div>
            <div class="number">{{ total_books }}</div>
            <div class="label">图书总数</div>
        </div>
    </div>
    <div class="col-md-3 mb-3">
        <div class="card stat-card">
            <div class="icon"><i class="fas fa-book-reader" style="color:#28a745;"></i></div>
            <div class="number">{{ total_borrowed }}</div>
            <div class="label">借阅中</div>
        </div>
    </div>
    <div class="col-md-3 mb-3">
        <div class="card stat-card">
            <div class="icon"><i class="fas fa-users" style="color:#17a2b8;"></i></div>
            <div class="number">{{ total_students }}</div>
            <div class="label">学生总数</div>
        </div>
    </div>
    <div class="col-md-3 mb-3">
        <div class="card stat-card">
            <div class="icon"><i class="fas fa-exclamation-triangle" style="color:#dc3545;"></i></div>
            <div class="number">{{ overdue_count }}</div>
            <div class="label">逾期未还</div>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-12">
        <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0">最近借阅记录</h5>
                <a href="{% url 'admin_borrow_records' %}" class="btn btn-sm btn-primary">查看全部</a>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th>学生</th>
                                <th>图书</th>
                                <th>借阅日期</th>
                                <th>应还日期</th>
                                <th>状态</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for record in recent_records %}
                            <tr>
                                <td>{{ record.student.username }}</td>
                                <td>{{ record.book.title }}</td>
                                <td>{{ record.borrow_date|date:"Y-m-d" }}</td>
                                <td>{{ record.due_date|date:"Y-m-d" }}</td>
                                <td>
                                    {% if record.status == 'borrowed' %}
                                        <span class="badge bg-warning text-dark">借阅中</span>
                                    {% elif record.status == 'returned' %}
                                        <span class="badge bg-secondary">已归还</span>
                                    {% elif record.status == 'overdue' %}
                                        <span class="badge bg-danger">逾期</span>
                                    {% endif %}
                                </td>
                            </tr>
                            {% empty %}
                            <tr><td colspan="5" class="text-center text-muted">暂无记录</td></tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}"""

# admin_books.html
templates["admin_books.html"] = """{% extends "library_app/base.html" %}
{% block title %}图书管理 - 图书管理系统{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h3><i class="fas fa-book me-2"></i>图书管理</h3>
    <a href="{% url 'admin_book_add' %}" class="btn btn-primary"><i class="fas fa-plus me-1"></i>添加图书</a>
</div>

<form class="mb-4" method="get">
    <div class="input-group">
        <input type="text" name="search" class="form-control" placeholder="搜索书名、作者或ISBN..." value="{{ search_query }}">
        <button class="btn btn-primary" type="submit"><i class="fas fa-search me-1"></i>搜索</button>
    </div>
</form>

<div class="card">
    <div class="card-body">
        <div class="table-responsive">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>书名</th>
                        <th>作者</th>
                        <th>ISBN</th>
                        <th>总数量</th>
                        <th>可借数量</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                    {% for book in books %}
                    <tr>
                        <td>{{ book.title }}</td>
                        <td>{{ book.author }}</td>
                        <td>{{ book.isbn }}</td>
                        <td>{{ book.total_quantity }}</td>
                        <td>
                            {% if book.available_quantity > 0 %}
                                <span class="badge bg-success">{{ book.available_quantity }}</span>
                            {% else %}
                                <span class="badge bg-danger">{{ book.available_quantity }}</span>
                            {% endif %}
                        </td>
                        <td>
                            <a href="{% url 'admin_book_edit' book.id %}" class="btn btn-sm btn-warning action-btn"><i class="fas fa-edit"></i></a>
                            <a href="{% url 'admin_book_delete' book.id %}" class="btn btn-sm btn-danger action-btn" onclick="return confirm('确定要删除《{{ book.title }}》吗？')"><i class="fas fa-trash"></i></a>
                        </td>
                    </tr>
                    {% empty %}
                    <tr><td colspan="6" class="text-center py-4 text-muted">暂无图书</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}"""

# admin_book_form.html
templates["admin_book_form.html"] = """{% extends "library_app/base.html" %}
{% block title %}{{ action }}图书 - 图书管理系统{% endblock %}
{% block content %}
<h3 class="mb-4"><i class="fas fa-{% if action == '添加' %}plus{% else %}edit{% endif %} me-2"></i>{{ action }}图书</h3>

<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    <div class="mb-3">
                        <label class="form-label">书名 *</label>
                        <input type="text" name="title" class="form-control" value="{{ book.title|default:'' }}" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">作者 *</label>
                        <input type="text" name="author" class="form-control" value="{{ book.author|default:'' }}" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">出版社</label>
                        <input type="text" name="publisher" class="form-control" value="{{ book.publisher|default:'' }}">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">ISBN *</label>
                        <input type="text" name="isbn" class="form-control" value="{{ book.isbn|default:'' }}" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">总数量 *</label>
                        <input type="number" name="total_quantity" class="form-control" value="{{ book.total_quantity|default:'1' }}" min="1" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">出版日期</label>
                        <input type="date" name="publish_date" class="form-control" value="{{ book.publish_date|date:'Y-m-d'|default:'' }}">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">描述</label>
                        <textarea name="description" class="form-control" rows="3">{{ book.description|default:'' }}</textarea>
                    </div>
                    <div class="d-flex justify-content-between">
                        <a href="{% url 'admin_books' %}" class="btn btn-secondary">返回</a>
                        <button type="submit" class="btn btn-primary">保存</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}"""

# admin_borrow_records.html
templates["admin_borrow_records.html"] = """{% extends "library_app/base.html" %}
{% block title %}借阅记录 - 图书管理系统{% endblock %}
{% block content %}
<h3 class="mb-4"><i class="fas fa-list me-2"></i>借阅记录</h3>

<div class="card mb-4">
    <div class="card-body">
        <form method="get" class="row g-3">
            <div class="col-md-6">
                <input type="text" name="search" class="form-control" placeholder="搜索学生或图书..." value="{{ search }}">
            </div>
            <div class="col-md-4">
                <select name="status" class="form-select">
                    <option value="">全部状态</option>
                    <option value="borrowed" {% if status_filter == 'borrowed' %}selected{% endif %}>借阅中</option>
                    <option value="returned" {% if status_filter == 'returned' %}selected{% endif %}>已归还</option>
                    <option value="overdue" {% if status_filter == 'overdue' %}selected{% endif %}>逾期</option>
                </select>
            </div>
            <div class="col-md-2">
                <button type="submit" class="btn btn-primary w-100">筛选</button>
            </div>
        </form>
    </div>
</div>

<div class="card">
    <div class="card-body">
        <div class="table-responsive">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>学生</th>
                        <th>图书</th>
                        <th>借阅日期</th>
                        <th>应还日期</th>
                        <th>归还日期</th>
                        <th>状态</th>
                    </tr>
                </thead>
                <tbody>
                    {% for record in records %}
                    <tr>
                        <td>{{ record.student.username }}</td>
                        <td>{{ record.book.title }}</td>
                        <td>{{ record.borrow_date|date:"Y-m-d H:i" }}</td>
                        <td>{{ record.due_date|date:"Y-m-d" }}</td>
                        <td>{{ record.return_date|date:"Y-m-d"|default:"-" }}</td>
                        <td>
                            {% if record.status == 'borrowed' %}
                                <span class="badge bg-warning text-dark">借阅中</span>
                            {% elif record.status == 'returned' %}
                                <span class="badge bg-secondary">已归还</span>
                            {% elif record.status == 'overdue' %}
                                <span class="badge bg-danger">逾期</span>
                            {% endif %}
                        </td>
                    </tr>
                    {% empty %}
                    <tr><td colspan="6" class="text-center py-4 text-muted">暂无记录</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        <p class="text-muted mb-0">共 {{ records|length }} 条记录</p>
    </div>
</div>
{% endblock %}"""

# admin_statistics.html
templates["admin_statistics.html"] = """{% extends "library_app/base.html" %}
{% block title %}统计 - 图书管理系统{% endblock %}
{% block content %}
<h3 class="mb-4"><i class="fas fa-chart-bar me-2"></i>借阅统计</h3>

<div class="row mb-4">
    <div class="col-md-3 mb-3">
        <div class="card stat-card">
            <div class="icon"><i class="fas fa-exchange-alt" style="color:#1e3c72;"></i></div>
            <div class="number">{{ total_borrows }}</div>
            <div class="label">总借阅次数</div>
        </div>
    </div>
    <div class="col-md-3 mb-3">
        <div class="card stat-card">
            <div class="icon"><i class="fas fa-book-open" style="color:#28a745;"></i></div>
            <div class="number">{{ active_borrows }}</div>
            <div class="label">当前借阅中</div>
        </div>
    </div>
    <div class="col-md-3 mb-3">
        <div class="card stat-card">
            <div class="icon"><i class="fas fa-check-circle" style="color:#17a2b8;"></i></div>
            <div class="number">{{ returned_borrows }}</div>
            <div class="label">已归还</div>
        </div>
    </div>
    <div class="col-md-3 mb-3">
        <div class="card stat-card">
            <div class="icon"><i class="fas fa-exclamation-circle" style="color:#dc3545;"></i></div>
            <div class="number">{{ overdue_count }}</div>
            <div class="label">逾期</div>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-md-6 mb-4">
        <div class="card">
            <div class="card-header"><h5 class="mb-0">借阅状态分布</h5></div>
            <div class="card-body">
                <table class="table">
                    <thead><tr><th>状态</th><th>数量</th></tr></thead>
                    <tbody>
                        {% for stat in status_stats %}
                        <tr>
                            <td>
                                {% if stat.status == 'borrowed' %}<span class="badge bg-warning text-dark">借阅中</span>
                                {% elif stat.status == 'returned' %}<span class="badge bg-secondary">已归还</span>
                                {% elif stat.status == 'overdue' %}<span class="badge bg-danger">逾期</span>
                                {% endif %}
                            </td>
                            <td>{{ stat.count }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <div class="col-md-6 mb-4">
        <div class="card">
            <div class="card-header"><h5 class="mb-0">热门图书排行榜</h5></div>
            <div class="card-body">
                <table class="table">
                    <thead><tr><th>排名</th><th>书名</th><th>作者</th><th>借阅次数</th></tr></thead>
                    <tbody>
                        {% for book in most_borrowed %}
                        <tr>
                            <td>{{ forloop.counter }}</td>
                            <td>{{ book.book__title }}</td>
                            <td>{{ book.book__author }}</td>
                            <td><span class="badge bg-primary">{{ book.borrow_count }}</span></td>
                        </tr>
                        {% empty %}
                        <tr><td colspan="4" class="text-center text-muted">暂无数据</td></tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

<div class="card mb-4">
    <div class="card-header"><h5 class="mb-0">逾期记录</h5></div>
    <div class="card-body">
        {% if overdue_books %}
        <div class="table-responsive">
            <table class="table table-hover">
                <thead><tr><th>学生</th><th>图书</th><th>借阅日期</th><th>应还日期</th><th>逾期天数</th></tr></thead>
                <tbody>
                    {% for record in overdue_books %}
                    <tr>
                        <td>{{ record.student.username }}</td>
                        <td>{{ record.book.title }}</td>
                        <td>{{ record.borrow_date|date:"Y-m-d" }}</td>
                        <td>{{ record.due_date|date:"Y-m-d" }}</td>
                        <td><span class="badge bg-danger">{{ record.days_overdue }} 天</span></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% else %}
        <p class="text-muted mb-0">暂无逾期记录</p>
        {% endif %}
    </div>
</div>
{% endblock %}"""

for filename, content in templates.items():
    filepath = os.path.join(TEMPLATE_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.lstrip("\n"))
    print(f"{filename} written ({len(content)} chars)")

print(f"\nTotal templates: {len(templates)}")
