from flask import Flask , jsonify,request
from groq import Groq
from dotenv import load_dotenv
import os
from flask_cors import CORS



# Load environment variables from .env file
load_dotenv()
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),  
)
# Initialize Flask application
sql_app=Flask(__name__)
CORS(sql_app)
@sql_app.route('/Generate_sql_query', methods=['POST'])
def get_openai_response():
    # Get the input text from the request body
    data= request.json
    try:
        if 'input' in data:
            user_input = data['input']  # Store the value
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are a SQL export your role is to Convert the following natural language description into a SQL query and give me just the code with explanation after this pattren '\n```\n\n' without the word  explanation in it ."},
                    {"role": "user","content":user_input}
                ],
                temperature=0.5,
                max_tokens=230,
            )
            print(completion)
            # Extract the content from the response 
            sql_query=completion.choices[0].message.content
            # Return the response as a JSON object
            return jsonify({"sqlQuery": sql_query}), 200
        else:
            return jsonify({"error": "No value provided"}), 400
    except Exception as e:
        # Handle exceptions and return an error response
        return jsonify({"error": str(e)}), 500
@sql_app.route('/')
def hello():
    return 'is working'
if __name__ == '__main__':
    sql_app.run()
