#!/usr/bin/env python
# -*- coding: utf8 -*-
 
import RPi.GPIO as GPIO
import MFRC522
import time

GPIO.cleanup
GPIO.setmode(GPIO.BOARD)
 
def sample_func(sample_var):
    # Beispiel Funktion
    # Skript starten, Daten loggen, etc.
    print("Test Funktion wurde aufgerufen")
 
# ...
 
MIFAREReader = MFRC522.MFRC522()
authcode = [144, 145, 151, 156, 145, 155, 165, 144, 144] # die ersten 9 Ziffern sind der Authentifizierungscode
 
try:
    while True:
        # Scan for cards    
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
 
        # If a card is found
        if status == MIFAREReader.MI_OK:
            # Get the UID of the card
            (status,uid) = MIFAREReader.MFRC522_Anticoll()
      
            try:
               uid
            except NameError:
               print "no uid!"
            else:
               # This is the default key for authentication
               key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
               # Select the scanned tag
               MIFAREReader.MFRC522_SelectTag(uid)
               # Authenticate
               status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
               # Check if authenticated
               if status == MIFAREReader.MI_OK:
                   # Read block 8
                   data = MIFAREReader.MFRC522_Read(8)
                   MIFAREReader.MFRC522_StopCrypto1()
                   print data
                   if data[:9] == authcode:
                       sample_func(data)

                        # Open door/blink led
                       GPIO.setup(40, GPIO.OUT)
                       GPIO.output(40, GPIO.HIGH)
                       time.sleep(0)
                       GPIO.output(40, GPIO.LOW)
                       GPIO.cleanup
                       time.sleep( 0 )
                   #elif ...
 
except KeyboardInterrupt:
    print("Abbruch")
    GPIO.cleanup()

