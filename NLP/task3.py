from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

MODEL_NAME = "microsoft/DialoGPT-medium"

def load_model():
    """Download (first run) and load the tokenizer + model."""
    print("Loading model... (first run downloads ~350MB, please wait)\n")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model     = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    model.eval()           # inference mode — saves memory
    return tokenizer, model


def generate_response(user_input, chat_history_ids, tokenizer, model):
    """
    Encode the new user message, append to history, generate reply.

    Returns:
        response_text  (str)  — the bot's reply
        chat_history_ids      — updated token history for next turn
    """
    # Encode user input and append end-of-string token
    new_input_ids = tokenizer.encode(
        user_input + tokenizer.eos_token,
        return_tensors="pt"
    )

    # Append to full conversation history
    bot_input_ids = (
        torch.cat([chat_history_ids, new_input_ids], dim=-1)
        if chat_history_ids is not None
        else new_input_ids
    )

    # Safety: keep only the last 1000 tokens so RAM doesn't explode
    if bot_input_ids.shape[-1] > 1000:
        bot_input_ids = bot_input_ids[:, -1000:]

    # Generate response
    chat_history_ids = model.generate(
        bot_input_ids,
        max_new_tokens=150,       # max tokens to generate per reply
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,           # sampling → more natural replies
        top_k=50,                 # consider top-50 likely next tokens
        top_p=0.95,               # nucleus sampling threshold
        temperature=0.75,         # creativity: 0=robotic, 1=wild
        repetition_penalty=1.3,   # discourages repeating phrases
    )

    # Decode only the new tokens (skip the prompt)
    response_ids = chat_history_ids[:, bot_input_ids.shape[-1]:]
    response_text = tokenizer.decode(response_ids[0], skip_special_tokens=True)

    return response_text, chat_history_ids


def main():
    tokenizer, model = load_model()

    print("=" * 55)
    print("  Chatbot ready!  Type 'exit' or 'quit' to stop.")
    print("=" * 55)

    chat_history_ids = None   # starts empty; grows with each turn

    while True:
        # Get user input
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Goodbye!")
            break

        # Exit condition
        if user_input.lower() in {"exit", "quit"}:
            print("Bot: Goodbye! It was nice talking to you.")
            break

        # Skip empty input 
        if not user_input:
            print("Bot: Please say something!")
            continue

        # Generate and display response
        response, chat_history_ids = generate_response(
            user_input, chat_history_ids, tokenizer, model
        )
        print(f"Bot: {response}")


if __name__ == "__main__":
    main()