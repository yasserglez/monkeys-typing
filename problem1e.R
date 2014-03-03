library("rjson")
library("lattice")


INDEX_MAP <- ' !"#\'(),-.:;?@abcdefghijklmnopqrstuvwxyz'
index2char <- function (i) substr(INDEX_MAP, i, i)
char_labels = strsplit(INDEX_MAP, "")[[1]]
num_chars <- 40


agnes_grey_2nd_order <- fromJSON(file = "agnes_grey_2nd_order.json")
max_2nd_order <- max(unlist(agnes_grey_2nd_order))
data <- matrix(NA, num_chars^2, 3)
n <- 1
for (i in seq(length = num_chars)) {
  for (j in seq(length = num_chars)) {
    ngram <- paste0(sapply(c(i, j), index2char), collapse = "")
    freq <- agnes_grey_2nd_order[[ngram]]
    norm_freq <- ifelse(is.null(freq), 0, freq / max_2nd_order)
    data[n, ] <- c(i, j, norm_freq)
    n <- n + 1
  }
}
data <- as.data.frame(data)
colnames(data) <- c("c1", "c2", "Freq")
data <- as.data.frame.table(xtabs(Freq ~ c1 + c2, data))

trellis.device(device = pdf, color = FALSE, file = "agnes_grey_2nd_order.pdf")
plot <- levelplot(Freq ~ c2 * c1, data,
          xlab = "2nd Character", ylab = "1st Character",
          scales = list(x = list(labels = char_labels),
                        y = list(labels = char_labels)),
          colorkey = list(space = "top"),
          col.regions = gray(seq(from = 95, to = 0) / 100),
          panel = function(...) { 
            panel.levelplot(...) 
            panel.grid(num_chars - 1, num_chars - 1, col.line = "white")
          })
print(plot)
dev.off()



agnes_grey_3rd_order <- fromJSON(file = "agnes_grey_3rd_order.json")
max_3rd_order <- max(unlist(agnes_grey_3rd_order))
data <- matrix(NA, num_chars^3, 4)
n <- 1
first_chars <- c(1, 15, 34)
for (i in first_chars) {
  for (j in seq(length = num_chars)) {
    for (k in seq(length = num_chars)) {
      ngram <- paste0(sapply(c(i, j, k), index2char), collapse = "")
      freq <- agnes_grey_3rd_order[[ngram]]
      norm_freq <- ifelse(is.null(freq), 0, freq / max_3rd_order)
      data[n, ] <- c(i, j, k, norm_freq)
      n <- n + 1
    }
  }
}
data <- as.data.frame(data)
colnames(data) <- c("c1", "c2", "c3", "Freq")
data <- as.data.frame.table(xtabs(Freq ~ c1 + c2 + c3, data))

trellis.device(device = pdf, color = FALSE, width = 2.5 * 7, height = 7,
              file = "agnes_grey_3rd_order.pdf")
plot <- levelplot(Freq ~ c3 * c2 | factor(c1, levels = first_chars, labels = c("space", "a", "t")), data,
          xlab = "3rd Character", ylab = "2nd Character",
          scales = list(x = list(labels = char_labels),
                        y = list(labels = char_labels)),
          colorkey = list(space = "top"),
          col.regions = gray(seq(from = 95, to = 0) / 100),
          panel = function(...) { 
            panel.levelplot(...) 
            panel.grid(num_chars - 1, num_chars - 1, col.line = "white")
          })
print(plot[c(1,2,3)])
dev.off()
