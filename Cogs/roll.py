import re
from client import Aspid
from random import randint
from discord import errors
from math import floor, ceil
from discord.ext import commands


regex_comment= r'[\+\-\*\/]?\s?(\d+\.?\d*d\d+\.?\d*)\s?([\+\-\*\/]\s?\d+\.?\d*\s?)*(?!d)'
regex_brac= r'\((?=.*((\d+d\d+)|[\+\-\/]))[^()]*\)'
regex_dice= r'(\d+\.?\d*d\d+\.?\d*)'
regex_cursive = r'\*{2,}'


class RollDice(commands.Cog): 
    def __init__(self, bot: Aspid): 
        self.bot = bot

    @commands.command(name='roll') 
    async def roll_send(self, ctx, *, input): 
        try: 
            await ctx.message.delete() 
        except errors.NotFound: 
            print('Message has been deleted\n') 
            return
#--------Separate commentary and remove spaces
        body = input
        nb_rep = 1 
        while (nb_rep):
            (body, nb_rep) = re.subn(regex_brac, '1d20', body)
        res = re.sub(regex_comment, '', body)
        body = input.replace(res, '') 
#--------Separate dices, roll and save data
        split = re.split(regex_dice, body)
        split = [spl.replace('*', '\*') for spl in split]
        spl = split[0]
        results = []
        if len(split) <= 1:
            await ctx.send(f'No dices found in "{input}"')
            return
        for i in range(1, len(split)-1, 2):
            dices  = split[i].split('d') 
            for idx, j in enumerate(dices):
                flt = float(j)
                dices[idx] = floor(flt) if flt > 1 else ceil(flt)          
            split[i] = f'{dices[0]}d{dices[1]}'
            if dices[0] > 100:
                await ctx.send('Too many dices in one throw')
                return
            rand = [randint(1, dices[1]) for k in range(dices[0])]        
            demo = '('
            for j in rand:
                crit = '**' if j == dices[1] or j == 1 else ''
                demo += f'{crit}{str(j)}{crit}, '
            demo = f'{demo[:-2]})'
            spl += split[i] + demo + split[i+1]
            results.append(rand)   
#--------Calculate
        if len(results) > 1:
            for i in results:
                body = re.sub(regex_dice, str(sum(i)), body, 1)
            try:
                summa = round(eval(body), 2)
            except SyntaxError:
                await ctx.send("I can't calculate that!")
                return
        else:
            body = [re.sub(regex_dice, str(j), body, 1) for j in results[0]]
            try:
                body = [round(eval(j), 2) for j in body]
            except SyntaxError:
                await ctx.send("I can't calculate that!")
                return           
            summa = body[0] if len(body) == 1 else tuple(body)          
#--------Result
        res = 'Result' if res == '' else re.sub(regex_cursive ,'*',res)
        message = f'{ctx.message.author.mention} 🎲\n**{res}:** {spl} \n**Total: **{summa}\n'
        if len(message) > 1950:
            await ctx.send('The answer is too long')
            return
        await ctx.send(message) 

async def setup(bot): 
    await bot.add_cog(RollDice(bot))