from deep_translator import GoogleTranslator

print("Working")

def get_response(message):

    try:

        # Convert any language to English
        english = GoogleTranslator(
            source='auto',
            target='en'
        ).translate(message)

        # Simple AI response
        response = "I understood: " + english

        return response

    except Exception as e:

        return "Sorry, I couldn't process your message."