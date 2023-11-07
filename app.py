import re
import tkinter as tk

import pythonnet

pythonnet.load("coreclr")

import clr

# Caliculation.dllからCalculationという名前空間を参照に追加
clr.AddReference("Calculation")

import Calculation as calc


# tk.Frameを継承したApplicationクラスを作成
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # ウィンドウの設定
        root.title("電卓アプリ")
        root.geometry("310x500")

        # 変数定義
        self.button_number = [
            ["", "", "C", "B"],
            ["", "(", ")", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["00", "0", ".", "="],
        ]
        self.symbol = ["+", "-", "*", "/"]
        self.calc_str = ""

        # 実行内容
        self.pack()
        self.create_widget()
        self.create_button()

    # create_widgetメソッドを定義
    def create_widget(self):
        # フレーム
        self.calc_frame = tk.Frame(self.master, width=300, height=60)
        self.calc_frame.propagate(False)  # (この設定がTrueだと内側のwidgetに合わせたフレームサイズになる)
        self.calc_frame.pack(side=tk.TOP, padx=10, pady=20)
        self.button_frame = tk.Frame(self.master, width=300, height=360)
        self.button_frame.propagate(False)  # (この設定がTrueだと内側のwidgetに合わせたフレームサイズになる)
        self.button_frame.pack(side=tk.TOP)

        # ディスプレイ用ウィジェット変数の定義
        self.calc_var = tk.StringVar()  # 計算用ディスプレイの表示
        self.ans_var = tk.StringVar()  # 結果用ディスプレイの表示

        # 計算式用ディスプレイ
        self.calc_label = tk.Label(
            self.calc_frame, textvariable=self.calc_var, font=("游ゴシック体", "15", "bold")
        )  # 計算式用のLabel
        self.calc_label.pack(anchor=tk.E)  # 右揃えで配置

        # 結果用ディスプレイ
        self.ans_label = tk.Label(
            self.calc_frame, textvariable=self.ans_var, font=("游ゴシック体", "20", "bold")
        )  # 結果用のLabel
        self.ans_label.pack(anchor=tk.E)  # 右揃えで配置

    # create_buttonメソッドを定義
    def create_button(self):
        for y, row in enumerate(self.button_number):  # button_numberリストの各要素を取得
            for x, num in enumerate(row):  # button_numberリストの各要素内の要素を取得
                button = tk.Button(
                    self.button_frame,
                    text=num,
                    font=("游ゴシック体", "15", "bold"),
                    width=5,
                    height=2,
                )
                button.grid(row=y, column=x)  # 列と行を指定して配置
                button.bind("<Button-1>", self.button_clicked)  # Buttonが左クリックされた場合

    # ボタンが押された時の処理
    def button_clicked(self, event):
        check = event.widget["text"]  # 押されたボタンのテキストを取得

        # クリアの場合OK
        if check == "C":
            self.calc_str = ""
            self.calc_var.set(self.calc_str)  # 計算用ディスプレイの表示を変更
            self.ans_var.set("")  # 結果用ディスプレイの表示を変更

        # バックの場合OK
        elif check == "B":
            self.calc_str = self.calc_str[:-1]  # 最後の１文字以外を代入
            self.calc_var.set(self.calc_str)  # 計算用ディスプレイの表示を変更

        # イコールの場合
        elif check == "=":
            if self.calc_str != "":  # calc_strが空でない場合
                if self.calc_str[-1:] in self.symbol:  # 最期の１文字が記号の場合
                    self.calc_str = self.calc_str[:-1]  # 最後の１文字以外を代入

                try:
                    calculator = calc.Calculator()
                    result = calculator.CalculateInfix(format_expression(self.calc_str))
                    result = int(result) if result % 1 == 0 else result
                    result = "= " + str(result)
                except Exception as e:
                    print(e)
                    if e.args[0] == "Cannot divide by zero.":
                        result = "0で割れません"
                    elif (
                        e.args[0]
                        == "Operand cannot contain more than one decimal point."
                    ):
                        result = "不正な値があります"
                    elif (
                        e.args[0] == "Operand must be a number."
                        or e.args[0] == "Unmatched closing parenthesis detected."
                    ):
                        result = "括弧が閉じていません"
                    elif e.args[0] == "Result is infinity":
                        result = "オーバーフロー"
                    elif e.args[0] == "Invalid expression":
                        result = "不正な入力です"

                # 計算＆出力
                self.calc_var.set(self.calc_str)  # 計算用ディスプレイの表示を変更
                self.ans_var.set(result)  # 結果をans_var変数にセット

        # 記号の場合
        elif check in self.symbol:
            if (
                self.calc_str[-1:] not in self.symbol and self.calc_str != ""
            ):  # 最後の１文字が記号も空でもない場合
                self.calc_str += check  # calc_strに最後の１文字を連結
                self.calc_var.set(self.calc_str)  # 計算用ディスプレイの表示を変更
            elif self.calc_str[-1:] in self.symbol:  # 最後の１文字が記号の場合
                self.calc_str = self.calc_str[:-1] + check  # 最後の１文字を今押した記号に入れ替える
                self.calc_var.set(self.calc_str)  # 計算用ディスプレイの表示を変更

        # その他、数字などの場合
        else:
            self.calc_str += check  # 末尾に最後の文字を連結
            self.calc_var.set(self.calc_str)  # 計算用ディスプレイの表示を変更


def format_expression(expr):
    formatted_expr = re.sub(r"([+\-*/()])", r" \1 ", expr)
    formatted_expr = re.sub(r"\s+", " ", formatted_expr).strip()
    return formatted_expr


# メインの処理
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
