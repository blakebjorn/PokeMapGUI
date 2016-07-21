# PokeMapGUI
PySide GUI wrapper for https://github.com/AHAAAAAAA/PokemonGo-Map

Dependencies: PySide (pip install pyside)

###Usage:

  1. Copy source from https://github.com/AHAAAAAAA/PokemonGo-Map into folder (if you are changing the folder name/script name, specify the new file names in GuiConfig.json)
  2. pip install -r "PokemonGo-Map-develop/Easy Setup/requirements.txt"
  3. Run Main.py - hitting "GO!" will launch the flask server in a subprocess and pop open your web browser
  4. Fields are saved into GuiConfig.json *(name/password is not encrypted)*
  
![ScreenShot](https://github.com/blakebjorn/PokeMapGUI/blob/master/Screenshot.png)


*    WINDOWS INSTALLER: https://mega.nz/#!XcQGxADC!Qdj9JUPyZx1_9mThFDDP5Ay5XnfmWPQRowwq9UQJ8wU
*    bundles all dependencies, including python 2.7.12 distribution (does not install python or add to PATH)
*    if requirements change, they can be updated by running the python .exe and entering the following:
*    import pip
*    pip.main(['install','DEPENDENCYNAME'])

donate: 1NCEiwtzTwAM2jsiWtCeqspE1yvNbgtyAC
