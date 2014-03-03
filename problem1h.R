
data <- read.csv("problem1h.csv", header = FALSE)
labels <- c("A Christmas Carol", "A Tale of Two Cities", "Wuthering Heights", 
    "Agnes Grey", "Jane Eyre", "Tarzan of the Apes", "Warlord of Mars",
    "The People that Time Forgot", "The Land that Time Forgot",
    "King Solomon's Mines", "Fanny Hill", "Alice's Adventures in Wonderland",
    "Through the Looking Glass", "Legend of Sleepy Hollow", 
    "The Adventures of Sherlock Holmes", "The Lost World", 
    "The Hound of the Baskervilles", "Tales of Terror and Mystery",
    "Adventures of Huckleberry Finn", "The Adventures of Tom Sawyer",
    "A Connecticut Yankee in King Arthur's Court", "The Prince",
    "War of the Worlds", "The Time Machine", "Metamorphosis",
    "The Trial", "The Jungle Book")

num_books <- 27
dissimilarity <- matrix(0, num_books, num_books)
for (i in seq(length = nrow(data))) {
  dissimilarity[data[i, 1], data[i, 2]] <- data[i, 3]
  dissimilarity[data[i, 2], data[i, 1]] <- data[i, 3]
}

tree <- hclust(as.dist(dissimilarity), method = "complete")

pdf(file = "problem1h.pdf", width = 7, height = 2 * 7)
plot(tree, labels = labels, main = "", sub = "",
     ylab = "CNG Dissimilarity", xlab = "")
dev.off()
