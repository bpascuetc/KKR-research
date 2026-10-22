"""Shared Lab15 engine. Units: decimal annual returns/volatility, decimal weights."""
import csv
import io
import json
import math
from datetime import date
from pathlib import Path
import numpy as np

P = Path(__file__).resolve().parent
MERIDIAN_FILE = P / 'meridian_inputs.json'

def load_meridian(source=None):
    """Read actual course inputs; never infer them from rounded answer weights."""
    data = json.loads((source or MERIDIAN_FILE).read_text())
    if any(data.get(k) is None for k in ('returns', 'volatilities', 'correlations')):
        raise ValueError('The four-sleeve Lab14 table is missing. Supply actual returns, volatilities and correlations in meridian_inputs.json.')
    n = len(data['labels'])
    if data['labels'] != ['Bills', '10-year note', 'IG bonds', 'Equity']:
        raise ValueError('Meridian order must be Bills / 10-year note / IG bonds / Equity.')
    if data['reserve_eligible'] != [True, True, False, False]:
        raise ValueError('Training reserve eligibility must be bills and 10-year note.')
    cov = covariance(data['volatilities'], data['correlations'])
    validate_inputs(data['returns'], cov, data['reserve_eligible'])
    return data

def load_proxy():
    """Explicit market-proxy practice, never official course-table verification."""
    data = load_meridian(P / 'meridian_proxy_inputs.json')
    if data.get('status') != 'MARKET_PROXY_PRACTICE_ONLY_NOT_COURSE_TABLE':
        raise ValueError('Practice inputs must retain their explicit source status.')
    return data

def covariance(volatilities, correlations):
    vol = np.asarray(volatilities, dtype=float)
    corr = np.asarray(correlations, dtype=float)
    if not np.isfinite(vol).all() or np.any(vol < 0):
        raise ValueError('Volatilities must be finite and nonnegative.')
    if corr.shape != (len(vol), len(vol)) or not np.isfinite(corr).all():
        raise ValueError('Correlation dimensions or values invalid.')
    if not np.allclose(corr, corr.T, atol=1e-12, rtol=0) or not np.allclose(np.diag(corr), 1):
        raise ValueError('Correlations must be symmetric with unit diagonal.')
    if np.max(np.abs(corr)) > 1 + 1e-12 or np.linalg.eigvalsh(corr).min() < -1e-10:
        raise ValueError('Correlation matrix must be positive semidefinite and within [-1,1].')
    return vol[:, None] * corr * vol[None, :]

def validate_inputs(returns, cov, eligible):
    mu = np.asarray(returns, dtype=float)
    cov = np.asarray(cov, dtype=float)
    if mu.ndim != 1 or not 2 <= len(mu) <= 6 or not np.isfinite(mu).all():
        raise ValueError('Use 2–6 finite expected returns (3–6 funds for your own universe).')
    if cov.shape != (len(mu), len(mu)) or not np.isfinite(cov).all():
        raise ValueError('Covariance shape or values invalid.')
    if len(eligible) != len(mu) or any(not isinstance(v, (bool, np.bool_)) for v in eligible):
        raise ValueError('One true/false reserve flag is required per asset.')
    if not np.allclose(cov, cov.T, atol=1e-12, rtol=0) or np.linalg.eigvalsh(cov).min() < -1e-10:
        raise ValueError('Covariance must be symmetric positive semidefinite.')
    return mu, cov

def compositions(total, n):
    if n == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for tail in compositions(total - first, n - 1):
                yield (first,) + tail

def search(returns, cov, reserve_eligible, objective=.065, reserve_minimum=.03):
    """Enumerate ALL long-only 5-point grid mixes, filter, minimize variance.

    Equal variance ties retain the first lexicographic integer composition.
    No objective relaxation; None means no feasible grid mix, not a solver error.
    """
    mu, cov = validate_inputs(returns, cov, reserve_eligible)
    if not math.isfinite(objective) or not math.isfinite(reserve_minimum) or not 0 <= reserve_minimum <= 1:
        raise ValueError('Objective must be finite; reserve minimum must be between zero and one.')
    units = np.array(list(compositions(20, len(mu))), dtype=float)
    weights = units / 20
    expected = weights @ mu
    reserves = weights @ np.asarray(reserve_eligible, dtype=float)
    valid = (expected >= objective - 1e-12) & (reserves >= reserve_minimum - 1e-12)
    if not valid.any():
        return None
    feasible = weights[valid]
    variances = np.einsum('ij,jk,ik->i', feasible, cov, feasible)
    best = int(np.argmin(variances))
    w = feasible[best]
    return {'weights': w.tolist(), 'return': float(w @ mu),
            'volatility': math.sqrt(max(0., float(variances[best]))),
            'reserve_weight': float(w @ np.asarray(reserve_eligible, dtype=float)),
            'grid_mixes': len(weights), 'feasible_mixes': int(valid.sum())}

def estimate(source, last36=False):
    """Monthly adjusted prices -> simple monthly returns -> annual estimates.

    Use 37 price rows for last 36 RETURNS. Never forward fill or mix samples.
    """
    if isinstance(source, Path):
        text = source.read_text(encoding='utf-8-sig')
    elif isinstance(source, bytes):
        text = source.decode('utf-8-sig')
    else:
        text = source
    reader = csv.reader(io.StringIO(text))
    allrows = list(reader)
    if not allrows or len(allrows[0]) < 4 or allrows[0][0].strip().lower() != 'date':
        raise ValueError('CSV needs date first and 3–6 fund columns.')
    labels = [s.strip() for s in allrows[0][1:]]
    if not 3 <= len(labels) <= 6 or len(set(labels)) != len(labels) or any(not s for s in labels):
        raise ValueError('Use 3–6 distinct nonempty ticker labels.')
    dates, prices = [], []
    for row in allrows[1:]:
        if len(row) != len(labels) + 1:
            raise ValueError('Missing or extra CSV values; no imputation is permitted.')
        dates.append(date.fromisoformat(row[0]))
        prices.append([float(v) for v in row[1:]])
    if len(dates) < 37 or dates != sorted(set(dates)):
        raise ValueError('Need at least 37 sorted unique monthly price dates.')
    if any((b.year-a.year)*12+b.month-a.month != 1 for a, b in zip(dates, dates[1:])):
        raise ValueError('Dates must have exactly one observation in each consecutive month.')
    px = np.asarray(prices)
    if not np.isfinite(px).all() or (px <= 0).any():
        raise ValueError('Adjusted prices must be positive and finite; no silent filling.')
    ret = px[1:] / px[:-1] - 1
    if last36:
        ret = ret[-36:]
    means = ret.mean(axis=0)*12
    cov = np.cov(ret, rowvar=False, ddof=1)*12
    vol = np.sqrt(np.diag(cov))
    if (vol <= 0).any():
        raise ValueError('Zero variance asset: correlation undefined; review inputs.')
    corr = cov / np.outer(vol, vol)
    validate_inputs(means, cov, [False]*len(labels))
    return {'labels': labels, 'returns': means.tolist(), 'volatilities': vol.tolist(),
            'correlations': corr.tolist(), 'covariance': cov.tolist(),
            'observations': len(ret), 'price_start': dates[-len(ret)-1].isoformat(),
            'price_end': dates[-1].isoformat(), 'estimate_label': 'Historical estimate, not a forecast',
            'price_rows': len(dates)}

def largest_change(a, b):
    return None if a is None or b is None else max(abs(x-y) for x,y in zip(a['weights'], b['weights']))*100

def meridian_checks(data):
    """Independent assignment anchors, evaluated only with actual course tables."""
    cov = covariance(data['volatilities'], data['correlations'])
    base = search(data['returns'], cov, data['reserve_eligible'])
    changed_mu = list(data['returns']); changed_mu[3] = .07
    changed = search(changed_mu, cov, data['reserve_eligible'])
    corr = np.array(data['correlations'], dtype=float); corr[2,3] = corr[3,2] = .50
    engine = search(data['returns'], covariance(data['volatilities'], corr), data['reserve_eligible'])
    expected = [([0,.2,.25,.55], .0651,.0944), ([0,.1,.1,.8],.0653,.1294), ([0,.4,0,.6],.0652,.0973)]
    checks=[]
    for name, result, (w, ret, vol) in zip(['as_loaded','equity_7pct','IG_equity_corr_050'], [base,changed,engine], expected):
        passed = result is not None and np.allclose(result['weights'],w) and abs(result['return']-ret)<.000051 and abs(result['volatility']-vol)<.000051
        checks.append({'name':name,'passed':bool(passed),'actual':result})
    return {'checks':checks,'largest_weight_change_pp':largest_change(base,changed)}

if __name__ == '__main__':
    # Preserve the actual saved Lab14 printout. No original portfolio.py existed.
    old = json.loads((P/'lab14_saved_results.json').read_text())
    print(json.dumps({k:{a:b for a,b in v.items() if a!='weights'} for k,v in old['results'].items()},indent=2))
    try:
        print('\nUpdated Meridian checks:')
        print(json.dumps(meridian_checks(load_meridian()),indent=2))
    except ValueError as exc:
        print('NOT VERIFIED:', exc)
