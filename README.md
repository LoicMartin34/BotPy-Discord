# PyBot-Discord
**PyBot** is a Discord bot developed with Python.

## Help command
The command **!help** allows you to see signature and descriptions of commands.  
_!help_ shows you the entire list of commands of each section (Admin, Moderation, Musiques, ...)  
_!help section_ presents the commands of the section wanted  
_!help ban_ explain you how to use this command  

## Admin and moderation commands
He allows multiples admin commands like ban, unban and kick from the server. We got also moderation commands like mute, allmute, deaf and kick from the voice channel.

## Wheel of fortune
There is also a wheel of fortune who allows people who are currently in the voice channel to play. They can "win" some rewards like kick, mute and deaf (they got kicked from the voice channel, mute for 30sec or deaf for 15sec). There is also a randomKick who pick randomly someone and kick him fro the voice channel.

## LolPicker
It is also possible to use the LoLPicker command. She's usefull for League of Legends players and allows you to pick a random champion and lane.

## Music bot
It is also possible to make the bot join the current voice channel and let him plays some musics. Some commands are available to make easier the use.



### List of the commands and there arguments :

1. **Cogs are used to allow easier developement, it's possible to modify some functions without disconnect the bot.**

*unload X* : Before modify the code, you need to unload the extension X (file) where the function is.  
*load X*: Once the modifications done, you can load the extension and get back the multiples commands.  
*reload X*: For easier use, you can just modify the file and reload the extension to get the modifications available. 

2. **Admin and moderation commands**

*serverInfo* : This command allows to obtain some informations on the server like the number of members or ther number of voice and textual channels.  
*clear X* : You can clear the last X messages from the current textual channel. The command message is also deleted.  
*ban Member / unban Member* : These commands are used to ban or unban the member indefinitely.  
*getBanList* : You can as well obtain the list of members banned.  
  
*mute Member X/ unmute Member* : It is possible to mute the member selected during X seconds or endlessly if X isn't indicate. You can also revoke the mute with the unmute command.  
*deaf Member X/ deaf Member* : Same operation than mute command, but deaf the member.  
*allmute / allunmute* : This command can mute/unmute all the people in the voice channel except the author of the command.  
*kick Member* :  
*kickServer Member* :  

3. **Wheel of fortune**
