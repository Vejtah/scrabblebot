# Scrabble-Bot #

Welcome to my project of creating a bot that will be your opponent in the game of Scrabble.
---

### Build Your Own

In case you would like to build your own SB (*Scrabble-Bot*), you can find the source code under `/code/main`. 
You will need:

- 3D printer
- Raspberry pi 4 model B *(Other models will probably work as well, but you I haven't checked)*
- adafruit DC+Stepper Motor hat, *(to control the 2 stepper motors)*
- PCA9685 Servo Driver hat
- *...*
- patience
- time

I will add the 3D models to `/3Dmodels` eventually, once I get them to a usable state.

**Don't be afraid to reach out.**

---

### Virtual SB

You can use the virtual version of SB located under `code/virtual/v_scrabble.py`.

---
## how does it work?
### Play

The playing sequence of SB:

1. Place your move and press a continue button  
2. Get the image from the camera on top  
3. Use AI to transform this image into letters  
4. Use my dictionary and scoring algorithm to find the best move  
5. Move selected tiles with the physical hand to build the word  
