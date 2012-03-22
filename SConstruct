env = Environment()

rbuild = Builder(action='R -q --vanilla $SCRIPTOPTS < $SOURCE')
cropbuild = Builder(action='pdfcrop $SOURCE $TARGET')
cropbuild = Builder(action='pdfcrop $SOURCE $TARGET')
env.Append(BUILDERS=dict(R=rbuild, PdfCrop=cropbuild))

env.Command("out.csv", "thing.py", "python2 $SOURCE")

env.R(["plot.pdf", "plot-small.pdf"], ["plot.r", "out.csv"])
env.PdfCrop("plot-crop.pdf", "plot.pdf")
env.PdfCrop("plot-small-crop.pdf", "plot-small.pdf")
env.PDF("presentation.tex")
