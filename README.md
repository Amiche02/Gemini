# Gemini: OCR and LLM for Table Extraction from Images

## Description

Gemini is an innovative tool that combines Optical Character Recognition (OCR) and an advanced Language Model (LLM) to extract and interpret tables from images. This project aims to provide a precise and efficient solution for converting tables from images into structured, usable data.

## Features

- **Advanced OCR:** Utilizes Tesseract for text recognition in images.
- **Language Model:** Integrates the Gemini model to analyze and structure the extracted data into tables.
- **High Accuracy:** Optimized algorithms to enhance the precision and speed of extraction.
- **Versatility:** Capable of processing various types of images containing tables.
- **Comprehensive Documentation:** Detailed user guide and technical documentation.

## Prerequisites

Before starting, make sure you have the following installed:

- Python 3.8 or later
- Gemini API Key
- Required Python libraries (see `requirements.txt`)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Amiche02/Gemini.git
    cd Gemini
    ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Ensure that Tesseract OCR is installed and properly configured on your system.

## Usage

1. Place the images containing tables in the `input_images` directory.
2. Run the main script:
    ```bash
    python app.py
    ```
or
    ```bash
    python sylva.py
    ```
3. The results will be saved in the `output_tables` directory as CSV files.

## Project Structure

- `input_images/` : Directory for images to be processed.
- `output_tables/` : Directory for generated CSV files.
- `main.py` : Main script for table extraction.
- `requirements.txt` : List of required Python libraries.
- `README.md` : This README file.

## Contribution

Contributions are welcome! Please follow these steps to contribute:

1. Fork the project
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -am 'Add a feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

## Authors

- **Amiche02** - Creator and main developer

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Thanks to the developers of Tesseract OCR and the Gemini model for their exceptional tools.
- Thanks to the open-source community for their support and contributions.
