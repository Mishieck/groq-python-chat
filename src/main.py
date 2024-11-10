import os
import sys
from groq import Groq
from rich.console import Console
from typing import List
from dataclasses import dataclass
from dataclasses import asdict

MODEL = os.environ.get('MODEL')
API_KEY = os.environ.get('GROQ_API_KEY')
NERD_FONT_FLAG = '--unf'

@dataclass(frozen=True)
class Message:
  role: str # 'system' | 'assistant' | 'user'
  content: str

@dataclass(frozen=True)
class TextStyles:
  foreground: str
  background: str

  @property
  def foreground_and_background(self) -> str:
    return f'bold {self.foreground} on {self.background}'

@dataclass(frozen = True)
class Icons:
  user: str
  assistant: str

@dataclass(frozen = True)
class Header:
  using_nerd_font: bool
  role: str
  text: str

  def __repr__(self):
    if self.using_nerd_font: return self.format_using_nerd_font()
    else: return self.format_without_nerd_font()

  def format_using_nerd_font(self) -> str:
    icon = self.get_icon(nerd_font_icons)
    heading = f'{icon}  {self.text}'
    styles = text_styles[self.role]
    open = Header.set_text_styles(styles.background, '')
    close = Header.set_text_styles(styles.background, '')
    middle = Header.set_text_styles(styles.foreground_and_background, heading)
    return f'{open}{middle}{close}'

  def format_without_nerd_font(self) -> str:
    styles = text_styles[self.role].foreground_and_background
    return Header.set_text_styles(styles, f' @{self.text} ')

  def get_icon(self, icons: Icons) -> str:
    return icons.user if self.role == 'user' else icons.assistant

  def set_text_styles(styles, text) -> str:
    return f'[{styles}]{text}[/]'

client = Groq(api_key = API_KEY)
system_message = Message(role = 'system', content = 'you are a helpful assistant.')
messages: List[Message] = [asdict(system_message)]

using_nerd_font = len(sys.argv) > 1 and sys.argv[1] == NERD_FONT_FLAG
magenta = TextStyles(foreground = 'white', background = 'magenta')
cyan = TextStyles(foreground = 'black', background = 'cyan')
text_styles = { 'user': magenta, 'assistant': cyan }
nerd_font_icons = Icons(user = '󰀄', assistant = '󰚩')

username = os.getlogin()
user_header = Header(using_nerd_font = using_nerd_font, role = 'user', text = username)
model_name = MODEL.split('-')[0]
ai_header = Header(using_nerd_font = using_nerd_font, role = 'assistant', text = model_name)

headers = {
  'user': str(user_header),
  'assistant': str(ai_header)
}

console = Console()

def main():
  print("Enter 'exit' to quit chat.\n")
  console.print(headers['assistant'])
  print('How may I assist you?')
  print()

  while True:
    user_message = get_user_message()
    if user_message.content == 'exit': break
    messages.append(asdict(user_message))
    print()
    ai_message = get_ai_message()
    messages.append(asdict(ai_message))
    print('\n')

def get_user_message() -> Message:
  console.print(headers['user'])
  return Message(role = 'user', content = input())

def get_ai_message() -> Message:
  console.print(headers['assistant'])
  stream = get_ai_message_stream(messages)
  content = ''

  for chunk in stream:
    new_content = chunk.choices[0].delta.content
    print(new_content, end = '')
    if new_content: content = content + new_content

  return Message(role = 'assistant', content = content)

def get_ai_message_stream(messages: List[Message]):  
  return client.chat.completions.create(
    messages = messages,
    model = MODEL,
    temperature = 0.5,
    max_tokens = 1024,
    top_p = 1,
    stop = None,
    stream = True,
  )

if __name__ == '__main__':
  main()
