"""
پروژه آزمایشگاه هوش مصنوعی - گام دوم
توسعه‌دهنده : عرفان دهستانی
"""

import numpy as np

class TicTacToeEnv:
    # هشت خط برد (۳ سطر، ۳ ستون، ۲ قطر)
    WIN_LINES = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # سطرها
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # ستون‌ها
        (0, 4, 8), (2, 4, 6)              # قطرها
    ]

    def __init__(self):
        self.board = np.zeros(9, dtype=int)
        self.current_player = 1  # 1 معادل X، و 1- معادل O
        self.done = False
        self.winner = None

    def reset(self):
        """بازنشانی کامل تخته به وضعیت اولیه"""
        self.board = np.zeros(9, dtype=int)
        self.current_player = 1
        self.done = False
        self.winner = None
        return self.board.copy()

    def get_legal_actions(self):
        """استخراج لیست خانه‌های خالی و مجاز برای بازی (۰ تا ۸)"""
        if self.done:
            return []
        return [i for i, val in enumerate(self.board) if val == 0]

    def check_winner(self):
        """بررسی وضعیت برنده یا تساوی در تخته"""
        for x, y, z in self.WIN_LINES:
            if self.board[x] != 0 and self.board[x] == self.board[y] == self.board[z]:
                return self.board[x]  # برنده: 1 یا 1-
        if 0 not in self.board:
            return 0  # تساوی (Draw)
        return None  # بازی هنوز ادامه دارد

    def step(self, action):
       
        if self.done:
            raise ValueError("بازی به پایان رسیده است؛ ابتدا محیط را reset کنید.")
        
        if action < 0 or action > 8 or self.board[action] != 0:
            raise ValueError(f"حرکت غیرمجاز: خانه {action} پر است یا معتبر نیست.")

        # نشستن مهره بازیکن جاری
        self.board[action] = self.current_player
        
        # بررسی وضعیت بازی
        result = self.check_winner()
        if result is not None:
            self.done = True
            self.winner = result
        else:
            # تغییر نوبت
            self.current_player = -self.current_player

        return self.board.copy(), self.winner, self.done, {}

    def render(self):
        """نمایش تمیز تخته در کنسول"""
        symbols = {1: "X", -1: "O", 0: "."}
        grid = [symbols[val] for val in self.board]
        print("\n وضعیت تخته:")
        for r in range(3):
            print(f" {grid[r*3]} | {grid[r*3+1]} | {grid[r*3+2]} ")
            if r < 2:
                print("---+---+---")
        print()