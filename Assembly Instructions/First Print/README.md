# First Print

## Load your PLA filament

Manually move the bed down so the nozzle is not to close to the bed

![Calibration Picture](./Raw Calibration Pictures/PKC_4.JPG)

Preheat the nozzle by navigating on the LCD controller to prepare, then preheat PLA, then preheat PLA 1. Wait until the nozzle is up to more than 180 degrees C.

![Calibration Picture](./Raw Calibration Pictures/PKC_5.JPG)

Cut off the tip of the filament if needed (if the end of the filament is not clean, is bent, or has a molten blob).  Mount the spool on the spool holder and feed the tip of the filament into the bottom of the extruder.

![Calibration Picture](./Raw Calibration Pictures/PKC_6.JPG)

Holding the filament into the extruder, navigate on the LCD to prepare, and then load filament. The extruder should feed the filament up through the Bowden tube.

![Calibration Picture](./Raw Calibration Pictures/PKC_7.JPG)

Navigate to prepare, then purge 5mm on the LCD. Purge 5mm until the filament is flowing smoothly out of the nozzle. (It doesn’t hurt to purge a little more than you probably need  in order to ensure all the air bubbles in the nozzle have come out)

![Calibration Picture](./Raw Calibration Pictures/PKC_8.JPG)

Navigate to prepare, then cooldown.

![Calibration Picture](./Raw Calibration Pictures/PKC_9.JPG)



## First Print

There is gcode file (no slicer needed) ready to go for a first print. [FirstPrint_3DBenchy.gcode](https://github.com/woolfepr/Printer-Kitten/blob/master/Assembly%20Instructions/First%20Print/FirstPrint_3DBenchy.gcode) Simply put it on the SD card, navigate to print from SD, and select it. Your printer should heat up and successfully print for the first time.

![Calibration Picture](./Raw Calibration Pictures/PKC_10.JPG)

Once the first print is finished and you are ready to print items of your own choice or design you will need to begin using a slicer/ tool pathing program. I recommend using [Cura by Ultimaker](https://ultimaker.com/en/products/cura-software). Download and install the latest version.

The profile I have fine-tuned to run PLA on the kitten is available on Github. [Kitten 1.75.ini](https://github.com/woolfepr/Printer-Kitten/blob/master/Software/Cura%20Profile/Kitten%201.75.ini)  This profile should be a good starting point as far as tuning. You will want to play with the settings in order to get the best results on different models.
