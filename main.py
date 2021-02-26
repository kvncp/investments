from scipy import optimize

FUNDS_TO_UPDATE = ['vtsax', 'vtiax', 'vbtlx']
INVESTMENT_ALLOCATIONS = ['large cap', 'midsmall cap', 'international', 'bonds']

STOCK_ALLOCATION = 0.9
US_STOCK_ALLOCATION = 0.75
LARGE_CAP_ALLOCATION = 0.84*US_STOCK_ALLOCATION*STOCK_ALLOCATION
MIDSMALL_CAP_ALLOCATION = 0.16*US_STOCK_ALLOCATION*STOCK_ALLOCATION
INTERNATIONAL_ALLOCATION = (1-US_STOCK_ALLOCATION)*STOCK_ALLOCATION
BOND_ALLOCATION = 1-STOCK_ALLOCATION

def min_func(x, funds, desired_allocations):

    # Update funds with new value
    for fund, value in zip(FUNDS_TO_UPDATE, x):
        funds[fund] = value

    proposed_allocations = compute_investment_mix(funds)

    error = 0
    for a in INVESTMENT_ALLOCATIONS:
        error += (proposed_allocations[a] - desired_allocations[a])**2

    return error**0.5


def get_fund_dict(request):
    return {k.lower():float(v) for k, v in zip(request.args['keys'].split(';'), request.args['values'].split(';'))}


def compute_investment_mix(funds):
    allocations = {}
    allocations['large cap'] =  funds['goog'] + funds['googl'] + funds['vtsax']*.84
    allocations['midsmall cap'] =  funds['vexax'] + funds['vtsax']*.16
    allocations['international'] =  funds['vtiax']
    allocations['bonds'] =  funds['vbtlx']

    return allocations


def desired_allocations(total):
    desired_pct = [LARGE_CAP_ALLOCATION, MIDSMALL_CAP_ALLOCATION, INTERNATIONAL_ALLOCATION, BOND_ALLOCATION] # TODO: get from sheet
    desired_amt = {x: y * total for x, y in zip(INVESTMENT_ALLOCATIONS, desired_pct)}

    return desired_amt


def calc(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    funds = get_fund_dict(request)
    to_invest = float(request.args['to_invest'])

    # Initialize with current values
    x_0 = [funds[f] for f in FUNDS_TO_UPDATE]

    # Only allow funds to increase in this optimization.
    bounds = [(funds[f], None) for f in FUNDS_TO_UPDATE]

    # Total changes must equal amount to invest.
    investment_constraint = optimize.LinearConstraint([1]*len(FUNDS_TO_UPDATE), sum(x_0) + to_invest, sum(x_0) + to_invest)

    total = sum(x for x in funds.values()) + to_invest

    res = optimize.minimize(min_func, x_0, args = (funds, desired_allocations(total)), bounds=bounds, constraints=(investment_constraint))

    return ','.join(FUNDS_TO_UPDATE) + '\n' + ','.join(str(round(x-y)) for x, y in zip(res.x, x_0))
