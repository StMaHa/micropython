# Aufgaben## +++ 1) +++# Messen mit einem Ultraschallentfernungssensor (HC-SR04).#   Hilfe? Suchen im Internet: HC-RS04 gpiozero# +++ 2) +++# Ansteuerung einer LED mit Taster. (LED leuchtet -> Robo faehrt, LED blinkt -> Robo im Stand-By)#   Hilfe? Suchen im Internet: LED gpiozero, BUTTON gpiozero# +++ 3) +++# Ansteuerung der Motoren#   Hilfe? Suchen im Internet: MOTOR gpiozero# +++ 4) +++# Ansteuerung der Motoren in Abhaengigkeit der Entfernung# Bibliotheken und Klassenfrom machine import Pin, Timerfrom time import sleepfrom random import choicefrom hcsr04 import HCSR04from motor import Motor# Globale Variablenspeed_m1 = 0.5speed_m2 = 0.5# GPIOs zur Ansteuerung der Motorenpin_m1a = 23  # motor 1pin_m1b = 19  # motor 1pin_m2a = 26  # motor 2pin_m2b = 18  # motor 2# GPIOs des Abstanzsensorspin_trigger = 21pin_echo = 22# GPIOs des Robo Statuspin_led = 16pin_button = 17# Programmsteuerungrun_status = Falsebutton_busy = False# Erzeugen einer Instanz der LED-Klasse, zuweisen der Pin-Factory# +++ 2) +++led = Pin(pin_led, Pin.OUT)# Erzeugen einer Instanz der Button-Klasse# aktivieren des Pull-up Widerstands, definieren des Haltezeit und zuweisen der Pin-Factory# +++ 2) +++button = Pin(pin_button, Pin.IN, Pin.PULL_UP)# Timer objectrelease_timer = Timer(1)# Timer-Callback-Funktion zum entprellen des Tasters# Taster wird freigegebendef release_button(timer):    global button_busy    print("Button released.")    button_busy = False# Callback-Funktion zum aendern des Roboterstatus (start/stop)# Ausgeloest durch einen einfachen Tastendruckdef button_pressed(button):    global button_busy    global run_status    global release_timer    # Wegen dem Prellen des Tastern, muss ein wiederholtes Ausführen verhindert werden.    if not button_busy:        print("Button pressed.")        # Taster gedrueckt merken        button_busy = True        # Robo start/stop        run_status = not run_status        # nach 300 ms Taster wieder freigeben        release_timer.init(period=300, mode=Timer.ONE_SHOT, callback=release_button)  # Hier bgeinnt das Hauptprogrammif __name__ == '__main__':    # Erzeugen einer Instanz der Motor-Klasse    # aktivieren von PWM and zuweisen der Pin-Factory    # +++ 3) +++    motor1 = Motor(pin_m1a, pin_m1b, pwm=True)    motor2 = Motor(pin_m2a, pin_m2b, pwm=True)    # Erzeugen einer Instanz der Distanzsensor-Klasse    # +++ 1) +++    sensor = HCSR04(trigger_pin=pin_trigger, echo_pin=pin_echo, echo_timeout_us=10000)    # Der Button-Instanz die Callback-Funktion fuer Tastendruck zuweisen    # +++ 2) +++    button.irq(trigger=Pin.IRQ_FALLING, handler=button_pressed)    # Try-Catch-Block    try:        # Schleife so lange durchlaufen bis das Programm beendet wird (langer Tastendruck)        while True:            # Schreibe Sensormesswert (cm) auf die Konsole (kann spaeter wieder auskommentiert werden)            # +++ 1) +++            #print(sensor.distance_cm())            # Wie ist der Programmstatus? Wecchseln durch Tastendruck            if run_status:                # wenn Robo faehrt                # LED dauerhaft einschalten                # +++ 2) +++                led.on()                # Ist der Sensormesswert (cm) kleiner 40 cm?                # +++ 4) +++                # messe Entfernung                if sensor.distance_cm() < 40:                    # alle Motoren stop                    # +++ 4) +++                    motor1.stop()                    motor2.stop()                    # eine 1/2 Sekunde warten                    sleep(0.5)                    # Waehle zufaellig eine Drehrichtung                    if choice([0, 1]):   # +++ 4) +++ einkommentieren                        # Robo dreht mit 1/2 Leistung in die eine Richtung                        # +++ 4) +++                        motor1.forward(speed_m1)                        motor2.backward(speed_m2)                    else:   # +++ 4) +++ einkommentieren                        # Robo dreht mit 1/2 Leistung in die andere Richtung                        # +++ 4) +++                        motor1.backward(speed_m1)                        motor2.forward(speed_m2)                    # Lass den Robo eine 1/2 Sekunde drehen                    sleep(0.5)                    # alle Motoren stop                    # +++ 4) +++                    motor1.stop()                    motor2.stop()                    # eine 1/2 Sekunde warten                    sleep(0.5)                else:   # +++ 3) +++ einkommentieren                    # fahre Robo mit 1/2 Leistung vorwaerts                    # +++ 3) +++                    motor1.forward(speed_m1)                    motor2.forward(speed_m2)            else:                # wenn Robo haelt                # alle Motoren stop                # +++ 3) +++                motor1.stop()                motor2.stop()                # LED wechselt bei jedem Schleifen druchlauf den Zustand, sie blinkt                # LED wechselt ihren Zustand                # +++ 2) +++                if(led.value() == 0):                    led.on()                else:                    led.off()                # eine 1/2 Sekunde warten                sleep(0.5)    # Fangen eines Fehlers/Signals    except KeyboardInterrupt:        print("Programm abgebrochen.")    # Dieser Block wird immer ausgefuehrt: zum Schluss muss man aufraeumen    finally:        # LED aus        led.off()        # Motoren aus        motor1.stop()        motor2.stop()        print("Programm beendet.")