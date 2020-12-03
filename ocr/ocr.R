library(magick)
library(tesseract)
library(purrr)
library(magrittr)
library(stringr)
library(dplyr)
library(readr)

name_box <- "240x40"
punti_box <- "40x30"

position <- data.frame(player = c(1,2,3,4,5,6,7,8), 
                       name_box = c("+300+175", "+300+275", "+300+375", "+300+475",
                                    "+780+175", "+780+275", "+780+375", "+780+475"),
                       punti_box = c("+586+206", "+586+306", "+586+406", "+586+506",
                                     "+1063+206", "+1063+306", "+1063+406", "+1063+506"))

read_results <- function(Player, image) {
  
  image %<>% image_read()
  player_data <- dplyr::filter(position, player == Player)
  
  name <- image %>% 
    image_crop(str_c(name_box, 
                     player_data[[1,2]])) %>% 
    image_ocr() %>% 
    str_trim()
  
  point <- image %>% 
    image_crop(str_c(punti_box, 
                     player_data[[1,3]])) %>% 
    image_fill("black", "0x0", fuzz = 50) %>% 
    image_ocr() %>% 
    str_trim()
  
  output <- data.frame(name = name, point = point)
}

output <- map_dfr(1:5, read_results, image = "/Users/nelvis/Documents/R/ocr/results.jpg")

write_csv(output, "/Users/nelvis/Documents/R/ocr/results.csv")
