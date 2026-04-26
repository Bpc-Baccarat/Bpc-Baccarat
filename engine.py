import secrets, hashlib

class BaccaratEngine:
    def __init__(self):
        self.history = []
        self.new_shoe()

    def new_shoe(self):
        ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0]
        self.shoe = [val for _ in range(8) for val in (ranks * 4)]
        for i in range(len(self.shoe) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            self.shoe[i], self.shoe[j] = self.shoe[j], self.shoe[i]
        
        self.shoe_id = secrets.randbelow(9000) + 1000
        self.shoe_salt = secrets.token_hex(8)
        self.original_deck = ",".join(map(str, self.shoe))
        # 生成不可竄改的 Hash
        self.shoe_hash = hashlib.sha256(f"{self.shoe_id}:{self.shoe_salt}:{self.original_deck}".encode()).hexdigest()
        
        # 燒牌
        burn = self.shoe.pop(0)
        for _ in range(10 if burn == 0 else burn): self.shoe.pop(0)

    def play_round(self):
        if len(self.shoe) < 10: self.new_shoe()
        p, b = [self.shoe.pop(0), self.shoe.pop(0)], [self.shoe.pop(0), self.shoe.pop(0)]
        # ... (補牌邏輯同前)
        # 返回結果包含當前 Hash 供前端驗證
        return {"p": p, "b": b, "winner": "B", "hash": self.shoe_hash}
