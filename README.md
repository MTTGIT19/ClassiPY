# ClassiPY Images
Automatic Image labeler. *Automagically* adds the following to ALL images in a folder. 
- A classification banner.
-  The corresponding classification to the file name.
- A small black border to the image.<br>
- The labeled images are then all dumped into a folder on the desktop. Works on .JPG and .PNG and .JPEG

## :one: Installation
Requirements:  
```
Python3
```
```
pip3 install wand
```
## :two: Directions
#### Required flags:  
` -I  ` = /Path/to/orginal/images/  
` -C ` = CUI or S  
#### Optional flags:  
` -O ` = /NEW_FOLDER <br>  
:bangbang: **BY DEFAULT FILES WILL DUMP INTO THE SAME DIRECTORY AS THE ORIGINALS Unless you speficiy the -O flag. See examples below.**
## :three: Examples
#### CUI banner labels
`./classiPY -I <image directory> -C CUI` 
#### Secret banners
`./classiPY -I <image directory> -C S` 
#### CUI banner with seperate folder
`./classiPY -I <image directory> -C CUI -O CUI_IMAGES`

 ## :three: Whats it look like:   
#### Orginal Images:<br>
<img src="https://github.com/MTTGIT19/ClassiPY/assets/89365060/20ab6abf-ca50-48e2-b0b3-c062b15e36e3" width= "350" height="300">
<img src="https://github.com/MTTGIT19/ClassiPY/assets/89365060/3c1409e0-ce45-4fd6-b47e-1dedf492cece" width= "350" height="300"><br>

#### After classipy:  
<img src="https://github.com/MTTGIT19/ClassiPY/assets/89365060/e16b1464-9404-45da-b19c-6fa72d98a0f5" width= "350" height="300">
<img src="https://github.com/MTTGIT19/ClassiPY/assets/89365060/1cb2f95b-109b-48d9-82d2-e5274ecb7def" width= "350" height="300"><br>   

#### Renaming:<br>  
<img src="https://github.com/MTTGIT19/ClassiPY/assets/89365060/e76df50f-4232-40dc-b0dc-596b15755fe5" width= "500">

## Notes
* *New* - Works for both Windows or Linux. Feedback and suggestions welcome. 
