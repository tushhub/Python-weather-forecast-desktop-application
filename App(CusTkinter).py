import tkinter as tk
import customtkinter
from PIL import Image
import requests
import json
import geocoder  

root = customtkinter.CTk()
width = 400
height = 600
root.geometry(f"{width}x{height}")
root.title('weather forecast App (by Tushar)')

inp_label = customtkinter.CTkLabel(root, text="Enter Your City/Country: ",  
                                   font=customtkinter.CTkFont(family="poppins", size=21))
inp_label.pack(pady=35)

inp_var = tk.StringVar()
inp_entry = customtkinter.CTkEntry(master=root, width=300, height=40, border_width=2, 
                                   corner_radius=10, textvariable=inp_var, bg_color="transparent")
inp_entry.pack(pady=20)

def checkWeth(location):
    try:
        r = requests.get(f"http://api.weatherapi.com/v1/current.json?key=617be559b34648c591e60935240606&q={location}&aqi=no")
        data = r.json()
        curr_temp = data["current"]["temp_c"]
        icon = data["current"]["condition"]["icon"]
        current_condition = data["current"]["condition"]["text"]
        humidity = data["current"]["humidity"]
        wind = data["current"]["wind_kph"]
        icon_url = "https:" + icon

        # Create the CTkImage object for weather icon
        weather_icon = customtkinter.CTkImage(light_image=Image.open(requests.get(icon_url, stream=True).raw),
                                              dark_image=Image.open(requests.get(icon_url, stream=True).raw),
                                              size=(75, 85))

        # Create the CTkImage object for humidity icon
        humidity_icon = customtkinter.CTkImage(light_image=Image.open("humidity.png"),
                                               dark_image=Image.open("humidity.png"),
                                               size=(30, 30))

        # Create the CTkImage object for wind icon
        wind_icon = customtkinter.CTkImage(light_image=Image.open("wind.png"),
                                           dark_image=Image.open("wind.png"),
                                           size=(30, 30))


        # Update the output_label and condition_label
        output_label.configure(text=f"{curr_temp}°C", image=weather_icon, compound="left")
        condition_label.configure(text=current_condition)
        humidity_label.configure(text=f"{humidity}%", image=humidity_icon, compound="left")
        wind_label.configure(text=f"{wind} km/h", image=wind_icon, compound="left")
        # precise_icon.configure(text=f"{wind} km/h", image=wind_icon, compound="left")

    except Exception as e:
        output_label.configure(text="Not found...!", image=None)
        condition_label.configure(text="")
        print(f"Unhandled error: {e}")

def checkCityWeather():
    city = inp_var.get()
    checkWeth(city)

def checkCurrentLocationWeather():
    g = geocoder.ip('me')
    latlng = f"{g.latlng[0]},{g.latlng[1]}"
    checkWeth(latlng)

btn = customtkinter.CTkButton(root, text="Check", width=40, command=checkCityWeather)
btn.pack(pady=5, side=tk.TOP)

        # Create the CTkImage object for precise icon
precise_icon = customtkinter.CTkImage(light_image=Image.open("target.png"),
                                           dark_image=Image.open("target.png"),
                                           size=(30, 30))

output_label = customtkinter.CTkLabel(master=root, text="", height=40, corner_radius=10, 
                                      text_color="white",  
                                      font=("Helvetica", 34), image=None, compound="left")
output_label.pack(padx=20)

condition_label = customtkinter.CTkLabel(master=root, text="", height=30, corner_radius=10, 
                                         text_color="white", font=("Helvetica", 24))
condition_label.pack(padx=20)

humidity_label = customtkinter.CTkLabel(master=root, text="", height=10, width=50, 
                                        corner_radius=10, text_color="white",  
                                        font=("Helvetica", 24), compound="left")
humidity_label.pack(padx=40, pady=15)

wind_label = customtkinter.CTkLabel(master=root, text="", height=10, width=50, 
                                    corner_radius=10, text_color="white", 
                                    font=("Helvetica", 24), compound="left")
wind_label.pack(padx=40, pady=15)


button = customtkinter.CTkButton(root, text="Use Precise Location", command=checkCurrentLocationWeather,image=precise_icon)
button.pack()

root.mainloop()
