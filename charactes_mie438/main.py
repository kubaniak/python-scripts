import tkinter as tk

class CharGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("SSD1306 Character Generator")
        
        self.cols = 8
        self.rows = 16
        self.pixel_size = 30
        
        self.pixels = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.rects = []
        
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(padx=20, pady=20)
        
        self.canvas = tk.Canvas(self.canvas_frame, 
                                width=self.cols * self.pixel_size, 
                                height=self.rows * self.pixel_size, 
                                bg="white")
        self.canvas.pack()
        
        for r in range(self.rows):
            row_rects = []
            for c in range(self.cols):
                x1 = c * self.pixel_size
                y1 = r * self.pixel_size
                x2 = x1 + self.pixel_size
                y2 = y1 + self.pixel_size
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="gray")
                row_rects.append(rect)
            self.rects.append(row_rects)
            
        # Left click / drag to draw (black)
        self.canvas.bind("<B1-Motion>", lambda event: self.set_pixel(event, 1))
        self.canvas.bind("<Button-1>", lambda event: self.set_pixel(event, 1))
        
        # Right click / drag to erase (white)
        self.canvas.bind("<B3-Motion>", lambda event: self.set_pixel(event, 0))
        self.canvas.bind("<Button-3>", lambda event: self.set_pixel(event, 0))
            
        self.clear_btn = tk.Button(root, text="Clear", command=self.clear)
        self.clear_btn.pack(pady=5)

        self.output_top = tk.Text(root, height=3, width=90)
        self.output_top.pack(pady=5, padx=10)
        
        self.output_bot = tk.Text(root, height=3, width=90)
        self.output_bot.pack(pady=5, padx=10)
        
        self.update_output()
        
    def set_pixel(self, event, val):
        c = event.x // self.pixel_size
        r = event.y // self.pixel_size
        
        if 0 <= c < self.cols and 0 <= r < self.rows:
            if self.pixels[r][c] != val:
                self.pixels[r][c] = val
                color = "black" if val else "white"
                self.canvas.itemconfig(self.rects[r][c], fill=color)
                self.update_output()
        
    def clear(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.pixels[r][c] = 0
                self.canvas.itemconfig(self.rects[r][c], fill="white")
        self.update_output()

    def update_output(self):
        top_bytes = []
        bot_bytes = []
        
        for c in range(self.cols):
            top_byte = 0
            bot_byte = 0
            # For SSD1306, LSB is generally the top pixel in a vertical 8-pixel column
            for r in range(8):
                if self.pixels[r][c]:
                    top_byte |= (1 << r)
            for r in range(8, 16):
                if self.pixels[r][c]:
                    bot_byte |= (1 << (r - 8))
            
            # Format as binary strings matching the C array syntax
            top_bytes.append(f"0b{top_byte:08b}")
            bot_bytes.append(f"0b{bot_byte:08b}")
            
        self.output_top.delete(1.0, tk.END)
        self.output_top.insert(tk.END, "top array row:\n{" + ",".join(top_bytes) + "}\n")
        
        self.output_bot.delete(1.0, tk.END)
        self.output_bot.insert(tk.END, "bottom array row:\n{" + ",".join(bot_bytes) + "}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = CharGenerator(root)
    root.mainloop()
