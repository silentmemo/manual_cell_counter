# manual_cell_counter
Development of a manual cell counter that is less noisy and more intelligent. 

## Background and Motivation
__Note : This is a STEM project mostly for entertainment and education.__ 

Counting cell manually using a hemocytometer is a very common task in a cell biology lab. Counting cell on a hemocytometer involve several steps. 

1. prepare (dilute, stain) the biological sample (e.g., suspension of cells / particles)
2. load the sample on a hemocytometer
3. load the hemocytometer on a microscope 
4. count the cells/ particles in fixed volume "squares" on the hemocytometer
5. calculate the concentrations, viability of the original samples

These step when well prepared, usually won't take more than 10 minutes to perform. Sometimes, however, it is desirable to get this step done as quick as possible. When available, using an automatic cell counter makes the most sense. However, not everyone has immediate access to one, or it may require the use of consumables which will racks up operation-cost. 
To assist manual cell counting, typically a tally counter will be used. It makes a clicky sound and tactile feedback when pressed. If the tally counter makes a loud clicky sound, it can be a source of noise when used frequently. Also, counting different squares or live/dead cells or making amendment on hemocytometers requires a reset on the tally counter, which forces user to either remember the tally or spent time marking down the numbers. These features make the cell counting task a lot less enjoyable. 

This project fills in the unique niche, to make manual cell counting a bit more efficient by outsourcing the calculation to an accessible and affordable computer chip, and a bit less annoying by making use of more silent switches and light as the feedback which is non-audible. 

---

## Implementation
The cell counter is built using [Adafruit MacroPad RP2040](https://www.adafruit.com/product/5128). The MacroPad was chosen for the project for several reasons:

- The RP2040 chip is programmable.  
- It contains many keys which is required.
- It contains a display to show the calculation result in real-time. 
- The switches are "hot-swappable", lifting the hurdles of requiring soldering. 
- Different switches can be used to provide tactile feedback. (not used in this project)
- The circuit board contains all the components, making it easy to assemble

The RP2040 is loaded with CircuitPython. A [custom python scripts](/src/code.py) was written to add tallying and calculation functions on the MacroPad.  

---

## Usage
### Operating the MacroPad
#### Tallying
1. Connect the board to power via the USB-c connector on the board. 
2. Verify that the setting is: "LIVE" and "ADD" on the MacroPad's display (white and green LED at the bottom row of keys) 
3. Count living cells on squares, starting from Top-left corner, then repeats to other corners. (TL -> TR -> BL -> BR)
   1. press corresponding switch once, the board will become brighter, a red-light blink on the pressed button
4. To count dead cell, press the switch with white LED light once, the led light should turn blue, and "DEAD" should appear in place of "LIVE". 
5. Count dead cells on squares, starting from Top-left corner, then repeats to other corners. (TL -> TR -> BL -> BR)
   1. press corresponding switch once, the board will become brighter, a red-light blink on the pressed button
#### Adjusting dilution factor 
Turn the rotary switch to adjust the dilution factor of the sample. "DF" will be changed accordingly on the display.
#### Adjusting tally on corner(s) 
If needed to reduce the tally on any corner, press the switch with green LED. It should turn red, and "MINUS" should appear in place of "ADD". Press corresponding switch once to reduce tally at corresponding corner by one. Press the switch with red LED to toggle back to "ADD" state. 
#### Reset the MacroPad
Press the rotary switch once, the MacroPad should beep once, and the display will be reset. __Verify that the setting is: "LIVE" and "ADD" on the MacroPad's display__ before next count. 

### MacroPad Result interpretation

The cell concentration (cell/mL) and viability (%) will be displayed on top with white background. Additionally, 95% confidence interval of the cell concentration of the count will be shown in the bottom of the display (M stand for 1*10^6).   
The tally on each corner will be displayed as {LIVE cell}:{DEAD cell} . 

## Drawbacks / TODOs 
1. The MacroPad is not portable
   1. because it depends on external power source. 
   2. and because the size is big, relative to a tally counter
2. It is not waterproof or ethanol-proof.
   1. It is difficult to sanitize, may be prone to contamination issue  
