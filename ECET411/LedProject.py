import RPi.GPIO as GPIO
from tkinter import *

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

LED = 21
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)

root = Tk()
root.title("LED Project")
root.geometry('600x400')

Count = 0

def greenClick():
    global Count
    Count += 1
    counterReminder = Count % 2
    if counterReminder == 1:
        greenLabel.config(text="Green LED ON", bg="green")
        GPIO.output(LED, GPIO.HIGH)  # Turn on
    else:
        greenLabel.config(text="Green LED OFF", bg="green")
        GPIO.output(LED, GPIO.LOW)  # Turn Off

greenLedButton = Button(root, text="GREEN", command=greenClick, padx=20, pady=10, fg="white", bg="green")
greenLedButton.grid(row=3, column=5)

greenLabel = Label(root, text="Green LED OFF", fg="white", bg="green")
greenLabel.grid(row=7, column=5)

root.columnconfigure(5, weight=1)
root.rowconfigure(7, weight=1)
root.rowconfigure(3, weight=1)

root.mainloop()
