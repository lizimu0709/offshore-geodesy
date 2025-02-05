import pandas as pd
import scipy.stats

from .constants import SP_DEPTH, SP_SOUND_SPEED


def _compute_hm(svdf: pd.DataFrame, start_depth: float, end_depth: float) -> float:
    """
    Computes harmonic mean using `scipy's hmean <https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.hmean.html>`_ method.
    It takes the sound speed 'sv' as the input array and the depth 'dd' differences as the weights.

    Note that this function assumes absolute values for depth array,
    sound speed array, start depth, and end depth.

    The underlying formula is

    H = (w1+...+wn) / ((w1/x1)+...+(wn/xn))

    H is the resulting harmonic mean
    w is the weight value, in this case, the depth differences
    x is the input value, in this case, the sound speed

    Parameters
    ----------
    svdf : pd.DataFrame
        Sound speed profile data as dataframe with columns 'dd' and 'sv'
    start_depth : float
        The start depth for calculation
    end_depth : float
        The end depth for calculation

    """  # noqa
    for col in [SP_DEPTH, SP_SOUND_SPEED]:
        if col not in svdf.columns:
            raise ValueError(f"{col} column must exist in the input dataframe!")

    filtdf = svdf[
        (svdf[SP_DEPTH].round() >= start_depth) & (svdf[SP_DEPTH].round() <= end_depth)
    ]

    # Get weights
    weights = filtdf[SP_DEPTH].diff()

    return scipy.stats.hmean(filtdf[SP_SOUND_SPEED], weights=weights, nan_policy="omit")


def sv_harmonic_mean(svdf: pd.DataFrame, start_depth: float, end_depth: float) -> float:
    """
    Computes harmonic mean from a sound profile
    containing depth (dd) and sound speed (sv)

    Parameters
    ----------
    svdf : pd.DataFrame
        Sound speed profile data as dataframe
    start_depth : int or float
        The start depth for harmonic mean to be computed
    end_depth : int or float
        The end depth for harmonic mean to be computed

    Returns
    -------
    float
        The sound speed harmonic mean value
    """
    if svdf.empty:
        raise ValueError("Dataframe is empty! Please check your data inputs.")
    # Clean up the sound speed value, ensuring that there's no negative value
    svdf = svdf[svdf[SP_SOUND_SPEED] > 0].reset_index(drop=True)
    # Make all of the values absolute values, so we're only dealing with positives
    abs_start = abs(start_depth)
    abs_end = abs(end_depth)
    abs_sv = abs(svdf)

    return _compute_hm(abs_sv, abs_start, abs_end)
