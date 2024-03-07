import os
import sys
from groq import Groq
from rich.console import Console

MODEL = 'mixtral-8x7b-32768'
API_KEY = os.environ.get('GROQ_API_KEY')
NERD_FONT_FLAG = '--unf'

def run():
  console.print(format_heading('assistant', model_name))
  print('How may I assist you?')
  print()

  while True:
    user_message = get_user_message()
    if user_message['content'] == 'exit': break
    messages.append(user_message)
    print()
    ai_message = get_ai_message()
    messages.append(ai_message)
    print('\n')

def get_user_message():
  console.print(format_heading('user', username))
  content = input()
  return create_user_message(content)

def get_ai_message():
  console.print(format_heading('assistant', model_name))
  stream = get_ai_message_stream(messages)
  content = ''

  for chunk in stream:
    new_content = chunk.choices[0].delta.content
    print(new_content, end='')
    if new_content: content = content + new_content

  return create_ai_message(content)

def create_ai_message(content):
  return create_message('assistant', content)

def create_user_message(content):
  return create_message('user', content)

def create_message(role, content):
  return { 'role': role, 'content': content }

def get_ai_message_stream(messages):  
  return client.chat.completions.create(
    messages = messages,
    model = MODEL,
    temperature=0.5,
    max_tokens=1024,
    top_p=1,
    stop=None,
    stream=True,
  )

def get_nerd_font_flag(args: list[str]):
  return len(args) > 1 and args[1] == NERD_FONT_FLAG

def format_emoji_heading(role, name):
  return underline(f'{emojis[role]} {name}')

def format_nerd_font_heading(role, name):
  styles = nerd_font_styles[role]
  icon = nerd_font_icons[role]
  heading = f'{icon}  {name}'
  open = set_text_styles(styles['foreground'], '')
  close = set_text_styles(styles['foreground'], '')
  middle = set_text_styles(styles['text'], heading)
  return f'{open}{middle}{close}'

def underline(string):
  return string + '\n' + '-' * (len(string) + 1)

def set_text_styles(styles, text):
  return f'[{styles}]{text}[/]'

def get_model_name(id: str):
  return id.split('-')[0]

model = 'mixtral-8x7b-32768'
username = os.getlogin()
client = Groq(api_key = API_KEY)
model_name = get_model_name(MODEL)
system_message = create_message('system', 'you are a helpful assistant.')
messages = [system_message]
using_nerd_font = get_nerd_font_flag(sys.argv)
format_heading = format_emoji_heading
if using_nerd_font: format_heading = format_nerd_font_heading
console = Console()

emojis = {
  'user': ':thinking_face:',
  'assistant': ':robot_face:'
}

magenta = {
  'text': 'bold white on magenta',
  'foreground': 'magenta'
}

cyan = {
  'text': 'bold black on cyan',
  'foreground': 'cyan'
}

nerd_font_styles = {
  'user': magenta,
  'assistant': cyan
}

nerd_font_icons = {
  'user': '󰀄',
  'assistant': '󰚩'
}

if __name__ == '__main__':
  run()
