# Kumho Compiler
#### Video Demo: [https://youtu.be/E5cMcW69Uc0](https://youtu.be/E5cMcW69Uc0)
#### Description:

*I'm not sure where that crazy indentation came from once the conversion finished.* ¯\\_(ツ)_/¯

This command-line program automates the process of organizing and synthesizing a large volume of data (i.e., thousands of .DAT files) into meaningful graphs — work that was previously done manually and tediously.

It was intended for use only by **Kumho Eng, Inc.**, and thus was written in a way that was catered to the use of their associates and the developer.

## Usage
### Install dependencies
Before running the script, you need to have its dependencies (namely `matplotlib`) installed locally (and preferably in a virtual environment).

From within the same directory containing `requirements.txt` run :
```
pip install -r requirements.txt
```

Alternatively, [follow matplotlib's installation instructions](https://matplotlib.org/stable/users/installing.html).

### Running the script
1. Ensure `FTViewFileViewer.exe` is in the directory containing all other data directories.
2. Place the `kumhocompiler` directory inside the same directory.
3. Run `python kumhocompiler` from within that directory and follow the on-screen prompts.

## History

This endeavor began in 2019 as a project not only to eliminate the tedium of my partner's job, but also to satisfy the final project requirement of [CS50x](https://cs50.harvard.edu/x/) and thus cement my growth as a budding software engineer.

In its previous "production" state, the program worked as expected on the small sample set I used to test during development, but undesirably froze up when run on the thousands of files it was intended to process. Feeling as though I needed to step back and re-evaluate my design, I put the project on hold, but I didn't anticipate that the hiatus would be two years long.

While I was gone, my partner coded his own version, [the repo for which can be found on his GitHub](https://github.com/alpacapetter/kumho-compiler).

The redux that now lives in this repo serves as a final project submission for CS50x 2021 and as a personal reminder to commit to finish the things I start.

### To-dos
- [x] Prompt user for configuration
- [x] Convert relevant DAT to CSV
- [x] Calculate averages of each CSV
- [x] Graph out averages (x-axis: day/month, y-axis: value)
