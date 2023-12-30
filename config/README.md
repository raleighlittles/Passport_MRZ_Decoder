To get the optical character recognition to work, I had to use a special trained dataset provided 
[here](https://github.com/Shreeshrii/tessdata_ocrb/blob/master/ocrb.traineddata) using [this](https://github.com/Shreeshrii/tessdata_ocrb/commit/9135a9e9db502db1b3e983da39bc21ba83bbab47) commit.

I didn't know how to specify this in the arguments to pytesseract so as a workaround, 
I downloaded the `ocrb.traineddata` file, renamed it to `eng.traineddata` ('eng' for English)

and then placed it here; passing the "config-directory" variable to tesseract tells it to look 
for a training data file matching the given language.