import RPi.GPIO as GPIO
import time
import mido

# piny
SWITCH_PINS = [17, 18, 22, 27]

# režimy GPIO pinů
GPIO.setmode(GPIO.BCM)
for pin in SWITCH_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# uložení předchozího stavu přepínačů
previous_states = {pin: None for pin in SWITCH_PINS}

# virtuální MIDI výstupu
output = mido.open_output('Midi Through Port-0')

# nastvení MIDI zprávy a typu zprávy
CONTROL_CHANGE = 0xB0  

try:
    print("Čekání na změny stavu přepínačů...")
    while True:
        for pin in SWITCH_PINS:
            current_state = GPIO.input(pin)
            
            if current_state != previous_states[pin]:
                if current_state == GPIO.HIGH:
                    print(f"Přepínač na pinu {pin} je v poloze ON")
                else:
                    print(f"Přepínač na pinu {pin} je v poloze OFF")
                    
                # Poslání MIDI message s parametrem control
                message = mido.Message('control_change', control=SWITCH_PINS.index(pin) + 1)
                output.send(message)
                    
                previous_states[pin] = current_state
        
        time.sleep(0.1)  # Cooldown

except KeyboardInterrupt: # ctrl + C ukočí program
    GPIO.cleanup()
    print("Program ukončen.")
