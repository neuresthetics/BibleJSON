import json
from openai import OpenAI
import logging
import time

# Configure logging
logging.basicConfig(filename='bible_processing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure the OpenAI client for LM Studio's local server
client = OpenAI(
    base_url="http://10.0.0.23:6789/v1",
    api_key="not-needed"
)

def generate_header(verse_text, book_name, chapter, verse, retry_count=1):
    """Generate a header for a Bible verse using only user and assistant roles."""
    prompt = f"""
    As a biblical scholar, create a concise header (10-15 words) that captures the main theme or context of the following Bible verse from {book_name} {chapter}:{verse}. The header should be suitable as a title.

    Verse: {verse_text}

    Example: "God's Promise of Restoration" for a verse about divine renewal.
    """
    for attempt in range(retry_count + 1):
        try:
            response = client.chat.completions.create(
                model="local-model",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=50,
                timeout=10
            )
            header = response.choices[0].message.content.strip()
            logging.info(f"Generated header for {book_name} {chapter}:{verse}: {header}")
            return header
        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed for header {book_name} {chapter}:{verse}: {str(e)}")
            if attempt < retry_count:
                time.sleep(2)
            else:
                return "Generated Header (Error)"

def generate_footer(verse_text, book_name, chapter, verse, retry_count=1):
    """Generate a footer for a Bible verse using only user and assistant roles."""
    prompt = f"""
    As a biblical scholar, create a concise footer (15-25 words) that provides a reflection, commentary, or cross-reference for the following Bible verse from {book_name} {chapter}:{verse}. The footer should enhance understanding or connect to other scriptures.

    Verse: {verse_text}

    Example: "Reflects enduring love, similar to 1 Corinthians 13:4-7" for a verse about love.
    """
    for attempt in range(retry_count + 1):
        try:
            response = client.chat.completions.create(
                model="local-model",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=75,
                timeout=10
            )
            footer = response.choices[0].message.content.strip()
            logging.info(f"Generated footer for {book_name} {chapter}:{verse}: {footer}")
            return footer
        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed for footer {book_name} {chapter}:{verse}: {str(e)}")
            if attempt < retry_count:
                time.sleep(2)
            else:
                return "Generated Footer (Error)"

def process_bible_verses(input_file, output_file):
    """Loop through Bible verses, generate headers/footers, and save to a new file."""
    # Test server connectivity
    try:
        test_response = client.chat.completions.create(
            model="local-model",
            messages=[{"role": "user", "content": "Ping test for server connectivity."}],
            max_tokens=10,
            timeout=5
        )
        logging.info("Server connectivity test successful")
    except Exception as e:
        logging.error(f"Server connectivity test failed: {str(e)}")
        print(f"Error: Cannot connect to server at http://10.0.0.23:6789: {str(e)}")
        return

    # Read the input JSON
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logging.info(f"Successfully loaded {input_file}")
    except Exception as e:
        logging.error(f"Error reading {input_file}: {e}")
        print(f"Error reading {input_file}: {e}")
        return

    # Process each book and chapter
    for book in data:
        book_name = book['book_name']
        chapter = book['chapter']
        for verse in book['verses']:
            verse_num = verse['verse']
            verse_text = verse['text']
            
            logging.info(f"Processing {book_name} {chapter}:{verse_num}")
            print(f"Processing {book_name} {chapter}:{verse_num}")
            
            # Generate header and footer
            verse['header'] = generate_header(verse_text, book_name, chapter, verse_num)
            verse['footer'] = generate_footer(verse_text, book_name, chapter, verse_num)
            
            print(f"  Header: {verse['header']}")
            print(f"  Footer: {verse['footer']}")

    # Write the updated data to a new JSON file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logging.info(f"Successfully wrote output to {output_file}")
        print(f"Successfully wrote output to {output_file}")
    except Exception as e:
        logging.error(f"Error writing to {output_file}: {e}")
        print(f"Error writing to {output_file}: {e}")

def main():
    input_file = "consolidated.json"
    output_file = "consolidated_with_headers_footers.json"
    process_bible_verses(input_file, output_file)

if __name__ == "__main__":
    main()