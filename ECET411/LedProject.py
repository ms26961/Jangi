import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep func�on from the �me module
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
LED = 21
GPIO.setup(LED, GPIO.OUT, inial=GPIO.LOW) # Set pin 21 to be an output pin
from tkinter import * 
root = Tk()
root.title("LED Project")
root.geometry('600x400')
Count = 0
def greenClick(): global Count Count = Count + 1 counterReminder = Count % 2 if counterReminder == 1: greenLabel = Label(root, text = "Green LED ON", fg = "white", bg ="green") greenLabel.grid(row=7, column=5)
 GPIO.output(LED, GPIO.HIGH) # Turn on
 else: greenLabel = Label(root, text = "Green LED OFF", fg = "white", bg ="green") greenLabel.grid(row=7, column=5)
 GPIO.output(LED, GPIO.LOW) # Turn Off
greenLedButton = Button(root, text="GREEN",command=lambda:greenClick(), padx = 10,
pady = 0, fg = "white", bg = "green")
greenLabel = Label(root, text = "Green LED OFF", fg = "white", bg ="green")
root.columnconfigure(5, weight=1)
root.rowconfigure(7, weight = 1)
root.rowconfigure(3, weight = 1)
greenLedButton.grid(row=3, column=5)
greenLabel.grid(row=7, column=5)
root.mainloop()
