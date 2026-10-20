# Logo Creation

I am not sure I can duplicate the gymnastics that went into creating the logo for this project. Here's my best recall.

1. I was interested in using a lower-case letter "j" to reflect a smaller version of the Joplin desktop, which uses an upper case J in its logo, see e.g. the [Joplin landing page](https://joplinapp.org/) and the [logo svg file](https://joplinapp.org/images/logo-text.svg) itself.
2. So I went to [Google Fonts](fonts.google.com) and found something I like, specifically the [Playwrite Argentina](https://fonts.google.com/specimen/Playwrite+AR?preview.text=j&categoryFilters=Calligraphy:%2FScript%2FHandwritten&preview.script=Latn&preview.layout=grid&query=playwrite+argen&specimen.preview.text=j) font, which looks like a cursive lowercase lettering.
3. Google Gemini then gave me the `extract-font.py` script to extract the letter "j" and write out to svg.
4. I first had to download the Playwrite Argentina font package, and provided the `PlaywriteAR-Regular.ttf` file to the script.
5. Side note: The resulting `playwrite-argentina-j.svg` file clipped the upper part of the font. So Gemini modified the `extract-font.py` script to find the "pen bounds" of the object, and adjusted the viewport to so the the full letter would display.
6. I then used Gemini chat to manually add a transform to fit a standard format (0, 0, 512, 512). The resulting file is `gemini-svg.svg`.
7. I next asked Gemini chat to place the geometry in `gemini-svg.svg` onto the blue Joplin background. I downloaded that file and renamed it `mini-joplin.svg`. Whew!
