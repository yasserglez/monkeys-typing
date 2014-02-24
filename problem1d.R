library("lattice")

data <- read.csv("problem1d.csv", header = FALSE,
                 col.names = c("order", "rate", "word_yield"))
data["word_yield"] <- 100 * data["word_yield"]

trellis.device(device = pdf, color = FALSE, file = "problem1d.pdf")
xyplot(word_yield ~ rate, data = data, groups = order,
       type = "b", pch = c(1, 2, 3),
       xlab = "Resolution Rate", ylab = "Word Yield (%)",
       key = list(columns = 3, points = list(pch = c(1, 2, 3)),
                  lines = list(lty = c(1, 2, 3)),
                  text = list(lab = c("1st order", "2nd order", "3rd order"))))
dev.off()
