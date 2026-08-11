import turtle
import math

screen = turtle.Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Corazón")

t = turtle.Turtle()
t.hideturtle()
t.speed(0)
t.color("#ffb6c1")
t.pensize(2)

# Dibujar varios corazones escalados (capas)
for scale in range(11, 17):
    t.penup()
    first_point = True
    # recorrer 0..359 grados en pasos de 3° para una curva suave
    for deg in range(0, 360, 3):
        angle = math.radians(deg)
        x = 16 * (math.sin(angle) ** 3) * scale
        y = (13 * math.cos(angle)
             - 5 * math.cos(2 * angle)
             - 2 * math.cos(3 * angle)
             - math.cos(4 * angle)) * scale
        if first_point:
            t.goto(x, y)
            t.pendown()
            first_point = False
        else:
            t.goto(x, y)
    t.penup()

# Escribir el mensaje en el centro
t.goto(0, -30)
t.color("white")
# Fuente: (familia, tamaño, estilo)
t.write("¿QUIERES SER MI NOVIA?", align="center", font=("Arial", 24, "bold"))

t.hideturtle()
turtle.done()
