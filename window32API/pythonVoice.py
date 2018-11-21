#coding:utf-8
import win32com.client

speaker = win32com.client.Dispatch("SAPI.SpVoice")

speaker.Speak("B H C G price 19.25, this is the first try")