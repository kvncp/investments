# Investment allocation calculator

This library provides an endpoint deployed to Google Cloud Functions that calculates how much of different funds to purchase in order to move towards a desired allocation of investment funds. This problem is trivial for tax-advantaged (401k, IRA) accounts, which can be re-balanced as needed. In standard brokerage accounts, there are tax implications of selling funds, so this code determines the optimal purchase of funds to move towards the optimal allocation without selling any funds.

In order to determine the purchase plan, the following information is needed.
1. Existing fund amounts
2. Mapping of funds to categories
3. Desired category allocations
4. Which funds to purchase
5. How much to purchase in total

## Input Format

Because this library is called via a Google Sheet hyperlink right now, all parameters are passed in via the URL instead of a simpler POST request, and the format is based on what is easiest to produce with spreadsheet functions. I might eventually create a simple GUI frontend and move everything into a webapp, but for now Google Sheets provides a nice frontend for everything.

```
fund_names: semicolon separated list of existing funds.
fund_values: semicolon separated list of current value in each fund.
to_invest: amount to invest
funds_to_trade: semicolon separated list of which funds to consider purchasing.
allocations: semicolon separated list of desired percentage allocations across 5 categories (see below).
```

My current investment strategy considers the percentage of my portfolio invested across 5 different categories:
* US Large Cap
* US Mid/Small Cap
* International Developed Markets
* International Emerging Markets
* Bonds

In order to determine which funds to purchase, each fund needs to be mapped to it's allocation. Since this mapping remains static over time, this information is provided as a config file, instead of a runtime parameter.

## Future work
1. Allow selling funds with loses or minimal gains.
2. Add a term for simplification to remove additional funds from the portfolio.
