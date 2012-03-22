#!/usr/bin/env Rscript
library(ggplot2)
library(reshape2)
library(plyr)

d <- melt(read.csv("out.csv"), id=c("method", "h", "t"))

hs <- c("1/1000", "1/100", "1/10")
vars <- c("y1", "y2", "y3")

p <- ggplot(subset(d, method=="2" & h %in% hs & variable %in% vars),
            aes(x=t, y=value, linetype=h, color=variable)) +
	geom_line() + scale_linetype_manual(values=c(2, 1, 3)) +
	ylim(-0.35, 0.65) + xlim(0, 1) +
	theme_bw() + ylab("y") + opts(title="Computed Solutions for Various Mesh Sizes")

ggsave("plot.pdf", width=7, height=5, p)
