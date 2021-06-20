import discord
import math
import base64
import re
import textwrap
from io import BytesIO
from typing import Optional, Union
from redbot.core.data_manager import cog_data_path, bundled_data_path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
from functools import partial

class EventCard:

    __author__ = "OGKaktus (OGKaktus#5299)"
    __version__ = "1.0"
       
    def __init__(self) -> discord.File:
        self.eventbg = str(bundled_data_path(self) / "card.png")
        self.eventfont = str(bundled_data_path(self) / "BebasNeue.otf")
        
    def setBot(self, bot):
        self.bot = bot
        
    async def get_card(self,ctx, message, avatars):
        userdata = {}
        #for x in users:
        #    userdata[ctx.guild.get_member(x).name] = {}
        #    userdata[ctx.guild.get_member(x).name]["avatar"] = await self.get_avatar(ctx.guild.get_member(x))
            
        #avatar_bytes = await self.get_avatar(user)
        #card = Image.open(self.eventbg)        
        
        #member_colour = user.colour.to_rgb()
        fn = partial(self.processing, self, ctx, self.eventfont, message, avatars)

        final_buffer = await self.bot.loop.run_in_executor(None, fn)
        
        file = discord.File(filename="bfee_hg.png", fp=final_buffer)
        return file
             
    @staticmethod
    def processing(self, ctx, font, message, avatarsraw) -> BytesIO:
        card_size = (450, 130)
        card_color = (93, 80, 80)
        player_color = (251, 130, 0)
        text_color = (255, 255, 255)
        size = 90, 90
        
        space_char = "|--|--|--|"
        color_char = "|>>>|"
        
        avatars = []
        
        if len(avatarsraw) > 4:
            new_h = card_size[1] + 110
            card_size = (450, new_h)
        
        card = Image.new( mode = "RGB", size = card_size, color = card_color )
        
        ava_y = 10
       
        if avatarsraw is not None:                
            for ava in avatarsraw:
                avatar = Image.open(ava)
                avatar = avatar.resize(size)
                avatars.append(avatar)
                
            avatarsss = []
            tmpava = []
            a_step = 0
            
            for tav in avatars:
                tmpava.append(tav)
                a_step += 1
                if a_step is 4:
                    avatarsss.append(tmpava)
                    tmpava = []
                    a_step = 0
            avatarsss.append(tmpava)
                    
            for avatarss in avatarsss:                
                dist_between_pics = math.ceil((card_size[0] - (len(avatarss) * size[0])) / (len(avatarss) + 1))
                x = dist_between_pics
                for ava in avatarss:
                    card.paste(ava, (x,ava_y))
                    x += dist_between_pics + size[0]
                ava_y += 100
                print("AVA_Y: {0}".format(ava_y))

            if len(avatarsraw) is 4:
                ava_y -= 100
            #dist_between_pics = math.ceil((card_size[0] - (len(avatars) * size[0])) / (len(avatars) + 1))
            #x = dist_between_pics
            #for ava in avatars:
            #    card.paste(ava, (x,ava_y))
            #    x += dist_between_pics + size[0]
            
        eventtextfont = ImageFont.truetype(font, 20)
        
        
        #d = ImageText((450, 150), background=(255, 255, 255, 200)) # 200 = alph
        #color = (50, 50, 50)
        #d.write_text_box((300, 50), message, box_width=230, font_filename=eventtextfont,
        #           font_size=20, color=color)
        
        #d = ImageDraw.Draw(card)
        #
        #for line in textwrap.wrap(message, width=int(card_size[0] - 20)):
        #    d.text((margin, offset), line, font=eventtextfont, fill=(255, 255, 255))
        #    offset += eventtextfont.getsize(line)[1]
        
        
        #d = ImageDraw.Draw(card)
        #description_wrapped = self.text_wrap(message,eventtextfont,d,430,35)
        
        offset = ava_y + 10
        description_wrapped = self.get_wrapped_text(message, eventtextfont, line_length=(card_size[0] - 30))
        print("")
        print("")
        print("")
        print("")
        for msg in description_wrapped:
            card = self.add_textrowspace(card, card_color, eventtextfont.getsize("BFEE")[1] + 5)
            d = ImageDraw.Draw(card)
            
            txtoffset = 10
            msgparts = msg.split()
            for x in msgparts:
                print("WORD: {}".format(x))
                if x[ 0 : 5 ] == "|>>>|":
                    # Colorize
                    word = "{0} ".format(x[5:])
                    col = player_color
                else:
                    word = "{0} ".format(x)
                    col = text_color
                print("WORD2: {}".format(word))
                d.text((txtoffset,offset), word.replace(space_char," "), font=eventtextfont, fill=col)
                print("txtoffset: {0}".format(txtoffset))
                print("offset: {0}".format(offset))
                txtoffset += eventtextfont.getsize(word.replace(space_char," "))[0]
                
            
            #msgparts = msg.split(color_char)
            #isname = False
            #txtoffset = 10
            #for x in msgparts:
            #    if isname:
            #        d.text((txtoffset,offset), x.replace(space_char," "), font=eventtextfont, fill=player_color)
            #        txtoffset += eventtextfont.getsize(x)[0]
            #        isname = False
            #    else:
            #        d.text((txtoffset,offset), x.replace(space_char," "), font=eventtextfont, fill=text_color)
            #        txtoffset += eventtextfont.getsize(x)[0]
            #        isname = True
                
            #d.text((10,offset), msg, font=eventtextfont, fill=(255, 255, 255))
            offset += eventtextfont.getsize("BFEE")[1] + 5
                
        ## RANK & LEVEL TEXT
        #ranktextfont = ImageFont.truetype(font, 40)
        #ranktextfont2 = ImageFont.truetype(font, 80)
        #ranktextfont3 = ImageFont.truetype(font, 50)
        #d = ImageDraw.Draw(card)
        #
        #lvlktxtx = maxx - ranktextfont2.getsize(ulevel)[0]
        #d.text((lvlktxtx,45), ulevel, font=ranktextfont2, fill=(37, 94, 212))
        #
        #lvltextdesc = lvlktxtx - ranktextfont.getsize(leveltxt)[0] - 10
        #d.text((lvltextdesc,80), leveltxt, font=ranktextfont, fill=(16, 195, 233))
        #
        #urankx = lvltextdesc - ranktextfont2.getsize(urank)[0] - 20
        #d.text((urankx,45), urank, font=ranktextfont2, fill=(255, 255, 255))
        #
        #rankx = urankx - ranktextfont.getsize(ranktxt)[0] - 10
        #d.text((rankx,80), ranktxt, font=ranktextfont, fill=(255, 255, 255))
        #
        ## USERNAME
        #d.text((usernamex,120), user.name, font=ranktextfont3, fill=(255, 255, 255))
        #
        ## USER ACCOUNT NUMBER
        #useridx = usernamex + ranktextfont3.getsize(user.name)[0] + 10
        #d.text((useridx,130), "#" + str(user.discriminator), font=ranktextfont, fill=(186, 186, 186))
        #
        ## XP
        #nextlevelxpx = maxx - ranktextfont.getsize("/ " + curgoal)[0] - 10
        #d.text((nextlevelxpx,130), "/ " + curgoal, font=ranktextfont, fill=(186, 186, 186))
        #
        #curxpx = nextlevelxpx - ranktextfont.getsize(curxp)[0] - 10
        #d.text((curxpx,130), curxp, font=ranktextfont, fill=(255, 255, 255))

        # FINISH
        final_buffer = BytesIO()
        card.save(final_buffer, "png")

        final_buffer.seek(0)

        return final_buffer
    
    def get_wrapped_text(self, text: str, font: ImageFont.ImageFont, line_length: int):
        lines = []
        lines_formatted = []
        line = ""
        line_formatted = ""
        space_char = "|--|--|--|"
        color_char = "|>>>|"
        
        for word in text.split():
            word_formatted = word.replace(color_char, "").replace(space_char, " ")
            if font.getsize("{0} {1}".format(line_formatted, word_formatted))[0] <= line_length:
                line += " {0}".format(word)
                #line += word
                line_formatted += word_formatted
            else:
                lines.append(line)
                lines_formatted.append(line_formatted)
                line = word
                line_formatted = word_formatted
        lines.append(line)
        lines_formatted.append(line_formatted)
        print(lines)
        return lines
        
    def add_textrowspace(self, img, color, add_height):
        width, height = img.size
        new_height = height + add_height
        result = Image.new(img.mode, (width, new_height), color)
        result.paste(img, (0, 0))
        return result
        
    def divide_chunks(self,l, n):
        # looping till length l
        for i in range(0, len(l), n): 
            yield l[i:i + n]