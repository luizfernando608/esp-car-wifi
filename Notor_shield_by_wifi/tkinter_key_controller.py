################################################################################
## Controle com python foi abandonado visto que o javascript oferece melhores soluções
################################################################################

# #%%
# try:
#     import tkinter as tk
# except ImportError:
#     import Tkinter as tk

# import requests
# from time import sleep

# link = "http://192.168.0.101"

# # def event_handle(event):
# #     # Replace the window's title with event.type: input key
# #     if event.keysym == 'w':
# #         motor = "front_AB"
# #     elif event.keysym == "s":
# #         motor = "back_AB"
# #     elif event.keysym == "a":
# #         motor = "front_A"
# #     elif event.keysym == "d":
# #         motor = "front_B"


# #     try:
# #         requests.get(f"{link}/{motor}")
# #     except:
# #         pass

# #     root.title("{}: {}".format(str(event.type), event.keysym))
# #     print(f"{event.type}, {event.keysym}")

# # def event_commom(event):
# #     try:
# #         requests.get(f"{link}/CLOSE")
# #         requests.get(f"{link}/CLOSE")
# #     except:
#         # pass

# pressedStatus = {"w": False, "s": False, "a": False, "d": False}
# get_string = "/{}{}/{}{}/{}/{}"
# get_comand = {"left_motor":"0",
#               "right_motor":"0",
#               "left_direction":"+",
#               "right_direction":"+",
#               "vertical_angle":"5.0",
#               "horizontal_angle":"5.0"}
# # left_motor = "0"
# # right_motor = "0"
# # left_direction = "+"
# # right_direction = "+"
# # vertical_angle = float(0.5)
# # horizontal_angle = float(0.5)
# def pressed(event):
#     pressedStatus[event.keysym] = True 
#     generate_get_request()

# def released(event):
#     pressedStatus[event.keysym] = False

# def generate_get_request():
#     new_get_string = "/{}{}/{}{}/{}/{}".format(get_comand["left_direction"],get_comand["left_motor"],
#                                     get_comand["right_direction"], get_comand["right_motor"],
#                                     get_comand["vertical_angle"], get_comand["horizontal_angle"])
#     if new_get_string != get_string:
#         try:
#             requests.get(link+get_string)
#         except:
#             pass

                    
# def move():
#     if pressedStatus["w"] == True and pressedStatus["d"] == True:
#         get_comand["left_direction"] = "+"
#         get_comand["right_direction"] = "+"
#         get_comand["left_motor"] = "5"
#         get_comand["right_motor"] = "2"
    
#     elif pressedStatus["w"] == True and pressedStatus["a"] == True:
#         get_comand["left_direction"] = "+"
#         get_comand["right_direction"] = "+"
#         get_comand["left_motor"] = "2"
#         get_comand["right_motor"] = "5"

#     root.after(1000, move)

# def send_request():
#     print(get_string)
#     # try:
#     #     requests.get(get_string)
#     #     requests.get(get_string)
#     # except:
#     #     pass
#     root.after(80, send_request)
# #%%
# if __name__ == '__main__':
#     root = tk.Tk()
    
#     for char in ["w", "s", "a", "d"]:
#         root.bind(f"<KeyPress-{char}>", pressed)
#         root.bind(f"<KeyRelease-{char}>" , released)
#     # event_sequence = '<KeyPress>'
#     # root.bind(event_sequence, event_handle)
#     # root.bind('<KeyRelease>', event_commom)
#     # root.attributes("-fullscreen", True)
#     move()
#     # send_request()
#     root.mainloop()

# #%%
