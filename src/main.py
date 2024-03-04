import os;
from groq import Groq;

MODEL = 'mixtral-8x7b-32768';
API_KEY = os.environ.get('GROQ_API_KEY');

client = Groq(
  api_key = API_KEY
);

def run():
  print('Groq:');
  print('How may I assist you?');
  print('');

  while True:
    user_message = get_user_message();
    if user_message['content'] == 'exit': break;
    messages.append(user_message);
    print();
    ai_message = get_ai_message();
    messages.append(ai_message);
    print('\n');

def get_user_message():
  print('You:');
  content = input('> ');
  return create_user_message(content);

def get_ai_message():
  print('Groq:');
  stream = get_ai_message_stream(messages);
  content = '';

  for chunk in stream:
    new_content = chunk.choices[0].delta.content;
    print(new_content, end='');
    if new_content: content = content + new_content;

  return create_ai_message(content);


def add_user_message(content):
  messages.append(create_user_message(content));

def create_ai_message(content):
  return create_message('assistant', content);

def update_ai_message(message, new_content):
  message.content = message['content'] + new_content;

def create_user_message(content):
  return create_message('user', content);

def create_message(role, content):
  return { 'role': role, 'content': content };

def get_ai_message_stream(messages):  
  return client.chat.completions.create(
    messages = messages,
    model = MODEL,
    temperature=0.5,
    max_tokens=1024,
    top_p=1,
    stop=None,
    stream=True,
  );

system_message = create_message('system', 'you are a helpful assistant.');
messages = [system_message];

run();
