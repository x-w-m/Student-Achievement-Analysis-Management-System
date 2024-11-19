# 学生成绩分析管理系统

## 简介
这是一个使用 **Django** 开发的简单学生成绩分析管理系统。该系统允许管理员管理学生信息、录入学生成绩，并对成绩数据进行分析和可视化。适合初学者学习 Django 开发和数据管理的练手项目。

---

## 功能

1. **学生管理**
   - 添加、编辑、删除学生信息。
   - 按班级或学号查询学生信息。

2. **成绩管理**
   - 添加、编辑、删除学生成绩。
   - 按科目或时间范围筛选成绩。

3. **成绩分析**
   - 计算单科平均分、最高分、最低分。
   - 生成成绩分布图（如柱状图、饼图）。
   - 按学生或班级生成报告。

4. **用户权限**
   - 管理员可以执行所有操作。
   - 普通用户仅能查看分析结果。

---

## 技术栈

- **后端**：Django 5.x
- **前端**：HTML + CSS + Bootstrap
- **数据库**：MySQL（默认，可更改为 SQLite）
- **数据可视化**：PyCharts

---

## 安装与使用

### 1. 克隆项目
```bash
git clone https://github.com/your-username/student-grade-system.git](https://github.com/x-w-m/Student-Achievement-Analysis-Management-System.git
cd Student-Achievement-Analysis-Management-System
```

### 2. 安装依赖
确保已安装 Python（建议使用 3.8+），然后运行：
```bash
pip install -r requirements.txt
```

### 3. 配置数据库
- 在项目根目录的 `settings.py` 文件中，配置数据库信息：
  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': 'student_db',
          'USER': 'your-username',
          'PASSWORD': 'your-password',
          'HOST': 'localhost',
          'PORT': '3306',
      }
  }
  ```
- 如果使用默认的 SQLite，无需修改配置。

### 4. 初始化数据库
运行以下命令迁移数据库：
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 创建超级用户
创建管理员账户以管理系统：
```bash
python manage.py createsuperuser
```

### 6. 运行服务器
启动 Django 开发服务器：
```bash
python manage.py runserver
```
打开浏览器访问 `http://127.0.0.1:8000/`。

---

## 项目结构

```
待完善
```

---

## 功能展示

### 1. 学生管理
- 界面友好的表单，支持增删改查操作。
- 按学号或班级筛选学生信息。

### 2. 成绩录入
- 支持批量导入（CSV 文件）。
- 成绩录入简单明了。

### 3. 成绩分析
- 生成如下分析图表：
  - 成绩分布柱状图
  - 班级成绩饼图
  - 学生成绩趋势折线图

---

## 贡献

欢迎贡献代码或提供反馈！  
提交 Pull Request 或 Issues，我们会尽快回复。

---

## 许可证
本项目基于 [MIT License](LICENSE)。
