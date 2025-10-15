import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3

class SQLiteViewer:
    """
    SQLite 数据库查看器类，用于连接 SQLite 数据库并查看表数据。
    
    功能：
    - 连接 SQLite 数据库
    - 显示数据库中的所有表
    - 查看选中表的数据
    - 新建数据库文件
    - 新建表
    - 新建表数据
    """
    def __init__(self, root):
        """
        初始化 SQLiteViewer 界面。
        
        参数:
        - root: tkinter 的根窗口对象
        """
        self.root = root
        self.root.title("SQLite 数据库查看器")
        self.root.geometry("1000x800")
        
        # 数据库连接部分
        self.db_path_label = tk.Label(root, text="数据库文件路径:")
        self.db_path_label.pack(pady=5)
        
        self.db_path_entry = tk.Entry(root, width=50)
        self.db_path_entry.pack(pady=5)
        
        self.connect_button = tk.Button(root, text="连接数据库", command=self.connect_db)
        self.connect_button.pack(pady=5)
        
        # 新建数据库部分
        self.new_db_button = tk.Button(root, text="新建数据库", command=self.create_db)
        self.new_db_button.pack(pady=5)
        
        # 表列表部分
        self.tables_label = tk.Label(root, text="表列表:")
        self.tables_label.pack(pady=5)
        
        self.tables_listbox = tk.Listbox(root, width=50, height=10)
        self.tables_listbox.pack(pady=5)
        self.tables_listbox.bind("<<ListboxSelect>>", self.show_table_data)
        
        # 新建表部分
        self.new_table_button = tk.Button(root, text="新建表", command=self.create_table)
        self.new_table_button.pack(pady=5)
        
        # 表数据部分
        self.data_label = tk.Label(root, text="表数据:")
        self.data_label.pack(pady=5)
        
        self.data_tree = ttk.Treeview(root)
        self.data_tree.pack(pady=5, fill=tk.BOTH, expand=True)
        
        # 新建数据部分
        self.new_data_button = tk.Button(root, text="新建数据", command=self.insert_data)
        self.new_data_button.pack(pady=5)
        
        # 断开连接部分
        self.disconnect_button = tk.Button(root, text="断开连接", command=self.disconnect_db)
        self.disconnect_button.pack(pady=5)
        
        self.status_label = tk.Label(root, text="状态: 未连接", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X)
        
        self.conn = None  # 数据库连接对象
        self.last_activity_time = None  # 记录最后一次操作时间
        self.timeout_id = None  # 定时器ID
    
    def connect_db(self):
        """
        连接 SQLite 数据库并加载表列表。
        
        步骤:
        1. 获取用户输入的数据库文件路径
        2. 验证路径是否为空
        3. 尝试连接数据库
        4. 查询所有表名并显示在列表中
        5. 更新状态栏
        """
        db_path = self.db_path_entry.get()
        if not db_path:
            messagebox.showerror("错误", "请输入数据库文件路径")
            return
        
        try:
            self.conn = sqlite3.connect(db_path)
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            self.tables_listbox.delete(0, tk.END)
            for table in tables:
                self.tables_listbox.insert(tk.END, table[0])
            
            self.status_label.config(text=f"状态: 已连接 - {db_path}")
        except Exception as e:
            messagebox.showerror("错误", f"连接数据库失败: {e}")
    
    def create_db(self):
        """
        新建 SQLite 数据库文件。
        
        步骤:
        1. 弹出对话框输入新数据库文件名
        2. 创建数据库文件
        3. 更新状态栏
        """
        db_path = simpledialog.askstring("新建数据库", "请输入数据库文件路径:")
        if not db_path:
            return
        
        try:
            self.conn = sqlite3.connect(db_path)
            self.db_path_entry.delete(0, tk.END)
            self.db_path_entry.insert(0, db_path)
            self.status_label.config(text=f"状态: 已创建 - {db_path}")
            messagebox.showinfo("成功", "数据库文件创建成功！")
        except Exception as e:
            messagebox.showerror("错误", f"创建数据库失败: {e}")
    
    def create_table(self):
        """
        在已连接的数据库中新建表。
        
        步骤:
        1. 弹出对话框输入表名和字段定义
        2. 执行 SQL 创建表
        3. 刷新表列表
        """
        if not self.conn:
            messagebox.showerror("错误", "请先连接数据库")
            return
        
        table_name = simpledialog.askstring("新建表", "请输入表名:")
        if not table_name:
            return
        
        columns = simpledialog.askstring("新建表", "请输入字段定义 (例如: id INTEGER PRIMARY KEY, name TEXT):")
        if not columns:
            return
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"CREATE TABLE {table_name} ({columns});")
            self.conn.commit()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            self.tables_listbox.delete(0, tk.END)
            for table in tables:
                self.tables_listbox.insert(tk.END, table[0])
            
            messagebox.showinfo("成功", "表创建成功！")
        except Exception as e:
            messagebox.showerror("错误", f"创建表失败: {e}")
    
    def insert_data(self):
        """
        向已选中的表中插入新数据。
        
        步骤:
        1. 获取选中的表名
        2. 弹出对话框输入数据
        3. 执行 SQL 插入数据
        4. 刷新表数据
        """
        if not self.conn:
            messagebox.showerror("错误", "请先连接数据库")
            return
        
        selected_table = self.tables_listbox.get(self.tables_listbox.curselection())
        if not selected_table:
            messagebox.showerror("错误", "请先选择表")
            return
        
        data = simpledialog.askstring("新建数据", "请输入数据 (例如: 1, 'John'):")
        if not data:
            return
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"INSERT INTO {selected_table} VALUES ({data});")
            self.conn.commit()
            self.show_table_data(None)
            messagebox.showinfo("成功", "数据插入成功！")
        except Exception as e:
            messagebox.showerror("错误", f"插入数据失败: {e}")
    
    def show_table_data(self, event):
        """
        显示选中表的数据。
        
        步骤:
        1. 获取用户选中的表名
        2. 查询表数据
        3. 清空 Treeview 并设置列名
        4. 填充数据到 Treeview
        """
        selected_table = self.tables_listbox.get(self.tables_listbox.curselection())
        if not selected_table:
            return
        
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {selected_table};")
        data = cursor.fetchall()
        
        # 清空 Treeview
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        
        # 设置列名
        columns = [description[0] for description in cursor.description]
        self.data_tree["columns"] = columns
        self.data_tree["show"] = "headings"
        
        for col in columns:
            self.data_tree.heading(col, text=col)
            self.data_tree.column(col, width=100)
        
        # 填充数据
        for row in data:
            self.data_tree.insert("", tk.END, values=row)
        
        # 更新最后一次操作时间
        self.reset_timeout()
    
    def disconnect_db(self):
        """
        手动断开数据库连接。
        
        步骤:
        1. 关闭数据库连接
        2. 清空表列表和数据
        3. 清空列头名称
        4. 更新状态栏
        """
        if self.conn:
            self.conn.close()
            self.conn = None
            self.tables_listbox.delete(0, tk.END)
            for item in self.data_tree.get_children():
                self.data_tree.delete(item)
            self.data_tree["columns"] = ()
            self.data_tree["show"] = ""
            self.status_label.config(text="状态: 未连接")
            messagebox.showinfo("成功", "数据库已断开连接")
        else:
            messagebox.showerror("错误", "当前未连接数据库")
    
    def reset_timeout(self):
        """
        重置超时定时器。
        
        步骤:
        1. 取消之前的定时器（如果存在）
        2. 设置新的定时器，5分钟后自动断开连接
        """
        if self.timeout_id:
            self.root.after_cancel(self.timeout_id)
        self.timeout_id = self.root.after(300000, self.disconnect_db)  # 5分钟 = 300000毫秒

if __name__ == "__main__":
    """
    主入口函数，启动 SQLite 数据库查看器。
    
    步骤:
    1. 创建 tkinter 根窗口
    2. 初始化 SQLiteViewer 实例
    3. 启动主事件循环
    """
    root = tk.Tk()
    app = SQLiteViewer(root)
    root.mainloop()