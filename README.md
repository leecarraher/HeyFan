# HeyFan
Control a common RF remote controlled ceiling fan with google home using a raspberry pi and 433mhz modulator

use Goggle Assitant in
ifttt to connect to webhooks.
web hooks app POSTs to the webserver

./ngrok http 80
Web Interface                 http://127.0.0.1:4040
Forwarding                    http://xxxxxx.ngrok.io -> localhost:80
Forwarding                    https://xxxxxx.ngrok.io -> localhost:80



## Reverse Engineer the Remote
Read pin 4 of the DIP on the remote with a scope and got the bits that go to the RF modulator.

signal is 433.92MHZ carrier.
format looks like this:
[Preamble][Message 24 bits]

measure the preamble:
short pulse, then a long pause then a signal
+400us
11000us

the base symbol looks to be 11400/31  = 367.7us

the signal looks closer to 400us and 1000us
[
bit is 1400us
1 = High_1000us + Low_400us
0 = High_400us  + Low_1000us
]

we are probably within error, but could program the true 367.7 just as easily. not sure if gpio is that fast though

low and high are a 1:3 ratio

First signal to decode:
little pulses are 0s, longer pulses are 1s
preamble+0011 1101 1101 0000 1001 0101
... weight is 24? binary golay code?
what is this in hexacode... meh maybe later check this

get this working first then record the other commands. no sense doing this tedious task if the whole thing is worthless.


## BOM
Raspberry Pi 0-W
https://www.amazon.com/433Mhz-Transmitter-Receiver-Link-Arduino/dp/B016V18KZ8/ref=sr_1_6?ie=UTF8&qid=1512621556&sr=8-6&keywords=433mhz
some wire for an antenna quarter wave antenna => (speed of light / 433000000)/4 ~173mm
solder and soldering iron to connect the rf modulator to the power, ground and pin GPIO 21 on the pi.

## Basic startup script
#Start gpio daemon:
sudo pigpoid 
#Start ngrok:
#no reserved dynamic dns routes unless you pay, so write down whatever this thing says
#then you have to update you ifttt webhook bindings to this address. its a pain, but i'm
#cheap, you may not be, so totally support ngrok's business.
./ngrok http 8000
#Start the webserver:
python webserver.py





