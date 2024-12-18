import tkinter as tk
import random



class Bird:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.gravity = 0.05
        self.current_image = 0 # Tracks the current image
        self.bird_images = []
        self.load_images()
        self.bird = self.canvas.create_image(self.x, self.y, image=self.bird_images[self.current_image])


    def load_images(self):
        try:
            for filename in ["bird_up.png", "bird_down.png"]:
                image = tk.PhotoImage(file=filename)
                self.bird_images.append(image) # Add image to list
        except tk.TclError as e:
           print(f"Error loading image {filename}: {e}") # Important error handling
           exit() # Exit the program if image loading fails.




    def draw(self):
        self.dy += self.gravity
        self.y += self.dy
        self.canvas.move(self.bird, 0, self.dy)


        if self.dy > 0: #Bird is falling
            self.current_image = 1 # Change to down image
        else:
            self.current_image = 0 #Change to up image



        self.canvas.itemconfig(self.bird, image=self.bird_images[self.current_image])



    def jump(self, event):
        self.dy = -2





class Pillar:
    def __init__(self, canvas, x, y, gap_size=100):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = 10
        self.height = 400
        self.color = "brown"
        self.gap_size = gap_size
        self.gap_y = random.randint(0, self.height - self.gap_size)
        self.pillar_top = self.canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.gap_y,
                                                       fill=self.color)
        self.pillar_bottom = self.canvas.create_rectangle(self.x, self.y + self.gap_y + self.gap_size,
                                                          self.x + self.width, self.y + self.height, fill=self.color)
        self.passed = False

    def draw(self):
        self.x -= 2
        self.canvas.move(self.pillar_top, -2, 0)
        self.canvas.move(self.pillar_bottom, -2, 0)

    def is_hit(self, bird):
        return (bird.x > self.x and bird.x < self.x + self.width and
                (bird.y > self.y and bird.y < self.y + self.gap_y or
                 bird.y > self.y + self.gap_y + self.gap_size and bird.y < self.y + self.height))

    def is_passed(self, bird):
        return bird.x > self.x + self.width and not self.passed


class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Flappy Bird")
        self.root.configure(background="lightblue")
        self.canvas_width = 600
        self.canvas_height = 400
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        self.bird = Bird(self.canvas, 50, self.canvas_height // 2)
        self.pillars = []
        self.pillar_interval = 200
        self.last_pillar_x = self.canvas_width
        self.score = 0
        self.score_text = self.canvas.create_text(40, 10, text="Score: 0", font=("Arial", 16))
        self.game_over_text = None
        self.root.bind("<KeyPress>", self.bird.jump)
        self.update()

    def update_score(self):
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

    def show_game_over(self):
        if self.game_over_text is None:
            self.game_over_text = self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2,
                                                          text="Game Over!", font=("Arial", 24), fill="red")
            self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2 + 30,
                                     text=f"Your score: {self.score}", font=("Arial", 16), fill="black")

    def update(self):
        self.bird.draw()
        for pillar in self.pillars:
            pillar.draw()
            if pillar.is_passed(self.bird):
                self.score += 1
                self.update_score()
                pillar.passed = True

            if pillar.is_hit(self.bird):
                self.show_game_over()
                return

        if len(self.pillars) == 0 or self.pillars[-1].x < self.last_pillar_x - self.pillar_interval:
            self.pillars.append(Pillar(self.canvas, self.last_pillar_x, 0))
            self.last_pillar_x += self.pillar_interval

        if self.bird.y < 0 or self.bird.y > self.canvas_height:
            self.show_game_over()
            return

        self.root.after(10, self.update)


class MainMenu:
    def __init__(self, root):
        self.root = root

        # Create the main menu frame
        self.main_menu_frame = tk.Frame(self.root)
        self.main_menu_frame.pack()

        # Create the title label
        self.title_label = tk.Label(self.main_menu_frame, text="Flappy Bird", font=("Arial", 48))
        self.title_label.pack()

        # Create the buttons
        self.play_button = tk.Button(self.main_menu_frame, text="Play", command=self.play_game)
        self.play_button.pack()

        self.leaderboard_button = tk.Button(self.main_menu_frame, text="Leaderboard", command=self.show_leaderboard)
        self.leaderboard_button.pack()

        self.shop_button = tk.Button(self.main_menu_frame, text="Shop", command=self.open_shop)
        self.shop_button.pack()

    def play_game(self):
        # Start the game
        game = Game()
        game.run()  # Start the main game loop

    def show_leaderboard(self):
        # Show the leaderboard
        pass

    def open_shop(self):
        # Open the shop
        pass


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Flappy Bird")
    root.geometry("600x400")

    menu = MainMenu(root)

    root.mainloop()

