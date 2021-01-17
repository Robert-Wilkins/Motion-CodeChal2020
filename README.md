# Motion R&D - Coding Challenge 2020
This is Robert Wilkins' Weta Motion R&amp;D Software Developer coding challenge 2020 submission.

This was my first time ever using pyqt or any dedicated UI scripting, so this week has been a very enjoyable, self-driven crash course. I've been relying heavily on https://www.learnpyqt.com/ to get me up and running, so huge credit to Martin Fitzpatrick for the excellent resource. I bought his book and tried my best to learn and do everything from the ground up, but because this was my first experience I ended up having to rely quite heavily on this example: https://www.learnpyqt.com/examples/megasolid-idiom-rich-text-editor/

I tried my best to extend it by reworking and organizing the code, writing some custom widgets to handle the 140 character special case, and polishing off some rough user interaction edges, like being able to type custom font sizes, and emitting the selection changed signal when the arrow keys are presssed. I also added some features like dialogs for unsaved changes, a text colour selection widget, persistant window locations between sessions, a status bar with the character display and a message when you go over the limit, as well as changing up the visual style and tweaking some of the icons. 

All in all, this was a very enlightening experience! Like I said, this was my first time with this kind of coding, and it's a bit of a breath of fresh air! It's so relieving to be working with code that can actually run without errors on the first try! This is as compared to the arcane, C++, algorithm heavy coding I'm used to, where you're really just trying to get it to run at all.

Thanks very much for the experience, and I hope to talk with you soon!

### To Run The Code
Make sure you have Python3 and git installed and then do the following from the command line:
```
$ git clone https://github.com/Robert-Wilkins/Motion-CodeChal2020.git
$ cd Motion-CodeChal2020
$ python3 -m venv venv
```
Then if you're on Mac:
```
$ source venv/bin/activate
```
Or if you're on Windows:
```
"venv/Scripts/activate.bat"
```
Then do:
```
$ pip install -r requirements.txt
$ python MainApplication.py
```

If that isn't working, here's a link to a zip where the virtual environment is already set up:
    https://drive.google.com/drive/folders/1voLpyoCb_VyaWgMxWJg-7ZvrfNc-u4bx?usp=sharing


If that STILL isn't working then please let me know straight away!

### Other licenses

Icons used in the application are by [Yusuke Kamiyaman](http://p.yusukekamiyamane.com/).