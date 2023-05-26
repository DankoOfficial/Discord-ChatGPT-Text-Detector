from discord.ext import commands
from requests import post
from discord import File
from os import remove
from random import randint

client = commands.Bot(command_prefix='.')

def scan(text):
    r = post('https://api.zerogpt.com/api/detect/detectText', json={"input_text": text}, headers={'Accept': 'application/json, text/plain, */*','Accept-Encoding': 'gzip, deflate, br','Accept-Language': 'en-US,en;q=0.9','Content-Length': '1922','Content-Type': 'application/json','Origin': 'https://www.zerogpt.com','Referer': 'https://www.zerogpt.com/','Sec-Ch-Ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"','Sec-Ch-Ua-Mobile': '?0','Sec-Ch-Ua-Platform': '"Windows"','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-site','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'})
    return r

@client.command()
async def detect(ctx, *, text=None):
    if not text and not ctx.message.attachments or text and ctx.message.attachments:
        await ctx.send('No text or file detected. Command: `.detect <Text>`, or if your text is too big, do `.detect <File>`.' if not text and not ctx.message.attachments else 'You can only do either text or file, not both at once.')
        return

    if text:
        r = scan(text)
        if 'fakePercentage' in r.text:
            fake = r.json()['data']['fakePercentage']
            if fake > 0:
                rnd = randint(1000, 9999)
                fake_text = '\n'.join(r.json()['data']['h'])
                open(f'AI Generated Text {rnd}.txt', 'a').write(fake_text)
                await ctx.send(f'This text is {fake}% fake (or AI-generated). About `{r.json()["data"]["aiWords"]}` are AI words ',file=File(f'AI Generated Text {rnd}.txt'))
                remove(f'AI Generated Text {rnd}.txt')
            else:
                await ctx.send('The text is not AI-generated (fake percentage is 0).')
        else:
            await ctx.send('Detection failed.')
    else:
        if len(ctx.message.attachments) != 1:
            await ctx.send('Max is 1 attachment per command.')
            return
            
        if ctx.message.attachments[0].filename.endswith('.txt'):
            cnt = await ctx.message.attachments[0].read() 
            file_text = cnt.decode('utf-8')
            r = scan(text=file_text)
            if 'fakePercentage' in r.text:
                fake = r.json()['data']['fakePercentage']
                if fake > 0:
                    rnd = randint(1000, 9999)
                    fake_text = '\n'.join(r.json()['data']['h'])
                    open(f'AI Generated Text {rnd}.txt', 'a').write(fake_text)
                    await ctx.send(f'This text is {fake}% fake (or AI-generated). About `{r.json()["data"]["aiWords"]}` are AI words ',file=File(f'AI Generated Text {rnd}.txt'))
                    remove(f'AI Generated Text {rnd}.txt')
                else:
                    await ctx.send('The text is not AI-generated (fake percentage is 0).')
            else:
                await ctx.send('Detection failed.')
                
client.run('TOKEN')
