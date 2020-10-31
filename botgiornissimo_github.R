library(telegram.bot)
library(magrittr)
library(lubridate)

bg_token <- Sys.getenv("BOTGIORNISSIMO_TOKEN")

botgiornissimo <- Bot(token = bg_token)

setwd("~/Documents/R/botgiornissimo")

print(botgiornissimo$getMe())
print(botgiornissimo$getUpdates())

updaterissimo <- Updater(token = bg_token)

# buongiornissimo command

buongiornissimo_df <- data.frame(Chat_id = ...,
                                 Count = 0,
                                 Time = Sys.time())

buongiornissimo <- function(bot, update) {
  
  chat_id <- update$message$chat_id
  
  if(!(chat_id %in% buongiornissimo_df$Chat_id)) {
    buongiornissimo_df <<- buongiornissimo_df %>%
      mutate(Time = as_datetime(Time)) %>% 
      add_row(
        Chat_id = chat_id,
        Count = 0,
        Time = as_datetime(Sys.time())
      )
  }
  
  buongiornissimo_count <- buongiornissimo_df %>% filter(Chat_id == chat_id) %$% Count
  buongiornissimo_time <- buongiornissimo_df %>% filter(Chat_id == chat_id) %$% Time
  
  if (day(as_datetime(buongiornissimo_time)) < day(Sys.time())) {
    buongiornissimo_count <- 0
  }
  
  if (buongiornissimo_count == 0) {
    
    buongiornissimo_df <<- buongiornissimo_df %>%
      mutate(Count = ifelse(Chat_id == chat_id,
                            1,
                            Count),
             Time = ifelse(Chat_id == chat_id,
                           Sys.time(),
                           Time))
    
    image <- switch(weekdays(Sys.time()),
                     Monday = list.files("./buongiornissimo") %>% 
                       str_subset(pattern = "(^LU|^X|^IMG)"),
                     Tuesday = list.files("./buongiornissimo") %>% 
                       str_subset(pattern = "(^MA|^X|^IMG)"),
                     Wednesday = list.files("./buongiornissimo") %>% 
                       str_subset(pattern = "(^ME|^X|^IMG)"),
                     Thursday = list.files("./buongiornissimo") %>% 
                       str_subset(pattern = "(^GI|^X|^IMG)"),
                     Friday = list.files("./buongiornissimo") %>% 
                       str_subset(pattern = "(^VE|^X|^IMG)"),
                     Saturday = list.files("./buongiornissimo") %>% 
                       str_subset(pattern = "(^SA|^X|^IMG)"),
                     Sunday = list.files("./buongiornissimo") %>% 
                       str_subset(pattern = "(^DO|^X|^IMG)"),
                     ) %>% 
      sample(1)
    
    bot$sendPhoto(chat_id = chat_id,
                  photo = str_c("~/Documents/R/botgiornissimo/buongiornissimo/", image),
                  sprintf("Buongiornissimo %s!", update$message$from$first_name))

  } else {
    bot$sendMessage(chat_id = update$message$chat_id,
                    text = sprintf("Torna domani per un nuovo buongiornissimo!"))
  }
  
}

buongiornissimo_handler <- CommandHandler("buongiornissimo", buongiornissimo)

updaterissimo <- Updater(token = bg_token) %>% 
  add(buongiornissimo_handler)

# start command

start <- function(bot, update){
  bot$sendMessage(chat_id = update$message$chat_id,
                  text = sprintf("Hello %s!", update$message$from$first_name))
}

start_handler <- CommandHandler("start", start)

updaterissimo %<>% add(start_handler)

# to start
updaterissimo$start_polling()

#to stop
updaterissimo$stop_polling()













