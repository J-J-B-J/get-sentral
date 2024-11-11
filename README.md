# Archiving get-sentral

TL;DR: head to https://github.com/mario872/sentralify

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

A replacement is Mario872's Sentralify, which can be found [here](https://github.com/mario872/sentralify).

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
