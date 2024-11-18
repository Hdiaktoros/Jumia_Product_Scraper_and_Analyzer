# Jumia Product Scraper and Analyzer

This project is a web scraping and data analysis tool designed to extract product information from [Jumia Ghana](https://www.jumia.com.gh). It includes functionality for scraping **Black Friday deals** and **searching for specific products**, with features to visualize and analyze the collected data.

## Features

- **Black Friday Scraper**: Automatically navigates through all pages in the Black Friday catalog and collects product details.
- **Product Search**: Allows users to search for specific products (e.g., "washing machine") and scrape all available results.
- **Data Visualization**:
  - Bar charts showing the top 10 cheapest products.
  - Histograms of product price distribution.
- **Data Export**: Saves the collected data into a CSV file for further analysis.

## Technologies Used

- **Python**: The primary programming language.
- **Selenium**: For web scraping dynamic content.
- **Pandas**: For data manipulation and analysis.
- **Matplotlib**: For data visualization.

## Prerequisites

1. **Python** (Version 3.7 or later)
2. **Microsoft Edge WebDriver**: Ensure it's installed and matches your Edge browser version.
   - [Download Microsoft Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)
   - Add the WebDriver to your system's PATH.
3. **Required Python Libraries**:
   Install the necessary dependencies by running:
   ```bash
   pip install pandas matplotlib selenium
   ```

## Setup Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/Hdiaktoros/jumia-product-scraper.git
   cd jumia-product-scraper
   ```

2. Ensure you have the correct version of Microsoft Edge WebDriver installed.

3. Run the project in Jupyter Notebook or directly from a Python script.

## Usage

### 1. Scraping Black Friday Products
To scrape all Black Friday deals:
```python
scrape_black_friday_products()
```
The script will:
- Scrape product details across all pages.
- Sort the data by price (ascending).
- Save the results to `black_friday_sorted_products.csv`.
- Display data visualizations (e.g., bar charts for the cheapest products).

### 2. Searching for Specific Products
To search for specific products (e.g., "washing machine"):
```python
search_products("washing machine")
```
The script will:
- Scrape product details for the search query.
- Sort the data by price (ascending).
- Save the results to `washing_machine_sorted_products.csv`.
- Display data visualizations.

## Data Collected

- **Name**: The product's name.
- **Current Price**: The current price of the product (GH₵).
- **Initial Price**: The original price before any discounts (GH₵).
- **Discount**: The percentage discount applied.
- **Reviews**: The number of reviews for the product.
- **Stars**: The product's star rating.
- **URL**: The link to the product page.

## Visualizations

1. **Top 10 Cheapest Products**:
   - A horizontal bar chart showing the cheapest products.
2. **Price Distribution**:
   - A histogram showing the distribution of product prices.

## Example Outputs

### Bar Chart: Top 10 Cheapest Products
![Top 10 Cheapest Products](images/top_cheapest_products.png)

### Histogram: Price Distribution
![Price Distribution](images/price_distribution.png)

## Error Handling

- Handles missing data gracefully by assigning default values.
- Automatically stops scraping if no more products are found.

## Contribution

Contributions are welcome! If you'd like to enhance the project, feel free to submit a pull request or open an issue.

1. Fork the repository.
2. Create your feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature
   ```
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or feedback, feel free to contact:
- **Your Name**
- **Email**: your-email@example.com
- **GitHub**: [your-username](https://github.com/your-username)

---

Replace placeholders like `your-username`, `your-email@example.com`, and image links with appropriate values specific to your project. Let me know if you’d like further customizations! 🚀