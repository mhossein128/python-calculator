import tkinter as tk
import math

class Calculator:
    """کلاس اصلی ماشین حساب علمی"""
    
    def __init__(self):
        # ساخت پنجره اصلی
        self.root = tk.Tk()
        self.root.title("ماشین حساب علمی")
        self.root.geometry("420x440")
        self.root.resizable(False, False)
        
        # تنظیم وزن ستون‌ها برای توزیع یکنواخت فضا
        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1, uniform="col")
        
        # متغیر برای نگهداری عبارت
        self.expression = ""
        
        # ساخت صفحه نمایش
        self.display = tk.Entry(
            self.root,
            font=("Arial", 20),
            justify="right",
            bd=10,
            relief="sunken"
        )
        self.display.grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky="ew")
        
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
                font=("Arial", 12),
                width=5,
                height=2,
                bg="#e1bee7",
                command=lambda x=btn: self.apply_scientific(x)
            )
            button.grid(row=1, column=i, padx=1, pady=1, sticky="nsew")
        
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
                font=("Arial", 12),
                width=5,
                height=2,
                bg="#fff9c4",
                command=command
            )
            button.grid(row=2, column=i, padx=1, pady=1, sticky="nsew")

        
        # دکمه‌های اعداد و عملگرها
        buttons = [
            ['7', '8', '9', '/', ''],
            ['4', '5', '6', '*', ''],
            ['1', '2', '3', '-', ''],
            ['0', '.', '=', '+', '']
        ]
        
        for row_index, row in enumerate(buttons):
            for col_index, btn in enumerate(row):
                if btn == '':
                    continue  # رد شدن از ستون خالی
                    
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
                    font=("Arial", 16),
                    width=5,
                    height=2,
                    bg=bg_color,
                    command=command
                )
                button.grid(row=row_index + 3, column=col_index, padx=1, pady=1, sticky="nsew")
    
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
        """محاسبه نتیجه عبارت"""
        try:
            # تبدیل ^ به ** برای توان
            expr = self.expression.replace('^', '**')
            
            # محاسبه نتیجه
            result = eval(expr)
            
            # نمایش نتیجه
            self.expression = str(result)
            self.update_display()
            
        except ZeroDivisionError:
            self.expression = "Error"
            self.update_display()
        except:
            self.expression = "Error"
            self.update_display()
    
    def apply_scientific(self, func_name):
        """اعمال توابع علمی"""
        try:
            # گرفتن عدد فعلی
            value = float(self.expression)
            
            if func_name == 'sin':
                # تبدیل درجه به رادیان و محاسبه سینوس
                result = math.sin(math.radians(value))
            elif func_name == 'cos':
                # تبدیل درجه به رادیان و محاسبه کسینوس
                result = math.cos(math.radians(value))
            elif func_name == 'tan':
                # تبدیل درجه به رادیان و محاسبه تانژانت
                result = math.tan(math.radians(value))
            elif func_name == 'sqrt':
                # بررسی عدد منفی
                if value < 0:
                    self.expression = "Error"
                    self.update_display()
                    return
                result = math.sqrt(value)
            elif func_name == 'log':
                # بررسی عدد نامعتبر
                if value <= 0:
                    self.expression = "Error"
                    self.update_display()
                    return
                result = math.log(value)
            
            # نمایش نتیجه
            self.expression = str(result)
            self.update_display()
            
        except:
            self.expression = "Error"
            self.update_display()
    
    def run(self):
        """اجرای برنامه"""
        self.root.mainloop()


# اجرای برنامه
if __name__ == "__main__":
    calc = Calculator()
    calc.run()
