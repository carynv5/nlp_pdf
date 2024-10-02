import tika
from tika import parser

# Increase timeout and disable server spawnning
tika.TikaClientOnly = True
tika.TIKA_CLIENT_ONLY = True
tika.TIKA_SERVER_JAR = 'http://search.maven.org/remotecontent?filepath=org/apache/tika/tika-server-standard/2.9.1/tika-server-standard-2.9.1.jar'

# Initialize Tika
tika.initVM()

print("Tika version:", tika.__version__)
print("Tika library initialized successfully!")

# Try to parse a PDF file
pdf_path = '/Users/carynv5/Documents/dev/nlp/pdf-extraction-examples/pdf/B.08W9127N20B0017Plans.pdf'

parsed = parser.from_file(pdf_path)

print("Parsing successful!")
print("Content (first 200 characters):", parsed["content"][:200] if parsed["content"] else "No content extracted")
print("\nMetadata:")
for key, value in parsed["metadata"].items():
    print(f"{key}: {value}")
