# Archiving get-sentral

## Why we archived get-sentral
Hi, there!
Recently, a number of factors that get-sentral relies on have released updates which have slowly brought the program to a point where it has stopped working in multiple ways.
In our naivety, we also used frameworks which were not well suited to the purposes we put them to.
These factors include:

- Sentral completely changing the layout of their website
- Pillow introducing a series of high-severity bug patches which require us to update package versions
- Our own failure to write tests
- Tkinter not allowing us to package our app into an installer file

As such, we have decided to archive get-sentral, as it has reached a point where it is beyond repair.

## get-sentral 2
We made get-sentral because it was challenging, fun and useful, and it still is!
We're now building a **second version** of the product, which you can find [here](https://github.com/J-J-B-J/get-sentral-2) (once its published).
The second version of this product is, as of 26 Dec 2023, still in development. We will be working on it throughout the (Australian) school holidays.
We hope to rebuild get-sentral from the ground up to be scalable, testable and intuitive.
Our aim is to eventually get it to the point where we can have a better Sentral which can easily be accessed from any device quickly and easily used.

By the way, we're looking for a better name for the second version of get-sentral. If you have any suggestions, email us at `hibachi.agenda05@icloud.com`!

Thank you for using get-sentral, and we look forward to releasing version 2!

Here's the README:

<h1>get-sentral</h1>
<br>
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.
<h2>A simple Python function to summon your timetable from Sentral.</h2>
<img src="https://github.com/J-J-B-J/get-sentral/raw/main/docs/img/SentralHome.png" alt="Sample Sentral Dashboard" width="100%">
<p>
    get-sentral is a package that allows you to fetch your timetable and other data from Sentral.
    Because it is pure Python, it can be run on microcontrollers running MicroPython or CircuitPython and that have Wi-Fi, including:
</p>
<ul>
    <li>
        Raspberry Pi
        <a class="link" href="https://www.raspberrypi.com/products/raspberry-pi-3-model-a-plus/">A</a>,
        <a class="link" href="https://www.raspberrypi.com/products/raspberry-pi-4-model-b/">B</a>,
        <a class="link" href="https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/">Zero W</a> and
        <a class="link" href="https://www.raspberrypi.com/products/raspberry-pi-pico/">Pico W</a>
    </li>
    <li>
        <a class="link" href="https://docs.arduino.cc/hardware/nano-rp2040-connect?queryID=undefined">Arduino Nano RP2040 Connect</a>
    </li>
    <li>
        Boards using
        <a class="link" href="https://espressif.com/en/products/socs/esp32">ESP32</a> or
        <a class="link" href="https://espressif.com/en/products/socs/esp8266">ESP8266</a>
    </li>
</ul>

<p>
    See our <a href="https://j-j-b-j.github.io/get-sentral/">official documentation</a> or <a href="https://pypi.org/project/SentralTimetable/">PyPi page</a> for more information.
</p>
