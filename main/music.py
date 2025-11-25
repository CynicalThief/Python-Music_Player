import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame as game


game.init()           
game.mixer.init() 

MUSIC_END = game.USEREVENT + 1
game.mixer.music.set_endevent(MUSIC_END)

paused = False
position = 0
position2 = 0
Loopc = False

def rewind():
     global position2
     position2+=10
     current_songpos = game.mixer.music.get_pos()
     current_pos = current_songpos / 1000.0
     new_pos = current_pos - position2
     return new_pos

while Loopc:
     for event in game.event.get():
          if event.type == MUSIC_END and Loopc:
               game.mixer.music.play(start = 0)
               print("Song looped.")

def forward():
     global position
     position+=10
     current_songpos = game.mixer.music.get_pos()
     current_pos = current_songpos / 1000.0
     new_pos = current_pos + position
     return new_pos

def play_music(folder, song_name):
     file_path = os.path.join(folder, song_name)


     if not os.path.exists(file_path):
          print("File not found")
          return
     game.mixer.music.load(file_path)
     game.mixer.music.play()

     Loop = "Off"
     global Loopc

     print(f"\nNow playing: {song_name}")
     print(f"Commands: [P]ause | [R]esume | [S]top | R[E]wind | [F]orward | [L]00P = {Loop}")
     while True:
          for event in game.event.get():
            if event.type == MUSIC_END and Loopc:
               game.mixer.music.play(start=0)
               print("Song looped!")

          command = input(">> ").upper()

          if command == "P":
               paused = True
               game.mixer.music.pause()
               print("Paused")
          elif command == "R":
               paused = False
               game.mixer.music.unpause()
               print("Resume")
          elif command == "S":
               game.mixer.music.stop()
               return
          elif command == "E":
               if game.mixer.music.get_busy():
                 game.mixer.music.play(start = rewind())
               else:
                    game.mixer.music.play(start = rewind())
                    game.mixer.music.pause() 
               print("Rewind by 10 seconds!")
          elif command == "F":
               if game.mixer.music.get_busy():
                 game.mixer.music.play(start = forward())
               else:
                    game.mixer.music.play(start = forward())
                    game.mixer.music.pause() 
               print("Forwarded by 10 seconds!")
          elif command == "L":
               Loopc = not Loopc
               Loop = "On" if Loopc else "Off"
               print(f"Loop {Loop}")
          else: 
               print("Invalid command!")

               
     


def main():
    global position
    global position2
    global Loopc

    try:
          game.mixer.init()
    except game.error as e:
          print("Audio initialization failed! ", e)
          return
    
    folder = "music_list"

    if not os.path.isdir(folder):
        print(f"Folder '{folder}' not found")
        return
    mp3_files = [file for file in os.listdir(folder) if file.endswith(".mp3")]

    if not mp3_files:
        print("No song founded.")

    
    while True:
        print("***** MP3 PLAYER *****")
        print("My song list: ")  
        
        for index, song in enumerate(mp3_files, start=1):
            print(f"{index}. {song}")
        
        choice_input = input("\nEnter the song # to play (or 'Q' to quit): ")

        if choice_input.upper() == "Q":
             print("Bye!")
             break
        if not choice_input.isdigit():
             print("Enter a valid number!")
             continue
    
             
        choice = int(choice_input) - 1
        
        if 0 <= choice < len(mp3_files):
             play_music(folder, mp3_files[choice])
        else:
             print("Invalid choice!")

        if paused:
          pass
        elif game.mixer.music.get_busy():
             position = 0
             position2 = 0
             play_music(folder, mp3_files[choice-1])
     
          


if __name__ == "__main__":
        main()