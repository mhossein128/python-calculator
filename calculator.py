import tkinter as tk
import numpy as np
from sympy import sympify, N, SympifyError
import re

class Calculator:
    """کلاس اصلی ماشین حساب علمی"""
    
    def __init__(self):
        # ساخت پنجره اصلی
        self.root = tk.Tk()
        self.root.title("ماشین حساب علمی")
        self.root.geometry("480x530")
        self.root.resizable(False, False)
        
        # متغیر برای نگهداری عبارت
        self.expression = ""
        
        # ساخت صفحه نمایش
        self.display = tk.Entry(
            self.root,
            font=("Arial", 24),
            justify="right",
            bd=10,
            relief="sunken"
        )
        self.display.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")
        
        # ساخت دکمه‌ها
        self.create_buttons()
        
    def create_buttons(self):
        """ساخت همه دکمه‌های ماشین حساب"""
        
        # دکمه‌های علمی - ردیف اول
        scientific_buttons = ['sin', 'cos', 'tan', 'log', 'sqrt']
        for i, btn in enumerate(scientific_buttons):
            button = tk.Button(
                self.root,
                text=btn,
                font=("Arial", 14),
                width=6,
                height=2,
                bg="#e1bee7",
                command=lambda x=btn: self.apply_scientific(x)
            )
            button.grid(row=1, column=i, padx=2, pady=2)
        
        # دکمه‌های خاص - ردیف دوم
        special_buttons = ['(', ')', '^', 'π', 'C']
        for i, btn in enumerate(special_buttons):
            if btn == 'C':
                command = self.clear
            elif btn == 'π':
                command = lambda: self.click('3.14159265359')
            else:
                command = lambda x=btn: self.click(x)
            
            button = tk.Button(
                self.root,
                text=btn,
                font=("Arial", 14),
                width=6,
                height=2,
                bg="#fff9c4",
                command=command
            )
            button.grid(row=2, column=i, padx=2, pady=2)

        
        # دکمه‌های اعداد و عملگرها
        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', '=', '+']
        ]
        
        for row_index, row in enumerate(buttons):
            for col_index, btn in enumerate(row):
                if btn == '=':
                    command = self.calculate
                    bg_color = "#a5d6a7"  # سبز برای مساوی
                elif btn in ['+', '-', '*', '/']:
                    command = lambda x=btn: self.click(x)
                    bg_color = "#90caf9"  # آبی برای عملگرها
                else:
                    command = lambda x=btn: self.click(x)
                    bg_color = "#ffffff"  # سفید برای اعداد
                
                button = tk.Button(
                    self.root,
                    text=btn,
                    font=("Arial", 18),
                    width=6,
                    height=2,
                    bg=bg_color,
                    command=command
                )
                button.grid(row=row_index + 3, column=col_index, padx=2, pady=2)
    
    def click(self, value):
        """اضافه کردن مقدار به عبارت"""
        self.expression += str(value)
        self.update_display()
    
    def update_display(self):
        """به‌روزرسانی صفحه نمایش"""
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)
    
    def clear(self):
        """پاک کردن صفحه نمایش"""
        self.expression = ""
        self.update_display()
    
    def calculate(self):
        """محاسبه نتیجه عبارت با استفاده از SymPy"""
        try:
            # تبدیل ^ به ** برای توان
            expr = self.expression.replace('^', '**')
            
            # استفاده از SymPy برای محاسبات نمادین و دقیق‌تر
            # sympify عبارت را به فرم ریاضی تبدیل می‌کند
            result = sympify(expr)
            
            # تبدیل به عدد اعشاری با دقت بالا
            # result = N(result, 12)
            
            # نمایش نتیجه
            self.expression = str(result)
            self.update_display()
            
        except ZeroDivisionError:
            self.expression = "خطا: تقسیم بر صفر"
            self.update_display()
        except SympifyError:
            self.expression = "خطا: عبارت نامعتبر"
            self.update_display()
        except:
            self.expression = "خطا"
            self.update_display()
    
    def apply_scientific(self, func_name):
        """اعمال توابع علمی با استفاده از NumPy برای دقت بالاتر"""
        try:
            # گرفتن عدد فعلی
            value = float(self.expression)
            
            if func_name == 'sin':
                # استفاده از NumPy برای محاسبات دقیق‌تر
                # تبدیل درجه به رادیان و محاسبه سینوس
                result = np.sin(np.radians(value))
            elif func_name == 'cos':
                # تبدیل درجه به رادیان و محاسبه کسینوس
                result = np.cos(np.radians(value))
            elif func_name == 'tan':
                # تبدیل درجه به رادیان و محاسبه تانژانت
                result = np.tan(np.radians(value))
            elif func_name == 'sqrt':
                # NumPy می‌تواند جذر اعداد منفی را هم محاسبه کند (عدد مختلط)
                if value < 0:
                    result = np.sqrt(value + 0j)  # عدد مختلط
                else:
                    result = np.sqrt(value)
            elif func_name == 'log':
                # بررسی عدد نامعتبر
                if value <= 0:
                    self.expression = "خطا: log فقط برای اعداد مثبت"
                    self.update_display()
                    return
                result = np.log(value)  # لگاریتم طبیعی
            
            # نمایش نتیجه با دقت بالا
            # اگر عدد مختلط است، به صورت a+bj نمایش می‌دهد
            if isinstance(result, complex):
                self.expression = f"{result.real:.10f}+{result.imag:.10f}j"
            else:
                self.expression = f"{result:.10f}"
            
            self.update_display()
            
        except ValueError as e:
            self.expression = f"خطا: {str(e)}"
            self.update_display()
        except:
            self.expression = "خطا"
            self.update_display()
    
    def run(self):
        """اجرای برنامه"""
        self.root.mainloop()


# اجرای برنامه
if __name__ == "__main__":
    calc = Calculator()
    calc.run()
