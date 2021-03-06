This command-line program automates the process of organizing and synthesizing a large volume of data (i.e., thousands of .DAT files) into meaningful graphs — work that was previously done manually and tediously.

It was intended for use only by **Kumho Eng, Inc.**, and thus was written in a way that is catered to the use of their associates and the developer.

# Usage
TODO

## To-dos
- [x] Prompt user for configuration
- [ ] Convert relevant DAT to CSV
- [ ] Calculate averages of each CSV
- [ ] Graph out averages (x-axis: day/month, y-axis: value)

---

## History

This endeavor began in 2019 as a project not only to eliminate the tedium of my partner's job, but also to satisfy the final project requirement of CS50x and thus cement my growth as a budding software engineer.

In its previous "production" state, the program worked as expected on the small sample set I used to test during development, but undesirably froze up when run on the thousands of files it was intended to process. Feeling as though I needed to step back and re-evaluate my design, I put the project on hold, but I didn't anticipate that the hiatus would be two years long.

While I was gone, my partner coded his own version, [the repo for which can be found on his GitHub](https://github.com/alpacapetter/kumho-compiler).

The redux that now lives in this repo serves as a final project submission for CS50x 2021 and as a personal reminder to commit to finish the things I start.