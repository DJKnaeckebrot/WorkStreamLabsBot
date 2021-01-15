#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Work command"""
#---------------------------------------
# Libraries and references
#---------------------------------------
import codecs
import json
import os
import winsound
import ctypes
from array import *
#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "Work"
Website = "https://github.com/mrdennis1212"
Creator = "mrdennis1212"
Version = "1.0"
Description = "Work command"
#---------------------------------------
# Versions
#---------------------------------------
""" Releases (open README.md for full release notes)
1.0 - Initial Release
"""
#---------------------------------------
# Variables
#---------------------------------------
settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")

#---------------------------------------
# Classes
#---------------------------------------
class Settings:
    """" Loads settings from file if file is found if not uses default values"""

    # The 'default' variable names need to match UI_Config
    def __init__(self, settingsFile=None):
        if settingsFile and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig', mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig')

        else: #set variables if no custom settings file is found
            self.OnlyLive = False
            self.Command = "!work"
            self.Cost = 0
            self.Permission = "Everyone"
            self.PermissionInfo = ""
            self.Usage = "Stream Chat"
            self.UseCD = True
            self.Cooldown = 1800
            self.OnCooldown = "{0} the command is still on cooldown for {1} seconds!"
            self.UserCooldown = 10
            self.OnUserCooldown = "{0} the command is still on user cooldown for {1} seconds!"
            self.CasterCD = True
            self.NotEnoughResponse = "{0} you don't have enough {1} to attempt this! You will need atleast {2} {1}."
            self.PermissionResponse = "{0} -> only {1} ({2}) and higher can use this command"
            self.Timeout = False
            self.TL = 60
            self.B1Name = "NoWork"
            self.B1WinChance = 100
            self.B1Win = 2
            self.B1WinText = "{0} du sollst arbeiten und nicht am Handy spielen! Hier hast du {1} {2}"
            self.B2Name = "YouTried"
            self.B2WinChance = 100
            self.B2Win = 5
            self.B2WinText = "{0} naja immerhin hast du es versucht.. Hier hast du {1} {2}."
            self.B3Name = "OK"
            self.B3WinChance = 100
            self.B3Win = 10
            self.B3WinText = "{0} deine arbeit war ganz ok. Hier hast du {1} {2}."
            self.B4Name = "GoodWork"
            self.B4WinChance = 100
            self.B4Win = 20
            self.B4WinText = "{0} gute Arbeit! Hier hast du {1} {2}!"
            self.B5Name = "WOW"
            self.B5WinChance = 100
            self.B5Win = 80
            self.B5WinText = "{0} sehr gute Arbeit! Hier hast du {1} {2}!"

    # Reload settings on save through UI
    def ReloadSettings(self, data):
        """Reload settings on save through UI"""
        self.__dict__ = json.loads(data, encoding='utf-8-sig')
        return

    # Save settings to files (json and js)
    def SaveSettings(self, settingsFile):
        """Save settings to files (json and js)"""
        with codecs.open(settingsFile, encoding='utf-8-sig', mode='w+') as f:
            json.dump(self.__dict__, f, encoding='utf-8-sig')
        with codecs.open(settingsFile.replace("json", "js"), encoding='utf-8-sig', mode='w+') as f:
            f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8-sig', ensure_ascii=False)))
        return
#---------------------------------------
# [OPTIONAL] Settings functions
#---------------------------------------
def SetDefaults():
    """Set default settings function"""

    #play windows sound
    winsound.MessageBeep()

    #open messagebox with a security check
    MessageBox = ctypes.windll.user32.MessageBoxW
    returnValue = MessageBox(0, u"You are about to reset the settings, "
                                "are you sure you want to contine?"
                             , u"Reset settings file?", 4)

    #if user press "yes"
    if returnValue == 6:

        # Save defaults back to file
        Settings.SaveSettings(MySet, settingsFile)

        #show messagebox that it was complete
        MessageBox = ctypes.windll.user32.MessageBoxW
        returnValue = MessageBox(0, u"Settings successfully restored to default values"
                                 , u"Reset complete!", 0)

#---------------------------------------
# [Required] functions
#---------------------------------------
def Init():
    """data on Load, required function"""
    global MySet
    MySet = Settings(settingsFile)

def Execute(data):
    """Required Execute data function"""
    if data.IsChatMessage() and data.GetParam(0).lower() == MySet.Command.lower():

        if not IsFromValidSource(data, MySet.Usage):
            return

        if not Parent.HasPermission(data.User, MySet.Permission, MySet.PermissionInfo):
            message = MySet.PermissionResponse.format(data.User, MySet.Permission, MySet.PermissionInfo)
            SendResp(data, message)

        if not HasPermission(data):
            return

        if not MySet.OnlyLive or Parent.IsLive():

            if IsOnCooldown(data):
                return
                        
            Boss = [[MySet.B1Name, MySet.B1WinChance, MySet.B1Win, MySet.B1WinText.format(data.UserName, MySet.B1Win, Parent.GetCurrencyName())], \
                    [MySet.B2Name, MySet.B2WinChance, MySet.B2Win, MySet.B2WinText.format(data.UserName, MySet.B2Win, Parent.GetCurrencyName())], \
                    [MySet.B3Name, MySet.B3WinChance, MySet.B3Win, MySet.B3WinText.format(data.UserName, MySet.B3Win, Parent.GetCurrencyName())], \
                    [MySet.B4Name, MySet.B4WinChance, MySet.B4Win, MySet.B4WinText.format(data.UserName, MySet.B4Win, Parent.GetCurrencyName())], \
                    [MySet.B5Name, MySet.B5WinChance, MySet.B5Win, MySet.B5WinText.format(data.UserName, MySet.B5Win, Parent.GetCurrencyName())]]           
                        
            selectedboss = Parent.GetRandom(0,5)
            
            Boss = Boss[selectedboss]
            
            Parent.AddPoints(data.User, data.UserName, Boss[2])

            userBalance = str(Parent.GetPoints(data.User))
            message = Boss[3] + " Du hast also " + userBalance + " " + Parent.GetCurrencyName() + " !"

            SendResp(data, message)

            AddCooldown(data)
            

def Tick():
    """Required tick function"""

#---------------------------------------
# [Optional] Functions for usage handling
#---------------------------------------
def SendResp(data, sendMessage):
    """Sends message to Stream or discord chat depending on settings"""

    if not data.IsFromDiscord() and not data.IsWhisper():
        Parent.SendStreamMessage(sendMessage)

    if not data.IsFromDiscord() and data.IsWhisper():
        Parent.SendStreamWhisper(data.User, sendMessage)

    if data.IsFromDiscord() and not data.IsWhisper():
        Parent.SendDiscordMessage(sendMessage)

    if data.IsFromDiscord() and data.IsWhisper():
        Parent.SendDiscordDM(data.User, sendMessage)

def CheckUsage(data, rUsage):
    """Return true or false depending on the message is sent from
    a source that's in the usage setting or not"""

    if not data.IsFromDiscord():
        l = ["Stream Chat", "Chat Both", "All", "Stream Both"]
        if not data.IsWhisper() and (rUsage in l):
            return True

        l = ["Stream Whisper", "Whisper Both", "All", "Stream Both"]
        if data.IsWhisper() and (rUsage in l):
            return True

    if data.IsFromDiscord():
        l = ["Discord Chat", "Chat Both", "All", "Discord Both"]
        if not data.IsWhisper() and (rUsage in l):
            return True

        l = ["Discord Whisper", "Whisper Both", "All", "Discord Both"]
        if data.IsWhisper() and (rUsage in l):
            return True

    return False

def IsOnCooldown(data):
    """Return true if command is on cooldown and send cooldown message if enabled"""
    cooldown = Parent.IsOnCooldown(ScriptName, MySet.Command)
    userCooldown = Parent.IsOnUserCooldown(ScriptName, MySet.Command, data.User)
    caster = (Parent.HasPermission(data.User, "Caster", "") and MySet.CasterCD)

    if (cooldown or userCooldown) and caster is False:

        if MySet.UseCD:
            cooldownDuration = Parent.GetCooldownDuration(ScriptName, MySet.Command)
            userCDD = Parent.GetUserCooldownDuration(ScriptName, MySet.Command, data.User)

            if cooldownDuration > userCDD:
                m_CooldownRemaining = cooldownDuration

                message = MySet.OnCooldown.format(data.UserName, m_CooldownRemaining)
                SendResp(data, message)

            else:
                m_CooldownRemaining = userCDD

                message = MySet.OnUserCooldown.format(data.UserName, m_CooldownRemaining)
                SendResp(data, message)
        return True
    return False

def HasPermission(data):
    """Returns true if user has permission and false if user doesn't"""
    if not Parent.HasPermission(data.User, MySet.Permission, MySet.PermissionInfo):
        message = MySet.PermissionResponse.format(data.UserName, MySet.Permission, MySet.PermissionInfo)
        SendResp(data, message)
        return False
    return True

def IsFromValidSource(data, Usage):
    """Return true or false depending on the message is sent from
    a source that's in the usage setting or not"""
    if not data.IsFromDiscord():
        l = ["Stream Chat", "Chat Both", "All", "Stream Both"]
        if not data.IsWhisper() and (Usage in l):
            return True

        l = ["Stream Whisper", "Whisper Both", "All", "Stream Both"]
        if data.IsWhisper() and (Usage in l):
            return True

    if data.IsFromDiscord():
        l = ["Discord Chat", "Chat Both", "All", "Discord Both"]
        if not data.IsWhisper() and (Usage in l):
            return True

        l = ["Discord Whisper", "Whisper Both", "All", "Discord Both"]
        if data.IsWhisper() and (Usage in l):
            return True
    return False

def AddCooldown(data):
    """add cooldowns"""
    if Parent.HasPermission(data.User, "Caster", "") and MySet.CasterCD:
        Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)
        return

    else:
        Parent.AddUserCooldown(ScriptName, MySet.Command, data.User, MySet.UserCooldown)
        Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)
