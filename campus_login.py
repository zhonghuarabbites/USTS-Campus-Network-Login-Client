import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import urllib.request
import urllib.parse
import re
import socket

class CampusLoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("校园网登录器")
        self.root.geometry("350x280")
        self.root.resizable(False, False)
        
        self.config_file = "config.json"
        self.load_config()
        
        self.create_widgets()
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(main_frame, text="账号:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username_var = tk.StringVar(value=self.config.get("username", ""))
        self.username_entry = ttk.Entry(main_frame, textvariable=self.username_var, width=30)
        self.username_entry.grid(row=0, column=1, pady=5, padx=(5, 0))
        
        ttk.Label(main_frame, text="密码:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.password_var = tk.StringVar(value=self.config.get("password", ""))
        self.password_entry = ttk.Entry(main_frame, textvariable=self.password_var, show="*", width=30)
        self.password_entry.grid(row=1, column=1, pady=5, padx=(5, 0))
        
        ttk.Label(main_frame, text="运营商:").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.carriers = {
            "校园用户": "@xyw",
            "校园电信": "@dx",
            "校园联通": "@lt",
            "校园移动": ""
        }
        
        carrier_names = list(self.carriers.keys())
        
        saved_carrier_suffix = self.config.get("carrier", "@xyw")
        saved_carrier_name = "校园用户"
        for name, suffix in self.carriers.items():
            if suffix == saved_carrier_suffix:
                saved_carrier_name = name
                break
        
        self.carrier_var = tk.StringVar(value=saved_carrier_name)
        self.carrier_combo = ttk.Combobox(
            main_frame, 
            textvariable=self.carrier_var, 
            values=carrier_names, 
            state="readonly", 
            width=28
        )
        self.carrier_combo.grid(row=2, column=1, pady=5, padx=(5, 0))
        
        self.remember_var = tk.BooleanVar(value=self.config.get("remember", True))
        ttk.Checkbutton(main_frame, text="记住密码", variable=self.remember_var).grid(
            row=3, column=0, columnspan=2, sticky=tk.W, pady=10)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        self.login_btn = ttk.Button(button_frame, text="登录", command=self.login, width=10)
        self.login_btn.grid(row=0, column=0, padx=10)
        
        self.logout_btn = ttk.Button(button_frame, text="注销", command=self.logout, width=10)
        self.logout_btn.grid(row=0, column=1, padx=10)
        
        self.status_label = ttk.Label(main_frame, text="", foreground="gray")
        self.status_label.grid(row=5, column=0, columnspan=2, pady=5)
        
    def load_config(self):
        self.config = {}
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
            except:
                self.config = {}
    
    def save_config(self):
        carrier_name = self.carrier_var.get()
        carrier_suffix = self.carriers.get(carrier_name, "@xyw")
        
        if self.remember_var.get():
            config = {
                "username": self.username_var.get(),
                "password": self.password_var.get(),
                "carrier": carrier_suffix,
                "remember": True
            }
        else:
            config = {"remember": False}
        
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    
    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("10.160.63.9", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "10.160.2.43"
    
    def check_online_status(self):
        try:
            url = "http://10.160.63.9/drcom/chkstatus?callback=dr1234&jsVersion=3.0&_=1234567890"
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            
            with urllib.request.urlopen(req, timeout=5) as response:
                result = response.read().decode("utf-8", errors="ignore")
                if '"result":1' in result or '"result": 1' in result:
                    return True
                return False
        except:
            return False
    
    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        carrier_name = self.carrier_var.get()
        carrier = self.carriers.get(carrier_name, "@xyw")
        
        if not username or not password:
            messagebox.showwarning("提示", "请输入账号和密码")
            return
        
        self.save_config()
        self.login_btn.config(state="disabled")
        self.status_label.config(text="正在登录...", foreground="blue")
        self.root.update()
        
        full_username = username + carrier
        user_ip = self.get_local_ip()
        
        # 使用端口801进行登录
        url = "http://10.160.63.9:801/eportal/?c=ACSetting&a=Login"
        
        params = {
            "DDDDD": ",1," + full_username,
            "upass": password,
            "0MKKey": "Login",
            "buttonClicked": "",
            "redirect_url": "",
            "err_flag": "",
            "username_suffix": "",
            "user": username,
            "password": password,
            "user_type": "1",
            "loginurl": "",
            "radius_nasip": "",
            "radius_nasportid": "",
            "acession_mac": "",
            "user_mac": "000000000000",
            "wlan_user_ip": user_ip,
            "wlan_user_mac": "000000000000",
            "vlanid": "0",
            "nasportid": ""
        }
        
        data = urllib.parse.urlencode(params).encode("utf-8")
        
        try:
            req = urllib.request.Request(url, data=data, method="POST")
            req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            req.add_header("Content-Type", "application/x-www-form-urlencoded")
            req.add_header("Referer", "http://10.160.63.9/a79.htm?wlanuserip=" + user_ip)
            
            with urllib.request.urlopen(req, timeout=15) as response:
                result = response.read().decode("utf-8", errors="ignore")
                
                if "login_ok" in result.lower() or "Dr.COMWebLoginID_3.htm" in result:
                    self.status_label.config(text="登录成功", foreground="green")
                    messagebox.showinfo("成功", "登录成功！")
                else:
                    error_msg = self.parse_login_result(result)
                    self.status_label.config(text="登录失败", foreground="red")
                    messagebox.showerror("登录失败", error_msg)
        except urllib.error.URLError:
            self.status_label.config(text="网络错误", foreground="red")
            messagebox.showerror("网络错误", "无法连接到认证服务器\n请检查网络连接")
        except Exception as e:
            self.status_label.config(text="连接失败", foreground="red")
            messagebox.showerror("错误", f"连接失败: {str(e)}")
        finally:
            self.login_btn.config(state="normal")
    
    def parse_login_result(self, html):
        if not html:
            return "服务器返回空响应"
        
        html_lower = html.lower()
        
        if "Dr.COMWebLoginID_2.htm" in html:
            return "认证失败，请检查账号密码是否正确"
        
        error_patterns = [
            (r"password\s*error", "密码错误"),
            (r"userid\s*error", "账号不存在"),
            (r"account\s*not\s*exist", "账号不存在"),
            (r"account\s*disabled", "账号已停用"),
            (r"account\s*expired", "账号已过期"),
            (r"balance\s*not\s*enough", "账户余额不足"),
            (r"arrearage", "账户已欠费"),
            (r"max\s*connections", "在线用户数已达上限"),
            (r"already\s*online", "账号已在线"),
            (r"auth\s*fail", "认证失败"),
            (r"error", "账号或密码错误"),
        ]
        
        for pattern, msg in error_patterns:
            if re.search(pattern, html_lower):
                return msg
        
        if len(html) < 300:
            return f"服务器返回: {html}"
        
        return "登录失败，请检查账号密码"
    
    def logout(self):
        self.logout_btn.config(state="disabled")
        self.status_label.config(text="正在注销...", foreground="blue")
        self.root.update()
        
        # 先检查是否在线
        is_online_before = self.check_online_status()
        
        if not is_online_before:
            self.status_label.config(text="当前不在线", foreground="orange")
            messagebox.showinfo("提示", "当前不在线，无需注销")
            self.logout_btn.config(state="normal")
            return
        
        # 使用正确的注销接口和参数
        username = self.username_var.get().strip()
        carrier_name = self.carrier_var.get()
        carrier = self.carriers.get(carrier_name, "@xyw")
        full_username = username + carrier
        user_ip = self.get_local_ip()
        
        url = "http://10.160.63.9/eportal/?c=ACSetting&a=Logout&ver=1.0"
        params = {
            "DDDDD": ",1," + full_username,
            "upass": "",
            "user_ip": user_ip,
            "wlan_user_ip": user_ip
        }
        data = urllib.parse.urlencode(params).encode("utf-8")
        
        try:
            req = urllib.request.Request(url, data=data, method="POST")
            req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            req.add_header("Content-Type", "application/x-www-form-urlencoded")
            
            resp = urllib.request.urlopen(req, timeout=10)
            html = resp.read().decode("gbk", errors="ignore")
            
            # 注销成功后会断网，所以直接判断为成功
            import time
            time.sleep(1)
            
            # 尝试检查在线状态，如果断网说明注销成功
            is_online_after = self.check_online_status()
            
            if not is_online_after:
                self.status_label.config(text="注销成功", foreground="green")
                messagebox.showinfo("成功", "注销成功！")
            elif "Dr.COMWebLoginID_3.htm" in html:
                self.status_label.config(text="注销成功", foreground="green")
                messagebox.showinfo("成功", "注销成功！")
            else:
                self.status_label.config(text="注销失败", foreground="red")
                messagebox.showerror("失败", "注销失败，请稍后重试")
        except urllib.error.URLError:
            # 网络断开说明注销成功
            self.status_label.config(text="注销成功", foreground="green")
            messagebox.showinfo("成功", "注销成功！")
        except Exception as e:
            self.status_label.config(text="连接失败", foreground="red")
            messagebox.showerror("错误", f"连接失败: {str(e)}")
        finally:
            self.logout_btn.config(state="normal")

def main():
    root = tk.Tk()
    app = CampusLoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
