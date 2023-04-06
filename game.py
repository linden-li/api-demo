# File: game.py
# Inspired by: https://matt.might.net/articles/make-a-text-game-with-generative-ai/

import openai
import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# thanks gpt4
LORE = """
In the year 3030, Earth has become a hub of scientific research and collaboration. \
A group of young and eccentric researchers, known as the "Lab Rats," dedicate their \
lives to uncovering the mysteries of the universe. They work in a top-secret facility \
known as The Labrynth, hidden beneath the remnants of the Large Hadron Collider.

One day, while conducting a routine experiment, the Lab Rats stumble upon an ancient \
alien artifact. The artifact contains a cryptic message revealing the existence of the \
Cosmic Cheese, a legendary substance said to hold the answers to the universe's most \
profound questions. The Cosmic Cheese is also rumored to have the power to grant the \
user ultimate knowledge and wisdom, with a side effect of extreme hilarity.

Enthralled by the discovery, the Lab Rats form a team to embark on a quest to find the \
Cosmic Cheese. They quickly realize that they are not alone in their pursuit. An evil \
organization of scientific geniuses, known as the "Mousetrap," has also caught wind of \
the artifact and will stop at nothing to find the Cosmic Cheese first.

As the Lab Rats explore strange new worlds, interact with bizarre alien species, and \
navigate through a series of hilarious scientific mishaps, they learn that the journey \
itself holds the key to unlocking the universe's greatest secrets. They also learn the \
importance of friendship, teamwork, and the power of laughter in the face of adversity.

Throughout their journey, the Lab Rats continue to uncover clues that bring them \
closer to the Cosmic Cheese, while also outwitting the sinister Mousetrap. The game \
culminates in an epic showdown between the two factions, with the fate of the universe \
hanging in the balance. Will the Lab Rats locate the Cosmic Cheese and save the \
universe from the Mousetrap's nefarious plans? Or will their mission end in a \
hilarious disaster, leaving the Cosmic Cheese lost forever?

In Lab Rats: The Quest for the Cosmic Cheese, players will navigate through a universe \
filled with laughter, adventure, and mind-bending scientific conundrums. 

Get ready to embark on the cheesiest adventure of a lifetime!
"""


def game():
    # Right now, the cheapest and best way to interact with the API is through
    # OpenAI's `ChatCompletion` API, which is initialized with a series of messages.
    # The first message in the system instruction, which describes the behavior of the
    # assistant. There are two ways to proceed:
    # 1) If you want normal completion that isn't dependent on previous messages, you
    #    can just pass in a single user message along with the system instruction.
    # 2) If your app requires state that's dependent on previous messages sent, you can
    #    pass in a list of messages. We're doing this here to simulate a game.
    messages = [
        {"role": "system", "content": get_system_instruction()},
        {
            "role": "user",
            "content": "The game has started. Explain the game like a storyteller and \
                provide a tutorial on how to play",
        },
    ]

    start_action = get_next_action(messages)
    print(start_action["content"])
    messages.append(start_action)

    while True:
        user_action = input("\nYour action> ")
        messages.append({"role": "user", "content": user_action})
        if user_action == "/quit":
            break
        next_action = get_next_action(messages)
        print(next_action["content"])
        messages.append(next_action)


def get_next_action(messages):
    """
    This function takes in the user prompt and returns the next action.
    """
    # This is the ChatCompletion API call.
    # You can find documentation at:
    # https://platform.openai.com/docs/api-reference/completions/create
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
        # Additional parameters can be set here, such as:
        #   temperature: higher values will result in more creative responses
        #   max_tokens: the maximum number of tokens to return
        #   top_p: only consider results with cumulative probability of top_p
        #   frequency_penalty: "Positive values penalize new tokens based on their
        #                       existing frequency in the text so far, decreasing the
        #                       model's likelihood to repeat the same line verbatim."
    )

    # The API response will have the following schema:
    # {
    #  'id': 'chatcmpl-<id>',
    #  'object': 'chat.completion',
    #  'created': <timestamp>,
    #  'model': 'gpt-3.5-turbo',
    #  'usage': {
    #      'prompt_tokens': <prompt_tokens>,
    #      'completion_tokens': <completion_tokens>,
    #      'total_tokens': <total_tokens>
    #   },
    #  'choices': [
    #    {
    #     'message': {
    #       'role': 'assistant',
    #       'content': <assistant_response>
    #     'finish_reason': 'stop',
    #     'index': 0
    #    }
    #   ]
    # }
    # The output is a dictionary, and you can extract the `content` value.
    # This is just a normal string so you can process it however you'd like.
    return response["choices"][0]["message"]


def get_system_instruction():
    """
    The system instruction in an OpenAPI call helps set the behavior of the system.
    In this case, we initialize with instructions for the game.
    """
    sys_instr = (
        f"{LORE}"
        "You will simulate a text-based game based on the lore above. "
        "You understand at least these commands, and you may add more:\n"
        "When I type the command /mod <instruction>, break out of the game and execute "
        " its input as a high level instruction that may modify the state of the game. "
        "When I type the command /help, show me a list of available commands.\n"
        "When I type the command /look, describe the environment I'm in.\n"
        "When I type the command /inventory, describe the contents of my inventory.\n"
        "When I type the command /look <object>, describe the object.\n"
        "After every command, display a list of actions I can take."
    )
    return sys_instr


if __name__ == "__main__":
    game()
